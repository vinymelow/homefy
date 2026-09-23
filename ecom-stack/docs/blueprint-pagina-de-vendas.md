# Blueprint — Página de Vendas de Produto (método The Ecom King + kit do tutor)

> Síntese do vídeo "$390K/Month With Claude AI Dropshipping" + guia passo-a-passo do
> tutor (docs/tutor/) + skills de criativos. Especificação que a Kimi Code segue
> para construir cada página. Prompts prontos em `prompts/`.

## 1. Filosofia central

**Não se constrói uma página copiando UMA loja inteira.** Junta-se o melhor de TRÊS
referências diferentes (caso concreto do tutor — Flovir, loja a ~$100K/mês):

| Componente | Referência do tutor | De onde vem |
|---|---|---|
| Homepage | uk.pulsetto.tech | Estrutura, movimento, ritmo das secções |
| PDP (página de produto) | pettichat.com | Ordem das secções, sistema de compra |
| Hero da PDP | nordicstretch.com (screenshot) | Galeria + bundle selector + painel de oferta |

Critérios para escolher referências no Winning Hunter (Landers):
1. **Receita estimada visível** — a página não só tem de ser bonita, tem de gerar dinheiro.
2. **Filtro por nicho** — mas podes roubar estrutura de qualquer nicho.
3. **Mobile primeiro** — inspeciona sempre a 390px (80–90% do tráfego pago é mobile).
4. **Referência = estrutura e movimento. NUNCA** logo, imagens, copy, reviews, claims
   ou código. O que não for verificado vira placeholder editável — nunca inventar
   preços, garantias, prazos, stock ou endorsements.

## 2. Sistema visual

Uma **galeria em sequência de persuasão**, não fotos soltas (método EcomAlchemist,
detalhe em docs/metodo-criativos.md):
- **Hero (frame 1)** — produto REAL em uso + painel translúcido com stack de 4–5
  benefícios. Tem de funcionar sozinho como thumbnail.
- **Recognition** (só produtos high-consideration) — 1–2 avatares que se reconhecem
  no problema nas primeiras 3 trocas de imagem.
- **Payoffs** — 1 imagem por desejo ranqueado (espelha os recognition frames).
- **Mechanism** — cutaway/glow que torna visível o benefício invisível.
- **How-to (1-2-3)**, **vs alternativa**, **prova social**, **oferta por último**
  (garantia em baixo, depois de já o quererem).
- Regras de texto: 1 ideia por imagem, headline 4–8 palavras, safe zone do carousel
  (terço do meio livre nas bordas), painel sólido atrás do texto, legível a braço
  de distância. Produto real recortado (rembg), nunca regenerado por IA.

## 3. Estrutura da PDP (ordem das secções)

### Hero de compra (o mais crítico — spec da referência nordicstretch)
- **2 colunas no desktop** (~49% galeria / ~51% compra), galeria com
  `position: sticky`; **1 coluna no mobile**, galeria primeiro.
- Galeria: media principal ~1:1, setas circulares, thumbnails no desktop,
  swipe + dots no mobile, crossfade 220–300ms, badge opcional (só se verificado).
- Coluna de compra: título (bold/uppercase) → rating real → preço + riscado +
  pill de poupança → **bundle selector: 3 cards** (1 un. / popular / melhor valor),
  card inteiro clicável, radio semantics, estado selecionado com borda de marca →
  **painel de oferta grátis** (pale, gift icon, "INCLUDED WITH THIS PURCHASE",
  3 slots de items incluídos — SÓ se realmente incluídos; esconder se não) →
  botão ADD TO CART · [preço] (full width, ~56px, dark) → linha de garantia →
  **trust chips** (envio / garantia) → introdução com 4 bullets de benefício →
  **accordions** (package, shipping/returns, warranty, payment, specs).
- **Sticky mobile ATC** aparece quando o botão principal sai do viewport.

### Abaixo da dobra (ritmo da referência pettichat/pulsetto)
1. Barra de anúncio no topo da página (oferta + prazo)
2. **Trust strip** — 4–6 ícones em row (frete, garantia, pagamento seguro, etc.)
3. **Media transition** — momento cinematográfico escuro (vídeo de demonstração)
4. **How it works** — 3 passos numerados, labels de 2 palavras
5. **Feature cards** — 3 cartões editoriais (imagem/vídeo + tag + headline)
6. **Specification hero** — secção escura imersiva com 4 spec points
7. **Story/engineering** — split media/copy, casos de uso
8. **Usage scenarios** — 6 cartões de contexto (grid desktop, scroll-snap mobile)
9. **Reviews** — cards com foto, rating, "Verified Buyer" (reviews reais ou nada)
10. **Trust/press marquee** — marcas/certificações verificadas ou trust marks
11. **Comparison** — "nós vs outros" (✓ verde / ✗ vermelho, sem nomes de marcas)
12. **Value statistics** — 2–3 cards de estatística com disclaimers editáveis
13. **Brand story** — split com mídia, sem inventar fundadores nem citações
14. **FAQ** — 5–10 perguntas que respondem objeções reais (accordion acessível)
15. **Garantia** — box de risco zero acima do CTA final
16. **CTA final** — imagem full-bleed + overlay + botão que faz scroll ao formulário
17. Footer do tema (intocado)

### Módulos branded opcionais (ativar quando o produto escalar)
Press bar "AS SEEN IN" · donuts de resultado (94/87/98%) · carrossel de reviews em
vídeo · pill "BEST SELLER · 10,000+ SOLD" · countdown + "Only X left in stock" ·
5-step ritual timeline. Fonte: docs/tutor/branded-shopify-store-builder.md.

## 4. Regras de copy (as 5 correções — passa/falha em cada frame e secção)

1. **Headline = RESULTADO em linguagem "you"**, 4–8 palavras — não problema, não
   feature. O problema aparece UMA vez (hero/recognition).
2. **Sem duplos negativos** — "clear head", não "no pills to fog your head".
3. **Sem repetição** — cada deseço aparece exatamente 1 vez.
4. **Confiança + diferenciação** — o conjunto responde "porquê tu" e cruza as
   objeções principais.
5. **Trust + honesty** — FOR/NOT-FOR, hedge em claims reversíveis, garantia em
   cima do CTA final. Título da página = benefício, não nome genérico.

## 5. Guardrails (o que mata a conta de anúncios e a loja)

- Nada de claims de cura/tratamento — "designed to help with" (Meta/FTC rejeitam).
- Reviews reais da loja OU "Dramatized customer story"; contagem de reviews só se
  real (se do fornecedor, atribuir à fonte).
- Sem logos de imprensa, prémios ou endorsements inventados.
- Specs/preços/garantia iguais em TODOS os frames e secções (passagem de
  consistência obrigatória antes de publicar).
- Uma página por produto, mobile-first, **um só CTA**, sem menus.
- Hero comprimido (<200KB WebP), página <2,5s em 4G mobile.

## 6. Fluxo de construção

1. **Pesquisa** — Winning Hunter Landers + ad library → 3 referências +
   3–6 frames de ads vencedores → `research/landers/`
2. **Brief** — `templates/product-brief.md` (avatars, desejos ranqueados, objeções,
   bundles reais, kit de marca, guardrails)
3. **Página** — página única: `prompts/pagina-vendas.md` · loja completa:
   `prompts/loja-completa.md` (cadeia do tutor)
4. **Validação** — 320→1440px, sem overflow, alvos ≥44px, safe-area
5. **Produto na loja primeiro** (senão o agente falha na conversão)
6. **Conversão para Liquid** — tema duplicado, secções com schema, nada
   hard-coded, header/footer/fonts intocados (master prompt em loja-completa.md)
7. **Criativos** — SOP em docs/metodo-criativos.md
8. **Subir assets** — substituir slots no theme editor
9. **Copy final** — título, descrição curta, FAQ

## 7. Métricas de validação (teste de 3 dias, €20–50/dia)

| Métrica | Mata o produto | Continua testando | Escala |
|---|---|---|---|
| CTR do anúncio | < 1% | 1–2% | > 2% |
| CPC | > €1,20 | €0,40–1,20 | < €0,40 |
| Conversão da página | < 0,8% | 0,8–1,5% | > 1,5% |
| CPA | > €35 | €15–35 | < €15 |
| Margem após produto+envio | — | > 15% | > 25% |

Regra: 3 dias de teste = decisão. Sem paixão por produto — dados decidem.
