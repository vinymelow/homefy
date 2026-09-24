# AGENTS.md — Homefy

Plataforma de automação de e-commerce. Orquestração: **AIOX Core** (`.aiox-core/`).
Runtime de execução: **Hermes Agent** (instalado por usuário, fora deste repositório).

## Estrutura

```
homefy/
├── .aiox-core/              # Framework AIOX (orquestração — não editar à mão)
├── .hermes/skills/          # Skills Hermes específicas do projeto (staging)
├── ecom-stack/              # Stack operacional original (CLI, prompts, templates)
│   ├── cli/cli.py           # CLI do projeto: python3 cli/cli.py ajuda
│   ├── config/              # config.example.env (variáveis de ambiente)
│   ├── docs/                # Blueprints e SOPs
│   ├── painel/              # Painel web (uvicorn)
│   ├── prompts/             # Prompts de pesquisa/página/criativos/loja
│   ├── skills/              # Skills do tutor (espelho de /skills)
│   └── templates/           # Landing pages + product-brief
├── squads/
│   └── ecommerce-growth/    # Squad AIOX (squad.yaml + agents/tasks/workflows/...)
├── skills/                  # Skills por domínio (ecommerce, shopify, research, ...)
├── workflows/
│   └── executors/hermes-exec.sh   # Ponte mínima AIOX → Hermes
└── AGENTS.md / README.md
```

## Regras críticas

1. Nunca commitar segredos. `.env` real fica em `ecom-stack/config/.env` (gitignored).
2. Nunca executar `npx aiox-core install --force` sem avaliar conflitos primeiro.
3. `ecom-stack/` é a stack operacional preservada — não remover nem renomear.
4. Execução delegada ao Hermes: usar `workflows/executors/hermes-exec.sh`.
5. Deploy/publicação (Shopify, Meta, TikTok) só com confirmação explícita do operador.

## Integração AIOX → Hermes

AIOX orquestra (squad `ecommerce-growth`), delega execução ao Hermes em modo
one-shot (`hermes -z`), consome o resultado e valida. Ver
`workflows/executors/hermes-exec.sh` e o relatório de instalação.
