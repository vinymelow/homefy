# Checklist: UX

> Usado pelo qa-specialist no step audit-page. Fonte de verdade:
> ecom-stack/docs/blueprint-pagina-de-vendas.md (secções 2 e 3). Inspeção
> obrigatória a 390px (mobile primeiro — 80–90% do tráfego pago é mobile)
> e validação 320→1440px sem overflow.

## Hierarquia visual e estrutura
- [ ] A ordem das secções abaixo da dobra segue o blueprint: announcement bar → trust strip → media transition → how it works → feature cards → spec hero → story → usage scenarios → reviews → trust/press → comparison → value stats → brand story → FAQ → garantia → CTA final
- [ ] O hero de compra tem 2 colunas no desktop (~49% galeria / ~51% compra) com galeria `position: sticky`, e 1 coluna no mobile com a galeria primeiro
- [ ] Cada secção comunica 1 ideia; o ritmo claro/escuro alterna conforme a referência copiada
- [ ] Headlines de secção têm 4–8 palavras e texto sobre imagem tem painel sólido atrás (legível a braço de distância)

## Mobile-first (390px)
- [ ] CTA de compra visível sem scroll no mobile (botão ATC do hero ou sticky bar na primeira viewport)
- [ ] Sticky mobile ATC aparece quando o botão principal sai do viewport e desaparece quando ele regressa
- [ ] Zero overflow horizontal em 320px, 390px, 768px, 1024px e 1440px (scrollWidth ≤ clientWidth em todos)
- [ ] Todos os alvos de toque (botões, setas de galeria, cards de bundle, accordions) têm ≥44px de altura/largura
- [ ] Safe-area insets respeitados (viewport-fit=cover + padding env(safe-area-inset-*)) em dispositivos com notch

## Galeria e media
- [ ] Galeria: media principal ~1:1, setas circulares, thumbnails no desktop, swipe + dots no mobile, crossfade de 220–300ms
- [ ] O hero (frame 1) funciona sozinho como thumbnail: produto real em uso + painel translúcido com 4–5 benefícios
- [ ] Todas as imagens têm atributo alt descritivo; vídeos têm poster e legenda ou texto alternativo equivalente
- [ ] Imagens de lifestyle hiper-realistas seguem as 5 chaves do método (pele, câmara nomeada, luz, imperfeição, ambiente)

## Legibilidade
- [ ] Tamanho base do corpo de texto ≥16px em mobile
- [ ] Contraste ≥4.5:1 para texto normal e ≥3:1 para texto grande (verificado contra as cores do tema, secção 8 do brief)
- [ ] 1 ideia por imagem de galeria; safe zone do carousel respeitada (terço do meio livre nas bordas)

## Conversão (caminho de compra)
- [ ] Compra em ≤3 cliques a partir do hero: selecionar bundle → ADD TO CART → checkout
- [ ] Bundle selector com 3 cards (1 un. / popular / melhor valor), card inteiro clicável, semântica de radio, estado selecionado com borda de marca visível
- [ ] Página sem menus de navegação nem links externos que diluam o funil (1 objetivo por página)
- [ ] Accordion de compra completo: package, shipping/returns, warranty, payment, specs
- [ ] O CTA final faz scroll suave até ao ponto de compra (âncora funcional, testada por clique)
