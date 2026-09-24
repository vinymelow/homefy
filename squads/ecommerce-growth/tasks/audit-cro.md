# Task: audit-cro

task: auditarCRO()
responsavel: cro-specialist
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Auditoria de conversão da página (preview ou publicada): percorrer o funil de
anúncio a checkout, cruzar heurísticas de CRO com as métricas reais do teste e
sair com hipóteses priorizadas de melhoria — cada uma com problema, evidência,
hipótese, teste proposto e métrica de sucesso. É a task que transforma dados do
teste de 3 dias em decisão: matar, continuar ou escalar.

## Entrada
- página auditada: URL do preview do tema duplicado ou ecom-stack/templates/<slug>.html
- métricas do teste (quando existirem): CTR, CPC, taxa de conversão, CPA por criativo/campanha
- contratos: ecom-stack/research/landers/<slug>-page-spec.md e <slug>-offer.md
- tabela de decisão: ecom-stack/docs/blueprint-pagina-de-vendas.md §7 (mata/continua/escala por métrica)
- guia de operação: ecom-stack/docs/guia-uso.md Fase 5 (decisão ao fim do dia 2–3)
- checklist: squads/ecommerce-growth/checklists/cro.md

## Saida
- cro-audit: ecom-stack/research/landers/<slug>-cro-audit.md com hipóteses priorizadas (impacto × esforço) e plano de teste
- recomendação de decisão: matar (CTR < 1% ao fim do dia 2 ou CPA > €35 sem compra), continuar testando (CPA €15–35 + 2 criativos novos) ou escalar (CPA < €15, +20%/dia)
- top 3 de testes A/B com critério de sucesso e janela de decisão (3 dias, €20–50/dia)
- Entrada para: prepare-launch (re-lançamento) ou page-optimization (workflow de otimização)

## Procedure
1. Mapear o funil completo: anúncio (hook + criativo) → landing (hero → oferta → CTA) → checkout (Shopify). Marcar cada ponto de fricção observável (passos, campos, distrações, custo de envio revelado tarde).
2. Aplicar heurísticas de conversão na página: a oferta é compreensível em 5 segundos; prova social acima da dobra; CTA sempre visível (sticky ATC); preço e garantia sem surpresas; velocidade < 2.5s em 4G mobile; uma ideia por secção.
3. Cruzar com as métricas reais quando o teste já correu, usando a tabela do blueprint §7: CTR < 1% mata; CPC > €1,20 é caro; conversão < 0,8% indica página/oferta fraca; CPA > €35 sem compra mata; CPA < €15 escala.
4. Diagnosticar por métrica: CTR baixo = problema de criativo/hook (devolver a generate-creative-brief); cliques sem compra = problema de página/oferta (hipóteses de CRO); CPC alto = audiência/país ou leilão.
5. Escrever cada hipótese no formato: problema observado → evidência (métrica ou heurística) → hipótese de causa → teste proposto (o que muda, em que secção) → métrica de sucesso e limiar de decisão.
6. Priorizar por impacto × esforço: quick wins de copy/oferta primeiro (ex.: reordenar prova acima da dobra, clarificar bundles), mudanças estruturais depois (hero, pricing).
7. Selecionar o top 3 de testes com janela de decisão de 3 dias a €20–50/dia, compatível com o plano da CLI (`python3 ecom-stack/cli/cli.py anuncio plano <slug>`).
8. Emitir a recomendação de decisão (matar/continuar/escalar) com base nos limiares — dados decidem, sem paixão por produto.
9. Delegar ao Hermes (secção "Delegação Hermes") para a análise estruturada; o cro-specialist valida cada hipótese contra a evidência e grava o cro-audit.

## Validation
- Cada hipótese tem evidência real (métrica ou heurística verificada na página) — zero achismo.
- Priorização explícita (impacto × esforço) e top 3 com critério de sucesso mensurável.
- Recomendação de decisão dentro dos limiares do blueprint §7 (CTR/CPA).
- Plano de teste compatível com `python3 ecom-stack/cli/cli.py anuncio plano <slug>`.
- Auditoria validada contra checklists/cro.md.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o cro-specialist produz a análise manualmente a partir das métricas e da tabela de decisão.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: revisão humana; hipóteses sem evidência são descartadas.
- Métricas indisponíveis (pixel sem dados, campanha ainda a correr há < 2 dias): limitar a auditoria às heurísticas de página e marcar as conclusões como "pré-dados"; não recomendar matar/escalar sem dados.

## Checklist
- [ ] Funil anúncio → landing → checkout mapeado com pontos de fricção
- [ ] Heurísticas de CRO aplicadas (oferta em 5s, prova acima da dobra, sticky ATC, velocidade)
- [ ] Métricas cruzadas com a tabela do blueprint §7 (quando existem)
- [ ] Diagnóstico por métrica (CTR → criativo; cliques sem compra → página/oferta)
- [ ] Hipóteses no formato problema→evidência→hipótese→teste→métrica
- [ ] Priorização impacto × esforço + top 3 de testes com janela de 3 dias
- [ ] Recomendação matar/continuar/escalar com limiares
- [ ] Cro-audit gravado em ecom-stack/research/landers/<slug>-cro-audit.md

## Delegação Hermes
- slug sugerido: growth-audit-cro-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-cro.prompt.md (métricas do teste + HTML/URL da página + tabela de decisão do blueprint §7 + formato obrigatório das hipóteses)
- comando: bash workflows/executors/hermes-exec.sh -t growth-audit-cro-<slug> -f /tmp/aiox-prompts/<slug>-cro.prompt.md -d /root/homefy -T 25
- timeout sugerido: 25 min
- leitura do result.json: campo "status" — SUCCESS (validar hipóteses contra a evidência e gravar), PARTIAL (revisão humana), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
