# Task: build-landing-page

task: construirLandingPage()
responsavel: shopify-engineer
responsavel_type: Agente
atomic_layer: Page

## Purpose
Implementar a landing page como HTML/CSS/JS estático local, arquivo único
self-contained, a partir do landing-page-spec e do template base
ecom-stack/templates/landing-page.html. É a prévia real da página antes da conversão
para Shopify. Regra de ouro: NUNCA publicar — nenhuma chamada de API, nenhum deploy;
a publicação acontece só em build-shopify-page com aprovação humana explícita.

## Entrada
- landing-page-spec: ecom-stack/research/landers/<slug>-page-spec.md (contrato de secções, slots e requisitos)
- product_brief completo (ecom-stack/templates/product-brief.md — consome seções 5, 6, 8 e 9)
- copy-doc: ecom-stack/research/landers/<slug>-copy.md (headline, benefícios, how-to, FAQ)
- offer-brief: ecom-stack/research/landers/<slug>-offer.md (preços e bundles reais)
- template base: ecom-stack/templates/landing-page.html (sistema visual + slots data-slot)
- fotos reais do produto: ecom-stack/assets/creatives/ (se existirem; senão placeholders nomeados)
- prompt de construção: ecom-stack/prompts/pagina-vendas.md

## Saida
- página estática: ecom-stack/templates/<slug>.html (arquivo único, inline CSS/JS, sem dependências externas)
- inventário de slots preenchido: estado de cada slot (imagem real ou placeholder nomeado)
- artefatos do run em .aiox/external-runs/<run>/artifacts/ (cópia da página + notas de implementação)
- Entrada para: audit-page (auditoria QA da página)

## Procedure
1. Verificar pré-requisitos: spec aprovado (create-page-spec), copy final (create-copy) e oferta fechada (create-offer). Se algum falta, devolver à task correspondente — não improvisar conteúdo.
2. Copiar ecom-stack/templates/landing-page.html como base e substituir todos os placeholders pelos valores do brief; cada imagem fica num slot nomeado via data-slot (hero-main, bundle-1/2/3, payoff-1/2/3, infographic-mech, how-to, vs-alternative, review-avatar-1/2/3, ugc-video) para troca programática.
3. Implementar a sequência de secções na ordem exata do spec, com a copy verbatim do copy-doc — nunca reescrever claims no código.
4. Hero de compra: galeria com thumbnails (desktop) e swipe + dots (mobile), bundle selector com 3 cards inteiramente clicáveis (radio semantics, card popular com borda de marca), preço + riscado + pill de poupança, painel grátis só se real, botão ADD TO CART com preço (~56px, full width), linha de garantia, trust chips e accordions.
5. Interações em JS vanilla: sticky mobile ATC via IntersectionObserver (aparece quando o botão principal sai do viewport), FAQ accordion acessível, troca de bundle atualizando preço apresentado. Sem bibliotecas externas, sem jQuery.
6. Sistema visual do template: fundo #F5F6F2, texto #111, uma cor de acento só para CTA/badges/highlights, sem gradientes, sem exclamações fora da announcement bar.
7. Performance: hero comprimido < 200KB WebP, imagens abaixo da dobra com loading="lazy", alvo de página < 2.5s em 4G.
8. Validar localmente a 320px, 390px, 768px e 1440px (browser ou screenshot): sem overflow horizontal, alvos de toque ≥ 44px, safe-area respeitado, reduced-motion.
9. Verificar guardrails no HTML: preços/garantia/prazo iguais ao offer-brief, claims suavizados, reviews reais ou "Dramatized customer story", zero logos de imprensa inventados. Bloquear qualquer divergência.
10. Gravar a página em ecom-stack/templates/<slug>.html, copiar para .aiox/external-runs/<run>/artifacts/ e registrar o inventário de slots. Não publicar nada.

## Validation
- Arquivo único self-contained (inline CSS/JS), abre via file:// sem rede.
- Sequência de secções idêntica ao spec; copy idêntica ao copy-doc.
- CTA único "Add to Cart", zero menus e zero links para outras páginas.
- Todos os valores comerciais conferidos contra o offer-brief (preços, riscados, garantia, prazo).
- Responsivo sem overflow de 320px a 1440px; sticky ATC funcional; alvos ≥ 44px.
- Hero < 200KB; página dentro do alvo < 2.5s em 4G.
- Zero chamadas de rede de publicação/escrita — build é 100% local.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o shopify-engineer implementa manualmente as secções em falta a partir do spec.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL com arquivo incompleto: não entregar; completar as secções em falta antes de gravar.
- Guardrail quebrado no output (claim proibido, valor divergente): corrigir na origem (copy/offer) e regenerar — nunca "ajustar" silenciosamente no HTML.

## Checklist
- [ ] Pré-requisitos confirmados (spec + copy + oferta fechados)
- [ ] Base landing-page.html copiada e placeholders substituídos
- [ ] Sequência de secções idêntica ao spec
- [ ] Bundle selector funcional (3 cards, radio semantics, preço atualiza)
- [ ] Sticky mobile ATC com IntersectionObserver
- [ ] Slots data-slot nomeados conforme inventário do spec
- [ ] Valores comerciais conferidos contra o offer-brief
- [ ] Guardrails verificados (claims, reviews, logos, garantia)
- [ ] Validação 320/390/768/1440px sem overflow; alvos ≥ 44px
- [ ] Hero < 200KB; lazy loading abaixo da dobra
- [ ] Página gravada em ecom-stack/templates/<slug>.html e artefatos no run
- [ ] Nenhuma ação de publicação executada

## Delegação Hermes
- slug sugerido: growth-build-landing-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-landing.prompt.md (spec completo + copy verbatim + oferta + regras do template base + proibição explícita de publicar)
- comando: bash workflows/executors/hermes-exec.sh -t growth-build-landing-<slug> -f /tmp/aiox-prompts/<slug>-landing.prompt.md -d /root/homefy -T 40
- timeout sugerido: 40 min
- leitura do result.json: campo "status" — SUCCESS (validar o HTML gerado e gravar), PARTIAL (completar secções em falta), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
