---
name: homefy-page-build
description: Como construir uma landing page local no Homefy — partir da base ecom-stack/templates/landing-page.html, entregar o artefato HTML+CSS+JS em .aiox/external-runs/<run>/artifacts/ via workflows/executors/hermes-exec.sh, e validar contra os checklists do squad.
---

# Homefy — construção de landing page local

## 1. Base de construção

- Ponto de partida obrigatório: `ecom-stack/templates/landing-page.html` (HTML autocontido com CSS/JS inline e slots `data-slot` nomeados).
- Inputs: `product-brief.md` preenchido (colar no prompt) + 3 referências estruturais (brief secção 4).
- Regras de página: mobile-first 390px, CTA único "Add to Cart", secções na ordem do blueprint, sem menus.

## 2. Execução via executor (AIOX → Hermes)

A construção corre como run one-shot do Hermes. A task AIOX (WHAT/WHEN/WHO) chama o executor; esta skill define o HOW.

```bash
cd /root/homefy
workflows/executors/hermes-exec.sh \
  -t build-landing-<slug> \
  -f squads/ecommerce-growth/tasks/build-landing-page.md \
  -d /root/homefy \
  -T 20
```

- O executor grava artefatos do run em `.aiox/external-runs/<timestamp>-<slug>/` (`prompt.md output.md hermes.log usage.json result.json metadata.json` + `artifacts/`).
- **O artefato entregue (HTML+CSS+JS) vai para `.aiox/external-runs/<run>/artifacts/`** — nome `<slug>-landing.html`. Se o hermes escrever o ficheiro no workdir, o orquestrador/operador move-o para `artifacts/`; o run dir é a fonte de verdade do que foi produzido.
- Verificar o resultado no fim do run:

```bash
cat .aiox/external-runs/<run>/result.json     # status SUCCESS/PARTIAL/FAILED/TIMEOUT/REJECTED
```

- `FAILED`/`TIMEOUT`/`REJECTED` → reportar ao orquestrador com o conteúdo de `hermes.log`; não retryar em laço.

## 3. Preenchimento dos slots

- Substituir os `data-slot` (hero-main, bundle-1/2/3, gift-1/2/3, trust-1..6, scenario-1..6, review-avatar-1/2/3, media-transition, feature-1/2/3, final-bg, thumb-1..6) pelos assets em `ecom-stack/assets/creatives/`.
- Valores comerciais (preço, bundles, garantia) conforme o brief secção 5 — **só valores confirmados**; o resto fica como placeholder editável identificado, nunca inventado.
- Copy conforme as 5 correções (headline resultado 4–8 palavras "you", sem duplos negativos, 1 ideia por secção).

## 4. Validação contra checklists

Antes de entregar, validar a página contra os checklists objetivos do squad:

- `squads/ecommerce-growth/checklists/` — critérios copy/ux/performance (ler os ficheiros do diretório; aplicar cada item passa/falha).
- Mínimos sempre aplicáveis: sem overflow 320–430px, alvos ≥44px, hero <200KB WebP, página <2,5s 4G mobile, safe-area insets, headline = resultado, CTA único com sticky ATC.

## Outputs

- `<slug>-landing.html` em `.aiox/external-runs/<run>/artifacts/`.
- Lista de slots preenchidos vs. pendentes (com motivo).
- Checklist de validação preenchido (passa/falha por critério).

## Guardrails

- Base sempre `ecom-stack/templates/landing-page.html` — não reconstruir página do zero sem justificativa registada.
- Nunca inventar preços/garantias/prazos/stock/claims — placeholder editável ou bloqueado.
- Publicação na loja fora do escopo desta skill (ver `homefy-shopify`); aqui só se entrega o artefato local.
- Respeitar o timeout do executor (`-T`); falha = reporte, não loop de retry.
