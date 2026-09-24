# Launch Report — [SLUG DO PRODUTO] — [data]

> Relatório de lançamento — output da task `prepare-launch`.
> REGRA DO SQUAD: `publish_requires_human_approval: true` (squad.yaml) — NADA é
> publicado sem confirmação explícita do operador (deploy Shopify, Meta, TikTok).
> Assets e campanhas ficam em status PREPARED até essa aprovação.
> Plano de teste alinhado com: `python3 ecom-stack/cli/cli.py anuncio plano <slug>`.

## 1. Status do lançamento
- [ ] PREPARING — artefacts em produção
- [ ] PREPARED — tudo pronto, à espera de aprovação humana
- [ ] APROVADO HUMANAMENTE — publicação autorizada em <data> por <operador>
- [ ] LIVE — campanha ativa (registar data/hora)
- [ ] ENCERRADO — teste concluído (resultado no secção 8)

## 2. Pré-condições (gate de lançamento)
- [ ] **QA PASS** — `templates/qa-report.md` com veredito APROVADO (ou COM
  RESSALVAS corrigidas) assinado por qa-specialist
- [ ] **Tracking OK** — Pixel Meta + CAPI a disparar Purchase/AddToCart
  (teste de compra com Shopify Bogus Gateway antes de lançar)
- [ ] **Aprovação humana registada** — nome + data do operador neste relatório
- [ ] Produto publicado no Shopify (rascunho → ativo) com imagens reais
- [ ] Tema duplicado publicado (MAIN intacto; secções editáveis no Theme Editor)
- [ ] Guardrails de claims da passagem de consistência sem BLOCKED em aberto

## 3. Plano de teste (alinhado ao `anuncio plano`)
- **Orçamento**: €20–50/dia × 3 dias (máx €150)
- **Plataforma**: TikTok Ads + Meta Ads (Advantage+ shopping ou CBO 3 adsets)
- **Países**: US, CA, AU, NZ, UK — UK separado num adset (CPMs diferentes)
- **Criativos**: 2–3 vídeos 9:16 (formatos A/B/C de `ecom-stack/prompts/criativos.md`)
  + static ads conforme `templates/creative-brief.md`
- **Evento de conversão**: Purchase
- **Regra de decisão (3 dias = decisão, dados decidem)**:
  | Métrica | Mata o produto | Continua testando | Escala |
  |---|---|---|---|
  | CTR do anúncio | < 1% | 1–2% | > 2% |
  | CPC | > €1,20 | €0,40–1,20 | < €0,40 |
  | Conversão da página | < 0,8% | 0,8–1,5% | > 1,5% |
  | CPA | > €35 | €15–35 | < €15 |
  | Margem após produto+envio | — | > 15% | > 25% |
  - Mata se: CTR < 1% ao fim do dia 2, ou CPA > €35 sem compra
  - Escala se: CPA < €15 → +20% orçamento/dia; CPA €15–35 → testar 2 criativos novos
  - Métricas completas: `ecom-stack/docs/blueprint-pagina-de-vendas.md` — Métricas
    de validação

## 4. Assets publicados (status PREPARED — não publicar ainda)
| Asset | Slot | Ficheiro | Estado | Aprovado por |
|---|---|---|---|---|
| Landing page | página | | PREPARED | |
| Vídeo ad | ugc-video | | PREPARED | |
| Static ads | static-ads-1/2/3 | | PREPARED | |
| Galeria PDP | hero-main, payoff-*, … | | PREPARED | |
| Campanha Meta | — | | PREPARED | |
| Campanha TikTok | — | | PREPARED | |

## 5. Riscos
| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Claims rejeitados pela plataforma (saúde/beleza) | | | Suavizar ("designed to help with"); revisão de claims obrigatória |
| CPA > €35 sem compras | | | Kill ao fim do dia 2–3; orçamento máx €150 |
| Fornecedor: prazo/qualidade | | | Verificar política de refunds antes do teste |
| Pixel/CAPI sem eventos | | | Bogus Gateway test antes de LIVE |

## 6. Rollback plan
1. Pausar campanhas (Meta/TikTok Ads Manager)
2. Reverter tema duplicado para o estado anterior (ou despublicar o tema duplicado)
3. Produto para rascunho no Shopify (se necessário)
4. Registar no `ecom-stack/research/tracker.md` a decisão + aprendizagem
5. Seguinte: voltar à shortlist (método: `ecom-stack/docs/metodo-pesquisa.md`)

## 7. Próximos passos
- [ ] Obter aprovação humana (operador) sobre esta secção completa
- [ ] Publicar tema/produto após aprovação
- [ ] Ativar campanhas com o plano da secção 3
- [ ] Ler métricas ao fim do dia 2 e do dia 3 → decisão (kill/scale)
- [ ] Se GREEN: workflow `page-optimization` (task `audit-cro`)

## 8. Resultado (preencher ao encerrar)
- Datas do teste: 
- CTR:  | CPC:  | Conversão:  | CPA:  | Margem: 
- Decisão final: [ ] ESCALAR  [ ] TESTAR CRIATIVOS NOVOS  [ ] KILL
- Aprendizagem principal (1 frase):
