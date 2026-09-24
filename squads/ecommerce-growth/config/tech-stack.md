# Tech Stack — Squad ecommerce-growth (Homefy)

> Descrição do ambiente real onde o squad opera (VPS do projeto). Verificado em
> 24/09/2026. Fontes: `AGENTS.md`, `ecom-stack/docs/setup-vps.md`,
> `.aiox-core/core-config.yaml`.

## 1. Infraestrutura
- **Ubuntu 24.04.4 LTS**, VPS headless (sem desktop; acesso SSH; VS Code
  Remote-SSH recomendado para edição — ver `ecom-stack/docs/guia-uso.md`).
- **Docker 29.7.2** — disponível no host, mas **não usado pelo runtime do squad**
  (orquestração AIOX + Hermes rodam nativamente; gateway MCP desktop desativado).

## 2. Runtimes e linguagens
| Componente | Versão | Uso |
|---|---|---|
| Node.js | v26.7.0 (npm 11.19.0) | AIOX Core e ferramentas do squad; deps isoladas em `.aiox-core/node_modules` |
| Python | 3.12.3 (sistema) | `ecom-stack/cli/cli.py`, painel web (uvicorn), scripts auxiliares |
| Python | 3.11.16 (embutido no Hermes) | runtime do Hermes Agent (instalação própria em `/usr/local/lib/hermes-agent`) |
| Git | 2.43.0 | versionamento do repo |

## 3. AIOX Core 5.4.1 — orquestração
- Instalado em `.aiox-core/` (framework — **não editar à mão**).
- CLI local via wrapper: `bin/aiox.js` (invoca `.aiox-core/cli/index.js`).
- Operações de framework (install/validate/doctor) via
  `npx aiox-core@5.4.1` — **nunca** `npx aiox-core install --force` sem avaliar
  conflitos (`AGENTS.md` regra 2).
- Squads em `squads/`; manifest do squad: `squads/ecommerce-growth/squad.yaml`.
- Config do projeto: `.aiox-core/core-config.yaml` — inclui `devLoadAlwaysFiles`
  apontando para `squads/ecommerce-growth/config/{coding-standards,tech-stack,source-tree}.md`.

## 4. Hermes Agent v0.20.2 — runtime de execução
- Binário: `~/.local/bin/hermes` (root; existe também instalação do usuário
  `hermes` — `hermes-exec.sh` escolhe automaticamente).
- Execução one-shot: `hermes -z "<prompt>" --in <workdir>` com `--usage-file`
  para telemetria; override de modelo com `-m`.
- **Modelo primário do runtime: Hermes/Groq — default `llama-3.3-70b-versatile`**
  (configuração do Hermes do operador; `-m <modelo>` sobrepõe por execução).
- Governança de modelos: `modelGovernance` em `.aiox-core/core-config.yaml` —
  teto de orçamento ($20/dia, $200/mês, ação `block_and_notify`), timeouts
  (default 20 min, long-running 60 min, browser automation 10 min),
  `maxIterations` (default 25, por task 15). O routing declarado (claude-*) é
  **metadado AIOX** — a execução real ocorre no Hermes.
- **Browser automation (playwright): PENDENTE na VPS** — módulo não instalado;
  tasks que exijam browser falham até a instalação da dependência de sistema.
- **MCP: suporte nativo no Hermes** via `hermes mcp` (add/remove/list/test/
  serve/configure); nenhum servidor MCP está configurado no projeto neste
  momento (não existe `.claude/mcp.json` no repo).

## 5. Ponte AIOX → Hermes
- `workflows/executors/hermes-exec.sh` (External Executor pattern):
  `bash workflows/executors/hermes-exec.sh -t <slug> -f <prompt.md> [-d workdir] [-m model] [-T timeout]`
- Artefactos por run em `.aiox/external-runs/<timestamp>-<slug>/`
  (gitignored): `prompt.md command.txt output.md hermes.log usage.json
  result.json metadata.json`.
- Contrato de status: SUCCESS / PARTIAL / FAILED / TIMEOUT / REJECTED
  (detalhe no cabeçalho do script).

## 6. ecom-stack (stack operacional)
- **Shopify** — tema em Liquid (OS 2.0: sections com schema, JSON templates,
  snippets), integração via Admin API com token em `.env`
  (`SHOPIFY_STORE_DOMAIN` + `SHOPIFY_ADMIN_API_TOKEN`); MAIN read-only, tema
  duplicado para escrever. Scopes e setup: `ecom-stack/docs/setup-vps.md` §2.
- **CLI** — `python3 ecom-stack/cli/cli.py ajuda` (status, brief, criativo,
  anuncio plano, doctor, painel).
- **Painel web** — FastAPI/uvicorn em `ecom-stack/painel/`, porta 8787 só em
  localhost (acesso via túnel SSH: `ssh -L 8787:localhost:8787 root@<vps>`).
- **Criativos** — geração local (sem API key): imagens hiper-realistas (5
  chaves), cutout com rembg via pip, overlays de texto com Pillow.
- **Meta/TikTok Ads** — manual no Ads Manager até ~€50/dia; APIs adiadas para a
  fase de escala (`docs/setup-vps.md` §3–4).

## 7. Deploy e publicação
- **Publicação (Shopify, Meta, TikTok) só com confirmação explícita do
  operador** (`AGENTS.md` regra 5; `publish_requires_human_approval: true` no
  squad.yaml).
