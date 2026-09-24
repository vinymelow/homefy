# Prompts — Pesquisa e validação de produtos (Winning Hunter)

> Método completo (fundamentos, scoring 0–100, gate ≥70, passagens 1–2):
> **docs/metodo-pesquisa.md**. Tracker dos candidatos: **research/tracker.md**.

## 0. Passagem 2 — deep dive (colar na IA com o produto escolhido do tracker)

```
Passagem 2 — deep dive no produto: [NOME]
1. Reviews 1–3★ das 3 lojas concorrentes principais: 5 queixas mais frequentes
   com citações — cada uma é um ângulo de ad ou objeção da landing page.
2. Economia: custo $[X] + envio $[Y], AOV $[Z] → margem e CPA máximo.
   Sobrevive a €20–50/dia de teste?
3. Veredito GREEN / AMBER / RED: o que gostas, o que não gostas, riscos.
   Se não recomendares, diz "não anunciava".
```

## 1. Filtros no Winning Hunter (Landers)

- Niche: Home & Kitchen / Beauty (ou o nicho ativo do momento)
- Ordenar por: revenue estimado (maior primeiro)
- Sinais de produto vencedor para copiar:
  - Loja com receita estimada > $50k/mês e ≤ 12 meses de idade
  - 3+ anúncios ativos no ad library há mais de 30 dias (spend contínuo = lucro)
  - Criativos majoritariamente UGC (imagem/vídeo amador) = produto impulsionado por
    conteúdo, não por marca
  - Preço de venda $25–70 com bundle (margem para ads)
  - Solução visual (o produto "mostra" o benefício em 2 segundos)

## 2. Análise do concorrente (colar na IA com os dados do Winning Hunter)

```
I'm evaluating a dropshipping product to test. Here's the competitor data:

- Product: [NOME]
- Store: [URL] — est. revenue: $[X]/month, store age: [Y] months
- Ad library: [N] active ads, running since [DATA], main format: [video/image]
- Top creative angle: [DESCREVER]
- Price: $[X], offer: [BUNDLE/DESCONTO]
- Shipping promise: [X] days
- Target countries visible in comments/ads: [US/CA/AU/NZ/UK...]

Answer:
1. Why is this product winning? (hook, audience pain, offer)
2. What's the weak point I can beat? (page, shipping, offer, creative freshness)
3. Estimated margin at $[CUSTO] product cost + $[ENVIO]: can it survive
   €20–50/day testing at $25–70 AOV?
4. Verdict: TEST / SKIP, in one sentence.
```

## 3. Registo — usar templates/
- Cada candidato → `research/landers/TEMPLATE-lander.md` preenchido
- Candidatos aprovados → `templates/product-brief.md` preenchido
- Máximo 3 candidatos por semana; 1 em teste de cada vez (orçamento apertado)
