# Integrações da CLI — ecom-stack

Documenta as integrações externas usadas pela CLI (`cli/cli.py`) e onde cada
credencial é usada. Para o setup passo-a-passo na VPS, ver `docs/setup-vps.md`.

> **Segurança**: o ficheiro real é `config/.env` (gitignored — nunca commitar).
> Este doc lista apenas os nomes das variáveis. Copiar o template:
> `cp config/config.example.env config/.env`

## Variáveis por integração

| Variável | Usada por | Estado |
|---|---|---|
| `SHOPIFY_STORE_DOMAIN` | `doctor` (liga à loja) | obrigatório p/ Shopify |
| `SHOPIFY_ADMIN_API_TOKEN` | `doctor` (themes.json, read-only) | obrigatório p/ Shopify |
| `SHOPIFY_API_VERSION` | `doctor` (default `2025-07`) | opcional |
| `META_ACCESS_TOKEN` | Fase 5 (publicar/testar) | adiável |
| `META_AD_ACCOUNT_ID` | Fase 5 | adiável |
| `TIKTOK_ACCESS_TOKEN` | Fase 5 | adiável |
| `TIKTOK_ADVERTISER_ID` | Fase 5 | adiável |
| `PICSART_API_KEY` | `criativo imagem` (Fase 4) | adiável |

## Comandos que tocam em integrações

- `python3 cli/cli.py doctor` — verifica `.env` e testa a ligação à Shopify
  (GET `/admin/api/<versão>/themes.json`, read-only). Não escreve nada na loja.
- `python3 cli/cli.py criativo imagem|video <slug>` — geração de criativos via
  API (implementação depende das chaves de Fase 4; até lá, imprime o plano).
- `python3 cli/cli.py anuncio plano <slug>` — plano de teste (offline, sem API).

## Regras

1. **Read-only por default**: a CLI nunca escreve na loja nem nas plataformas de
   ads sem comando explícito futuro + aprovação humana (ver `AGENTS.md` regra 5).
2. **Scopes mínimos**: o token Shopify deve ter apenas o necessário
   (`read_themes` para o `doctor`; escopos de escrita só quando a Fase de
   publicação for implementada e aprovada).
3. **Nunca** colocar tokens em prompts, tasks, workflows ou docs — apenas em
   `config/.env` local.
4. A camada de agentes (AIOX + Hermes) usa estas mesmas integrações através do
   executor — as mesmas regras aplicam-se. Ver `docs/../../workflows/executors/hermes-exec.sh`
   (raiz do repo) e `squads/ecommerce-growth/`.

## Histórico

Este ficheiro continha anteriormente o conteúdo da skill
`clone-link-to-my-shopify` (conteúdo trocado no commit inicial). O conteúdo da
skill vive corretamente em `skills/clone-link-to-my-shopify.skill` e
`../skills/clone-link-to-my-shopify.skill`; o prompt chain "Loja completa" vive
em `prompts/loja-completa.md`. Restaurado em 24/09/2026 com a documentação real
das integrações.
