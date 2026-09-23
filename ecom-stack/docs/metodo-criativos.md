# Método de criativos — consolidação dos documentos do tutor

Síntese operacional de 4 fontes: `clone-static-ad.md`, `hyperreal-image.skill`,
`product-pdp-image-builder.skill` (+ `references/infographic-recipes.md`) e a secção
de imagens do vídeo do Ecom King. Usa este documento como SOP de produção de criativos.

## Princípio unificador

Toda a imagem/vídeo que sai deste projeto deriva de **ads e páginas que já estão a
gerar dinheiro** (ad library dos concorrentes filtrado por spend, Landers do Winning
Hunter). Nada é criado "do zero": clona-se a estrutura vencedora e troca-se marca +
produto + copy. A imagem do produto é SEMPRE a foto real do produto (recortada),
nunca regenerada por IA.

## Pipeline por produto

```
1. ADS DE REFERÊNCIA  →  2. ANÁLISE ZONA-A-ZONA  →  3. COPY REESCRITA
   (ad library + WH)      (ficha de dissecação)      (estrutura mantida,
                                                      marca trocada)
        ↓                       ↓                          ↓
4. GERAÇÃO (3 variantes) → 5. QC → 6. overlay de texto se necessário → 7. publicar
```

## 1. Clonar ad estático (método clone-static-ad)

**Regras de ouro:** clonar fiéismente a composição (não "melhorar"); nunca inventar
detalhes de produto/marca; a imagem do produto vem das TUAS fotos reais; trocar só o
que é da marca (produto, logo, wordmark, claims).

**Dissecação da frame de referência** (obrigatória antes de gerar):
- Formato exato (1:1, 4:5, 9:16) e estilo da frame
- Mapa de zonas: para cada zona, posição aproximada (% do frame), conteúdo e tipo
  (BACKGROUND / PRODUCT IMAGE / LOGO / HEADLINE / SUB-COPY / BADGE / CTA / LEGAL) —
  marcar quais são estruturais (preservar) vs. de marca (trocar)
- Hierarquia visual: o que o olho vê 1º, 2º, 3º
- Paleta: 3–6 cores com papel (fundo, acento, texto, produto)
- Luz: direção + qualidade + comportamento da sombra
- Produto: enquadramento, escala relativa ao frame, props, contacto com superfície
- Tipografia por zona: copy verbatim, papel, posição, peso, caixa, cor, tamanho
  relativo ao frame, alinhamento
- Fórmula reutilizável: "[headline] sobre fundo [cor], [produto] centrado com
  [prop], [badge] topo-direita, [CTA] em baixo"

**Copy:** preservar estrutura, ritmo e comprimento; trocar só o que é da marca;
manter todas as zonas de texto. Confirmar com o utilizador antes de gerar.

**Geração — SEMPRE 3 variantes em paralelo** (mesmo prompt, mesmas referências).
Pontuar cada uma em: (1) fidelidade do produto à foto real, (2) texto correto nas
zonas certas. Nunca avançar com menos de 2 frames utilizáveis.

**Guardas de fiabilidade (sempre no prompt):**
- Travar o produto à imagem de referência ("EXACTLY the product in reference image 1,
  do not change shape, label, colors, proportions")
- Copiar verbatim todo o texto no ecrã ("render exactly as written, letter-for-letter")
  — texto em imagem é o ponto mais frágil; se falhar, queimar overlay limpo depois
- Proibir extras não descritos ("render ONLY what is described; no extra text, logos,
  badges, props")
- Posições em termos de grelha concreta ("top-left quadrant", "lower 15%")

## 2. Imagem hiper-realista (método hyperreal-image — as 5 chaves)

Para qualquer imagem lifestyle/UGC. Se faltar uma chave, parece IA. Sempre.

1. **Textura de pele** — ≥3 palavras: "visible pores", "faint shine on forehead",
   "fine lines at the corners of the eyes", "no smoothing, no retouching"
2. **Câmara específica** — "shot on iPhone 15 front camera", "50mm at f/2", "35mm
   film, mild grain". "Professional photo" não significa nada.
3. **Luz com nome e direção** — "soft golden morning light through sheer curtains
   from camera-left", "overcast diffused daylight". Nunca "well-lit".
4. **Micro-imperfeição** — "one piece of hair falling across her cheek", "looking
   slightly off-center", "shirt collar slightly stretched". A maior derrotadora do
   aspeto de IA.
5. **Ambiente plausível** — 3–5 objetos específicos em ligeira desordem ("small
   wooden nightstand with a brass lamp turned off, half-full glass of water,
   paperback face-down"). "A bedroom" = IA.

Fecho obrigatório do prompt: "no advertising polish, no smoothing, no glassy skin,
no studio lighting, no posing, no AI look." Gerar **2 variantes** sempre.

## 3. Galeria PDP (método EcomAlchemist — product-pdp-image-builder)

**Classificar primeiro:**
- **High-consideration** (saúde, beleza com claims, preço alto, comprador cético):
  sequência completa de 9–11 frames.
- **Low-stakes** (barato, visual, impulso — a maioria de casa/utilidades): sem pivot,
  sem mecanismo, sem "rock-throwing". Hero + payoffs + how-to + comparação + prova +
  oferta. 1 avatar, mais produto-em-uso.

**Sequência high-consideration:** HERO → RECOGNITION (1–2 avatares) → PIVOT
("TRÊS PROBLEMAS. UMA CAUSA.") → WHY NOTHING ELSE WORKED (atacar mecanismos das
alternativas, nunca marcas) → MECHANISM (cutaway do produto a atuar na causa) →
PAYOFFS (1 imagem por desejo, espelhando os recognition frames) → HOW EASY (1-2-3,
labels de duas palavras) → FOR/NOT-FOR → SOCIAL PROOF → OFFER (último; garantia em
baixo, só depois de já o quererem).

**As 5 correções de copy (passa/falha em cada frame):**
1. Headline = RESULTADO, não problema nem feature ("you sleep through the night")
2. Linguagem "you", nunca claims de clínica
3. Sem duplos negativos
4. Cada desejo aparece em exatamente 1 frame
5. Confiança + diferenciação presentes (responde "porquê tu")

**Regras duras de texto em imagem:**
- 1 ideia por imagem; headline 4–8 palavras
- Safe zone: terço horizontal do meio LIVRE de texto nas bordas esquerda/direita
  (setas do carousel cobrem); texto no terço de cima ou de baixo
- Painel sólido atrás de todo o texto
- Legível a braço de distância para 55–75 anos sem óculos; se não couber, corta
  palavra — nunca encolher tipo
- Produto REAL recortado e embutido (rembg), nunca regenerado; o que aparece na
  imagem tem de ser o que shipa e a correspondente ao diferenciador

**Os 6 arquétipos de infográfico** (references/infographic-recipes.md):
1. Condition/Benefit Stack (o hero — painel translúcido + stack de 4–5 linhas)
2. Mechanism Explainer (círculo de diagrama + glow colorido no ponto de ação — o
   frame mais valioso e difícil; heat=laranja, decompress=verde, support=ciano)
3. How-To Steps
4. Features Checklist
5. Vs-Alternative Comparison
6. Best-Seller Review card

**Kits de marca (escolher 1 e travar antes de gerar):** clinical-clean ·
bold-hype · premium-elegant · earthy-natural. O teu template base usa
premium-elegant/warm — manter coerência.

**Guardrails:** reviews reais da loja OU "Dramatized customer story" legível; contagem
de reviews só se real (se do fornecedor, atribuir à fonte); claims de saúde suavizados
("designed to help with"); nunca inventar specs; passagem de consistência obrigatória
(garantia/preço/specs iguais em TODOS os frames).

**QC — contact sheet antes de entregar:** (1) todas as headlines são resultados?
(2) foto contradiz a legenda? (3) texto na safe zone? (4) specs/preço/garantia
coerentes? (5) prova real e produto = o que shipa? Qualquer falha → regenerar frame.

## 4. Mapa: que método usar por slot da landing page

| Slot da página | Método |
|---|---|
| hero-main | Infográfico arquétipo 1 (Benefit Stack) com foto real recortada |
| angle-1/2/3 | Foto real + luz de estúdio simples; gerar com 2 variantes |
| lifestyle-1/2 | Hiper-real (5 chaves), 2 variantes |
| infographic-1 | Arquétipos 2–5 conforme o produto |
| ugc-video | Vídeo 9:16 estilo UGC (formatos A/B/C de prompts/criativos.md) |
| ads estáticos | Clonagem de ads vencedores (secção 1 deste doc) |

## 5. Mapa de ferramentas deste ambiente

| Documento pressupõe | Equivalente real aqui |
|---|---|
| arcads_* MCP (clone-static-ad) | image_generation (com referência) + análise manual da frame |
| Higgsfield generate_image (hyperreal) | image_generation plugin (aplicar as 5 chaves no prompt) |
| rembg para cutout | rembg via pip (funciona no sandbox) |
| Shopify MCP (clone-link skill) | Admin API com .env ou edição manual no admin |
| Claude Design / Co-Work | Kimi Code / agente com o master prompt (prompts/loja-completa.md) |
