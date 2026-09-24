# Arquitetura do Homefy

Decisões arquitetônicas do Homefy — E-commerce AI Operating System.
Estado: setembro de 2026 (AIOX Core 5.4.1, Hermes Agent v0.20.2).

## Visão geral

O Homefy separa quatro responsabilidades em quatro componentes, cada um com um
contrato bem definito:

| Componente | Onde vive | Responsabilidade |
|---|---|---|
| **AIOX Core** | `.aiox-core/` | Orquestração e governança: squads, agents, tasks, workflows, modelGovernance, ideSync |
| **Ecommerce Growth Squad** | `squads/ecommerce-growth/` | Domínio de negócio: pesquisa, oferta, copy, página, Shopify, criativos, CRO, QA |
| **Hermes Agent** | fora do repo (`~/.local/bin/hermes`) | Runtime de execução: roda prompts one-shot, skills, MCP, browser/terminal/files |
| **Homefy (produto)** | `ecom-stack/`, `skills/`, `docs/` | Conhecimento e operação: CLI, painel, prompts, templates, métodos |

```
HOMEFY (produto + conhecimento)
   → AIOX CORE (orquestração/governança)
   → ECOMMERCE GROWTH SQUAD (domínio: RESEARCH → STRATEGY → PRODUCTION → QA)
   → HERMES (execução one-shot)
   → Browser (pendente) / Terminal / Files
   → APIs · Shopify · Meta · TikTok · Web
```

## Decisão 1 — Separação orquestração × domínio × execução × conhecimento

**Contexto.** Um sistema de agentes para e-commerce precisa simultaneamente de
regras de negócio (o que fazer), de governança (limites de custo/iteração) e de
um runtime capaz de executar trabalho real (arquivos, terminal, web).

**Decisão.**
- O **AIOX Core** não sabe o que é um produto vencedor — ele sabe o que é um
  squad válido, um task completo, um workflow com gates. Framework genérico,
  instalado em `.aiox-core/` e protegido (não se edita à mão; o
  `boundary.frameworkProtection` protege o núcleo).
- O **squad** não executa nada — ele descreve: agents com papéis e autoridades,
  tasks com prompts e critérios, workflows com fases e gates. Todo o
  conhecimento de domínio fica aqui.
- O **Hermes** não decide nada — ele executa o prompt que recebe e devolve
  saída + `usage.json`. Qualquer veredito sobre o resultado é do orquestrador.
- A **ecom-stack** permanece como stack operacional original, preservada
  (regra crítica 3 do `AGENTS.md`): é o produto que o operador usa no dia a dia
  (CLI, painel, prompts, templates).

**Consequência.** Podemos trocar o runtime de execução (outro executor externo
seguindo o mesmo contrato de `.aiox/external-runs/`) ou adicionar novos squads
sem tocar no domínio de e-commerce.

## Decisão 2 — Task-first

**Decisão.** Tasks são o ponto de entrada primário do trabalho
(`components.tasks` no `squad.yaml`, 16 tasks). Workflows agrupam tasks em fases;
agents executam tasks. Nada começa "pelo workflow" — começa por uma task com
prompt, entrada esperada e critério de aceite concretos.

**Motivo.** Tasks one-shot são auditáveis (um run = um artefato em
`.aiox/external-runs/`), baratas de reexecutar e fáceis de validar. Workflows
são composições declaradas sobre tasks que já existem.

## Decisão 3 — Product Brief como contrato central de entrada

**Decisão.** `squads/ecommerce-growth/templates/product-brief.md` é o contrato
único de entrada: pesquisa, oferta, copy, spec de página, criativos e QA leem o
mesmo contexto estruturado do produto. Quem inicia uma cadeia produz/atualiza o
brief; quem continua a cadeia consome o brief.

**Motivo.** Elimina telefone-sem-fio entre agentes: o brief é a fonte de verdade
do produto (dados, referências, avatar, oferta, claims permitidas). Também é o
ponto onde o operador humano aprova o que entra na pipeline.

## Decisão 4 — Executor pattern com external-runs

**Decisão.** A integração AIOX → Hermes segue o contrato de executores externos
de `.aiox-core/development/external-executors/README.md`: o orquestrador mantém
a autoridade (seleção de task, aceite, estado); o executor externo apenas tenta
a implementação delegada. O script `workflows/executors/hermes-exec.sh`:

1. faz pré-checks (workdir legível, prompt não vazio, Hermes presente) —
   falha aqui = `REJECTED`;
2. executa `hermes -z` com timeout (default 20 min, `-T` para ajustar);
3. grava artefatos por run em `.aiox/external-runs/<timestamp>-<slug>/`:
   `prompt.md`, `command.txt`, `output.md`, `hermes.log`, `usage.json`,
   `result.json`, `metadata.json`, `artifacts/`;
4. classifica o resultado: `SUCCESS` / `PARTIAL` / `FAILED` / `TIMEOUT` /
   `REJECTED`, com detecção de erro fatal mesmo quando o processo sai com
   exit 0 (ex.: HTTP 404 de modelo → downgrade de SUCCESS para FAILED).

**Motivo.** Execução auditável e reproduzível: qualquer run pode ser inspecionado
posteriormente (o que foi pedido, o comando exato, a saída, o custo). O diretório
`.aiox/external-runs/` é gitignored — artefatos são locais.

Ver `docs/hermes-integration.md` para o contrato completo.

## Decisão 5 — ideSync multi-IDE

**Decisão.** A fonte de verdade dos agents fica em
`.aiox-core/development/agents` e o **ideSync** (`.aiox-core/core-config.yaml`)
projeta para os formatos de cada editor: `.kimi/skills`, `.codex/agents`,
`.claude/commands/AIOX/agents` + `.claude/skills`, `.gemini/rules/AIOX/agents`,
`.cursor/rules/agents`, `.antigravity/rules/agents`, `.github/agents`.
Validação em strict mode com `failOnDrift`.

**Regra.** Nunca editar as projeções à mão — edite a fonte e sincronize. Drift
entre projeção e fonte é erro de validação.

## Decisão 6 — modelGovernance (controle, não execução)

**Decisão.** A governança de modelos em `.aiox-core/core-config.yaml` é um
mecanismo de **controle** que workflows e agentes devem ler e respeitar — ela
não executa chamadas de modelo:

- **Budget ceiling:** US$ 20/dia, US$ 200/mês; ao exceder → `block_and_notify`
  (contador em `.aiox/usage/budget-counter.json`);
- **Max iterations:** 25 default, 15 por task, hard stop ao exceder;
- **Timeouts:** 20 min default, 60 min long-running, 10 min browser automation
  (o executor Hermes aplica o timeout default de 20 min via `-T`);
- **Routing (metadado):** default `claude-sonnet-4-6`, barato
  `claude-haiku-4-5`, complexo `claude-opus-4-6` — a execução real ocorre no
  Hermes (provider/modelo em `~/.hermes/config.yaml`, override `-m`);
- **Fallback:** ordem primary → cheap, no máximo 2 retries por modelo;
  `onModelError: retry_with_fallback`, `onRepeatedFailure: halt_and_escalate`,
  `onTimeout: mark_timeout_and_halt`;
- **Loops autônomos:** permitidos, mas com checkpoint obrigatório a cada 10
  passos e teto de 30 passos consecutivos — nenhum loop autônomo ilimitado.

**Motivo.** Custos previsíveis e falhas controladas: o sistema para e escala
para humano em vez de queimar budget em loop.

## Estado atual e limitações conhecidas

- **Browser automation PENDENTE nesta VPS.** A automação de browser do Hermes
  depende de componentes de sistema ainda não instalados. Degradação atual:
  HTTP básico via `curl`. Skills/agentes que exigem browser devem assumir o
  fallback ou aguardar a instalação dos componentes.
- **Gateway MCP desktop desativado na VPS.** O gateway Docker MCP
  (`docker mcp`, Docker Desktop) está desativado em `core-config.yaml`
  (`reason: headless-linux-vps`) — os comandos são exclusivos do Docker Desktop.
  Presets (`context7`, `desktop-commander`, `playwright`, `exa`) ficam mantidos
  como referência para desenvolvimento local. Na VPS, MCP é gerido nativamente
  via `.claude/mcp.json` e `hermes mcp`.
- **`hermes doctor` reporta itens conhecidos** (avisos, não bloqueios):
  `XAI_API_KEY` ausente (skill `x_search` indisponível), ausência de
  `GITHUB_TOKEN` (rate limit 60 req/hr no hub de skills), vulnerabilidades npm
  em workspaces do próprio Hermes (`agent-browser`, `web`, `ui-tui`) e a
  sugestão de rodar `hermes setup` para configurar chaves de API.
- **Workflows semi-manuais.** A execução do DAG descrito nos YAMLs dos
  workflows ainda é fase a fase via executor — não existe um runner automático
  de workflow. Ver `docs/workflows.md`.
- **Sem deploy automático.** Nenhuma publicação (Shopify/Meta/TikTok) é
  automatizada; a regra é aprovação humana explícita. Ver `docs/deployment.md`.
- **MCP `servers: []` no projeto.** Nenhum servidor MCP de projeto configurado
  no momento; integrações de API (Shopify, Meta, TikTok) usam variáveis de
  ambiente em `ecom-stack/config/.env`.
