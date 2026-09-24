---
name: homefy-page-audit
description: Como auditar uma página/landing page no Homefy — ler o HTML, verificar os critérios objetivos dos checklists copy/ux/performance do squad, e produzir relatório estruturado conforme squads/ecommerce-growth/templates/qa-report.md.
---

# Homefy — auditoria de página

## 1. Obter a página

- Artefato local: ler o ficheiro HTML diretamente (ex.: `.aiox/external-runs/<run>/artifacts/<slug>-landing.html` ou `ecom-stack/templates/landing-page.html` preenchido).
- Página na loja: obter o HTML via `curl -sL --max-time 30 <URL>` (ver skill `homefy-browser-research` para o modo browser e a degradação graciosa).
- Cross-check com o contrato: `ecom-stack/templates/product-brief.md` do produto (desejos, objeções, bundles, guardrails).

## 2. Verificar critérios objetivos

Ler os checklists em `squads/ecommerce-growth/checklists/` e aplicar cada item como passa/falha com evidência (seletor/linha do HTML). Cobertura mínima:

- **Copy:** headline = resultado 4–8 palavras em "you"; sem duplos negativos; cada desejo 1 vez; FAQ responde objeções reais; FOR/NOT-FOR presente; claims suavizados ("designed to help with"); garantia acima do CTA final.
- **UX:** ordem das secções do blueprint; CTA único com sticky ATC; alvos ≥44px; sem overflow 320–430px; bundle selector funcional (radio semantics); accordions acessíveis.
- **Trust/prova:** reviews reais ou "Dramatized customer story"; trust chips; política de envio; consistência de preço/garantia/specs em todas as secções.
- **Performance:** hero <200KB WebP; CSS/JS inline sem dependências externas desnecessárias; metas de <2,5s 4G mobile.

Ferramentas úteis para evidência objetiva:

```bash
rg -n 'data-slot|Add to Cart|guarantee|faq' pagina.html     # localizar elementos
grep -oE '<img[^>]+>' pagina.html | head                    # inspecionar imagens/alt
```

## 3. Relatório estruturado

Produzir o relatório no formato `squads/ecommerce-growth/templates/qa-report.md` (se o template ainda não existir no repositório, usar a estrutura: resumo executivo → achados por categoria copy/ux/performance/trust com severidade → hipóteses priorizadas → veredito). Guardar o relatório em `.aiox/external-runs/<run>/artifacts/` quando a auditoria correr num run do executor.

- Cada achado: critério, evidência (trecho/linha), severidade (bloqueador/alto/médio/baixo), hipótese de correção.
- Veredito final: APROVADO / APROVADO COM RESSALVAS / REPROVADO (bloqueadores listados).
- Nada de achados vagos — todo item passa/falha com evidência no HTML.

## Outputs

- Relatório QA estruturado (formato qa-report) com achados por categoria e severidade.
- Lista de bloqueadores (se houver) que impedem publicação.
- Hipóteses priorizadas para a próxima iteração.

## Guardrails

- Só critérios objetivos verificáveis no HTML — opiniões estéticas não entram no veredito.
- Nunca modificar a página auditada; auditoria é leitura.
- Claims de saúde, prova social inventada e valores comerciais inconsistentes são bloqueadores automáticos.
- Sem acesso à rede além da página auditada; sem scraping de terceiros.
