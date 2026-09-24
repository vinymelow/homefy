# Checklist: Shopify

> Usado pelo shopify-engineer (step audit-shopify em product-to-launch) e
> revalidado pelo qa-specialist. Fonte de verdade:
> ecom-stack/docs/blueprint-pagina-de-vendas.md (secção 6 — fluxo de
> construção) e AGENTS.md (regras críticas). Tema duplicado, nunca o live.

## Liquid e estrutura do tema
- [ ] `theme-check` (Shopify CLI) executado no tema sem erros de sintaxe Liquid
- [ ] Todas as secções novas têm schema JSON válido (parses sem erro no theme editor)
- [ ] Blocos reutilizáveis estão em snippets identificados (sem duplicação de markup entre secções)
- [ ] Zero conteúdo hard-coded no Liquid: texto/imagens editáveis via theme editor, metafields ou metaobjects
- [ ] Header, footer e fontes do tema estão intocados (diff confirma que não foram modificados)

## Dados e produto
- [ ] A URL do produto (secção 1 do Product Brief) existe na loja e o produto está publicado antes da conversão Liquid
- [ ] Metafields usados para specs/FAQ/bundles com namespaces e tipos validados na Admin API (nomes sem typos)
- [ ] Preços, preços riscados e garantia são lidos do produto/políticas da loja — a loja é a fonte única de verdade
- [ ] Bundle selector ligado a variantes/produtos reais do Shopify (IDs verificados), não a valores digitados à mão
- [ ] Painel de oferta grátis escondido quando não há items incluídos reais (nunca mostrar slots vazios)

## Responsivo e mídia
- [ ] Breakpoints testados no tema de pré-visualização: 390px, 768px, 1024px, 1440px
- [ ] Imagens servidas via Files/CDN da loja com dimensões apropriadas por breakpoint (srcset quando aplicável)
- [ ] Hero da galeria comprimido em WebP <200KB (blueprint secção 5)
- [ ] Vídeos de demonstração com poster e sem autoplay com som (política de browsers respeitada)

## Segurança (bloqueio imediato se falhar)
- [ ] Grep no diff do tema: zero tokens, senhas, chaves de API ou valores de .env hard-coded em Liquid/JS/CSS
- [ ] Zero scripts de terceiros injetados sem registo (cada script listado no relatório com origem e justificação)
- [ ] Todas as alterações testadas em tema duplicado de pré-visualização; nada publicado no tema live sem aprovação humana
- [ ] Credenciais de acesso (SHOPIFY_ADMIN_API_TOKEN etc.) lidas apenas de ecom-stack/config/.env, fora do repositório git
