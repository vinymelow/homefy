"""Painel web do ecom-stack — orquestra o pipeline de produto.

Arranque:  python3 cli/cli.py painel   (ou uvicorn painel.app:app)
Acesso:    túnel SSH  ssh -L 8787:localhost:8787 root@<vps>
"""
import os
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import briefs_io, etapas, trabalhos

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIEFS_DIR = os.path.join(ROOT, "research", "landers")
ASSETS = os.path.join(ROOT, "assets")
TOKEN = os.environ.get("PAINEL_TOKEN", "")

@asynccontextmanager
async def lifespan(_app):
    trabalhos.arrancar_worker()
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

# ---------- auth (opcional, só se PAINEL_TOKEN estiver definido) ----------

@app.middleware("http")
async def auth(request: Request, call_next):
    if TOKEN:
        cookie = request.cookies.get("painel_token")
        if request.query_params.get("token") == TOKEN:
            resp = await call_next(request)
            resp.set_cookie("painel_token", TOKEN, max_age=7*86400, httponly=True)
            return resp
        if cookie != TOKEN:
            return HTMLResponse("<h1>403</h1><p>Token em falta: acede com ?token=SEU_TOKEN</p>", status_code=403)
    return await call_next(request)

# ---------- rotas ----------

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    briefs = listar_briefs()
    ativos = listar_ativos()
    return templates.TemplateResponse(request, "dashboard.html", {
        "request": request, "briefs": briefs, "jobs": trabalhos.listar_jobs(),
        "n_ativos": len(ativos), "passo": proximo_passo(briefs)})

@app.get("/novo", response_class=HTMLResponse)
def novo_form(request: Request):
    return templates.TemplateResponse(request, "novo.html", {
        "request": request, "slots": briefs_io.SECOES_SLOTS})

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
    return templates.TemplateResponse(request, "produto.html", {
        "request": request, "slug": slug, "brief_html": briefs_io.md_para_html(md),
        "etapas": etapas.ETAPAS, "jobs": trabalhos.listar_jobs(produto=slug)})

@app.post("/p/{slug}/etapa/{tipo}")
def disparar(slug: str, tipo: str):
    caminho_brief(slug)
    if tipo not in etapas.ETAPAS:
        raise HTTPException(404, "etapa desconhecida")
    with open(os.path.join(BRIEFS_DIR, f"{slug}-brief.md"), encoding="utf-8") as f:
        md = f.read()
    m = re.search(r"Benefício principal \(headline\)\*\*: (.+)", md)
    jid = trabalhos.criar_job(slug, tipo, {"slug": slug, "headline": m.group(1).strip() if m else ""})
    return RedirectResponse(f"/trabalho/{jid}", status_code=303)

@app.get("/trabalho/{jid}", response_class=HTMLResponse)
def trabalho(request: Request, jid: int):
    job = trabalhos.obter_job(jid)
    if not job:
        raise HTTPException(404, "job não encontrado")
    meta = __import__("json").loads(job["meta"] or "{}")
    return templates.TemplateResponse(request, "trabalho.html", {
        "request": request, "job": job, "meta": meta, "log": mascarar(trabalhos.ler_log(jid))})

@app.get("/ativos", response_class=HTMLResponse)
def ativos(request: Request):
    return templates.TemplateResponse(request, "ativos.html", {
        "request": request, "ativos": listar_ativos()})

@app.get("/arquivo/{caminho:path}")
def arquivo(caminho: str):
    alvo = os.path.realpath(os.path.join(ASSETS, caminho))
    if not alvo.startswith(os.path.realpath(ASSETS) + os.sep) or not os.path.isfile(alvo):
        raise HTTPException(404, "ficheiro não encontrado")
    return FileResponse(alvo)
