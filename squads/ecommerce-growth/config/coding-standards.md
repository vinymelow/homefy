# Coding Standards — Squad ecommerce-growth (Homefy)

> Convenções do repositório Homefy para agentes do squad. Estende as regras do
> framework AIOX (`.aiox-core/`) e do projeto (`AGENTS.md`). Em caso de conflito,
> prevalecem as regras críticas de `AGENTS.md`.

## 1. Formatos de conhecimento
- **Markdown é o formato primário de conhecimento**: briefs, relatórios, specs,
  checklists, documentação e artefactos de pesquisa escrevem-se em `.md`
  (frontmatter YAML apenas quando o consumidor o exigir).
- **YAML para workflows e manifests**: `squads/ecommerce-growth/workflows/*.yaml`
  seguem o schema do AIOX (`.aiox-core/schemas/`); `squad.yaml` é manifest
  oficial — **não editar à mão** sem validar depois
  (`node squads/ecommerce-growth/tools/validate-squad.js ecommerce-growth`).
- **HTML/CSS/JS/Liquid para Shopify**: secções OS 2.0 com schema válido e
  presets; CSS/JS scoped com prefixo único por secção; nada de React/Vue/
  Tailwind/jQuery nas secções.

## 2. Scripts
- **Bash**: todo script bash começa com `set -euo pipefail` e shebang
  `#!/usr/bin/env bash` (padrão observado em `workflows/executors/hermes-exec.sh`).
- **Python 3**: código da CLI e do painel em `python3` (3.12), stdlib primeiro;
  a CLI do projeto é `ecom-stack/cli/cli.py` — comandos novos entram no dict
  `COMMANDS` e na docstring de ajuda.
- **Node.js**: ferramentas do squad em Node (ex.: `tools/validate-squad.js`),
  CommonJS, sem dependências externas além do que já existe em
  `.aiox-core/node_modules`.

## 3. Idioma e estilo
- Conteúdo de e-commerce (copy, briefs, relatórios, criativos) em **pt-PT/pt-BR
  conforme o artefacto de origem** — o ecom-stack usa pt-PT; manter coerência
  por ficheiro.
- Código, nomes de ficheiros e slugs em inglês/minúsculas; slugs sem espaços
  nem acentos (`slugify` em `cli.py`).
- Comentários só onde o "porquê" não é óbvio; sem comentários que descrevam o
  que o código já diz.

## 4. Commits (padrão observado no `git log`)
- Histórico real do repo mistura **conventional commits** (`Adiciona docs…`,
  `Atualiza config…`, `Restaura conteúdo…`) e commits de sync
  (`sync vps: DD/MM/YYYY HH:MM`).
- Usar mensagens curtas em **português**, imperativo, descrevendo o que mudou;
  `sync vps: …` é reservado ao script de sincronização do operador.

## 5. Segredos e ambiente
- **Nunca commitar segredos**: `.env` real fica em `ecom-stack/config/.env`
  (gitignored) e **só existe localmente na VPS**; usar
  `ecom-stack/config/config.example.env` como lista de variáveis.
- Nunca imprimir tokens em logs nem colar valores de `.env` em artefactos,
  issues ou prompts (o smoke-test do squad só deve reportar **se** existe,
  nunca os valores).
- Shopify: tema **MAIN é read-only** — duplicar antes de qualquer escrita;
  token Admin API só via `.env`.

## 6. Regras específicas de e-commerce
- **Revisão de claims obrigatória** em todo o conteúdo de e-commerce: nenhum
  preço/desconto/prazo/garantia/spec sem confirmação na loja ou fornecedor;
  claims de saúde/beleza suavizados ("designed to help with"); sem logos de
  imprensa/endorsements inventados; reviews reais ou "Dramatized customer
  story" legível.
- **Passagem de consistência obrigatória** antes de publicar: preço, garantia e
  specs iguais em TODOS os frames/secções (guardrails do product-brief, secção 7).
- Referências de concorrentes = estrutura e movimento; **nunca** copiar logo,
  imagens, copy, reviews, claims ou código.
- Artefactos de execução do Hermes ficam em `.aiox/external-runs/` (gitignored);
  não commitar esses artefactos.

## 7. Validação antes de entregar
- Mudanças no squad: `node squads/ecommerce-growth/tools/validate-squad.js ecommerce-growth`.
- Checklists do squad (`checklists/`) passam antes de qualquer artefacto avançar
  de task no workflow.
