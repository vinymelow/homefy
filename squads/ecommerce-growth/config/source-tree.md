# Source Tree — Squad ecommerce-growth (Homefy)

> Árvore real do repositório (levantada com
> `find /root/homefy -maxdepth 3 -type d`, excluindo `.git/` e `node_modules/`),
> com o papel de cada diretório para os agentes do squad. Atualizada em
> 24/09/2026.

```
homefy/
├── .aiox-core/                  # Framework AIOX Core 5.4.1 — NÃO EDITAR À MÃO
│   ├── cli/                     #   CLI do framework (invocado via bin/aiox.js)
│   ├── core/                    #   orquestração, sessão, permissões, MCP, ...
│   ├── development/             #   agents/ tasks/ workflows/ templates/ skills/
│   │                            #   (source of truth das projeções de IDE)
│   ├── schemas/                 #   schemas de validação (squad-schema.json, ...)
│   ├── manifests/               #   manifests instalados (.installed-manifest.yaml)
│   ├── governance/ hooks/ data/ #   governança, hooks, presets
│   └── core-config.yaml         #   config do projeto (modelGovernance, ide, ...)
├── .aiox/
│   └── external-runs/           # Artefatos de execução Hermes (GITIGNORED)
│                                #   <timestamp>-<slug>/: prompt.md, output.md,
│                                #   hermes.log, usage.json, result.json, ...
├── .hermes/skills/              # Skills Hermes específicas do projeto (staging)
├── bin/
│   └── aiox.js                  # Wrapper CLI local do AIOX (requiere .aiox-core/cli)
├── ecom-stack/                  # Stack operacional original (não remover/renomear)
│   ├── cli/cli.py               #   CLI do projeto (python3 cli/cli.py ajuda)
│   ├── config/                  #   config.example.env (.env real fica local, gitignored)
│   ├── docs/                    #   blueprints e SOPs (blueprint, métodos, setup)
│   ├── painel/                  #   painel web (FastAPI/uvicorn, porta 8787)
│   ├── prompts/                 #   prompts de pesquisa/página/criativos/loja
│   ├── research/                #   tracker.md + landers/ (briefs por produto)
│   ├── skills/                  #   skills do tutor (clone de página, PDP, hiper-real)
│   ├── templates/               #   landing-page.html, escova-alisadora.html,
│   │                            #   product-brief.md (CONTRATO CENTRAL)
│   ├── assets/                  #   creatives/ e uploads/ (assets gerados)
│   └── frontend/                #   frontend do painel
├── skills/                      # Skills por domínio do projeto
│   ├── copywriting/ creative/ cro/ ecommerce/ research/ shopify/
│   │                            #   (diretórios por domínio — staging)
│   └── *.md / *.skill           #   branded-shopify-store-builder, clone-static-ad,
│                                #   hyperreal-image, product-pdp-image-builder, ...
├── squads/
│   └── ecommerce-growth/        # SQUAD AIOX desta operação
│       ├── squad.yaml           #   manifest oficial (não editar à mão)
│       ├── agents/              #   agentes (ecommerce-master, copywriter, ...)
│       ├── tasks/               #   tasks (ponto de entrada primário)
│       ├── workflows/           #   workflows YAML (product-to-page, ...)
│       ├── checklists/          #   checklists de validação (copy, ux, shopify, ...)
│       ├── templates/           #   7 templates de artefactos do squad
│       ├── config/              #   coding-standards / tech-stack / source-tree
│       ├── data/                #   knowledge-map.md (conhecimento → consumidores)
│       └── tools/validate-squad.js  # validador do squad
├── workflows/
│   └── executors/
│       └── hermes-exec.sh       # Ponte AIOX → Hermes (External Executor)
├── .kimi/ .codex/ .claude/ .gemini/ .cursor/ .antigravity/ .github/
│                                # Projeções sincronizadas p/ cada IDE/agente
├── AGENTS.md                    # Regras críticas do projeto
└── README.md                    # Visão geral e arquitetura
```

## Papel dos diretórios-chave

### `.aiox-core/` — framework AIOX (não editar à mão)
Orquestração do AIOX Core 5.4.1: CLI (`cli/`), núcleo (`core/`), schemas de
validação (`schemas/`), manifest de instalação (`manifests/`), governança e
`core-config.yaml` (modelGovernance, seleção de IDEs, `devLoadAlwaysFiles`).
Qualquer mudança feita à mão pode ser revertida pelo framework; estender o
comportamento via `squads/` e `bin/aiox.js`.

### `.aiox/external-runs/` — artefatos de execução (gitignored)
Runs do Hermes produzidos por `workflows/executors/hermes-exec.sh`. Cada run
tem `prompt.md`, `command.txt`, `output.md`, `hermes.log`, `usage.json`,
`result.json` e `metadata.json`. São artefactos de diagnóstico — não versionar,
não usar como fonte de verdade de produto.

### `.hermes/skills/` — skills Hermes do projeto (staging)
Diretório onde skills específicas do projeto são disponibilizadas ao runtime
Hermes. Hoje está vazio (só `.gitkeep`); skills ativas vivem em `skills/` e
`ecom-stack/skills/`.

### `.kimi/ .codex/ .claude/ .gemini/ .cursor/ .antigravity/ .github/` — projeções de IDE
Cada diretório é a **projeção sincronizada** do AIOX para um IDE/agente
(rules, commands, skills, agents). **Source of truth =
`.aiox-core/development/agents/`** — editar sempre lá; as projeções são
geradas/sincronizadas pelo mecanismo de sync do AIOX (observado: `.codex/agents/`
espelha ficheiro a ficheiro os agents do `development/agents/`).

### `ecom-stack/` — stack operacional
Stack original do projeto (CLI, painel, prompts, templates, research). Papel por
subdiretório em `squads/ecommerce-growth/data/knowledge-map.md`. Regra crítica:
**não remover nem renomear** (`AGENTS.md` regra 3). O Product Brief canônico é
`ecom-stack/templates/product-brief.md`.

### `skills/` — skills por domínio
Skills organizadas por domínio (`copywriting/`, `creative/`, `cro/`,
`ecommerce/`, `research/`, `shopify/` — diretórios de staging) e skills
avulsas na raiz (`branded-shopify-store-builder.md`, `clone-static-ad.md`,
`hyperreal-image.skill`, `product-pdp-image-builder.skill`,
`clone-link-to-my-shopify.skill`), espelhando `ecom-stack/skills/`.

### `squads/ecommerce-growth/` — o squad
Squad AIOX de growth de e-commerce. `squad.yaml` é o manifest oficial;
tasks são o ponto de entrada; templates padronizam os artefactos; checklists
validam; `tools/validate-squad.js` valida o squad inteiro.

### `workflows/executors/` — ponte Hermes
`hermes-exec.sh` é a ponte mínima AIOX → Hermes (one-shot `hermes -z`),
seguindo o contrato de External Executor do framework. É o único caminho
suportado de execução delegada (`AGENTS.md` regra 4).

### Documentação em raiz
`AGENTS.md` (regras críticas) e `README.md` (arquitetura AIOX → Hermes).
Não existe diretório `docs/` na raiz neste momento (o AIOX reserva `docs/qa`,
`docs/prd` etc. em `core-config.yaml` para quando forem criados); a
documentação operacional vive em `ecom-stack/docs/`.
