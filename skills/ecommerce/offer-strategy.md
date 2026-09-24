---
name: offer-strategy
description: Construir a oferta comercial de um produto — bundle selector de 3 cards, painel de oferta grátis (só itens reais), garantia e risk reversal — ligada a produtos/variantes reais da loja e coerente em todos os frames e secções.
when_to_use: Ao preencher a secção 5 do product brief, ao desenhar o hero de compra (bundle selector + gift panel + garantia), ou sempre que preço/desconto/garantia entrarem numa página, anúncio ou criativo.
---

# Estratégia de oferta — bundles, grátis e risk reversal

## Quando usar

- Fase de oferta do ciclo: transformar um produto validado numa oferta que sobrevive ao teste de €20–50/dia.
- Preenchimento do brief (secção 5) antes de pedir landing page ou criativos.
- Qualquer revisão de preço/bundle/garantia numa página existente.

## Pré-requisitos

- Produto validado (veredito GREEN em `skills/research/product-research.md`).
- Produto e variantes já existentes na loja Shopify (URL do produto obrigatória no brief secção 1 — tem de existir antes do Liquid).
- Margem e CPA máximo calculados no tracker (ex.: AOV $69, margem $39 → CPA máx ~$20).
- Política real da loja: garantia/devoluções e prazo de entrega prometido.

## Procedimento

1. **Definir os 3 bundles** (ligados a variantes reais do Shopify):
   - Bundle 1 — 1 unidade: preço / preço riscado.
   - Bundle 2 — mais popular: preço / preço riscado.
   - Bundle 3 — melhor valor: preço / preço riscado.
   - Verificar que a estrutura deixa margem >15% após produto+envio no bundle âncora.
2. **Painel de oferta grátis:** listar o que está incluído em cada bundle (gift-1/2/3) — **só se REAL**. Se não houver gifts reais, o painel fica escondido (nunca renderizar slots vazios). Valor riscado só com base confirmada.
3. **Garantia e risk reversal:** escolher a garantia (dias) de acordo com a política real da loja; posicioná-la como linha de garantia junto ao botão e como box de risco zero acima do CTA final. Risk reversal só funciona se a promessa for honrável.
4. **Âncora de preço:** preço riscado + pill de poupança no hero de compra; desconto coerente com o anúncio que trouxe o tráfego.
5. **Passagem de consistência:** garantir que preço, desconto, gifts e garantia são idênticos no hero, na oferta final, em todos os frames de criativo e no FAQ — qualquer divergência mata a confiança (e a conta de anúncios).
6. Registar tudo no brief secção 5 e nas secções 1 (preços) e 7 (guardrails confirmados).

## Outputs

- Brief secção 5 preenchida: 3 bundles com preços, painel grátis (ou decisão de o esconder), garantia em dias.
- Valores de oferta prontos a consumir pela landing page (bundle selector + gift panel) e pelos criativos (frame de oferta por último).

## Referências

- `ecom-stack/templates/product-brief.md` — secção 5 (oferta e bundles), secção 1 (dados base), secção 7 (guardrails de claims).
- `ecom-stack/docs/blueprint-pagina-de-vendas.md` — secção 3 (spec do hero de compra: bundle selector, painel grátis, linha de garantia) e secção 5 (consistência).
- `ecom-stack/docs/metodo-pesquisa.md` — Parte 0 (CPA máximo e dinheiro primeiro).
- `ecom-stack/templates/landing-page.html` — slots `bundle-1/2/3` e `gift-1/2/3` onde a oferta é renderizada.

## Guardrails

- **Nunca inventar gifts** — o painel grátis só existe com itens realmente incluídos; caso contrário esconder.
- Nenhum preço/desconto/prazo/garantia sem confirmação na loja ou no fornecedor (brief secção 7).
- Garantia tem de bater certo com a política da loja em TODOS os frames e secções.
- Sem countdown/stock falsos — urgência só com base real.
- Deploy/publicação da oferta só com confirmação explícita do operador (regra 5 do AGENTS.md).
