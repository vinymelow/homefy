# Squad ecommerce-growth — Homefy

Squad AIOX de growth para e-commerce: pesquisa de produto e mercado, estratégia
de oferta, copywriting, landing pages, Shopify, criativos, CRO, QA e lançamento
de testes. Orquestração AIOX Core + execução delegada ao Hermes Agent.

- Manifest: `squads/ecommerce-growth/squad.yaml` (oficial — não editar à mão)
- Slash prefix: `growth` · AIOX Core ≥ 5.4.1 · Node ≥ 18

## Arquitetura

```
AIOX Core (.aiox-core/)          ← orquestra: squad.yaml, workflows, validação
  └── squads/ecommerce-growth/   ← ESTE SQUAD: agents, tasks, checklists,
        │                            templates, config, data
        └── Hermes Agent         ← runtime de execução (one-shot, hermes -z)
              (workflows/executors/hermes-exec.sh)
              └── artefactos em .aiox/external-runs/ (gitignored)
```

O AIOX mantém a orquestração; o Hermes executa; o squad produz os artefactos.

## Como os componentes se encaixam

- **Tasks first** — tasks são o ponto de entrada primário do squad
  (`tasks/*.md`): cada task é uma instrução executável com contexto, contrato de
  entrada e contrato de saída.
- **Product Brief como contrato central** — `templates/product-brief.md` é a
  versão-squad do contrato (fonte canônica: `ecom-stack/templates/product-brief.md`).
  Todas as tasks consomem o mesmo contexto estruturado do produto: avatar, pain,
  desejos, objeções, oferta, claims, assets e slots de criativos.
- **Workflows encadeiam tasks** — `workflows/product-to-page.yaml`,
  `workflows/product-to-launch.yaml` e `workflows/page-optimization.yaml`
  ordenam as tasks de pesquisa → oferta → copy → spec → página → criativos →
  QA → lançamento.
- **Checklists validam** — `checklists/` (copy, ux, shopify, performance, cro,
  launch) são os gates de qualidade entre tasks; o QA do squad
  (`templates/qa-report.md`) consome-os.
- **Templates padronizam artefactos** — `templates/` (product-brief,
  research-report, offer-brief, landing-page-spec, creative-brief, qa-report,
  launch-report): estrutura fixa + campos a preencher; agents preenchem, nunca
  reinventam.
- **Agents** — `agents/` define os papéis (ecommerce-master, market-researcher,
  product-researcher, offer-strategist, copywriter, ux-designer,
  shopify-engineer, creative-director, cro-specialist, qa-specialist).
- **Config** — `config/` descreve o repo real: convenções (`coding-standards.md`),
  ambiente (`tech-stack.md`) e árvore (`source-tree.md`); referenciados pelo
  `devLoadAlwaysFiles` do AIOX.
- **Data** — `data/knowledge-map.md` mapeia o conhecimento existente
  (ecom-stack, skills, CLI, executores) aos consumidores do squad. Regra:
  referências, não cópias.

## Como validar o squad

```bash
cd /root/homefy
node squads/ecommerce-growth/tools/validate-squad.js ecommerce-growth
# exit 0 = PASS · adicionar --strict para modo estrito
```

## Como executar um smoke test (AIOX → Hermes)

```bash
cd /root/homefy
bash workflows/executors/hermes-exec.sh \
  -t smoke-test \
  -f squads/ecommerce-growth/tasks/smoke-test-project-structure.md \
  -d /root/homefy
```

Saída em key=value (`STATUS=`, `RUN_DIR=`, `OUTPUT=`, `RESULT_JSON=`); artefactos
do run em `.aiox/external-runs/<timestamp>-smoke-test/`. Contrato de status:
SUCCESS / PARTIAL / FAILED / TIMEOUT / REJECTED (ver cabeçalho do script).

## Regra de publicação

**Nada é publicado sem aprovação humana.** Deploy/publicação (Shopify, Meta,
TikTok) exige confirmação explícita do operador — `publish_requires_human_approval:
true` no `squad.yaml`, regra 5 do `AGENTS.md`. O `templates/launch-report.md`
regista as pré-condições (QA PASS, tracking OK, aprovação humana) e mantém os
assets em status PREPARED até essa aprovação.

## Regras críticas (do AGENTS.md)

1. Nunca commitar segredos — `.env` real fica em `ecom-stack/config/.env`
   (gitignored, só local).
2. Nunca executar `npx aiox-core install --force` sem avaliar conflitos.
3. `ecom-stack/` é a stack operacional — não remover nem renomear.
4. Execução delegada ao Hermes só via `workflows/executors/hermes-exec.sh`.
5. Deploy/publicação só com confirmação explícita do operador.
