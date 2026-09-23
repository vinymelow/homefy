"""Conversão entre o formulário do painel e o ficheiro product-brief.md.

O ficheiro markdown é a fonte de verdade do projeto (cli.py e os prompts
leem-no diretamente), por isso o render aqui reproduz o template exato de
templates/product-brief.md.
"""
import html
import re

SECOES_SLOTS = [
    ("hero-main", "Benefit Stack (foto real em uso + painel translúcido)"),
    ("recognition-1/2", "Avatares a reconhecer o problema (só high-consideration)"),
    ("payoff-1/2/3", "1 imagem por desejo ranqueado"),
    ("infographic-mech", "Mechanism Explainer (cutaway + glow)"),
    ("how-to", "How-To Steps"),
    ("vs-alternative", "Comparação"),
    ("angle-1/2/3", "Ângulos reais do produto (foto, não IA)"),
    ("lifestyle-1/2", "Hiper-realistas (5 chaves), 2 variantes"),
    ("ugc-video", "Vídeo 9:16 para ads e página"),
    ("static-ads-1/2/3", "Clones de ads vencedores (3 variantes)"),
]

CAMPOS_GUARDAR = [
    "nenhum_preco_sem_confirmacao", "claims_suavizados", "sem_logos_inventados",
    "reviews_reais", "specs_verificados",
]

def _v(d, chave, default=""):
    val = d.get(chave, default)
    if isinstance(val, list):
        return [str(x).strip() for x in val]
    return str(val).strip()

def _check(valor):
    return "x" if valor else " "

def render_brief(d):
    n = lambda k: _v(d, k)
    lst = lambda k, i: (_v(d, k)[i] if isinstance(_v(d, k), list) and len(_v(d, k)) > i else "")
    clas = n("classificacao")
    hc = "x" if clas == "high" else " "
    lc = "x" if clas == "low" else " "
    linhas = []

    a = f"{n('avatar1')}\n- **Avatar 2** (se houver): {n('avatar2')}\n- **Avatar 3** (se houver): {n('avatar3')}"
    if not n('avatar2') and not n('avatar3'):
        a = n('avatar1')

    linhas.append(f"""# Product Brief — {n('nome').upper() or '[NOME DO PRODUTO]'}

> Preencher ISTO antes de pedir a landing page OU os criativos.
> Gerado pelo painel ecom-stack em `research/landers/{n('slug')}-brief.md`

## 1. Dados base
- **Slug/nome curto**: {n('slug')}
- **Nicho**: {n('nicho')} (casa & utilidades / beleza & cuidados pessoais)
- **URL do produto no Shopify** (obrigatório — tem de existir antes do Liquid): {n('url_shopify')}
- **Preço de venda**: €{n('preco')}   | **Preço riscado**: €{n('preco_riscado')}
- **Custo do produto + envio**: €{n('custo')}   | **Margem estimada**: {n('margem')}%
- **Prazo de entrega prometido**: {n('prazo')}

## 2. Classificação do produto (método EcomAlchemist — decide a sequência de criativos)
- [{hc}] **High-consideration** (saúde/beleza com claims, preço alto, comprador cético)
      → galeria PDP completa: 9–11 frames (hero → recognition → pivot → mechanism →
      payoffs → how-easy → for/not-for → proof → offer)
- [{lc}] **Low-stakes** (barato, visual, impulso — maioria de casa/utilidades)
      → galeria curta: hero + payoffs + how-to + comparação + prova + oferta

## 3. Público e promessa
- **Avatar 1** (principal): {n('avatar1')}
- **Avatar 2** (se houver): {n('avatar2')}
- **Avatar 3** (se houver): {n('avatar3')}
- **Desejos ranqueados** (o resultado que cada avatar quer, por ordem de intensidade):
  1. {lst('desejos', 0)}
  2. {lst('desejos', 1)}
  3. {lst('desejos', 2)}
- **Objeções principais** (cada uma TEM de ser respondida por uma imagem ou secção):
  1. {lst('objecoes', 0)}
  2. {lst('objecoes', 1)}
  3. {lst('objecoes', 2)}

## 4. Referências escolhidas (Winning Hunter / ad library)
| Componente | URL | O que vou copiar |
|---|---|---|
| Homepage | {n('ref_homepage')} | {n('ref_homepage_nota')} |
| Landing page (PDP) | {n('ref_pdp')} | {n('ref_pdp_nota')} |
| Hero section | {n('ref_hero')} | {n('ref_hero_nota')} |
| Ads vencedores (ad library, filtrar por spend) | {n('ref_ads')} | {lst('ref_ads_frames', 0) if isinstance(_v(d,'ref_ads_frames'), list) else n('ref_ads_nota')} |

- **Receita estimada da loja alvo**: {n('receita_estimada')}

## 5. Oferta e bundles (ligar a produtos REAIS do Shopify)
- **Bundle 1** (1 unidade): €{n('bundle1_preco')} / riscado €{n('bundle1_riscado')}
- **Bundle 2** (mais popular): €{n('bundle2_preco')} / riscado €{n('bundle2_riscado')}
- **Bundle 3** (melhor valor): €{n('bundle3_preco')} / riscado €{n('bundle3_riscado')}
- **Painel de oferta grátis**: {n('oferta_gratis')}
- **Garantia**: {n('garantia')}

## 6. Copy
- **Benefício principal (headline)**: {n('headline')}
- **Benefícios (máx. 5, escaneáveis)**:
  1. {lst('beneficios', 0)}
  2. {lst('beneficios', 1)}
  3. {lst('beneficios', 2)}
  4. {lst('beneficios', 3)}
  5. {lst('beneficios', 4)}
- **Como funciona (3 passos)**:
  1. {lst('como_funciona', 0)}
  2. {lst('como_funciona', 1)}
  3. {lst('como_funciona', 2)}
- **FAQ**:
  1. {lst('faq', 0)}
  2. {lst('faq', 1)}
  3. {lst('faq', 2)}
  4. {lst('faq', 3)}

## 7. Guardrails de claims
- [{_check(n('nenhum_preco_sem_confirmacao'))}] Nenhum preço/desconto/prazo/garantia sem confirmação na loja ou no fornecedor
- [{_check(n('claims_suavizados'))}] Claims de saúde/beleza suavizados ("designed to help with", não "cura/trata")
- [{_check(n('sem_logos_inventados'))}] Sem logos de imprensa/endorsements inventados
- [{_check(n('reviews_reais'))}] Reviews = reais da loja OU "Dramatized customer story" legível
- [{_check(n('specs_verificados'))}] Specs (medidas, materiais, tempos) verificados — senão BLOCKED

## 8. Assets e identidade
- **Kit de marca**: {n('kit_marca')}
- **Fotos reais do produto**: {n('fotos')}
- **Logo**: {n('logo')}
- **Cores da marca**: principal {n('cor_principal')} / acento {n('cor_acento')} / fundo {n('cor_fundo')}

## 9. Slots de criativos necessários (página + ads)""")
    selecionados = d.get("slots") or []
    for slot, desc in SECOES_SLOTS:
        marca = "x" if slot in selecionados else " "
        linhas.append(f"- [{marca}] `{slot}` — {desc}")
    return "\n".join(linhas) + "\n"

_MARCADOR = re.compile(r"^(#{1,4})\s+(.*)$")
_BOLD = re.compile(r"\*\*(.+?)\*\*")

def md_para_html(texto):
    """Markdown mínimo para exibir o brief (headers, listas, negrito, checkboxes)."""
    out, em_lista = [], False
    for raw in texto.splitlines():
        linha = raw.rstrip()
        m = _MARCADOR.match(linha)
        if m:
            if em_lista:
                out.append("</ul>")
                em_lista = False
            nivel = len(m.group(1)) + 1
            out.append(f"<h{nivel}>{_inline(m.group(2))}</h{nivel}>")
        elif linha.startswith("- ") or re.match(r"^\s+\d+\.\s", linha):
            if not em_lista:
                out.append("<ul>")
                em_lista = True
            item = re.sub(r"^(- |\s+\d+\.\s)", "", linha)
            item = item.replace("[ ]", "☐").replace("[x]", "☑")
            out.append(f"<li>{_inline(item)}</li>")
        elif linha.strip() == "":
            if em_lista:
                out.append("</ul>")
                em_lista = False
        elif linha.startswith(">"):
            out.append(f"<p class='nota'>{_inline(linha.lstrip('> '))}</p>")
        else:
            if em_lista:
                out.append("</ul>")
                em_lista = False
            out.append(f"<p>{_inline(linha)}</p>")
    if em_lista:
        out.append("</ul>")
    return "\n".join(out)

def _inline(t):
    t = html.escape(t)
    t = _BOLD.sub(r"<strong>\1</strong>", t)
    return t
