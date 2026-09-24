# Landing Page Spec — [SLUG DO PRODUTO] — [data]

> Spec de página consumível pelo agente `shopify-engineer` — output das tasks
> `create-copy` + `create-page-spec`.
> Contrato de entrada: `templates/product-brief.md` (posicionamento, avatares,
> desejos, objeções, bundles, slots) + `templates/offer-brief.md` (oferta,
> garantia, painel grátis).
> Referências estruturais: `ecom-stack/templates/landing-page.html` (padrão visual
> real), `ecom-stack/docs/blueprint-pagina-de-vendas.md` (ordem das secções),
> `ecom-stack/docs/metodo-criativos.md` (regras de mídia).
> Produção: referência = estrutura e movimento. NUNCA copiar logo, imagens, copy,
> reviews, claims ou código de terceiros.

## 1. Arquitetura de secções (ordem fixa)

Sequência de persuasão da galeria/página (método EcomAlchemist + blueprint).
Tabela de mapping para o template real `landing-page.html`:

| # | Secção (esta spec) | Equivalente em `landing-page.html` | Mídia (slots) |
|---|---|---|---|
| 0 | Announcement bar | `<!-- 0. BARRA DE ANÚNCIO -->` | — |
| 1 | Hero de compra | `<!-- 1. HERO DE COMPRA -->` (galeria + coluna de compra) | `hero-main`, thumbnails |
| 2 | Recognition | galeria, só high-consideration | `recognition-1/2` |
| 3 | Mechanism | galeria + `<!-- 6. SPEC HERO -->` | `infographic-mech` |
| 4 | Payoffs | galeria + `<!-- 5. FEATURE CARDS -->` | `payoff-1/2/3`, `feature-1..3` |
| 5 | How-to | `<!-- 4. HOW IT WORKS -->` | `how-to` |
| 6 | Vs-alternative | `<!-- 10. COMPARISON -->` | `vs-alternative` |
| 7 | Proof | `<!-- 3. MEDIA TRANSITION -->`, `<!-- 7. USAGE SCENARIOS -->`, `<!-- 8. REVIEWS -->`, `<!-- 9. RESULT DONUTS -->` | `ugc-video`, `lifestyle-1/2`, reviews |
| 8 | Offer | bundle selector + painel grátis (dentro do hero) + `<!-- 2. TRUST STRIP -->` | — |
| 9 | FAQ | `<!-- 11. FAQ -->` | — |
| 10 | Guarantee | `<!-- 12. GARANTIA -->` | — |
| 11 | Final CTA | `<!-- 13. CTA FINAL -->` + sticky ATC | `final-bg` |

## 2. Secção por secção

### 2.0 Announcement bar
- **Objetivo**: anunciar a oferta (1 linha, é a única zona com exclamação permitida)
- **Copy** (da task `create-copy`): 
- **Requisito**: sem countdown falso; prazo só se real

### 2.1 Hero de compra
- **Objetivo**: converter em <3s — resultado + preço + CTA acima da dobra
- **Galeria** (mobile primeiro): media principal ~1:1, swipe + dots, crossfade
  220–300ms; thumbnails só desktop; `position: sticky` no desktop
- **Coluna de compra**: título (bold/uppercase, benefício — não nome genérico) →
  rating real → preço + riscado + pill de poupança → bundle selector (3 cards,
  card inteiro clicável, estado selecionado com borda de marca) → painel de
  oferta grátis (só se real — senão esconder) → botão ADD TO CART · [preço]
  (full width, ~56px, dark) → linha de garantia → trust chips (envio/garantia)
- **Mídia**: `hero-main` (Benefit Stack: foto real em uso + painel translúcido,
  produto recortado com rembg — nunca regenerado por IA; <200KB WebP)
- **Tracking**: `ViewContent` ao carregar · `click_bundle_option` por card ·
  `AddToCart` no botão

### 2.2 Recognition (só high-consideration)
- **Objetivo**: o avatar reconhecer-se no problema nas primeiras 3 trocas de imagem
- **Copy**: problema em linguagem do cliente (1 ideia por frame, headline 4–8 palavras)
- **Mídia**: `recognition-1/2` (avatar na cena do pain — momento específico)
- **Tracking**: `gallery_nav` (swipe/dot/arrow)

### 2.3 Mechanism
- **Objetivo**: tornar visível o benefício invisível (cutaway + glow no ponto de ação)
- **Copy**: mecanismo factual, specs verificados (senão BLOCKED)
- **Mídia**: `infographic-mech` (arquétipo 2 — círculo de diagrama; heat=laranja,
  decompress=verde, support=ciano)
- **Tracking**: `gallery_nav`

### 2.4 Payoffs
- **Objetivo**: 1 imagem por desejo ranqueado (espelha os recognition frames)
- **Copy**: cada desejo aparece EXATAMENTE 1 vez; headline = RESULTADO em "you",
  4–8 palavras; sem duplos negativos; sem repetição
- **Mídia**: `payoff-1/2/3` (feature cards: imagem/vídeo + tag + headline)
- **Tracking**: `gallery_nav` · scroll depth 50%

### 2.5 How-to
- **Objetivo**: mostrar que é fácil (3 passos numerados, labels de 2 palavras)
- **Copy** (da secção 6 do product-brief):
  1. 
  2. 
  3. 
- **Mídia**: `how-to` (arquétipo 3 — How-To Steps)
- **Tracking**: scroll depth 75%

### 2.6 Vs-alternative
- **Objetivo**: "nós vs. outros" — ✓ verde / ✗ vermelho, SEM nomes de marcas
  (ataca mecanismos da alternativa, nunca marcas)
- **Copy** (linhas da comparação, com hedge em claims reversíveis):
- **Mídia**: `vs-alternative` (arquétipo 5)
- **Tracking**: `comparison_view`

### 2.7 Proof
- **Objetivo**: prova social real — reviews da loja OU "Dramatized customer story"
  legível; contagem só se real (se do fornecedor, atribuir à fonte)
- **Conteúdo**: `media-transition` (vídeo demo muted/autoplay/loop) → usage
  scenarios (6 cartões, scroll-snap mobile) → 3+ reviews com foto + rating +
  "Verified Buyer" → result donuts (só com disclaimers editáveis e valores reais)
- **Mídia**: `ugc-video` (9:16, 15–30s), `lifestyle-1/2` (hiper-realistas, 5 chaves)
- **Tracking**: `video_view` (play/25/50/75/100%) · scroll depth 90%

### 2.8 Offer
- **Objetivo**: o sistema de compra (bundle selector + painel grátis) já foi visto
  no hero; aqui reforça-se confiança
- **Conteúdo**: trust strip (4–6 ícones: frete, garantia, pagamento seguro) +
  accordions (package, shipping/returns, warranty, payment, specs)
- **Copy**: specs = produto REAL (variant IDs vivos, nada hard-coded)
- **Tracking**: `accordion_open` por item

### 2.9 FAQ
- **Objetivo**: responder objeções reais (secção 3 do product-brief)
- **Copy** (5–10 perguntas, accordion acessível):
  1. 
  2. 
  3. 
  4. 
  5. 
- **Tracking**: `faq_open` por pergunta (alimenta CRO)

### 2.10 Guarantee
- **Objetivo**: box de risco zero acima do CTA final — só DEPOIS de já o quererem
- **Copy**: garantia real da loja (dias = política confirmada, igual em TODOS os frames)
- **Tracking**: scroll depth 100%

### 2.11 Final CTA
- **Objetivo**: fechar — imagem full-bleed + overlay + botão que faz scroll ao
  formulário de compra (UM só CTA na página)
- **Mídia**: `final-bg` (lifestyle full-bleed)
- **Sticky mobile ATC**: aparece quando o botão principal sai do viewport
- **Tracking**: `click_final_cta` · `AddToCart` (sticky) · `InitiateCheckout`

## 3. Requisitos mobile (obrigatórios)
- [ ] Mobile-first: 390px é o viewport primário; validar 320→1440px
- [ ] 1 coluna no mobile, galeria primeiro
- [ ] Touch targets ≥44px
- [ ] Safe-area insets
- [ ] Sem overflow horizontal em nenhum breakpoint
- [ ] Sticky ATC funcional (aparece/desaparece no trigger certo)
- [ ] Hero comprimido (<200KB WebP); página <2,5s em 4G mobile
- [ ] Alvos de toque do bundle selector com radio semantics acessíveis

## 4. CTA placement (resumo)
| CTA | Local | Evento |
|---|---|---|
| ADD TO CART (hero) | coluna de compra, full width ~56px | `AddToCart` |
| Sticky ATC | bottom, após sair do hero | `AddToCart` |
| Final CTA | full-bleed overlay, scroll-to-form | `click_final_cta` |

## 5. Tracking events (mapa completo)
`PageView`/`ViewContent` (hero) · `click_bundle_option` · `AddToCart` (botão +
sticky) · `InitiateCheckout` · `gallery_nav` · `comparison_view` ·
`accordion_open` · `faq_open` · `video_view` (quartis) · scroll depth
(25/50/75/90/100) · Pixel Meta + CAPI verificados antes do lançamento
(veredito no `templates/launch-report.md`).

## 6. Critérios de aceitação
- [ ] **Copy**: passa nas 5 correções do blueprint (headline = resultado em "you" ·
  sem duplos negativos · sem repetição de desejos · confiança + diferenciação ·
      trust + honesty com FOR/NOT-FOR) — checklist `checklists/copy.md`
- [ ] **UX**: validação 320→1440px sem overflow, alvos ≥44px, safe-area,
      reduced-motion, WCAG AA — checklist `checklists/ux.md`
- [ ] **Shopify**: nada hard-coded (settings/blocks/metafields/dados vivos do
      produto), tema duplicado (MAIN read-only), secções com schema/presets,
      Theme Check limpo — checklist `checklists/shopify.md`
- [ ] **Performance**: hero <200KB WebP, página <2,5s 4G mobile — checklist
      `checklists/performance.md`
- [ ] **Claims**: guardrails do product-brief secção 7 passam na passagem de
      consistência (preço/garantia/specs iguais em TODOS os frames e secções)
- [ ] QA PASS assinado em `templates/qa-report.md` antes do launch-report

## 7. Handoff
- **Copiar/derivar de**: `ecom-stack/templates/landing-page.html` (estrutura base)
- **Entregar ao**: shopify-engineer → conversão Liquid (OS 2.0, secções com
  schema, `template_suffix` no produto, header/footer/fonts intocados)
- **Slots de mídia a gerar depois**: ver `templates/creative-brief.md`
