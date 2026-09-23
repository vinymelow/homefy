#!/usr/bin/env python3
"""
ecom-stack CLI — ponto de entrada único do projeto.

Uso:  python3 cli/cli.py <comando> [opções]

Comandos:
  ajuda                    mostra esta ajuda
  status                   estado do projeto + próximo passo sugerido
  brief novo <slug>        cria research/landers/<slug>-brief.md a partir do template
  brief listar             lista os briefs existentes
  criativo imagem <slug> [--slot SLOT]   gera imagem via API configurada no .env
  criativo video <slug> [--formato A]    gera vídeo via API configurada no .env
  anuncio plano <slug>     imprime o plano de teste (orçamento, países, métricas)
  doctor                   verifica .env e testa a ligação à Shopify
"""
import os, sys, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIEF_TEMPLATE = os.path.join(ROOT, "templates", "product-brief.md")
LANDERS_DIR = os.path.join(ROOT, "research", "landers")
CREATIVES_DIR = os.path.join(ROOT, "assets", "creatives")
ENV_FILE = os.environ.get("ECOM_ENV_FILE", os.path.join(ROOT, "config", ".env"))

def load_env():
    env = {}
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

def slugify(s):
    return "".join(c if c.isalnum() or c == "-" else "-" for c in s.lower()).strip("-")

def cmd_status():
    briefs = [f for f in os.listdir(LANDERS_DIR) if f.endswith("-brief.md")] \
        if os.path.isdir(LANDERS_DIR) else []
    creatives = os.listdir(CREATIVES_DIR) if os.path.isdir(CREATIVES_DIR) else []
    env = load_env()
    print("== ecom-stack — status ==")
    print(f"briefs de produto: {len(briefs)}", briefs or "(nenhum)")
    print(f"criativos em assets/creatives: {len(creatives)}", creatives or "(nenhum)")
    print(f".env configurado: {'sim' if env else 'não — copiar config/config.example.env'}")
    if not briefs:
        print("\nPróximo passo: pesquisar no Winning Hunter e preencher research/landers/ (ver prompts/pesquisa-produto.md)")
    elif not creatives:
        print("\nPróximo passo: gerar criativos com prompts/criativos.md")
    else:
        print("\nPróximo passo: pedir à Kimi Code a landing page com prompts/pagina-vendas.md")

def cmd_brief_novo(slug):
    slug = slugify(slug)
    os.makedirs(LANDERS_DIR, exist_ok=True)
    dest = os.path.join(LANDERS_DIR, f"{slug}-brief.md")
    if os.path.exists(dest):
        sys.exit(f"Já existe: {dest}")
    shutil.copy(BRIEF_TEMPLATE, dest)
    print(f"Criado: {dest}\nPreenche TUDO antes de gerar a landing page.")

def cmd_brief_listar():
    files = [f for f in os.listdir(LANDERS_DIR) if f.endswith("-brief.md")] \
        if os.path.isdir(LANDERS_DIR) else []
    print("\n".join(files) if files else "Sem briefs ainda.")

def cmd_criativo(tipo, slug, slot=None, formato=None):
    env = load_env()
    if not env:
        sys.exit("Configura em config/.env primeiro (ver docs/integracoes-cli.md).")
    slug = slugify(slug)
    brief = os.path.join(LANDERS_DIR, f"{slug}-brief.md")
    if not os.path.exists(brief):
        sys.exit(f"Sem brief para '{slug}'. Cria: python3 cli/cli.py brief novo {slug}")
    print(f"[{tipo}] brief: {brief}")
    if tipo == "imagem":
        print(f"slot: {slot or 'hero-main'} → ver prompts/criativos.md secção 2")
    else:
        print(f"formato: {formato or 'A'} → ver prompts/criativos.md secção 3")
    print("API: a implementar quando o .env tiver chaves (docs/integracoes-cli.md).")

def cmd_anuncio_plano(slug):
    print(f"""== Plano de teste — {slug} ==
Orçamento:  €20–50/dia × 3 dias (máx €150)
Plataforma: TikTok Ads + Meta Ads ( Advantage+ shopping ou CBO 3 adsets )
Países:     US, CA, AU, NZ, UK — separar UK num adset (CPMs diferentes)
Criativos:  2–3 vídeos 9:16 (formatos A/B/C de prompts/criativos.md)
Evento:     Purchase (pixel + CAPI verificados antes de lançar)
Mata se:    CTR<1% ao fim do dia 2, ou CPA>€35 sem compra
Escala se:  CPA<€15 → +20%/dia; CPA €15–35 → testar 2 criativos novos
Métricas completas: docs/blueprint-pagina-de-vendas.md secção 5""")

def cmd_doctor():
    import json, urllib.request
    env = load_env()
    print("== ecom-stack — doctor ==")
    if not env:
        sys.exit(".env não encontrado — copiar config/config.example.env → config/.env")
    keys = ["SHOPIFY_STORE_DOMAIN", "SHOPIFY_ADMIN_API_TOKEN",
            "META_ACCESS_TOKEN", "META_AD_ACCOUNT_ID",
            "TIKTOK_ACCESS_TOKEN", "TIKTOK_ADVERTISER_ID", "PICSART_API_KEY"]
    for k in keys:
        v = env.get(k, "")
        print(f"  {k}: {'OK' if v else '— vazio' + (' (adiável)' if k.split('_')[0] in ('META','TIKTOK','PICSART') else ' (OBRIGATÓRIO p/ Fase 2)')}")
    store, token = env.get("SHOPIFY_STORE_DOMAIN"), env.get("SHOPIFY_ADMIN_API_TOKEN")
    ver = env.get("SHOPIFY_API_VERSION", "2025-07")
    if store and token:
        try:
            req = urllib.request.Request(
                f"https://{store}/admin/api/{ver}/themes.json",
                headers={"X-Shopify-Access-Token": token})
            with urllib.request.urlopen(req, timeout=15) as r:
                themes = json.loads(r.read())["themes"]
            main = next((t for t in themes if t.get("role") == "main"), None)
            print(f"\nShopify: ligado — {len(themes)} tema(s). MAIN: '{main['name']}' (id {main['id']}) — read-only, duplicar antes de escrever.")
        except Exception as e:
            sys.exit(f"\nShopify: FALHA — {e}\nVerifica SHOPIFY_STORE_DOMAIN/SHOPIFY_ADMIN_API_TOKEN e os scopes do app (docs/setup-vps.md §2).")
    else:
        print("\nShopify: sem credenciais — seguir docs/setup-vps.md §2 (única integração obrigatória agora).")

COMMANDS = {
    "status": lambda a: cmd_status(),
    "doctor": lambda a: cmd_doctor(),
    "brief": lambda a: {"novo": cmd_brief_novo, "listar": cmd_brief_listar}[a[0]](*a[1:]),
    "criativo": lambda a: cmd_criativo(a[0], a[1], a[a.index("--slot")+1] if "--slot" in a else None,
                                       a[a.index("--formato")+1] if "--formato" in a else None),
    "anuncio": lambda a: {"plano": cmd_anuncio_plano}[a[0]](*a[1:]),
}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "ajuda":
        print(__doc__)
        sys.exit(0)
    fn = COMMANDS.get(args[0])
    if not fn:
        sys.exit(f"Comando desconhecido: {args[0]}\n\n{__doc__}")
    try:
        fn(args[1:])
    except (KeyError, IndexError):
        sys.exit(f"Argumentos inválidos para '{args[0]}'.\n\n{__doc__}")