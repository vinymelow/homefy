# Checklist: Performance

> Usado pelo qa-specialist no step audit-page e pelo shopify-engineer no
> step audit-shopify. Metas alinhadas com
> ecom-stack/docs/blueprint-pagina-de-vendas.md (secção 5): hero <200KB
> WebP e página <2,5s em 4G mobile. Medição: Lighthouse em simulação de
> 390px / 4G throttling, pelo menos 2 corridas.

## Imagens e mídia
- [ ] Todas as imagens comprimidas em WebP/AVIF e com dimensões iguais ou superiores ao tamanho exibido (nunca upscale invisível)
- [ ] Hero da página <200KB em WebP
- [ ] Imagens abaixo da dobra com `loading="lazy"` (e a hero com `fetchpriority="high"` ou equivalente)
- [ ] Vídeo de demonstração não bloqueia o carregamento: poster + lazy-load ou play sob interação

## CSS e JavaScript
- [ ] CSS crítico do hero inline ou carregado sem bloqueio; restante CSS diferido
- [ ] Todos os scripts com `defer`/`async` — zero JS síncrono no `<head>`
- [ ] Zero frameworks pesados não usados (jQuery, sliders antigos) no tema
- [ ] Cada app Shopify que carrega JS na PDP está justificado e medido; apps que adicionam >100KB sem função na conversão são removidos

## Core Web Vitals (4G mobile, 390px)
- [ ] LCP ≤2,5s em pelo menos 2 de 3 corridas de Lighthouse
- [ ] CLS <0,1 (todas as imagens e embeds têm width/height ou aspect-ratio reservado)
- [ ] INP <200ms nas interações principais: galeria (swipe/setas), bundle selector, accordions
- [ ] Página total carrega <2,5s em 4G mobile simulado (blueprint secção 5)

## Higiene de renderização
- [ ] Zero fontes web bloqueantes sem `font-display: swap` (ou subset inline do crítico)
- [ ] Zero redirecionamentos em cadeia na página e zero requests 404 no carregamento (verificados na rede)
- [ ] Preconnect/dns-prefetch aos domínios de terceiros realmente usados (CDNs de pagamento, reviews)
