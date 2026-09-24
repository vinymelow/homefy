# Task: audit-page

task: auditarPagina()
responsavel: qa-specialist
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Auditoria de qualidade da landing page estática (ecom-stack/templates/<slug>.html)
contra os checklists de copy e UX do squad, antes de qualquer conversão para Shopify.
O qa-specialist emite veredito PASS ou FAIL com achados classificados por severidade
(bloqueante / maior / menor). Veredito FAIL devolve a página às tasks de origem com
lista objetiva de correções — a página só avança para build-shopify-page com PASS.

## Entrada
- página auditada: ecom-stack/templates/<slug>.html (output de build-landing-page)
- contratos de referência: ecom-stack/research/landers/<slug>-page-spec.md, <slug>-copy.md, <slug>-offer.md e <slug>-positioning.md
- product_brief (ecom-stack/templates/product-brief.md — consome seções 5, 6 e 7 para conferência de valores e guardrails)
- checklists: squads/ecommerce-growth/checklists/copy.md e ux.md
- blueprint: ecom-stack/docs/blueprint-pagina-de-vendas.md §4 (5 correções) e §5 (guardrails)

## Saida
- qa-report: ecom-stack/research/landers/<slug>-qa-report.md (formato squads/ecommerce-growth/templates/qa-report.md) com veredito PASS/FAIL
- lista de achados: severidade, secção afetada, evidência e correção esperada
- decisão de rota: PASS → build-shopify-page; FAIL → build-landing-page ou create-copy com os achados bloqueantes

## Procedure
1. Conferir a estrutura contra o spec: secções presentes, na ordem do spec, com o conteúdo especificado — hero de compra completo (galeria, 3 bundles, painel grátis se real, trust chips, accordions) e CTA único "Add to Cart" sem menus nem links externos.
2. Auditar copy contra checklists/copy.md e as 5 correções do blueprint §4: headline = resultado em "you" com 4–8 palavras; sem duplos negativos; cada desejo aparece exatamente 1 vez; confiança + diferenciação; trust + honesty (título da página = benefício).
3. Auditar guardrails (brief seção 7 e blueprint §5): preços/descontos/prazos/garantia idênticos ao offer-brief; claims de saúde/beleza suavizados ("designed to help with"); zero logos de imprensa/endorsements inventados; reviews reais da loja ou "Dramatized customer story" legível; specs verificadas; consistência de valores em TODOS os frames e secções.
4. Auditar UX contra checklists/ux.md: 320/390/768/1440px sem overflow horizontal; alvos de toque ≥ 44px; sticky mobile ATC a aparecer após o hero; FAQ accordion acessível; safe-area; reduced-motion respeitado.
5. Auditar performance: hero < 200KB WebP; lazy loading abaixo da dobra; alvo < 2.5s em 4G; zero dependências externas.
6. Classificar cada achado: bloqueante (quebra guardrail/lei/plataforma ou impede a compra), maior (dano material de conversão), menor (polimento). PASS exige zero bloqueantes.
7. Gravar o qa-report com veredito explícito; em FAIL, devolver à task de origem (achados de implementação → build-landing-page; achados de texto → create-copy) com a lista de correções.

## Validation
- Veredito PASS/FAIL explícito no qa-report, assinado pelo qa-specialist.
- Zero achados bloqueantes em caso de PASS.
- Cada achado com severidade, secção, evidência (screenshot/linha) e correção esperada.
- Todos os itens dos checklists copy.md e ux.md avaliados (sem itens por avaliar).
- Valores comerciais conferidos 1:1 contra o offer-brief.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o qa-specialist executa a auditoria manualmente item a item dos checklists.
- FAILED/REJECTED: halt — não emitir veredito sem execução válida; escalar ao operador com o hermes.log.
- PARTIAL: revisão humana obrigatória; itens não avaliados contam como reprovados até serem verificados.
- Divergência de valores entre página e offer-brief: sempre bloqueante — corrigir na origem (create-offer/create-copy), nunca editar só o HTML.

## Checklist
- [ ] Estrutura e ordem das secções conferidas contra o spec
- [ ] Hero de compra completo (galeria, 3 bundles, painel grátis se real, accordions)
- [ ] CTA único, sem menus nem links externos
- [ ] 5 correções de copy verificadas (headline 4–8 palavras "you", sem duplos negativos, sem repetição)
- [ ] Guardrails da seção 7 passados (claims, reviews, logos, specs, valores)
- [ ] Valores comerciais 1:1 com o offer-brief
- [ ] UX: 320–1440px sem overflow, alvos ≥ 44px, sticky ATC, acessibilidade
- [ ] Performance: hero < 200KB, lazy loading, alvo < 2.5s 4G
- [ ] Veredito PASS/FAIL gravado no qa-report com rota definida

## Delegação Hermes
- slug sugerido: growth-audit-page-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-audit-page.prompt.md (HTML da página + spec + copy + oferta + checklists copy.md/ux.md verbatim + formato de saída dos achados)
- comando: bash workflows/executors/hermes-exec.sh -t growth-audit-page-<slug> -f /tmp/aiox-prompts/<slug>-audit-page.prompt.md -d /root/homefy -T 20
- timeout sugerido: 20 min
- leitura do result.json: campo "status" — SUCCESS (conferir achados e emitir veredito), PARTIAL (itens não avaliados reprovam até verificação humana), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
