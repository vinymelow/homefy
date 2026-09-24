---
name: shopify-development
description: Convenções de desenvolvimento Shopify do Homefy — arquitetura OS 2.0 (sections/snippets com schema, metafields, JSON templates), validação responsiva, integração com o repo (CLI doctor, tema duplicado) e conversão do HTML conceito em tema sem hardcoded values.
when_to_use: Ao implementar secções Liquid num tema, converter a landing page HTML em tema Shopify, criar/editar templates de produto, ou validar uma implementação existente. Para clonar uma página de referência completa, usar `skills/shopify/shopify-page-cloning.md`.
---

# Desenvolvimento Shopify — convenções Homefy

## Quando usar

- Implementação de homepage/PDP dentro do tema existente (fluxo PASSO 4 de `prompts/loja-completa.md`).
- Conversão do HTML conceito (landing-page.html) em secções Liquid editáveis.
- Manutenção/validação de secções existentes (theme check, responsivo).

## Pré-requisitos

- Produto já existe na loja (URL no brief secção 1) — senão a conversão falha.
- Ligação à loja verificada: `python3 ecom-stack/cli/cli.py doctor` (verifica `.env` e testa a ligação à Shopify).
- Tema de trabalho: **duplicado do MAIN** — o tema MAIN é read-only (regra permanente, ver `docs/setup-vps.md` §2).
- HTML conceito aprovado (gerado a partir de `ecom-stack/templates/landing-page.html`).

## Procedimento

1. **Arquitetura OS 2.0 nativa:** uma Liquid section por módulo, com schema válido e presets; snippets partilhados para markup repetido; templates JSON; CSS/JS scoped com prefixo único do slug. Sem React/Vue/Tailwind/page builders/jQuery.
2. **Nada hardcoded do lado do merchant:** headings, preços, variant IDs, bundles, promoções, garantias, reviews, FAQ, imagens, cores e menus vêm de theme settings, blocks, metafields, dados live do produto ou menus. Teste de aceitação: mudar o preço no admin tem de mudar na página.
3. **Tema intocado:** header, announcement bar, footer, navegação, cart drawer e fontes ficam EXATAMENTE como estão; as páginas renderizam dentro do layout normal do tema. Sem `{% layout none %}`, sem header/footer duplicado, sem fontes novas.
4. **Comércio real:** variant switching, preços live, product form nativo, refresh do cart drawer, sticky mobile ATC, quantity rules — sem carrinho falso.
5. **Templates:** homepage e PDP como templates separados; a PDP é atribuída ao produto via `template_suffix`; sem handles/IDs hardcoded.
6. **Responsivo e acessível:** mobile-first, sem overflow 320–430px, alvos de toque ≥44px, safe-area insets, WCAG AA, reduced-motion.
7. **Validação:** Theme Check sem erros, consola limpa; testar desktop/tablet/mobile e reportar honestamente; `python3 ecom-stack/cli/cli.py doctor` antes e depois para confirmar ligação.
8. **Publicação:** tema duplicado publicado só com confirmação explícita do operador (regra 5 do AGENTS.md); após cada publish, re-duplicar o tema (o draft vira MAIN e bloqueia escritas).

## Outputs

- Ficheiros Liquid/JSON criados/modificados listados, com template assignment instructions.
- Relatório de validação (Theme Check, breakpoints, comportamento do cart).
- Tema duplicado com as secções reordenáveis/editáveis no Theme Editor.

## Referências

- `ecom-stack/prompts/loja-completa.md` — PASSO 4 (master prompt, non-negotiables) e checklist pós-publicação.
- `ecom-stack/docs/integracoes-cli.md` — spec aprofundada de secções, schema rules, escrita de ficheiros no tema e verificação (Phases 5–11).
- `ecom-stack/cli/cli.py` — `doctor`, `status`, `brief` (comandos reais).
- `ecom-stack/docs/setup-vps.md` — regra MAIN read-only e duplicação.
- `skills/shopify/shopify-page-cloning.md` — atalho para clonar página de referência completa.
- `skills/clone-link-to-my-shopify.skill` (raiz de `skills/`) — skill profunda de transcrição DOM→Liquid.

## Guardrails

- Nunca escrever no tema MAIN; duplicar primeiro, sempre.
- Nunca publicar sem confirmação explícita do operador.
- Sem valores comerciais hardcoded — tudo editável no admin/Theme Editor.
- Re-duplicar o tema após cada publish (writes ao MAIN são bloqueados pela plataforma).
- Respeitar os guardrails de claims da copy dentro do Liquid (claims suavizados, prova real).
