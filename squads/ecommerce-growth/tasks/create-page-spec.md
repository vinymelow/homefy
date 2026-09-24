# Task: create-page-spec

task: criarSpecPagina()
responsavel: ux-designer
responsavel_type: Agente
atomic_layer: Template

## Purpose
Definir a arquitetura completa da landing page antes de qualquer código: a sequência
de persuasão em secções (hero → recognition → mechanism → payoffs → how-to →
comparação → prova → oferta → FAQ → CTA final), a hierarquia mobile-first a 390px e
o inventário de slots de imagem nomeados. O spec é o contrato entre estratégia
(copy/oferta) e construção (build-landing-page / build-shopify-page): se uma
objeção não tem secção no spec, ela fica sem resposta na página.

## Entrada
- product_brief completo (ecom-stack/templates/product-brief.md — consome seções 2, 3, 5, 6, 8 e 9)
- copy-doc: ecom-stack/research/landers/<slug>-copy.md (peças de copy por secção)
- offer-brief: ecom-stack/research/landers/<slug>-offer.md (bundles, painel grátis, garantia)
- blueprint: ecom-stack/docs/blueprint-pagina-de-vendas.md §2 (galeria em sequência de persuasão) e §3 (estrutura da PDP, hero de compra, secções abaixo da dobra)
- prompt: ecom-stack/prompts/pagina-vendas.md (hard requirements: mobile-first 390px, CTA único, slots nomeados, targets de carga)
- template base: ecom-stack/templates/landing-page.html (sistema visual e slots existentes)
- template: squads/ecommerce-growth/templates/landing-page-spec.md
- checklists: squads/ecommerce-growth/checklists/ux.md

## Saida
- landing-page-spec: ecom-stack/research/landers/<slug>-page-spec.md (formato squads/ecommerce-growth/templates/landing-page-spec.md)
- inventário de slots: nome, secção, aspect ratio e tamanho de cada imagem/vídeo (casa com a seção 9 do brief)
- decisão de sequência registada: high-consideration (galeria 9–11 frames com recognition/pivot/mechanism) ou low-stakes (sequência curta: hero + payoffs + how-to + comparação + prova + oferta)
- Entrada para: build-landing-page e build-shopify-page

## Procedure
1. Ler o brief completo e decidir a sequência pela classificação da seção 2 (método EcomAlchemist): high-consideration → galeria PDP completa (hero → recognition 1–2 → pivot "três problemas, uma causa" → why nothing else worked → mechanism → payoffs → how easy → for/not-for → social proof → offer); low-stakes → sequência curta sem pivot nem mechanism (hero + payoffs + how-to + comparação + prova + oferta).
2. Mapear cada desejo ranqueado para um frame de payoff e cada objeção da seção 3 para a secção que a responde; listar gaps e resolver antes de continuar.
3. Spec do hero de compra (blueprint §3): galeria ~1:1 com thumbnails (desktop) / swipe + dots (mobile), título, rating real, preço + riscado + pill de poupança, bundle selector com 3 cards clicáveis (radio semantics, card popular com borda de marca), painel de oferta grátis (só se real; esconder se não), botão ADD TO CART com preço (~56px, full width), linha de garantia, trust chips, introdução com 4 bullets, accordions (package, shipping/returns, warranty, payment, specs) e sticky mobile ATC quando o botão sai do viewport.
4. Spec das secções abaixo da dobra na ordem do blueprint: announcement bar → trust strip → media transition → how it works → feature cards → specification hero → story/engineering → usage scenarios → reviews (foto, rating, "Verified Buyer" — reais ou nada) → trust/press marquee (só marcas verificadas) → comparação (✓/✗ sem nomes de marcas) → value statistics (com disclaimers editáveis) → brand story → FAQ (accordion acessível) → caixa de garantia → CTA final (full-bleed + overlay) → footer do tema.
5. Definir o sistema visual do spec: fundo #F5F6F2, texto #111, UMA cor de acento só para CTAs/badges/highlights, sem gradientes, estilo premium mas warm, kit de marca da seção 8 travado.
6. Inventariar os slots de mídia com nome, secção, aspect ratio e peso-alvo (hero < 200KB WebP; nomes casando com a seção 9: hero-main, recognition-1/2, payoff-1/2/3, infographic-mech, how-to, vs-alternative, angle-1/2/3, lifestyle-1/2, ugc-video, static-ads-1/2/3).
7. Fixar requisitos duros no spec: mobile-first com 390px como viewport primário (escalar a desktop depois), CTA único "Add to Cart" sem menus nem links externos, carga < 2.5s em 4G, alvos de toque ≥ 44px, safe-area, sem overflow de 320px a 1440px, reduced-motion.
8. Delegar ao Hermes (secção "Delegação Hermes") para a redação estruturada do spec; o ux-designer revisa secção a secção, valida contra checklists/ux.md e grava o spec.

## Validation
- Cada objeção da seção 3 tem secção identificada que a responde.
- Cada desejo ranqueado tem frame de payoff correspondente.
- Slots do inventário casam 1:1 com a seção 9 do brief (nomes e quantidades).
- Sequência coerente com a classificação do produto (seção 2).
- Spec implementável sem ambiguidade: toda secção tem objetivo, conteúdo, slots e prova definidos.
- Requisitos duros presentes: 390px primeiro, 1 CTA, hero < 200KB, página < 2.5s, targets ≥ 44px.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o ux-designer escreve o spec manualmente secção a secção a partir do blueprint.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: revisão humana; o spec não pode ir para build-landing-page com secções em branco.
- Conflito entre copy e oferta (copy promete o que a oferta não entrega): devolver a create-copy ou create-offer com a divergência identificada — o spec não "resolve" promessa por conta própria.

## Checklist
- [ ] Sequência decidida e justificada pela classificação da seção 2
- [ ] Hero de compra especificado (galeria, bundles, painel grátis, sticky ATC, accordions)
- [ ] Secções abaixo da dobra ordenadas pelo blueprint §3
- [ ] Cada desejo ranqueado mapeado para frame de payoff
- [ ] Cada objeção mapeada para secção que a responde
- [ ] Inventário de slots com nome/ratio/tamanho casando com a seção 9
- [ ] Sistema visual definido (fundo #F5F6F2, tinta #111, 1 acento, sem gradientes)
- [ ] Requisitos duros no spec (390px, 1 CTA, hero <200KB, <2.5s 4G, ≥44px)
- [ ] Spec validado contra checklists/ux.md e gravado

## Delegação Hermes
- slug sugerido: growth-page-spec-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-page-spec.prompt.md (brief completo + copy + oferta + estrutura obrigatória de saída por secção)
- comando: bash workflows/executors/hermes-exec.sh -t growth-page-spec-<slug> -f /tmp/aiox-prompts/<slug>-page-spec.prompt.md -d /root/homefy -T 25
- timeout sugerido: 25 min
- leitura do result.json: campo "status" — SUCCESS (revisar secções contra o blueprint e gravar), PARTIAL (completar secções em falta manualmente), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
