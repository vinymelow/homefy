# Método de pesquisa de produtos — evidence-based (adaptado do tutor)

O princípio central: **não é o produto que vence — é o problema que ele resolve.**
O produto é a peça de ligação. Pesquisamos prova (evidence), não clones.

---

## Parte 0 — Os 4 fundamentos (antes de abrir qualquer ferramenta)

1. **Começa pelo problema, não pelo produto.** Procura um problema de que as pessoas
   se queixam **repetidamente** (reviews, comentários, Reddit). Copia as palavras
   exatas dos compradores — a tua copy e os teus ads vão falar como eles.
   Encontra **o momento em que acontece** (acordar com dores, preparar o jantar) —
   é essa cena que o criativo vai mostrar. Fad? Avança para o próximo.
2. **Procura prova, não clones.** Marcas a gastar em anúncios = produto com margem.
   Lê as reviews e comentários dos concorrentes para ver as **objeções reais**.
   Guarda link + data de cada fonte. Não copies a marca: encontra as queixas dela
   e faz ads que resolvam exatamente essas falhas — os teus ads ficam melhores que
   os do original.
3. **Constrói um ângulo melhor.** Pergunta: quem mais tem o mesmo problema? Muda o
   **momento do cliente** (mãe de manhã vs. estudante à noite) para abrir um público
   novo. Mantém a função factual do produto — a mensagem fica honesta.
   Regra: **uma pessoa específica + um momento específico** (nunca "para todos").
4. **Verifica o dinheiro primeiro.** Antes de qualquer anúncio: produto + envio +
   devoluções + taxas. Decide o **CPA máximo** (ex.: AOV $69, margem $39 → CPA máx
   ~$20). Depois decide com tracker/números, nunca com intuição.

## Parte 1 — Passagem 1: shortlist de candidatos (10 produtos)

Ferramentas de evidence: **Winning Hunter** (Landers: receita estimada, anúncios
ativos, criativos dominantes), **Meta Ad Library**, **TikTok Creative Center**,
**Reddit**, **Google Trends**.

> No nosso fluxo, esta passagem faz-se **aqui no chat comigo**: eu corro as
> pesquisas (ad library, reviews, trends) e entrego a shortlist com scores.
> O teu papel na passagem 1: definir **nicho**, **mercado** (ex.: US) e
> **faixa de preço** (ex.: $29–59), e validar no Winning Hunter as lojas que eu
> indicar (receita, idade, criativos).

Pedido tipo (colar no chat):

```
Passagem 1 de pesquisa — método evidence-based:
- Nicho: [beleza / casa-utilidades]
- Mercado: US
- Faixa de preço: $29–59
Encontra 10 candidatos. Para cada um: problema que resolve (com citações reais de
reviews/comentários), momento de uso, prova de spend (ads ativas há 30+ dias),
preço dos concorrentes, e um score 0–100 (5 dimensões × 20: procura, gap de
mercado, fornecedor, compliance, prova criativa). Gate: só continuo com ≥70.
```

Resultado regista-se em `research/tracker.md` (tabela dos candidatos + scores).

## Parte 2 — O score (gate ≥70/100)

| Dimensão (0–20) | O que pontua |
|---|---|
| Sinal de procura | Queixas recorrentes com palavras fortes; múltiplas marcas a gastar há 30+ dias |
| Gap de mercado | Reviews 1–3★ dos concorrentes com falhas claras que consegues resolver (envio, qualidade, ângulo) |
| Fornecedor | Custo + envio 5–15 dias viáveis (USA Drop/CJ/Zendrop/AliExpress), política de refunds |
| Compliance | Sem claims de saúde proibidos, sem marcas registadas, nicho sem restrições de anúncio |
| Prova criativa | Produto "mostra" o benefício em 2 segundos; cena UGC filmável no momento real |

- **≥ 70** → passa à passagem 2 (deep dive). **< 70** → descartar, sem mais tempo.
- Guardar sempre **link + data** de cada evidência (no tracker) — nada de fabricar.

## Parte 3 — Passagem 2: deep dive no candidato escolhido

Um produto de cada vez. Prompt tipo:

```
Passagem 2 — deep dive no produto: [NOME]
1. Lê as reviews 1–3★ das 3 lojas concorrentes principais: lista as 5 queixas mais
   frequentes (com citações) — cada uma é um ângulo de ad ou uma objeção a
   responder na landing page.
2. Economia: com custo estimado $[X] + envio $[Y] e AOV $[Z], calcula margem e
   CPA máximo. Sobrevive a €20–50/dia de teste?
3. Veredito GREEN / AMBER / RED com razões: o que gostas, o que não gostas, riscos.
   Se não recomendares, diz claramente "não anunciava".
```

- **GREEN** → preencher `templates/product-brief.md` (com as secções 1b/1c) e
  seguir para a landing page.
- **AMBER/RED** → voltar ao tracker, escolher o próximo candidato ≥70.
- Conta gastar **2–4 passagens 2** até ao primeiro GREEN — é o método a proteger-te
  de produtos maus, não falha tua.

## Parte 4 — Winning Hunter como acelerador

Filtros concretos (detalhe em `prompts/pesquisa-produto.md`):
- Landers → nicho → ordenar por receita: loja >$50k/mês com ≤12 meses
- 3+ anúncios ativos há 30+ dias; criativos UGC dominantes
- Preço $25–70 com bundles (margem para ads)

## Mapeamento tutor → ecom-stack

| Tutor (vídeo) | Nós |
|---|---|
| Claude co-work + skill "ecom product evidence research" | Pesquisa feita aqui no chat comigo (web search + browser) |
| Chrome extension para Reddit/Amazon/ad library | Ferramentas de browser próprias — mesma cobertura |
| Google Sheet "product validator tracker" | `research/tracker.md` (markdown, no projeto) |
| Prompts 2 e 3 do cheat sheet | Passagem 2 (Parte 3 deste doc) |
| USA Drop | Fornecedor à tua escolha (registar custo/envio no tracker) |
