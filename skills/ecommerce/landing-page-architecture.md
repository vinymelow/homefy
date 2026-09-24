---
name: landing-page-architecture
description: Arquitetar a sequência de secções de uma landing page de produto mobile-first — hero de compra com bundle selector, ritmo das secções abaixo da dobra, hierarquia a 390px e placement de CTA único com sticky add-to-cart.
when_to_use: Ao especificar ou construir uma landing page de produto (tarefa build-landing-page / create-page-spec), ao revisar a ordem das secções de uma página existente, ou ao converter o HTML conceito em tema Shopify.
---

# Arquitetura de landing page de produto

## Quando usar

- Construção da página a partir do `product-brief.md` preenchido e das 3 referências.
- Revisão estrutural de uma página que não converte (clareza de oferta, ritmo, CTA).
- Conversão do HTML conceito em secções Liquid OS 2.0 (ver `skills/shopify/shopify-development.md`).

## Pré-requisitos

- `ecom-stack/templates/product-brief.md` preenchido (avatars, desejos ranqueados, objeções, bundles reais).
- 3 referências estruturais escolhidas (brief secção 4) com "o que vou copiar" por referência.
- Base de construção: `ecom-stack/templates/landing-page.html` (slots nomeados).

## Procedimento

1. **Hero de compra (secção mais crítica — spec nordicstretch):**
   - Desktop: 2 colunas (~49% galeria / ~51% compra), galeria `position: sticky`; mobile: 1 coluna, galeria primeiro.
   - Galeria: media principal ~1:1, setas circulares, thumbnails no desktop, swipe + dots no mobile, crossfade 220–300ms.
   - Coluna de compra: título (bold/uppercase) → rating real → preço + riscado + pill de poupança → bundle selector de 3 cards (card inteiro clicável, radio semantics, selecionado com borda de marca) → painel de oferta grátis (só se real) → botão ADD TO CART · [preço] (full width, ~56px, dark) → linha de garantia → trust chips → 4 bullets de benefício → accordions.
   - Sticky mobile ATC aparece quando o botão principal sai do viewport.
2. **Abaixo da dobra (17 secções, ritmo pettichat/pulsetto):** barra de anúncio → trust strip → media transition → how it works (3 passos, labels de 2 palavras) → feature cards → specification hero → story/engineering → usage scenarios → reviews reais → trust/press marquee → comparação → value statistics → brand story → FAQ → garantia → CTA final → footer do tema.
3. **Galeria em sequência de persuasão:** hero com Benefit Stack → recognition (só high-consideration) → payoffs (1 imagem por desejo ranqueado) → mechanism → how-to → vs alternativa → prova → oferta por último (garantia em baixo, depois de já o quererem).
4. **Hierarquia mobile (390px = viewport primário, 80–90% do tráfego):** uma ideia por secção, alvos de toque ≥44px, safe-area insets, sem overflow 320–430px, validar 320→1440px.
5. **CTA placement:** um só CTA (Add to Cart); CTA final faz scroll ao formulário/hero; nenhum menu nem links para fora.
6. **Performance:** hero comprimido (<200KB WebP), página <2,5s em 4G mobile.

## Outputs

- Especificação da página (ordem das secções + o que cada secção responde do brief).
- HTML preenchido a partir do template base com slots `data-slot` nomeados trocados por assets reais (`ecom-stack/assets/creatives/`).
- Lista de slots de imagem com aspect ratios exatos para a produção criativa.

## Referências

- `ecom-stack/docs/blueprint-pagina-de-vendas.md` — secção 3 (estrutura da PDP), secção 2 (sistema visual da galeria), secção 6 (fluxo de construção).
- `ecom-stack/templates/landing-page.html` — template base com slots `data-slot` (hero-main, bundle-1/2/3, gift-1/2/3, trust-1..6, scenario-1..6, review-avatar-1/2/3, media-transition...).
- `ecom-stack/prompts/pagina-vendas.md` — prompt de geração com hard requirements.
- `skills/ecommerce/offer-strategy.md` — bundles/gift panel/garantia que o hero renderiza.
- `skills/creative/creative-strategy.md` — produção dos assets dos slots.

## Guardrails

- Uma página por produto, mobile-first, **um só CTA**, sem menus.
- Reviews reais da loja OU "Dramatized customer story" — nada de inventar prova social.
- Secções repetidas vêm de arrays/blocks, nunca markup duplicado.
- O que não for verificado vira placeholder editável — nunca inventar preços, garantias, prazos, stock ou endorsements.
- Header/footer/fonts do tema ficam intocados na conversão para Shopify.
