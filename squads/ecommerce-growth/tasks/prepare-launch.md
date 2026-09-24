# Task: prepare-launch

task: prepararLancamento()
responsavel: ecommerce-master
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Consolidar tudo para o lançamento do teste de 3 dias: o ecommerce-master coordena a
verificação final — o qa-specialist executa o checklist de lançamento — e só então é
emitido o launch-report com o plano de teste (orçamento, países, métricas, critérios
de matar/escalar). GATE duro: qualquer veredito QA diferente de PASS BLOQUEIA o
lançamento. Publicação do tema e ativação da campanha só após aprovação humana
explícita do operador.

## Entrada
- vereditos de QA: ecom-stack/research/landers/<slug>-qa-report.md (audit-page) e <slug>-shopify-audit.md (audit-shopify) com veredito final do qa-specialist
- oferta e criativos: ecom-stack/research/landers/<slug>-offer.md e <slug>-creative-brief.md + assets em ecom-stack/assets/creatives/
- product_brief (ecom-stack/templates/product-brief.md — consome seções 1, 5 e 9)
- plano de teste: `python3 ecom-stack/cli/cli.py anuncio plano <slug>` (orçamento, países, métricas, regras de matar/escalar)
- ligação e credenciais: `python3 ecom-stack/cli/cli.py doctor`
- checklist: squads/ecommerce-growth/checklists/launch.md
- template: squads/ecommerce-growth/templates/launch-report.md

## Saida
- launch-report: ecom-stack/research/landers/<slug>-launch-report.md (formato squads/ecommerce-growth/templates/launch-report.md) com estado, tracking checklist, plano de teste e riscos
- autorização registrada: aprovação humana explícita do operador (data + canal) antes de publicar tema ou ativar campanha
- Em bloqueio: relatório de bloqueio com o veredito reprovado e a rota de correção

## Procedure
1. GATE DE QA: ler os vereditos finais do qa-specialist (audit-page e audit-shopify). Qualquer FAIL ou veredito ausente → BLOQUEAR: gravar relatório de bloqueio com a rota de correção (qual task recebe o quê) e parar. Sem exceções.
2. Confirmar pré-requisitos comerciais: produto existente na loja com status aprovado pelo operador, preços e bundles finais idênticos ao offer-brief, garantia igual à política da loja, prazo de entrega prometido realista.
3. Executar o checklist de lançamento (checklists/launch.md) com o qa-specialist: página no tema duplicado preview-OK a mobile e desktop, assets nos slots certos (nomes casando com os slots da página), copy final sem placeholders, FAQ e políticas acessíveis.
4. Tracking checklist: pixel Meta + CAPI e pixel TikTok verificados; eventos PageView, ViewContent, AddToCart, InitiateCheckout e Purchase a disparar (validado com compra de teste Bogus Gateway); UTM/países configurados no plano.
5. Consolidar o plano de teste imprimindo `python3 ecom-stack/cli/cli.py anuncio plano <slug>`: orçamento €20–50/dia × 3 dias (máx. €150); TikTok Ads + Meta Ads (Advantage+ shopping ou CBO 3 adsets); países US, CA, AU, NZ, UK com UK em adset separado; evento Purchase; criativos 2–3 vídeos 9:16 (formatos A/B/C).
6. Fixar os critérios de decisão (guia-uso.md Fase 5 + blueprint §7): mata se CTR < 1% ao fim do dia 2 ou CPA > €35 sem compra; mantém e testa 2 criativos novos se CPA €15–35; escala +20%/dia se CPA < €15.
7. Compilar o launch-report: estado de cada item do checklist, tracking checklist, plano de teste anexado, riscos identificados (compliance, stock, prazo de envio) e critérios de decisão.
8. Submeter ao operador e aguardar aprovação humana explícita. SÓ depois dela: publicar o tema duplicado e ativar a campanha — o ecommerce-master nunca publica por iniciativa própria (publish_requires_human_approval: true).

## Validation
- GATE: vereditos QA PASS presentes (audit-page + audit-shopify); sem isso, launch bloqueado.
- Checklist de lançamento 100% verificado com evidências.
- Tracking checklist completo: 5 eventos verificados com teste Bogus.
- Plano de teste da CLI anexado ao launch-report com critérios de matar/escalar.
- Aprovação humana registrada antes de qualquer ação de publicação.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o ecommerce-master consolida manualmente o launch-report a partir dos artefatos gravados.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: itens do checklist não verificados contam como pendentes — lançamento bloqueado até resolução.
- Veredito QA FAIL: BLOQUEAR imediatamente e devolver à rota de correção; nunca contornar o gate.
- Doctor falhar perto do lançamento: BLOQUEAR a ativação e escalar — pixel/loja sem ligação invalida o teste.

## Checklist
- [ ] GATE QA: vereditos PASS de audit-page e audit-shopify confirmados
- [ ] Produto, preços, bundles e garantia finais conferidos contra o offer-brief
- [ ] Checklist launch.md executado com o qa-specialist (evidências registadas)
- [ ] Tracking: 5 eventos de pixel verificados com teste Bogus Gateway
- [ ] Plano de teste impresso da CLI (`python3 ecom-stack/cli/cli.py anuncio plano <slug>`) anexado
- [ ] Critérios de decisão no report (mata CTR<1%/CPA>€35; escala CPA<€15 +20%/dia)
- [ ] Riscos identificados (compliance, stock, prazo de envio)
- [ ] Launch-report gravado em ecom-stack/research/landers/<slug>-launch-report.md
- [ ] Aprovação humana explícita registrada antes de publicar/ativar

## Delegação Hermes
- slug sugerido: growth-prepare-launch-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-launch.prompt.md (vereditos QA + checklist launch.md + plano da CLI + formato do launch-report)
- comando: bash workflows/executors/hermes-exec.sh -t growth-prepare-launch-<slug> -f /tmp/aiox-prompts/<slug>-launch.prompt.md -d /root/homefy -T 20
- timeout sugerido: 20 min
- leitura do result.json: campo "status" — SUCCESS (conferir itens e gravar o launch-report), PARTIAL (pendentes bloqueiam o lançamento), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
- nota de coordenação: o ecommerce-master orquestra; a execução dos checks é do qa-specialist; a decisão de publicar é sempre do operador humano
