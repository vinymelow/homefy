"""Painel web do ecom-stack — orquestra o pipeline de produto.

Arranque:  python3 cli/cli.py painel   (ou uvicorn painel.app:app)
Acesso:    túnel SSH  ssh -L 8787:localhost:8787 root@<vps>
"""
import json
import os
import re
import shutil
import subprocess
from contextlib import asynccontextmanager
from urllib.parse import quote

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import briefs_io, control, etapas, security, settings, trabalhos

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIEFS_DIR = os.path.join(ROOT, "research", "landers")
ASSETS = str(settings.ASSET_DIR)

@asynccontextmanager
async def lifespan(_app):
    control.init()
    trabalhos.init()
    yield

app = FastAPI(title="ecom-stack painel", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=os.path.join(ROOT, "painel", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(ROOT, "painel", "templates"))

# ---------- helpers ----------

def listar_briefs():
    if not os.path.isdir(BRIEFS_DIR):
        return []
    return sorted(f[:-9] for f in os.listdir(BRIEFS_DIR) if f.endswith("-brief.md"))

def caminho_brief(slug):
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        raise HTTPException(400, "slug inválido")
    p = os.path.join(BRIEFS_DIR, f"{slug}-brief.md")
    if not os.path.exists(p):
        raise HTTPException(404, "produto não encontrado")
    return p

def listar_ativos():
    encontrados = []
    for base, sub in (("creatives", "Criativos"), ("uploads", "Uploads")):
        raiz = os.path.join(ASSETS, base)
        for dirpath, _, files in os.walk(raiz):
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(dirpath, f), ASSETS)
                encontrados.append((rel, sub, os.path.getsize(os.path.join(dirpath, f))))
    return sorted(encontrados, reverse=True)

def mascarar(texto):
    if not texto:
        return ""
    t = re.sub(r"((?:HF_API_KEY|SHOPIFY_ADMIN_API_TOKEN|META_ACCESS_TOKEN|TIKTOK_ACCESS_TOKEN|PICSART_API_KEY)[A-Z_]*\s*[=:]\s*)\S+",
               r"\1****", texto)
    t = re.sub(r"(Key\s+)[A-Za-z0-9-]+:[A-Za-z0-9-]+", r"\1****", t)
    return t

def proximo_passo(briefs):
    if not briefs:
        return "Criar o primeiro produto (botão «Novo Produto») — pesquisa antes no Winning Hunter."
    return "Escolher um produto e disparar a etapa «Gerar página de vendas»."

# ---------- autenticação obrigatória ----------
PUBLIC_PATHS = ("/login", "/setup", "/health", "/static/")
LOGIN_ATTEMPTS = {}

@app.middleware("http")
async def auth(request: Request, call_next):
    path = request.url.path
    public = any(path == value or (value.endswith("/") and path.startswith(value)) for value in PUBLIC_PATHS)
    session = control.get_session(request.cookies.get("homefy_session"))
    request.state.session = session
    if not public and not session:
        return RedirectResponse("/login?next=" + quote(path), status_code=303)
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        origin = request.headers.get("origin")
        referer = request.headers.get("referer", "").rstrip("/")
        allowed = {settings.PUBLIC_ORIGIN, str(request.base_url).rstrip("/")}
        if (not origin and not any(referer.startswith(value) for value in allowed)) or (origin and origin.rstrip("/") not in allowed):
            return JSONResponse({"detail": "origem inválida"}, status_code=403)
    response = await call_next(request)
    response.headers.update({"X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY",
        "Referrer-Policy":"same-origin","Permissions-Policy":"camera=(), microphone=(), geolocation=()",
        "Content-Security-Policy":"default-src 'self'; style-src 'self'; script-src 'self' 'unsafe-inline'; connect-src 'self'"})
    if settings.COOKIE_SECURE:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

def ctx(request: Request, **values):
    values.update(request=request, session=getattr(request.state, "session", None))
    return values

@app.get("/health")
def health(): return {"status":"ok","service":"homefy-web"}

@app.get("/setup", response_class=HTMLResponse)
def setup_form(request: Request, token: str = ""):
    if control.has_admin(): return RedirectResponse("/login", status_code=303)
    client=request.client.host if request.client else ""
    return templates.TemplateResponse(request, "setup.html", ctx(request, token=token, error="", ip_allowed=control.setup_ip_allowed(client)))

@app.post("/setup", response_class=HTMLResponse)
def setup_create(request: Request, email: str=Form(...), password: str=Form(...), token: str=Form("")):
    client=request.client.host if request.client else ""
    try: control.create_admin(email, password, token, client)
    except ValueError as exc:
        return templates.TemplateResponse(request,"setup.html",ctx(request,token=token,error=str(exc),ip_allowed=control.setup_ip_allowed(client)),status_code=400)
    session_token,_=control.create_session(); response=RedirectResponse("/setup/totp",status_code=303)
    response.set_cookie("homefy_session",session_token,max_age=settings.SESSION_TTL,httponly=True,secure=settings.COOKIE_SECURE,samesite="strict")
    return response

@app.get("/setup/totp", response_class=HTMLResponse)
def setup_totp(request: Request):
    with control.conn() as c: admin=c.execute("SELECT * FROM admins WHERE id=?",(request.state.session["admin_id"],)).fetchone()
    if admin["totp_enabled"]: return RedirectResponse("/",status_code=303)
    return templates.TemplateResponse(request,"totp.html",ctx(request,secret=admin["totp_secret"],uri=security.totp_uri(admin["totp_secret"],admin["email"]),error="",recovery_codes=[]))

@app.post("/setup/totp", response_class=HTMLResponse)
def setup_totp_confirm(request: Request, code: str=Form(...)):
    codes=control.enable_totp(request.state.session["admin_id"],code)
    if not codes:
        with control.conn() as c: admin=c.execute("SELECT * FROM admins WHERE id=?",(request.state.session["admin_id"],)).fetchone()
        return templates.TemplateResponse(request,"totp.html",ctx(request,secret=admin["totp_secret"],uri=security.totp_uri(admin["totp_secret"],admin["email"]),error="Código inválido",recovery_codes=[]),status_code=400)
    return templates.TemplateResponse(request,"totp.html",ctx(request,secret="",uri="",error="",recovery_codes=codes))

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request, next: str="/"):
    if request.state.session: return RedirectResponse("/",status_code=303)
    return templates.TemplateResponse(request,"login.html",ctx(request,error="",next=next,needs_setup=not control.has_admin()))

@app.post("/login", response_class=HTMLResponse)
def login(request: Request,email: str=Form(...),password: str=Form(...),code: str=Form(""),next: str=Form("/")):
    client=request.client.host if request.client else "unknown"; now=__import__("time").time()
    attempts=[stamp for stamp in LOGIN_ATTEMPTS.get(client,[]) if now-stamp<900]
    if len(attempts)>=5:
        return templates.TemplateResponse(request,"login.html",ctx(request,error="Muitas tentativas. Aguarde 15 minutos.",next=next,needs_setup=False),status_code=429)
    admin=control.verify_login(email,password,code)
    if not admin:
        attempts.append(now); LOGIN_ATTEMPTS[client]=attempts
        control.audit("auth.failed","anonymous",{"email":email.lower().strip()})
        return templates.TemplateResponse(request,"login.html",ctx(request,error="Credenciais ou código inválidos",next=next,needs_setup=False),status_code=401)
    LOGIN_ATTEMPTS.pop(client,None); token,_=control.create_session(admin["id"]); control.audit("auth.login","admin",{})
    response=RedirectResponse(next if next.startswith("/") and not next.startswith("//") else "/",status_code=303)
    response.set_cookie("homefy_session",token,max_age=settings.SESSION_TTL,httponly=True,secure=settings.COOKIE_SECURE,samesite="strict")
    return response

@app.post("/logout")
def logout(request: Request):
    control.delete_session(request.cookies.get("homefy_session")); response=RedirectResponse("/login",status_code=303); response.delete_cookie("homefy_session"); return response

# ---------- rotas ----------

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    briefs = listar_briefs()
    ativos = listar_ativos()
    jobs=trabalhos.listar_jobs()
    return templates.TemplateResponse(request,"dashboard.html",ctx(request,briefs=briefs,jobs=jobs,
        active_jobs=sum(j["estado"] in ("fila","rodando") for j in jobs),n_ativos=len(ativos),passo=proximo_passo(briefs),approvals=control.approvals(),chats=control.chats()))

@app.get("/novo", response_class=HTMLResponse)
def novo_form(request: Request):
    return templates.TemplateResponse(request,"novo.html",ctx(request,slots=briefs_io.SECOES_SLOTS))

@app.post("/novo")
def novo_gravar(
    request: Request,
    nome: str = Form(...), slug: str = Form(...), nicho: str = Form(""),
    url_shopify: str = Form(""), preco: str = Form(""), preco_riscado: str = Form(""),
    custo: str = Form(""), margem: str = Form(""), prazo: str = Form(""),
    classificacao: str = Form("low"),
    avatar1: str = Form(""), avatar2: str = Form(""), avatar3: str = Form(""),
    desejos: list[str] = Form([]), objecoes: list[str] = Form([]),
    ref_homepage: str = Form(""), ref_homepage_nota: str = Form(""),
    ref_pdp: str = Form(""), ref_pdp_nota: str = Form(""),
    ref_hero: str = Form(""), ref_hero_nota: str = Form(""),
    ref_ads: str = Form(""), ref_ads_nota: str = Form(""),
    receita_estimada: str = Form(""),
    bundle1_preco: str = Form(""), bundle1_riscado: str = Form(""),
    bundle2_preco: str = Form(""), bundle2_riscado: str = Form(""),
    bundle3_preco: str = Form(""), bundle3_riscado: str = Form(""),
    oferta_gratis: str = Form(""), garantia: str = Form(""),
    headline: str = Form(""), beneficios: list[str] = Form([]),
    como_funciona: list[str] = Form([]), faq: list[str] = Form([]),
    nenhum_preco_sem_confirmacao: str = Form(""), claims_suavizados: str = Form(""),
    sem_logos_inventados: str = Form(""), reviews_reais: str = Form(""),
    specs_verificados: str = Form(""),
    kit_marca: str = Form(""), fotos: str = Form(""), logo: str = Form(""),
    cor_principal: str = Form(""), cor_acento: str = Form(""), cor_fundo: str = Form(""),
    slots: list[str] = Form([]),
):
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower()).strip("-")
    if not slug:
        raise HTTPException(400, "slug obrigatório")
    os.makedirs(BRIEFS_DIR, exist_ok=True)
    dados = {k: v for k, v in vars().items() if k not in ("request",)}
    dados["nome"] = nome or slug
    caminho = os.path.join(BRIEFS_DIR, f"{slug}-brief.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(briefs_io.render_brief(dados))
    return RedirectResponse(f"/p/{slug}", status_code=303)

@app.get("/p/{slug}", response_class=HTMLResponse)
def produto(request: Request, slug: str):
    p = caminho_brief(slug)
    with open(p, encoding="utf-8") as f:
        md = f.read()
    return templates.TemplateResponse(request,"produto.html",ctx(request,slug=slug,brief_html=briefs_io.md_para_html(md),etapas=etapas.ETAPAS,workflows=etapas.WORKFLOWS,jobs=trabalhos.listar_jobs(produto=slug)))

@app.post("/p/{slug}/etapa/{tipo}")
def disparar(slug: str, tipo: str):
    caminho_brief(slug)
    if tipo not in etapas.ETAPAS:
        raise HTTPException(404, "etapa desconhecida")
    with open(os.path.join(BRIEFS_DIR, f"{slug}-brief.md"), encoding="utf-8") as f:
        md = f.read()
    m = re.search(r"Benefício principal \(headline\)\*\*: (.+)", md)
    meta={"slug":slug,"headline":m.group(1).strip() if m else ""}; paid,cost=etapas.ETAPAS[tipo][2],etapas.ETAPAS[tipo][3]
    if paid:
        control.create_approval(etapas.ETAPAS[tipo][0],slug,"Usa uma API paga e cria um novo ativo",cost,{"kind":"job","product":slug,"type":tipo,"meta":meta})
        return RedirectResponse("/aprovacoes",status_code=303)
    jid=trabalhos.criar_job(slug,tipo,meta)
    control.audit("job.created","admin",{"job_id":jid,"product":slug,"type":tipo})
    return RedirectResponse(f"/trabalho/{jid}", status_code=303)

@app.post("/p/{slug}/workflow/{workflow}")
def disparar_workflow(slug: str,workflow: str):
    caminho_brief(slug)
    if workflow not in etapas.WORKFLOWS: raise HTTPException(404,"workflow desconhecido")
    jid=trabalhos.criar_job(slug,f"workflow:{workflow}",{"slug":slug,"workflow":workflow}); control.audit("workflow.started","admin",{"job_id":jid,"product":slug,"workflow":workflow})
    return RedirectResponse(f"/trabalho/{jid}",status_code=303)

@app.get("/trabalho/{jid}", response_class=HTMLResponse)
def trabalho(request: Request, jid: int):
    job = trabalhos.obter_job(jid)
    if not job:
        raise HTTPException(404, "job não encontrado")
    meta = __import__("json").loads(job["meta"] or "{}")
    return templates.TemplateResponse(request,"trabalho.html",ctx(request,job=job,meta=meta,log=mascarar(trabalhos.ler_log(jid))))

@app.get("/ativos", response_class=HTMLResponse)
def ativos(request: Request):
    return templates.TemplateResponse(request,"ativos.html",ctx(request,ativos=listar_ativos()))

@app.get("/arquivo/{caminho:path}")
def arquivo(caminho: str):
    alvo = os.path.realpath(os.path.join(ASSETS, caminho))
    if not alvo.startswith(os.path.realpath(ASSETS) + os.sep) or not os.path.isfile(alvo):
        raise HTTPException(404, "ficheiro não encontrado")
    return FileResponse(alvo)

@app.get("/chat",response_class=HTMLResponse)
def chat_index(request: Request,id: int|None=None):
    rooms=control.chats(); room=messages=None
    if id:
        room,messages=control.chat(id)
        if not room: raise HTTPException(404,"conversa não encontrada")
    return templates.TemplateResponse(request,"chat.html",ctx(request,rooms=rooms,room=room,messages=messages or [],briefs=listar_briefs()))

@app.post("/chat/new")
def chat_new(title: str=Form("Nova conversa"),product: str=Form("")):
    chat_id=control.new_chat(title or "Nova conversa",product); control.audit("chat.created","admin",{"chat_id":chat_id,"product":product}); return RedirectResponse(f"/chat?id={chat_id}",status_code=303)

@app.post("/chat/{chat_id}/message")
def chat_message(chat_id: int,message: str=Form(...)):
    room,_=control.chat(chat_id)
    if not room: raise HTTPException(404,"conversa não encontrada")
    if not message.strip() or len(message)>12000: raise HTTPException(400,"mensagem vazia ou longa demais")
    jid=trabalhos.criar_job(room["product"] or "chat","chat",{"chat_id":chat_id,"message":message.strip(),"product":room["product"]}); control.add_message(chat_id,"user",message.strip(),jid); control.audit("chat.message","admin",{"chat_id":chat_id,"job_id":jid}); return RedirectResponse(f"/chat?id={chat_id}",status_code=303)

@app.get("/aprovacoes",response_class=HTMLResponse)
def approvals_page(request: Request):
    return templates.TemplateResponse(request,"approvals.html",ctx(request,pending=control.approvals("pending"),approved=control.approvals("approved"),rejected=control.approvals("rejected")))

@app.post("/aprovacoes/{aid}")
def approval_decide(aid: int,decision: str=Form(...),note: str=Form("")):
    approval=control.get_approval(aid)
    if not control.decide_approval(aid,decision,note): raise HTTPException(409,"aprovação inexistente, expirada ou já decidida")
    if decision=="approved" and approval:
        payload=json.loads(approval["payload"] or "{}")
        if payload.get("kind")=="job":
            jid=trabalhos.criar_job(payload["product"],payload["type"],payload.get("meta") or {}); control.audit("approved_job.created","admin",{"approval_id":aid,"job_id":jid})
    return RedirectResponse("/aprovacoes",status_code=303)

@app.get("/auditoria",response_class=HTMLResponse)
def audit_page(request: Request): return templates.TemplateResponse(request,"audit.html",ctx(request,events=control.recent_audit(100)))

@app.get("/api/system/health")
def system_health():
    hermes=shutil.which("hermes") or "/root/.local/bin/hermes"
    try: version=subprocess.run([hermes,"--version"],capture_output=True,text=True,timeout=5).stdout.strip()
    except Exception: version="indisponível"
    return {"web":"ok","worker_queue":sum(j["estado"] in ("fila","rodando") for j in trabalhos.listar_jobs()),"hermes":version,"aiox":"5.4.1","production_publish":"blocked"}

@app.get("/api/events")
async def events():
    async def stream():
        import asyncio
        for _ in range(60):
            latest=trabalhos.listar_jobs(limite=10); payload=[{"id":j["id"],"state":j["estado"],"type":j["tipo"],"product":j["produto"]} for j in latest]
            yield "data: "+json.dumps(payload,ensure_ascii=False)+"\n\n"; await asyncio.sleep(2)
    return StreamingResponse(stream(),media_type="text/event-stream",headers={"Cache-Control":"no-cache"})
