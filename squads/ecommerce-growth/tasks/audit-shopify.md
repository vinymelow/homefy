# Task: audit-shopify

task: auditarShopify()
responsavel: shopify-engineer
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Validação técnica da implementação Shopify no tema duplicado: sintaxe Liquid, schema
válido, responsividade, performance, tracking de pixels e componentes reais. O
shopify-engineer executa a revisão técnica e escreve o relatório; o VEREDITO final
(PASS/FAIL) é emitido pelo qa-specialist no qa-report — separação entre quem constrói
a técnica e quem fecha a qualidade.

## Entrada
- pacote instalado no tema duplicado: secções/snippets/assets/templates de .aiox/external-runs/<run>/artifacts/ (output de build-shopify-page)
- prep doc: ecom-stack/research/landers/<slug>-shopify-prep.md
- URL de preview do tema duplicado (draft_theme_id) e URL do produto (brief seção 1)
- ligação à loja: `python3 ecom-stack/cli/cli.py doctor`
- referências: ecom-stack/prompts/loja-completa.md (checklist pós-publicação e regras do PASSO 4)
- checklists: squads/ecommerce-growth/checklists/shopify.md e performance.md

## Saida
- shopify-audit: ecom-stack/research/landers/<slug>-shopify-audit.md com resultados técnicos item a item
- veredito técnico recomendado (PASS/FAIL) com achados classificados por severidade
- veredito final consolidado pelo qa-specialist no qa-report (templates/qa-report.md)
- Entrada para: prepare-launch (só avança com veredito final PASS)

## Procedure
1. Confirmar o alvo: tema duplicado (draft), nunca o MAIN; registrar live_theme_id e draft_theme_id. Escrever no MAIN = falha bloqueante imediata.
2. Validar sintaxe: Theme Check se disponível; caso contrário, revisão estrutural de cada ficheiro — schemas com nomes ≤ 25 caracteres, ids de settings únicos, defaults não vazios, max_blocks ≤ 50, block.shopify_attributes presente, sem tags de formulário com filtros inline (erro clássico de {% form %} com pipe).
3. Testar "nada hard-coded": mudar o preço de um variant no admin e confirmar que a página atualiza; trocar uma imagem no Theme Editor e confirmar a troca; verificar que bundles, garantia e FAQ vêm de settings/blocks/metafields.
4. Confirmar integração com o tema: header, announcement bar, footer, navegação, cart drawer e fontes reais e intocados no preview (desktop e mobile); zero {% layout none %}.
5. Responsividade: 320–430px sem overflow, alvos de toque ≥ 44px, safe-area insets, sticky mobile ATC funcional, variant switching a atualizar preço e CTAs.
6. Performance: hero comprimido (< 200KB), imagens abaixo da dobra lazy, peso da página < 2MB, alvo < 2.5s em 4G mobile.
7. Tracking: pixel Meta e TikTok a disparar PageView, ViewContent, AddToCart, InitiateCheckout e Purchase; validar com um teste de compra no Shopify Bogus Gateway antes de lançar; CAPI verificado quando configurado.
8. Comércio real: product form nativo, cart drawer com refresh, quantity rules, checkout a chegar ao fim no teste Bogus.
9. Compilar o shopify-audit com cada item verificado/reprovado + evidência; escrever o veredito técnico recomendado e entregar ao qa-specialist para o veredito final no qa-report.
10. Em caso de achados bloqueantes, devolver a build-shopify-page com a lista — nunca corrigir em silêncio durante a auditoria.

## Validation
- Zero erros de sintaxe Liquid/schema no pacote.
- Preço dinâmico confirmado (mudança no admin reflete na página).
- Header/footer/cart drawer do tema presentes no preview das duas páginas (desktop + mobile).
- Eventos de pixel verificados com compra de teste Bogus (5 eventos ou justificativa).
- Veredito final assinado pelo qa-specialist no qa-report (separação construtor/auditor).

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o shopify-engineer executa os checks manualmente (preview + admin + checklists).
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: itens não verificados reprovam até verificação humana.
- Doctor falhar ou preview indisponível: BLOQUEAR a auditoria — sem acesso à loja não há validação técnica; escalar ao operador.
- Qualquer escrita detetada no tema MAIN: parar imediatamente, reportar ao operador e reverter pela duplicação correta.

## Checklist
- [ ] Tema alvo confirmado como duplicado (ids live/draft registados)
- [ ] Sintaxe Liquid/schema validada (Theme Check ou revisão documentada)
- [ ] Teste de nada hard-coded (preço e imagem mudam pelo admin/editor)
- [ ] Header/footer/cart drawer/fontes intocados e presentes
- [ ] Responsivo 320–430px sem overflow; alvos ≥ 44px; sticky ATC
- [ ] Performance: hero < 200KB, lazy loading, página < 2MB
- [ ] Tracking: 5 eventos de pixel verificados com teste Bogus Gateway
- [ ] Comércio real: variant switching, cart drawer refresh, checkout completo
- [ ] Shopiy-audit gravado com veredito técnico recomendado
- [ ] Veredito final emitido pelo qa-specialist no qa-report

## Delegação Hermes
- slug sugerido: growth-audit-shopify-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-audit-shopify.prompt.md (lista de ficheiros do pacote + checklists shopify.md/performance.md + regras do PASSO 4 + formato de saída item a item)
- comando: bash workflows/executors/hermes-exec.sh -t growth-audit-shopify-<slug> -f /tmp/aiox-prompts/<slug>-audit-shopify.prompt.md -d /root/homefy -T 30
- timeout sugerido: 30 min
- leitura do result.json: campo "status" — SUCCESS (conferir itens e gravar o shopify-audit), PARTIAL (itens não verificados reprovam), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
