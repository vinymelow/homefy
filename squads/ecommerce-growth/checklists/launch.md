# Checklist: Launch

> Usado pelo qa-specialist no step final-qa (workflow product-to-launch) e
> pelo operador humano no step publish (manual_approval). Sem verdict PASS
> neste checklist não há pedido de aprovação de publicação. Fonte de
> verdade: ecom-stack/docs/blueprint-pagina-de-vendas.md (secção 7),
> ecom-stack/cli/cli.py (anuncio plano) e AGENTS.md (regra 5).

## QA completo
- [ ] QA PASS registado nos 5 checklists anteriores: copy.md, ux.md, shopify.md, performance.md, cro.md
- [ ] qa-report e final-qa-report preenchidos com verdict PASS e arquivados em ecom-stack/research/landers/<slug>-*-qa-report.md
- [ ] Todas as issues de severidade CRITICAL e HIGH dos relatórios estão resolvidas (zero pendentes)

## Loja conferida (dados reais, não do brief)
- [ ] Preços e preços riscados na página batem certo com os produtos publicados na loja Shopify
- [ ] Estoque disponível confirmado com o fornecedor e suficiente para o plano de teste (mín. 3 dias de vendas projetadas)
- [ ] Prazo de entrega prometido na página é igual ao configurado na loja e exequível pelo fornecedor
- [ ] Políticas de garantia, devolução e envio publicadas na loja e idênticas às mencionadas na página

## Tracking presente e testado
- [ ] Pixel com evento Purchase testado end-to-end (evento recebido no gerenciador de eventos, com valor e moeda corretos)
- [ ] CAPI ativo com deduplicação de eventos validada (eventID único por compra, sem duplicar conversões)
- [ ] ViewContent, AddToCart e InitiateCheckout disparando na página de teste
- [ ] ecom-stack/config/.env com as chaves da plataforma preenchidas (valores nunca expostos em artefatos nem no tema)

## Plano de teste definido
- [ ] Plano impresso e anexado ao launch-report: `python3 ecom-stack/cli/cli.py anuncio plano <slug>`
- [ ] Orçamento definido: €20–50/dia × 3 dias (máx. €150) conforme blueprint secção 7
- [ ] Países definidos: US, CA, AU, NZ, UK — UK separado num adset próprio (CPMs diferentes)
- [ ] Criativos prontos e aprovados: 2–3 vídeos 9:16 (formatos A/B/C) + 3 static ads conforme creative-brief
- [ ] Métricas de decisão registadas: mata (CTR<1% ao fim do dia 2 ou CPA>€35 sem compra), escala (CPA<€15 → +20%/dia)

## Aprovação humana (gate final — bloqueio intransponível)
- [ ] Aprovação humana explícita registada: nome do operador, data/hora e decisão GO por escrito
- [ ] Publicação executada apenas após o step publish (manual_approval, blocked_by_default) — nenhuma publicação automática existe
- [ ] Campanha/tema publicado manualmente pelo operador; o workflow não executa nenhum comando de publicação

## Rollback plan
- [ ] Tema live anterior identificado pelo nome/ID e restauro testado em tema duplicado (tempo medido ≤30 min)
- [ ] Plano de rollback escrito: quem executa, em que condições (quais métricas disparam) e os passos exatos
- [ ] Campanhas de anúncio podem ser pausadas em ≤10 min (acesso à plataforma confirmado antes do lançamento)
- [ ] Regra de paragem acordada: dados de 3 dias decidem — sem paixão por produto, sem exceções
