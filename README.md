# Homefy — E-commerce AI Operating System

O Homefy é um **sistema operacional de e-commerce baseado em agentes**: pesquisa de
produto e mercado, estratégia de oferta, copywriting, landing pages, Shopify,
criativos, CRO, QA e lançamento de testes — orquestrados por squads e executados
por um runtime de agentes.

Ele **não é apenas um gerador de landing pages**. É a arquitetura completa em torno
da operação: governança de modelos e custos, contratos de entrada entre agentes,
execução auditável com artefatos por run e uma regra crítica de publicação com
aprovação humana.

## Arquitetura

```
HOMEFY (produto + conhecimento: ecom-stack/, skills/, docs/)
   │
   ▼
AIOX CORE 5.4.1 (.aiox-core/)
   orquestração · governança · squads · ideSync multi-IDE
   │
   ▼
ECOMMERCE GROWTH SQUAD (squads/ecommerce-growth/)
   RESEARCH → STRATEGY → PRODUCTION → QA
   10 agents · 16 tasks · 3 workflows · 6 checklists · 7 templates
   │
   ▼  delegação one-shot (executor pattern)
HERMES AGENT v0.20.2 (instalado fora do repo: ~/.local/bin/hermes)
   │
   ▼
Browser (automação PENDENTE nesta VPS → fallback curl/HTTP) · Terminal · Files
   │
   ▼
APIs · Shopify · Meta · TikTok · Web
```

Cada camada tem uma responsabilidade única e um contrato bem definido com a
camada vizinha. Ver `docs/architecture.md` para as decisões e `docs/hermes-integration.md`
para o contrato de execução.

## Papel do AIOX

O **AIOX Core** (`.aiox-core/`, versão 5.4.1) é o framework de orquestração. Ele:

- define e valida o squad (`squads/ecommerce-growth/squad.yaml` é o manifest);
- mantém a governança de modelos e custos (`modelGovernance` em
  `.aiox-core/core-config.yaml`): teto de budget (US$ 20/dia, US$ 200/mês),
  max iterations, timeouts, fallback entre modelos e checkpoints obrigatórios
  em loops autônomos;
- projeta os agents para os IDEs/editores via **ideSync** (source of truth em
  `.aiox-core/development/agents` → `.kimi/`, `.codex/`, `.claude/`, `.gemini/`,
  `.cursor/`, `.antigravity/`, `.github/`) — nunca edite projeções à mão;
- fornece a CLI local (`bin/aiox.js`) e os validadores oficiais via
  `npx aiox-core@5.4.1`.

O AIOX **não executa** o trabalho: ele orquestra e delega.

## Papel do Hermes

O **Hermes Agent** (v0.20.2, instalado pelo usuário fora deste repositório em
`~/.local/bin/hermes`, também disponível para o usuário de sistema `hermes`) é o
runtime de execução. Ele:

- executa prompts em modo one-shot (`hermes -z`) delegados pelo orquestrador;
- usa como modelo default o **Groq `llama-3.3-70b-versatile`** (override por
  execução com `-m`; provider/modelo configurados em `~/.hermes/config.yaml`);
- dispõe de skills e MCP, e escreve a utilização de tokens em `usage.json`;
- integra-se ao projeto pelo executor `workflows/executors/hermes-exec.sh`, que
  aplica pré-checks, timeout (default 20 min) e classificação de status
  (SUCCESS / PARTIAL / FAILED / TIMEOUT / REJECTED), gravando artefatos por run
  em `.aiox/external-runs/<run>/`.

**Limitação atual nesta VPS:** a automação de browser do Hermes depende de
componentes de sistema ainda pendentes; enquanto isso, o runtime opera em modo
degradado com HTTP básico via `curl`. Ver `docs/hermes-integration.md`.

## Ecommerce Growth Squad

O squad `ecommerce-growth` é o domínio de negócio (ver
`squads/ecommerce-growth/squad.yaml`):

- **10 agents**: ecommerce-master (orquestração), market-researcher,
  product-researcher, offer-strategist, copywriter, ux-designer,
  shopify-engineer, creative-director, cro-specialist, qa-specialist;
- **16 tasks**: o ponto de entrada primário do trabalho (task-first);
- **3 workflows**: `product-to-page`, `product-to-launch`, `page-optimization`;
- **6 checklists** (copy, ux, shopify, performance, cro, launch) e
  **7 templates** — incluindo o **Product Brief** (`templates/product-brief.md`),
  o contrato central de entrada consumido por todos os agents.

Detalhes em `docs/agents.md` e `docs/workflows.md`.

## Como instalar

O **AIOX Core já vem no repositório** (`.aiox-core/`, alinhado com o manifesto de
instalação) — não é preciso instalá-lo. A CLI local é o wrapper `bin/aiox.js`.

O **Hermes é instalado pelo usuário, fora do repositório**:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Depois, configure provider/modelo e chaves em `~/.hermes/config.yaml` e
`~/.hermes/.env` (o comando `hermes setup` guia a configuração). O executor
detecta o binário em `~/.local/bin/hermes` (ou no usuário de sistema `hermes`).

Dependências do projeto (VPS Ubuntu): `python3`, `nodejs >= 18` (ideal 20 LTS).
Ver `ecom-stack/docs/setup-vps.md` para o passo a passo completo.

## Como validar

```bash
# Integridade da instalação AIOX e diagnósticos do framework
npx aiox-core@5.4.1 validate
npx aiox-core@5.4.1 doctor

# Validação do squad contra o schema oficial
node squads/ecommerce-growth/tools/validate-squad.js ecommerce-growth

# Diagnósticos do runtime de execução
hermes doctor

# Smoke test ponta a ponta da cadeia AIOX → task → Hermes → resultado
bash squads/ecommerce-growth/scripts/run-smoke-test.sh
```

Saídas esperadas: `validate` sem erros de integridade; `validate-squad.js` com
`== RESULTADO: PASS ==`; `hermes doctor` pode reportar itens conhecidos desta
VPS (ex.: `XAI_API_KEY` ausente para a skill `x_search`, vulnerabilidades npm em
workspaces do Hermes, sugestão de rodar `hermes setup`) — são avisos, não
bloqueios. Os runs de execução ficam em `.aiox/external-runs/<run>/result.json`.

## Como executar tasks e workflows

**Padrão de execução de uma task** — delegação one-shot ao Hermes via executor:

```bash
workflows/executors/hermes-exec.sh -t research-product \
  -f squads/ecommerce-growth/tasks/research-product.md \
  -d /root/homefy
```

O executor imprime `STATUS`, `RUN_DIR`, `OUTPUT` e `RESULT_JSON`, e grava em
`.aiox/external-runs/<timestamp>-<slug>/`: `prompt.md`, `command.txt`,
`output.md`, `hermes.log`, `usage.json`, `result.json`, `metadata.json` e o
diretório `artifacts/`. **Leia sempre o `result.json`** — o campo `status`
(`SUCCESS`/`PARTIAL`/`FAILED`/`TIMEOUT`/`REJECTED`) é o veredito da execução;
`PARTIAL` exige revisão humana antes de prosseguir. Opções: `-p "prompt inline"`,
`-m <modelo>` (override), `-T <minutos>` (timeout, default 20), `-d <workdir>`.

**Workflows** — os 3 workflows do squad (`workflows/*.yaml`) descrevem cadeias de
fases com gates de validação. A execução é **fase a fase, via executor** (cada
fase consome o artefato da anterior e valida o `result.json` antes de avançar).
A execução automática do DAG do workflow yaml ainda é semi-manual — ver
`docs/workflows.md`.

**Regra crítica:** publicação em Shopify/Meta/TikTok **somente com aprovação
humana explícita** — nenhum agente publica sozinho.

## Como configurar segredos

1. Copie o exemplo e preencha com suas credenciais:

   ```bash
   cp ecom-stack/config/config.example.env ecom-stack/config/.env
   ```

2. `ecom-stack/config/.env` é **gitignored** — nunca commite. O arquivo
   `config.example.env` lista as variáveis (Shopify, Meta, TikTok, Picsart)
   com placeholders vazios; serve apenas como referência.
3. O Hermes mantém suas próprias credenciais em `~/.hermes/` (fora do repo).
4. **Nunca** coloque segredos em código, prompts, tasks, logs, workflows ou
   documentação — apenas placeholders. Ver `docs/security.md`.

## Estrutura do projeto

```
homefy/
├── .aiox-core/                  # AIOX Core 5.4.1 (framework — não editar à mão)
├── .aiox/
│   └── external-runs/           # artefatos por run do executor (gitignored)
├── .hermes/skills/              # staging de skills Hermes específicas do projeto
├── bin/
│   └── aiox.js                  # wrapper da CLI AIOX local
├── docs/                        # documentação do projeto (arquitetura, agentes, …)
├── ecom-stack/                  # stack operacional original (preservada)
│   ├── cli/cli.py               # CLI do projeto: python3 cli/cli.py ajuda
│   ├── config/                  # config.example.env (o .env real é gitignored)
│   ├── docs/                    # blueprints e SOPs (setup-vps, guia-uso, …)
│   ├── painel/                  # painel web (localhost, via túnel SSH)
│   ├── prompts/                 # prompts de pesquisa/página/criativos/loja
│   ├── research/                # referências de landers por produto
│   ├── templates/               # landing pages + product-brief
│   └── assets/creatives/        # imagens e vídeos gerados
├── skills/                      # skills por domínio (ecommerce, shopify, research…)
├── squads/
│   └── ecommerce-growth/        # squad AIOX (squad.yaml + agents/tasks/workflows/…)
├── workflows/
│   └── executors/
│       └── hermes-exec.sh       # ponte AIOX → Hermes (executor pattern)
├── AGENTS.md                    # regras do projeto
└── README.md                    # este arquivo
```

## Regras de desenvolvimento

As 5 regras críticas de `AGENTS.md`, mais a regra de publicação:

1. Nunca commitar segredos — o `.env` real fica em `ecom-stack/config/.env`
   (gitignored).
2. Nunca executar `npx aiox-core install --force` sem avaliar conflitos primeiro.
3. `ecom-stack/` é a stack operacional preservada — não remover nem renomear.
4. Execução delegada ao Hermes sempre via `workflows/executors/hermes-exec.sh`.
5. Deploy/publicação (Shopify, Meta, TikTok) **só com confirmação explícita do
   operador** — aprovação humana é obrigatória, sem exceção.

Além delas: não editar projeções ideSync à mão (source of truth em
`.aiox-core/development/agents`) e não editar o framework em `.aiox-core/`.

## Documentação

- `docs/architecture.md` — decisões arquitetônicas e limitações atuais
- `docs/agents.md` — os 10 agents do squad e suas autoridades
- `docs/workflows.md` — os 3 workflows, gates e política de retry/halt
- `docs/hermes-integration.md` — contrato do executor e degradação graciosa
- `docs/deployment.md` — estado de deploy (nenhum deploy automático) e painel
- `docs/security.md` — segredos, tokens, logs e varredura de secrets
