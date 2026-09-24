# Homefy

Plataforma própria de automação de e-commerce: pesquisa de produtos, estratégia
de oferta, copywriting, landing pages, Shopify, criativos, CRO, QA e testes.

## Arquitetura

```
HOMEFY
  └── AIOX Core (orquestração) — .aiox-core/, squads/ecommerce-growth/
        └── Hermes Agent (runtime de execução) — instalado por usuário na VPS
              └── Browser / Terminal / Files
                    └── Shopify / Meta / TikTok / Web
```

- **AIOX Core** — orquestra squads, agentes, tasks e workflows (ver `squads/`).
- **Hermes Agent** — executa tarefas delegadas (ver `workflows/executors/`).
- **ecom-stack/** — stack operacional original: CLI, prompts, templates, painel.
  Comece por `ecom-stack/README.md`.

## Uso rápido

```bash
# Diagnósticos
npx aiox-core@latest doctor
python3 ecom-stack/cli/cli.py ajuda

# Squad ecommerce-growth
squads/ecommerce-growth/squad.yaml

# Execução delegada ao Hermes
workflows/executors/hermes-exec.sh -t <slug> -f <prompt.md> -d <workdir>
```

## Segredos

Nunca commitar `.env`. Ver `ecom-stack/config/config.example.env` para a lista
de variáveis necessárias e `AGENTS.md` para as regras do projeto.
