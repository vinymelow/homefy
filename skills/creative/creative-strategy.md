---
name: creative-strategy
description: Estratégia de produção criativa do Homefy — derivar criativos de ads e páginas que já geram dinheiro, mapear os slots de imagem/vídeo do brief (secção 9), dirigir imagens hiper-realistas com as 5 chaves e clonar ads estáticos vencedores com QC obrigatório.
when_to_use: Na Fase 3 do ciclo (gerar os assets dos slots da landing page e os anúncios do teste), ao planear criativos para um produto novo, ou ao clonar um ad vencedor de concorrente. Os métodos de execução vivem nas skills hyperreal-image/clone-static-ad/product-pdp-image-builder — esta skill orquestra.
---

# Estratégia criativa

## Quando usar

- Brief aprovado (secção 9 com slots necessários marcados) → produção dos assets.
- Plano de teste: 3 formatos de vídeo × 2–3 hooks = 6–9 criativos por produto.
- Clonagem de ads vencedores do ad library (filtrado por spend).

## Pré-requisitos

- `product-brief.md` preenchido: classificação high-consideration vs low-stakes, avatares, desejos ranqueados, kit de marca travado (1 de 4), fotos reais do produto (mín. 1).
- Referências de ads vencedores (3–6 frames, ad library/Winning Hunter).
- Skills de execução disponíveis: `hyperreal-image.skill`, `clone-static-ad.md`, `product-pdp-image-builder.skill` (raiz de `skills/`).

## Procedimento

1. **Princípio unificador:** nada é criado do zero — clona-se a estrutura vencedora e troca-se marca + produto + copy. A imagem do produto é SEMPRE a foto real recortada (rembg), nunca regenerada por IA.
2. **Classificar o produto** (decide a sequência): high-consideration → galeria PDP completa 9–11 frames (hero → recognition → pivot → why nothing else worked → mechanism → payoffs → how-easy → for/not-for → proof → offer); low-stakes → galeria curta (hero + payoffs + how-to + comparação + prova + oferta), 1 avatar, mais produto-em-uso.
3. **Mapear slots → método** (detalhe em `metodo-criativos.md` §4):
   - `hero-main` → Infográfico arquétipo 1 (Benefit Stack) com foto real recortada.
   - `angle-1/2/3` → foto real + luz de estúdio simples, 2 variantes.
   - `lifestyle-1/2` → hiper-realista com as 5 chaves (delegar à skill `hyperreal-image`), 2 variantes.
   - `infographic-mech` → arquétipos 2–5 (Mechanism Explainer é o frame mais valioso).
   - `ugc-video` → 9:16 formatos A/B/C (`prompts/criativos.md` §3).
   - `static-ads-1/2/3` → clonagem de ads vencedores (delegar à skill `clone-static-ad`), 3 variantes.
4. **Direção de imagem hiper-realista — as 5 chaves** (se faltar uma, parece IA): textura de pele (≥3 palavras), câmara específica, luz com nome e direção, micro-imperfeição, ambiente plausível (3–5 objetos em ligeira desordem); fecho obrigatório anti-IA no prompt.
5. **Clonagem de ads estáticos:** dissecação zona-a-zona obrigatória (formato, mapa de zonas, hierarquia visual, paleta, luz, tipografia por zona, fórmula reutilizável); gerar SEMPRE 3 variantes; nunca avançar com menos de 2 frames utilizáveis; guardas de fiabilidade no prompt (produto travado à referência, texto verbatim, sem extras, posições em grelha).
6. **Regras de texto em imagem:** 1 ideia por imagem; headline 4–8 palavras = resultado em "you"; safe zone (terço horizontal do meio livre nas bordas); painel sólido atrás do texto; legível a braço de distância para 55–75 anos — se não couber, corta palavra, nunca encolher tipo.
7. **QC — contact sheet antes de entregar:** headlines são resultados? foto contradiz a legenda? texto na safe zone? specs/preço/garantia coerentes em TODOS os frames? prova real e produto = o que shipa? Qualquer falha → regenerar o frame.

## Outputs

- Assets por slot em `ecom-stack/assets/creatives/` com nomes a casar com os `data-slot` da landing page.
- 6–9 criativos de anúncio (3 formatos de vídeo × 2–3 hooks) para o teste inicial.
- Fichas de dissecação dos ads de referência clonados.

## Referências

- `ecom-stack/docs/metodo-criativos.md` — SOP completo (pipeline, 5 chaves, arquétipos, QC, mapa slots→método).
- `ecom-stack/templates/product-brief.md` — secção 9 (slots), secção 2 (classificação), secção 8 (kit de marca/fotos).
- `ecom-stack/prompts/criativos.md` — prompts base por slot e formatos de vídeo A/B/C.
- `skills/hyperreal-image.skill`, `skills/clone-static-ad.md`, `skills/product-pdp-image-builder.skill` — execução.
- `skills/copywriting/direct-response-copy.md` — headlines dos frames.

## Guardrails

- Reviews reais da loja OU "Dramatized customer story" legível; contagem só se real (se do fornecedor, atribuir à fonte).
- Claims de saúde suavizados ("designed to help with"); nunca inventar specs.
- Nunca gerar com logos/marcas de terceiros; produto real recortado, nunca regenerado.
- Todas as imagens do mesmo produto: mesmo fundo/tom de luz — sistema visual, não fotos soltas.
- Passagem de consistência obrigatória (garantia/preço/specs iguais em todos os frames) antes de entregar.
