# Checklist: CRO

> Usado pelo cro-specialist (step audit-cro em page-optimization) e pelo
> qa-specialist. Gating do experimento: hipótese registrada + métrica-alvo
> + baseline antes de qualquer implementação. Fonte de verdade:
> ecom-stack/docs/blueprint-pagina-de-vendas.md (secções 5 e 7).

## Clareza da oferta (teste de 5 segundos)
- [ ] Oferta compreendida em ≤5s: uma pessoa fora do projeto, ao ver a página 5 segundos, diz o que se vende, para quem e por quanto
- [ ] Headline = resultado em linguagem "you"; subheadline apoia a promessa sem repetir a headline
- [ ] Preço, poupança (pill) e garantia visíveis no hero de compra sem scroll

## Fricção removida
- [ ] Zero campos de formulário desnecessários (apenas os exigidos pelo checkout da plataforma)
- [ ] Zero menus, links de rodapé externos ou popups que criem saída do funil antes do CTA final
- [ ] Caminho de compra em ≤3 cliques: bundle → ATC → checkout (verificado com cliques reais a 390px)

## Trust signals
- [ ] Trust chips no hero de compra: envio (com prazo real), garantia, pagamento seguro
- [ ] Box de garantia de risco zero posicionado acima do CTA final, com os dias exatos da política da loja
- [ ] Accordion shipping/returns com prazos reais e consistentes com o que está na loja
- [ ] Trust strip abaixo da dobra com 4–6 ícones (frete, garantia, pagamento seguro, suporte) — sem ícones que prometam o que a loja não cumpre

## Urgência honesta
- [ ] Countdown, stock counters e pills de "BEST SELLER · N+ SOLD" só existem se alimentados por dados reais/verificáveis
- [ ] Nenhuma urgência falsa inventada (sem timers que reiniciam, sem stock fake) — Meta/FTC rejeitam e matam a conta

## Hipótese de teste documentada (gate do experimento)
- [ ] Hipótese escrita no formato "Ao mudar X, espero Y porque Z" — com causa explícita
- [ ] Métrica-alvo nomeada com valor inicial (baseline) e valor meta (ex.: conversão 0,8% → 1,5%)
- [ ] Prazo mínimo de teste definido: ≥3 dias ou significância estatística declarada
- [ ] Critério de paragem pré-registado com os limiares do blueprint secção 7 (mata CTR<1% ao fim do dia 2, CPA>€35 sem compra; escala CPA<€15)
- [ ] Uma variável por iteração: o diff da alteração toca exatamente 1 elemento/fluxo
- [ ] Baseline das métricas registada antes da alteração (print ou export dos dados do período)
