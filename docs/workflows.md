# Workflows do Ecommerce Growth Squad

Os 3 workflows do squad (`squads/ecommerce-growth/workflows/`): composições
declarativas de tasks em fases, com gates de validação. Manifest em
`squads/ecommerce-growth/squad.yaml` (`components.workflows`).

> **Nota honesta sobre execução:** a execução automática do DAG descrito no
> YAML ainda é **semi-manual**. Hoje um workflow é executado fase a fase: o
> operador (ou o ecommerce-master) roda cada task via executor, valida o
> `result.json` e só então dispara a próxima fase. Um runner automático de
> workflow — Não implementado, próxima fase.

## Elementos comuns aos 3 workflows

### Gates de validação via result.json

Cada execução de task produz `.aiox/external-runs/<run>/result.json`. O gate de
cada fase lê o campo `status`:

| Status | Significado | Ação no workflow |
|---|---|---|
| `SUCCESS` | Saída válida, sem padrões fatais | Avança para a próxima fase |
| `PARTIAL` | Exit 0, mas saída vazia/curta demais | **Revisão humana obrigatória** antes de decidir retry ou avanço |
| `FAILED` | Exit ≠ 0 ou erro fatal detectado (ex.: HTTP 404 de modelo, mesmo com exit 0) | Retry com fallback conforme política abaixo |
| `TIMEOUT` | Excedeu o timeout (`-T`, default 20 min) | Halt + investigação; possível reexecução com timeout maior (long-running: 60 min) |
| `REJECTED` | Pré-checks falharam (workdir, prompt vazio, Hermes ausente) | Corrigir o pré-check e reenviar — não conta como execução |

### Política de retry / fallback / halt

Alinhada com `modelGovernance` (`.aiox-core/core-config.yaml`):

- **Retry com fallback:** em erro de modelo, retry na ordem primary → cheap,
  no máximo 2 retries por modelo (`fallback.maxModelRetries`);
- **Budget:** teto de US$ 20/dia e US$ 200/mês (`block_and_notify`) — verificar
  o consumo acumulado em `.aiox/usage/budget-counter.json` e o custo do run em
  `usage.json` antes de novas tentativas;
- **Halt e escalação:** falhas repetidas param o workflow e escalam para o
  operador humano (`onRepeatedFailure: halt_and_escalate`) — nunca loop
  infinito de retry;
- **Timeout:** `onTimeout: mark_timeout_and_halt` — o run é marcado como
  TIMEOUT (exit 124) e o workflow para até decisão humana;
- **Checkpoints:** em cadeias longas, checkpoint obrigatório a cada 10 passos
  (máx. 30 passos consecutivos autônomos).

### Publicação bloqueada por default

Nenhum workflow publica nada. As fases finais produzem artefatos **prontos para
publicação** (página, criativos, plano de campanha), mas a publicação em
Shopify/Meta/TikTok exige **aprovação humana explícita** (regra crítica 5 do
`AGENTS.md`). O gate de publicação é um human-in-the-loop: sem confirmação do
operador, o fluxo termina no artefato.

## Workflow 1 — `product-to-page`

Da ideia de produto a uma landing page validada. Consome o Product Brief como
contrato de entrada e termina com QA PASS da página.

| Fase | Tasks | Gate |
|---|---|---|
| 1. Research | `research-product`, `research-market`, `analyze-competitors`, `create-customer-avatar` | `result.json` SUCCESS em cada task; brief atualizado |
| 2. Estratégia | `create-offer`, `create-positioning` | Offer alinhado ao brief (claims com evidência) |
| 3. Copy | `create-copy` | Checklist de copy + revisão do copywriter |
| 4. Spec | `create-page-spec` | Spec consome copy + referências |
| 5. Produção | `build-landing-page` | HTML gerado a partir da spec |
| 6. QA | `audit-page` | **QA PASS do qa-specialist** — sem PASS, volta à fase indicada |

Saída: landing page (HTML) + spec + copy, prontos para conversão Liquid.

## Workflow 2 — `product-to-launch`

Extende `product-to-page` até o pacote de lançamento. A publicação continua
bloqueada para a aprovação humana.

| Fase | Tasks | Gate |
|---|---|---|
| 1–6. product-to-page | (mesmas fases acima) | QA PASS da página |
| 7. Shopify | `build-shopify-page` | Página convertida para Liquid/Shopify, checklist shopify |
| 8. Criativos | `generate-creative-brief` | Brief de criativos com slots e QC do creative-director |
| 9. Lançamento | `prepare-launch` | Launch report completo |
| 10. Smoke | `smoke-test-project-structure` | Cadeia AIOX → task → Hermes → resultado íntegra |

Saída: pacote de lançamento (página Shopify + criativos + plano de teste +
launch report). **Publicação: somente após aprovação humana explícita.**

## Workflow 3 — `page-optimization`

Ciclo de melhoria contínua sobre uma página existente.

| Fase | Tasks | Gate |
|---|---|---|
| 1. Auditoria CRO | `audit-cro` | Diagnóstico com hipóteses priorizadas |
| 2. Auditoria de página | `audit-page` | Lista de fricções/objeções mapeadas para seções |
| 3. Recomendação | melhorias encaminhadas ao ux-designer / copywriter / shopify-engineer conforme a natureza | Checklists cro + ux |
| 4. QA | re-`audit-page` após mudanças | **QA PASS** — comparação antes/depois |

Saída: página otimizada com registro do que mudou e por quê.

## Como executar um workflow (hoje, semi-manual)

```bash
# 1. Escolha a task da fase atual (ex.: research-product)
# 2. Execute via executor
workflows/executors/hermes-exec.sh -t research-product \
  -f squads/ecommerce-growth/tasks/research-product.md \
  -d /root/homefy

# 3. Leia o veredito
cat .aiox/external-runs/<run>/result.json   # campo "status"

# 4. Só avance para a próxima fase se o gate permitir (SUCCESS,
#    ou PARTIAL após revisão humana). FAILED → retry com fallback.
#    TIMEOUT/REJECTED → corrigir e reenviar.
```

Para a primeira verificação ponta a ponta da cadeia, existe a task
`smoke-test-project-structure` (só leitura local, sem rede) e o script
`bash squads/ecommerce-growth/scripts/run-smoke-test.sh`.
