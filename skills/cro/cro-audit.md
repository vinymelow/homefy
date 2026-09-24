---
name: cro-audit
description: Auditar uma landing page ou PDP em fricção, clareza de oferta e trust — checklist objetivo de conversão, hipóteses priorizadas por impacto e plano de experimento com métricas de decisão (CTR, CPC, conversão, CPA, margem).
when_to_use: Quando uma página não converte (CPA > €35 ou conversão < 0,8%), antes de escalar um produto que passou no teste, ou como revisão periódica pós-lançamento. Complementa a auditoria objetiva de critérios em skills/homefy-page-audit.
---

# Auditoria CRO

## Quando usar

- Fase 5 do ciclo: ler métricas e decidir matar/continuar/escalar — a auditoria explica o "porquê" por trás dos números.
- Antes de escalar (CPA < €15): remover fricção enquanto o orçamento sobe.
- Página nova antes do lançamento: auditoria pré-flight das 5 correções e da arquitetura.

## Pré-requisitos

- Página (HTML ou URL da loja) e o `product-brief.md` do produto.
- Métricas do teste quando existirem: CTR, CPC, taxa de conversão, CPA, margem.
- Acesso aos critérios objetivos em `squads/ecommerce-growth/checklists/` (copy/ux/performance).

## Procedimento

1. **Fricção (o que impede a compra):** contar passos até ao checkout, campos desnecessários, distância do CTA, popup/elementos que interrompem, velocidade (hero <200KB WebP, página <2,5s 4G), overflow ou alvos <44px no mobile.
2. **Clareza de oferta (5 segundos):** um visitante frio deve perceber em 5s o que é, para quem é e quanto custa. Headline = resultado 4–8 palavras "you"; preço âncora visível; bundle mais popular pré-selecionado; gift panel só se real.
3. **Trust:** garantia visível junto ao CTA e acima do CTA final, trust chips, reviews reais/"Dramatized customer story", política de envio clara, consistência de specs/preço/garantia em todas as secções.
4. **As 5 correções de copy (passa/falha por secção):** headline resultado; sem duplos negativos; sem repetição de desejos; confiança + diferenciação; trust + honesty (FOR/NOT-FOR, hedge, garantia).
5. **Hipóteses priorizadas:** cada falha vira hipótese "se mudarmos X, métrica Y melhora porque Z". Priorizar por impacto esperado × esforço; uma variável por experimento.
6. **Plano de experimento:** métrica primária, duração (3 dias de teste = decisão), orçamento €20–50/dia, critérios de corte.

## Outputs

- Relatório de auditoria: achados classificados (fricção / clareza / trust / copy) com severidade.
- Hipóteses priorizadas (impacto × esforço), uma variável por hipótese.
- Plano de experimento com métricas de decisão da tabela de validação.
- Se pedido no âmbito do squad: relatório estruturado via `squads/ecommerce-growth/templates/qa-report.md`.

## Referências

- `ecom-stack/docs/blueprint-pagina-de-vendas.md` — secção 4 (5 correções), secção 5 (guardrails), secção 7 (tabela de métricas de validação).
- `ecom-stack/docs/guia-uso.md` — Fase 5 (decisão por métricas: mata/continua/escala).
- `skills/ecommerce/landing-page-architecture.md` — arquitetura e CTA placement auditados.
- `skills/copywriting/direct-response-copy.md` — correções de copy aplicadas.
- `squads/ecommerce-growth/checklists/` — critérios objetivos copy/ux/performance.

## Guardrails

- Dados decidem, não opinião: toda hipótese liga-se a uma métrica e a um critério de corte.
- Tabela de validação (3 dias): CTR <1% mata o criativo; conversão <0,8% ou CPA >€35 mata a página/oferta; CPA <€15 escala.
- Uma variável por experimento — páginas reescritas inteiras não isolam causa.
- Nunca "otimizar" prova social inventada: reviews/claims reais ou nada.
- Margem após produto+envio >15% para continuar, >25% para escalar.
