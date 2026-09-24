---
name: homefy-shopify
description: Convenções Shopify do projeto Homefy — onde vivem os templates (ecom-stack/templates/), regras de claims, pré-condição de o produto existir na loja antes do Liquid, proibição de publicar sem aprovação, e verificação da ligação com python3 ecom-stack/cli/cli.py doctor.
---

# Homefy — convenções Shopify

## 1. Verificação da ligação à loja

Antes de qualquer tarefa que toque na loja e no fim dela:

```bash
cd /root/homefy
python3 ecom-stack/cli/cli.py doctor     # verifica .env e testa a ligação à Shopify
python3 ecom-stack/cli/cli.py status     # estado geral do projeto + próximo passo
```

- `doctor` a falhar = parar e reportar (verificar `SHOPIFY_STORE_DOMAIN`/`SHOPIFY_ADMIN_API_TOKEN` e scopes; nunca editar o `.env` à mão em run).
- `.env` real fica em `ecom-stack/config/.env` (gitignored) — nunca o commitar nem imprimir valores.

## 2. Onde vivem os templates e artefatos

- Templates base: `ecom-stack/templates/` — `landing-page.html` (página única com slots `data-slot`), `product-brief.md` (contrato central), `escova-alisadora.html` (exemplo real preenchido).
- Criativos: `ecom-stack/assets/creatives/` — nomes dos ficheiros têm de casar com os slots da página.
- Briefs: `ecom-stack/research/landers/<slug>-brief.md` (criar via `python3 ecom-stack/cli/cli.py brief novo <slug>`).
- Métodos: `ecom-stack/docs/blueprint-pagina-de-vendas.md`, `ecom-stack/prompts/loja-completa.md`.

## 3. Pré-condições antes de escrever Liquid

1. **O produto tem de existir na loja** (URL no brief, secção 1) — a conversão Liquid falha sem produto real. Não existindo, parar e pedir criação do produto.
2. Brief preenchido e guardrails da secção 7 confirmados.
3. Tema de trabalho = **duplicado do MAIN** (MAIN é read-only; re-duplicar após cada publish).

## 4. Regras de claims (o que mata a conta e a loja)

- Nada de claims de cura/tratamento — "designed to help with".
- Reviews reais da loja OU "Dramatized customer story" legível; contagem só se real.
- Sem logos de imprensa/prémios/endorsements inventados.
- Specs/preço/garantia iguais em TODOS os frames e secções (passagem de consistência obrigatória).
- Nada hardcoded do lado do merchant: preços, bundles, garantias e reviews vêm de settings/blocks/metafields/dados live.

## 5. Publicação

- **Nunca publicar (tema, página, produto) sem confirmação explícita do operador** — regra 5 do AGENTS.md. Preparar tudo, apresentar preview/relatório e aguardar.
- Checklist pós-publicação (`prompts/loja-completa.md`): header/footer reais no preview, nenhum valor hardcoded (mudar preço no admin muda na página), tema publicado a partir de duplicado, Theme Check sem erros, secções editáveis no Theme Editor, pixel a disparar nos eventos certos.

## Guardrails

- `python3 ecom-stack/cli/cli.py doctor` antes/depois de tarefas de loja; falha = stop and report.
- Produto existente na loja antes de qualquer Liquid.
- Tema MAIN read-only; escrever só em duplicado; re-duplicar após publish.
- Publicação/deploy só com confirmação explícita do operador.
- Nunca commitar nem revelar o `.env`; nunca imprimir tokens em logs.
