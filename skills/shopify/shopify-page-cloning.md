---
name: shopify-page-cloning
description: Fluxo operacional para clonar uma página de referência (URL ou HTML) como página de produto Shopify fiel — esta skill orquestra o trabalho, aponta para a skill profunda clone-link-to-my-shopify e detalha o fluxo fase a fase, do pre-flight à verificação.
when_to_use: Quando o operador pede para clonar/replicar uma página específica na loja ("clone this", "make this for my store", cola uma URL), em alternativa à cadeia manual de prompts de loja-completa.md. Sem acesso MCP/à loja, seguir a cadeia de prompts manual.
---

# Cloning de página para Shopify — fluxo operacional

## Quando usar

- Pedido explícito de clonar uma landing page de referência para a loja.
- O operador forneceu URL ou HTML/JSX da página-fonte.
- Pré-condição: acesso configurado à loja (MCP ou Admin API com `.env`).

## Pré-requisitos

- A skill profunda disponível: `skills/clone-link-to-my-shopify.skill` (zip com `SKILL.md` — é ela que executa o trabalho; esta skill apenas orquestra).
- Produto real criado na loja (a skill cria/atribui o produto no Phase 4, mas o produto-alvo tem de estar definido).
- Loja e tema OS 2.0 confirmados (Phase 0 faz a deteção; temas não-OS 2.0 caem no Page Fallback).

## Procedimento

1. **Delegar à skill profunda.** Abrir `skills/clone-link-to-my-shopify.skill` e seguir o seu SKILL.md fase a fase. Resumo operacional do fluxo (as regras detalhadas vivem lá):
   - **Phase 0 — Pre-flight:** fixar `STORE_DOMAIN`, confirmar ligação, detetar tema MAIN (OS 2.0) e **duplicar o tema** (write target = draft); re-duplicar após cada publish. Criar slug único (ex.: `clone-<nome>-001`) para todos os ficheiros.
   - **Phase 1 — Extração:** transcricao (não classificação) do DOM-fonte; tokens de design para `/tmp/source-tokens.css`; spec JSON por secção (`/tmp/section-NN.json`); ficheiros JS-rendered exigem render real (bundler unpacking ou browser).
   - **Phases 2–5 — Construção:** resolver tokens, migrar assets, criar o produto, transcrever cada secção em Liquid editável (settings/blocks por elemento dinâmico), escrever no tema em batches.
   - **Phases 6–9 — Função e qualidade:** CTA/carrinho reais (sticky mobile CTA sempre), SEO/structured data, performance, regras UX mobile+desktop.
   - **Phases 10–11 — Verificação e hand-off:** verificação completa antes de entregar resumo com ficheiros criados.
2. **Coordenar com o método Homefy:** a página-fonte é uma das 3 referências do brief (secção 4) — a estrutura clonada herda os guardrails de claims, prova real e consistência de valores (`skills/copywriting/direct-response-copy.md`, `skills/ecommerce/offer-strategy.md`).
3. **Sem acesso MCP/à loja:** não improvisar — mudar para a cadeia manual de `prompts/loja-completa.md` (master prompter → 3 HTML conceito → master prompt de publicação) e avisar o operador.

## Outputs

- Produto real + custom product template + custom theme sections na loja (URL live onde tudo funciona).
- Hand-off summary da skill profunda: ficheiros criados/modificados e instruções de template assignment.
- Tema draft (não publicado) — publish só com aprovação do operador.

## Referências

- `skills/clone-link-to-my-shopify.skill` — **fonte primária** (SKILL.md com as 11 phases, schema rules, failure modes, strict rules).
- `ecom-stack/prompts/loja-completa.md` — secção "Alternativa automatizada" e cadeia manual quando não há acesso.
- `ecom-stack/docs/integracoes-cli.md` — detalhe técnico das phases 5–11 (idêntico ao conteúdo da skill).
- `ecom-stack/templates/product-brief.md` — secção 4 (referências) e secção 7 (guardrails).
- `skills/shopify/shopify-development.md` — convenções de implementação no tema.

## Guardrails

- Duplicar o tema antes de qualquer escrita; re-duplicar após cada publish.
- Transcrever, não classificar — a classificação genérica é o failure mode nº 1 (página diluída).
- Nunca inventar detalhes de produto/marca; imagens do produto vêm das fotos reais do operador.
- Publish só com confirmação explícita do operador (regra 5 do AGENTS.md).
- Sem scraping em massa da fonte: extração pontual da página pedida, com timeouts.
