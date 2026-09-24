# QA Report — [SLUG DO PRODUTO / PÁGINA] — [data]

> Relatório de auditoria — output das tasks `audit-page`, `audit-cro`,
> `audit-shopify`, executadas pelo agente `qa-specialist`.
> Veredito valida as checklists do squad: `checklists/copy.md`, `checklists/ux.md`,
> `checklists/shopify.md`, `checklists/performance.md`, `checklists/cro.md`.
> Nenhum lançamento sem QA PASS + aprovação humana registrada
> (ver `templates/launch-report.md`).

## 1. Veredito
- [ ] **APROVADO** — sem issues ou só LOW; pode avançar para `prepare-launch`
- [ ] **APROVADO COM RESSALVAS** — só issues MEDIUM/LOW; avança com correções
  planeadas (lista na secção 6)
- [ ] **REJEITADO** — ≥1 issue CRITICAL ou HIGH; volta à task que produziu o artefacto

## 2. Escopo auditado
- [ ] Copy (headlines, benefícios, FAQ, guardrails de claims)
- [ ] UX/layout (mobile 320–1440px, alvos ≥44px, safe-area, acessibilidade)
- [ ] Shopify (schema, settings/blocks/metafields, tema duplicado, Theme Check)
- [ ] Performance (peso hero, tempo de carga 4G, WebP)
- [ ] CRO (CTA único, bundle selector, sticky ATC, prova social, FAQ/objeções)
- [ ] Tracking (pixel/CAPI, eventos por secção)

## 3. Resultados por checklist
| Checklist | Itens verificados | Passou | Falhou | Nota |
|---|---|---|---|---|
| copy | / | | | |
| ux | / | | | |
| shopify | / | | | |
| performance | / | | | |
| cro | / | | | |

## 4. Issues encontradas
> Severidade: CRITICAL (bloqueia publicação — claim falso/dados inventados) ·
> HIGH (quebra conversão/funcionalidade) · MEDIUM (qualidade, deve corrigir) ·
> LOW (polish).

| # | Severidade | Secção/frame | Descrição | Evidência (screenshot/linha/ficheiro) | Recomendação |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## 5. Claims auditados (passagem de consistência obrigatória)
| Claim (preço/desconto/prazo/garantia/specs/reviews) | Valor usado | Fonte verificada (loja/fornecedor/política) | Consistente em todos os frames? |
|---|---|---|---|
| Preço | | | |
| Preço riscado | | | |
| Garantia | | | |
| Prazo de entrega | | | |
| Specs | | | |
| Reviews (reais vs. dramatizadas) | | | |
| Painel grátis | | | |

Guardrails do product-brief secção 7:
- [ ] Nenhum preço/desconto/prazo/garantia sem confirmação
- [ ] Claims de saúde/beleza suavizados
- [ ] Sem logos de imprensa/endorsements inventados
- [ ] Reviews reais ou "Dramatized customer story" legível
- [ ] Specs verificados (nenhum BLOCKED em aberto)

## 6. Plano de correção (se APROVADO COM RESSALVAS / REJEITADO)
| Issue # | Correção | Responsável (agente/task) | Prazo | Estado |
|---|---|---|---|---|
| | | | | |

## 7. Veredito final
- **Decisão**: APROVADO / APROVADO COM RESSALVAS / REJEITADO
- **Assinado por**: qa-specialist
- **Data**: 
- **Revisão humana** (obrigatória antes do lançamento): aprovado por ___ em ___
