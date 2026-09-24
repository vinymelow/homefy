---
name: ecommerce-research
description: Conduzir pesquisa de mercado e nicho com método evidence-based — shortlist de candidatos a partir de sinais de demanda reais (ad library, reviews, Reddit, trends), scoring 0–100 e gate de validação antes de qualquer investimento em produto.
when_to_use: No início de um ciclo de produto novo, ao escolher nicho/mercado/faixa de preço, ou ao montar a shortlist de candidatos (passagem 1). Não usar para deep dive de um produto já escolhido (ver product-research).
---

# Pesquisa de mercado e nicho — evidence-based

## Quando usar

- Arranque de um ciclo novo: definir nicho, mercado (ex.: US) e faixa de preço (ex.: $29–59).
- Passagem 1 do método: gerar uma shortlist de ~10 candidatos com scores.
- Sempre que a pergunta for "em que vale a pena gastar o próximo orçamento de teste".

## Pré-requisitos

- Nicho, mercado-alvo e faixa de preço definidos pelo operador.
- Acesso às fontes de evidence: Winning Hunter (Landers), Meta Ad Library, TikTok Creative Center, Reddit, Google Trends.
- Tracker aberto em `ecom-stack/research/tracker.md` (tabela de candidatos + scores).

## Procedimento

1. **Aplicar os 4 fundamentos antes de abrir qualquer ferramenta** (detalhe em Referências):
   - Começar pelo problema, não pelo produto: queixas repetidas com palavras exatas dos compradores; identificar o momento em que acontece. Fad = avançar.
   - Procurar prova, não clones: marcas a gastar em anúncios = produto com margem; guardar link + data de cada fonte.
   - Construir um ângulo melhor: **uma pessoa específica + um momento específico** — nunca "para todos".
   - Verificar o dinheiro primeiro: produto + envio + devoluções + taxas → decidir o CPA máximo antes de qualquer anúncio.
2. **Passagem 1 — shortlist de 10 candidatos.** Correr as pesquisas nas fontes acima (filtros do Winning Hunter: loja >$50k/mês e ≤12 meses, 3+ anúncios ativos há 30+ dias, criativos dominantes UGC, preço $25–70 com bundles, solução visual). Para cada candidato registar: problema que resolve (com citações reais), momento de uso, prova de spend, preço dos concorrentes e score 0–100.
3. **Score (5 dimensões × 20 pontos):** sinal de procura, gap de mercado, fornecedor, compliance, prova criativa. Gate: **só passam ≥ 70**; abaixo disso descartar sem mais tempo.
4. **Registar cada candidato no tracker** com link + data de cada evidência — nada de fabricar números.
5. Entregar a shortlist ordenada por score ao operador e aguardar escolha do candidato para a passagem 2 (deep dive — skill `research/product-research`).

## Outputs

- `ecom-stack/research/tracker.md` atualizado (tabela de candidatos + scores + links + datas).
- Shortlist ranqueada com veredito de gate por candidato (≥70 passa / <70 descartado).

## Referências

- `ecom-stack/docs/metodo-pesquisa.md` — método completo (Parte 0 fundamentos, Partes 1–2 shortlist e score).
- `ecom-stack/prompts/pesquisa-produto.md` — filtros exatos do Winning Hunter e prompt de análise.
- `ecom-stack/research/tracker.md` — registo central dos candidatos.
- `skills/research/product-research.md` — passagem 2 (deep dive) do candidato escolhido.

## Guardrails

- Gate rígido: <70 não recebe mais tempo, independentemente de intuição.
- Toda evidência leva link + data no tracker; sem evidência não entra no score.
- Máximo 3 candidatos por semana e 1 em teste de cada vez (orçamento apertado).
- Não copiar marcas: usar as queixas dos concorrentes para construir ângulos próprios.
- Decisões com números (tracker/CPA), nunca com intuição.
