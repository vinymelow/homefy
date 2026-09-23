#!/usr/bin/env python3
"""
ecom-stack Dashboard — interface web local (sem dependências externas).

Uso:  python3 dashboard/server.py [--porta 8000]

Serve uma página de gestão do projeto em http://IP_DO_VPS:8000
Proteção: chave de acesso (DASHBOARD_KEY no config/.env, ou gerada no arranque —
é impressa no terminal). Abre sempre com ?key=A_TUA_CHAVE.
"""
import os, sys, json, time, urllib.request, argparse, secrets, html
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.environ.get("ECOM_ENV_FILE", os.path.join(ROOT, "config", ".env"))
LANDERS_DIR = os.path.join(ROOT, "research", "landers")
CREATIVES_DIR = os.path.join(ROOT, "assets", "creatives")
BRIEF_TEMPLATE = os.path.join(ROOT, "templates", "product-brief.md")

# ---------- helpers ----------

def load_env():
    env = {}
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

ENV = load_env()
KEY = ENV.get("DASHBOARD_KEY") or secrets.token_urlsafe(8)
_shopify_cache = {"t": 0, "ok": None, "detail": ""}

def slugify(s):
    return "".join(c if c.isalnum() or c == "-" else "-" for c in s.lower()).strip("-")

def shopify_status(force=False):
    if not force and time.time() - _shopify_cache["t"] < 60:
        return _shopify_cache["ok"], _shopify_cache["detail"]
    store, token = ENV.get("SHOPIFY_STORE_DOMAIN"), ENV.get("SHOPIFY_ADMIN_API_TOKEN")
    if not (store and token):
        _shopify_cache.update(t=time.time(), ok=False, detail="sem credenciais no .env")
        return False, "sem credenciais no .env"
    ver = ENV.get("SHOPIFY_API_VERSION", "2025-07")
    try:
        req = urllib.request.Request(f"https://{store}/admin/api/{ver}/themes.json",
                                     headers={"X-Shopify-Access-Token": token})
        with urllib.request.urlopen(req, timeout=15) as r:
            themes = json.loads(r.read())["themes"]
        main = next((t for t in themes if t.get("role") == "main"), None)
        _shopify_cache.update(t=time.time(), ok=True,
                              detail=f"{len(themes)} tema(s) · MAIN: {main['name']}")
        return True, _shopify_cache["detail"]
    except Exception as e:
        _shopify_cache.update(t=time.time(), ok=False, detail=str(e))
        return False, str(e)

def briefs():
    if not os.path.isdir(LANDERS_DIR):
        return []
    return sorted(f for f in os.listdir(LANDERS_DIR) if f.endswith("-brief.md"))

def creatives():
    if not os.path.isdir(CREATIVES_DIR):
        return []
    return sorted(os.listdir(CREATIVES_DIR))

def render_brief_md(form):
    """Gera o markdown do brief a partir do formulário do wizard."""
    def L(v): return v.strip()
    checks = "\n".join(f"- [{'x' if c in form.get('guardrails', []) else ' '}] {c}"
                       for c in ["Sem preços/garantias/stock inventados",
                                 "Claims de saúde suavizadas",
                                 "Reviews reais ou 'Dramatized customer story'",
                                 "Specs verificadas no fornecedor",
                                 "Fotos reais do produto para cutout"])
    return f"""# Brief — {L(form.get('nome',''))}

> Slug: `{slugify(form.get('slug') or form.get('nome',''))}` · Criado via dashboard em {time.strftime('%Y-%m-%d %H:%M')}

## 1. Dados base
- **Nome do produto:** {L(form.get('nome',''))}
- **URL do produto (fornecedor):** {L(form.get('url',''))}
- **Nicho:** {L(form.get('nicho',''))}
- **Preço de venda:** {L(form.get('preco',''))}
- **Classificação:** {'Alta consideração' if form.get('classificacao') == 'high' else 'Baixo risco / impulso'}
- **Custo do produto + envio:** {L(form.get('custo',''))}

## 2. Avatar principal
- **Quem:** {L(form.get('avatar',''))}
- **Desejo nº1 (ranked):** {L(form.get('desejo',''))}
- **Objeção nº1 a destruir:** {L(form.get('objecao',''))}

## 3. Referências (3 fontes — método do tutor)
| # | Tipo | URL | O que emprestar |
|---|------|-----|-----------------|
| 1 | Homepage | {L(form.get('ref1',''))} | {L(form.get('ref1_oq',''))} |
| 2 | Landing page / PDP | {L(form.get('ref2',''))} | {L(form.get('ref2_oq',''))} |
| 3 | Hero section | {L(form.get('ref3',''))} | {L(form.get('ref3_oq',''))} |

## 4. Oferta
- **Headline (4–8 palavras, língua do cliente):** {L(form.get('headline',''))}
- **Bundles:** {L(form.get('bundles',''))}
- **Garantia (tem de existir na Shopify):** {L(form.get('garantia',''))}

## 5. Guardrails (todos têm de estar OK)
{checks}

## 6. Slots criativos (gerar depois)
hero-main · angle-1..3 · lifestyle-1/2 · infographic-1 · ugc-video · review-avatar-1..3 · final-bg

---
### TODO antes de gerar a landing page
- [ ] Confirmar que o produto existe na Shopify (rascunho) com variantes/imagens reais
- [ ] Copiar este brief para o chat da Kimi + as 3 URLs de referência
- [ ] Aprovar copy gerada contra os guardrails acima
"""

# ---------- HTML ----------

PAGE = """<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ecom-stack — dashboard</title>
<style>
:root{--bg:#F5F6F2;--ink:#111;--accent:#FF5F1F;--line:#e2e4dc;--ok:#1a7f37;--bad:#c0392b}
*{box-sizing:border-box;margin:0}
body{font-family:-apple-system,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--ink);padding:24px;max-width:960px;margin:auto}
h1{font-size:22px;letter-spacing:-.02em}
h2{font-size:15px;text-transform:uppercase;letter-spacing:.08em;margin:28px 0 10px;color:#555}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .k{font-size:12px;color:#777;text-transform:uppercase;letter-spacing:.06em}
.card .v{font-size:18px;font-weight:700;margin-top:4px}
.ok{color:var(--ok)}.bad{color:var(--bad)}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);font-size:13px;text-align:left}
th{background:#fafbf8;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#777}
label{display:block;font-size:12px;color:#555;margin:10px 0 3px}
input,select,textarea{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font-size:13px;background:#fff;font-family:inherit}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:10px 18px;font-size:14px;font-weight:600;cursor:pointer;margin-top:14px}
.flash{margin:12px 0;padding:10px 14px;border-radius:8px;font-size:13px;display:none}
.flash.ok{display:block;background:#e7f6ec;color:var(--ok)}
.flash.bad{display:block;background:#fdeceb;color:var(--bad)}
.mono{font-family:ui-monospace,Consolas,monospace;font-size:12px}
small{color:#888}
details summary{cursor:pointer;font-size:13px;margin-top:8px}
</style>
</head>
<body>
<h1>ecom-stack <small>— homefy · vps</small></h1>

<div class="cards" style="margin-top:18px">
  <div class="card"><div class="k">Shopify</div><div class="v" id="shopify">…</div></div>
  <div class="card"><div class="k">Briefs</div><div class="v" id="nbriefs">…</div></div>
  <div class="card"><div class="k">Criativos</div><div class="v" id="ncriativos">…</div></div>
  <div class="card"><div class="k">Próximo passo</div><div class="v" style="font-size:13px" id="next">…</div></div>
</div>

<h2>Briefs de produto</h2>
<table><thead><tr><th>Ficheiro</th><th></th></tr></thead><tbody id="briefs"></tbody></table>

<h2>Novo brief (wizard)</h2>
<div class="card">
<form id="fbrief">
  <div class="cards">
    <div><label>Nome do produto *</label><input name="nome" required></div>
    <div><label>Slug (opcional — gera-se do nome)</label><input name="slug"></div>
  </div>
  <label>URL do produto no fornecedor *</label><input name="url" required placeholder="https://…">
  <div class="cards">
    <div><label>Nicho</label><select name="nicho"><option>Casa e utilidades</option><option>Beleza e cuidados pessoais</option><option>Outro</option></select></div>
    <div><label>Preço de venda (€)</label><input name="preco" placeholder="39.99"></div>
    <div><label>Custo + envio (€)</label><input name="custo" placeholder="12"></div>
  </div>
  <label>Classificação do produto</label>
  <select name="classificacao"><option value="low">Baixo risco / impulso (€20–40)</option><option value="high">Alta consideração (€40–70+)</option></select>
  <label>Avatar principal (quem compra, 1 frase) *</label><input name="avatar" required>
  <div class="cards">
    <div><label>Desejo nº1 (o que querem) *</label><input name="desejo" required></div>
    <div><label>Objeção nº1 (o que impede) *</label><input name="objecao" required></div>
  </div>
  <label>Referência 1 — Homepage (URL + o que emprestar) *</label>
  <div class="cards"><div style="flex:2"><input name="ref1" placeholder="https://loja-concorrente.com"></div><div><input name="ref1_oq" placeholder="ex.: faixa de confiança, galeria"></div></div>
  <label>Referência 2 — Landing page / PDP</label>
  <div class="cards"><div style="flex:2"><input name="ref2" placeholder="https://…"></div><div><input name="ref2_oq" placeholder="o que emprestar"></div></div>
  <label>Referência 3 — Hero section</label>
  <div class="cards"><div style="flex:2"><input name="ref3" placeholder="https://…"></div><div><input name="ref3_oq" placeholder="o que emprestar"></div></div>
  <label>Headline (4–8 palavras, língua do cliente)</label><input name="headline" placeholder="Get Rid of X Without Y">
  <label>Bundles (ex.: 1 un €39 · 2 un €69 · 3 un €89)</label><input name="bundles">
  <label>Garantia (só se existir na Shopify)</label><input name="garantia" placeholder="30 dias">
  <div id="gr" style="margin-top:12px"></div>
  <button type="submit">Criar brief</button>
  <div class="flash" id="flash"></div>
</form>
</div>

<h2>Plano de teste</h2>
<div class="card mono" style="white-space:pre-wrap" id="plano">…</div>
<p style="margin-top:20px"><small>ecom-stack · os ficheiros editam-se no VS Code (Remote-SSH) · este painel só lê/cria briefs</small></p>

<script>
const KEY = new URLSearchParams(location.search).get('key') || '';
const GR = ["Sem preços/garantias/stock inventados","Claims de saúde suavizadas","Reviews reais ou 'Dramatized customer story'","Specs verificadas no fornecedor","Fotos reais do produto para cutout"];
document.getElementById('gr').innerHTML = GR.map(g =>
  `<label style="display:flex;gap:8px;align-items:center;font-size:13px;margin:4px 0">
   <input type="checkbox" name="guardrails" value="${g}" style="width:auto"> ${g}</label>`).join('');

async function api(path, opts) {
  const r = await fetch(path + '?key=' + KEY, opts);
  if (r.status === 403) { document.body.innerHTML = '<h1>403 — chave inválida</h1>'; throw 0; }
  return r.json();
}

async function refresh() {
  const s = await api('/api/status');
  const el = document.getElementById('shopify');
  el.textContent = s.shopify_ok ? 'ligado' : 'falhou';
  el.className = 'v ' + (s.shopify_ok ? 'ok' : 'bad');
  el.title = s.shopify_detail;
  document.getElementById('nbriefs').textContent = s.briefs.length;
  document.getElementById('ncriativos').textContent = s.creatives.length;
  document.getElementById('next').textContent =
    !s.shopify_ok ? 'Corrigir Shopify (.env)' :
    s.briefs.length === 0 ? 'Pesquisar no Winning Hunter → criar brief' :
    s.creatives.length === 0 ? 'Gerar criativos (Kimi) → assets/creatives' : 'Publicar landing page';
  document.getElementById('briefs').innerHTML = s.briefs.map(b =>
    `<tr><td class="mono">${b}</td><td><a href="#" onclick="viewBrief('${b}');return false">ver</a></td></tr>`).join('')
    || '<tr><td colspan="2"><small>nenhum ainda</small></td></tr>';
}

async function viewBrief(f) {
  const b = await api('/api/brief/' + encodeURIComponent(f));
  const w = window.open('', '_blank');
  w.document.write('<pre style="white-space:pre-wrap;font-family:monospace;padding:20px">' +
    b.content.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</pre>');
}

document.getElementById('fbrief').addEventListener('submit', async e => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const data = Object.fromEntries(fd.entries());
  data.guardrails = fd.getAll('guardrails');
  const r = await fetch('/api/brief?key=' + KEY, {method:'POST', body: JSON.stringify(data)});
  const out = await r.json();
  const flash = document.getElementById('flash');
  flash.className = 'flash ' + (r.ok ? 'ok' : 'bad');
  flash.textContent = out.message || (r.ok ? 'Brief criado.' : 'Erro.');
  if (r.ok) { e.target.reset(); refresh(); }
});

api('/api/plano').then(p => document.getElementById('plano').textContent = p.plano);
refresh();
</script>
</body>
</html>
"""

PLANO = """== Plano de teste ==
Orçamento:  €20–50/dia × 3 dias (máx €150)
Plataforma: TikTok Ads + Meta Ads (Advantage+ shopping ou CBO 3 adsets)
Países:     US, CA, AU, NZ, UK — separar UK num adset (CPMs diferentes)
Criativos:  2–3 vídeos 9:16 (formatos A/B/C de prompts/criativos.md)
Evento:     Purchase (pixel + CAPI verificados antes de lançar)
Mata se:    CTR<1% ao fim do dia 2, ou CPA>€35 sem compra
Escala se:  CPA<€15 → +20%/dia; CPA €15–35 → testar 2 criativos novos
Métricas completas: docs/blueprint-pagina-de-vendas.md secção 5"""

# ---------- servidor ----------

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silenciar logs de acesso
        pass

    def _check(self, params):
        if params.get("key", [""])[0] != KEY:
            self.send_response(403); self.end_headers()
            self.wfile.write(b"forbidden"); return False
        return True

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        u = urlparse(self.path)
        p = parse_qs(u.query)
        if u.path == "/" :
            if not self._check(p): return
            body = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
        elif u.path == "/api/status":
            if not self._check(p): return
            ok, detail = shopify_status()
            self._json({"shopify_ok": ok, "shopify_detail": detail,
                        "briefs": briefs(), "creatives": creatives()})
        elif u.path == "/api/brief/" and p.get("f"):
            if not self._check(p): return
            f = os.path.basename(p["f"][0])
            fp = os.path.join(LANDERS_DIR, f)
            if not os.path.isfile(fp): return self._json({"error": "não encontrado"}, 404)
            self._json({"content": open(fp).read()})
        elif u.path == "/api/plano":
            if not self._check(p): return
            self._json({"plano": PLANO})
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        from urllib.parse import urlparse, parse_qs
        u = urlparse(self.path)
        p = parse_qs(u.query)
        if u.path != "/api/brief" or not self._check(p):
            if u.path == "/api/brief": return
            return
        try:
            form = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except Exception:
            return self._json({"message": "JSON inválido"}, 400)
        nome = (form.get("nome") or "").strip()
        if not nome:
            return self._json({"message": "Nome do produto é obrigatório"}, 400)
        slug = slugify(form.get("slug") or nome)
        os.makedirs(LANDERS_DIR, exist_ok=True)
        dest = os.path.join(LANDERS_DIR, f"{slug}-brief.md")
        if os.path.exists(dest):
            return self._json({"message": f"Já existe: {dest}"}, 409)
        open(dest, "w").write(render_brief_md(form))
        self._json({"message": f"Criado: {dest}", "slug": slug})

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--porta", type=int, default=8000)
    a = ap.parse_args()
    if not ENV.get("DASHBOARD_KEY"):
        print(f"[dashboard] DASHBOARD_KEY não definido no .env — chave desta sessão: {KEY}")
    print(f"[dashboard] em execução: http://{os.popen('hostname -I').read().split()[0]}:{a.porta}/?key={KEY}")
    print("[dashboard] Ctrl+C para parar. Em background: nohup python3 dashboard/server.py &")
    HTTPServer(("0.0.0.0", a.porta), H).serve_forever()