---
name: competitor-research
description: Identificar e dissecar concorrentes diretos — comparar oferta, preço, ângulo criativo e promessa de envio, e extrair os gaps das reviews 1–3★ que serão as objeções e ângulos da nossa página e anúncios.
when_to_use: Antes de definir a oferta e a copy de um produto, ao escolher as 3 referências estruturais da página, ou quando for preciso encontrar o ponto fraco a explorar ("what's the weak point I can beat").
---

# Análise de concorrentes

## Quando usar

- Fase de pesquisa do produto: mapear quem já ganha dinheiro com ele e como.
- Antes de construir a oferta (preço/bundles/garantia) e a copy — os gaps dos concorrentes são o input.
- Ao escolher as 3 referências estruturais (homepage / PDP / hero) do brief, secção 4.

## Pré-requisitos

- Nicho e produto definidos; shortlist ou candidato em validação.
- Acesso ao Winning Hunter (Landers), Meta Ad Library e às lojas concorrentes.
- Ficha vazia `ecom-stack/research/landers/TEMPLATE-lander.md` por concorrente.

## Procedimento

1. **Identificar os concorrentes:** no Winning Hunter Landers filtrar por nicho e ordenar por receita estimada; cruzar com ad library (anúncios ativos há 30+ dias = spend contínuo = lucro). Escolher as 3 lojas principais.
2. **Dissecar cada concorrente** (registar na ficha lander):
   - Oferta: preço, preço riscado, bundles, gifts incluídos, garantia.
   - ângulo criativo dominante e formato (UGC vídeo/imagem, infográfico).
   - Promessa de envio e países-alvo visíveis nos comentários/anúncios.
   - Receita estimada e idade da loja (valida que a página converte).
3. **Ler as reviews 1–3★** de cada loja e extrair as falhas recorrentes: envio lento, qualidade, ângulo não explorado, objeção sem resposta na página.
4. **Comparar lado a lado** (oferta/preço/ângulo/envio) e formular o gap explorável: "reviews 1–3★ do concorrente X queixam-se de Y — os nossos ads e a página respondem exatamente a isso".
5. **Escolher as 3 referências estruturais** (nunca de conteúdo) para o brief secção 4: homepage da melhor estrutura, melhor PDP, melhor hero de compra — cada uma com URL e "o que vou copiar" (estrutura, movimento, ritmo).

## Outputs

- 3 fichas `research/landers/<concorrente>-lander.md` preenchidas (uma por concorrente principal).
- Tabela comparativa oferta/preço/ângulo/envio.
- Lista de gaps priorizados → alimenta objeções do brief (secção 3) e ângulos de ads.
- As 3 referências estruturais registadas no brief (secção 4) com receita estimada da loja alvo.

## Referências

- `ecom-stack/prompts/pesquisa-produto.md` — prompt "análise do concorrente" com as 4 perguntas (porque ganha / ponto fraco / margem / TEST-SKIP).
- `ecom-stack/templates/product-brief.md` — secção 4 (referências escolhidas) e secção 3 (objeções).
- `ecom-stack/docs/metodo-pesquisa.md` — Parte 0 (prova, não clones) e Parte 4 (Winning Hunter como acelerador).
- `ecom-stack/docs/blueprint-pagina-de-vendas.md` — secção 1 (critérios de referência: receita visível, mobile-first, roubar estrutura de qualquer nicho).

## Guardrails

- Referência = estrutura e movimento. **Nunca** copiar logo, imagens, copy, reviews, claims ou código.
- Nunca inventar preços, garantias, prazos, stock ou endorsements do concorrente — o que não for verificado fica como nota, não como afirmação.
- Guardar link + data de cada evidência (tracker/ficha).
- Não atacar marcas por nome em comparações públicas; atacar mecanismos/queixas ("nós vs outros" sem nomes).
