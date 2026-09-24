# Task: generate-creative-brief

task: gerarBriefCriativos()
responsavel: creative-director
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Produzir o creative-brief: um prompt de geração pronto para cada slot de criativo da
seção 9 do brief (hero-main, recognition, payoffs, infographic-mech, how-to,
vs-alternative, angles, lifestyle, ugc-video, static-ads), derivado de ads e páginas
que já estão a ganhar dinheiro — nada é criado do zero. A imagem do produto é SEMPRE
a foto real recortada, nunca regenerada por IA; lifestyle/UGC segue as 5 chaves de
hiper-realismo do método.

## Entrada
- product_brief (ecom-stack/templates/product-brief.md — consome seções 2, 3, 5, 6, 8 e 9)
- landing-page-spec: ecom-stack/research/landers/<slug>-page-spec.md (inventário de slots com ratios)
- competitors-report: ecom-stack/research/landers/<slug>-competitors.md (frames de ads vencedores para clonar)
- copy-doc: ecom-stack/research/landers/<slug>-copy.md (textos verbatim dos overlays, headlines 4–8 palavras)
- método: ecom-stack/docs/metodo-criativos.md (clonagem zona-a-zona, 5 chaves, galeria PDP, regras de texto em imagem)
- prompts de referência: ecom-stack/prompts/criativos.md (prompts base por tipo de slot e formatos de vídeo A/B/C)
- fotos reais do produto: ecom-stack/assets/creatives/

## Saida
- creative-brief: ecom-stack/research/landers/<slug>-creative-brief.md (formato squads/ecommerce-growth/templates/creative-brief.md)
- prompts de geração: 1 prompt pronto por slot, com ratio, luz, fundo e copy verbatim do overlay
- plano de variância: 3 formatos de vídeo × 2–3 hooks = 6–9 criativos para o teste inicial
- comandos de geração: `python3 ecom-stack/cli/cli.py criativo imagem <slug> --slot <slot>` e `python3 ecom-stack/cli/cli.py criativo video <slug> --formato <A|B|C>` (requerem .env configurado)

## Procedure
1. Travar 1 kit de marca da seção 8 (clinical-clean / bold-hype / premium-elegant / earthy-natural) antes de gerar qualquer prompt — o template base do projeto usa premium-elegant/warm.
2. Confirmar a classificação da seção 2 e derivar a lista de slots: high-consideration inclui recognition-1/2 e infographic-mech; low-stakes remove recognition e pivot, com mais produto-em-uso.
3. Para cada slot, aplicar o fluxo de metodo-criativos.md: referência vencedora → dissecação zona-a-zona (formato, mapa de zonas com posições em grelha, hierarquia visual, paleta, luz, escala do produto, tipografia por zona) → copy reescrita mantendo a estrutura.
4. Hero-main (arquétipo 1, Benefit Stack): foto real do produto em uso + painel translúcido com stack de 4–5 benefícios; tem de funcionar sozinho como thumbnail.
5. Recognition/payoffs: 1 imagem por desejo ranqueado (payoff espelha o recognition); headline de cada frame = RESULTADO em 4–8 palavras, linguagem "you".
6. Infographic-mech (arquétipos 2–5): Mechanism Explainer com cutaway + glow no ponto de ação, ou How-To Steps, Features Checklist, Vs-Alternative conforme o produto.
7. Angles (angle-1/2/3): prompts para foto REAL do produto (macro/detalle, luz de estúdio simples, 2 variantes) — nunca gerar o produto por IA.
8. Lifestyle (lifestyle-1/2) e UGC: aplicar as 5 chaves de hiper-realismo em cada prompt — textura de pele (≥3 palavras: "visible pores", "fine lines"), câmara específica ("shot on iPhone 15 front camera"), luz com nome e direção ("soft golden morning light through sheer curtains from camera-left"), micro-imperfeição ("one piece of hair falling across her cheek"), ambiente plausível (3–5 objetos específicos em ligeira desordem) — e o fecho obrigatório "no advertising polish, no smoothing, no glassy skin, no studio lighting, no posing, no AI look". Gerar 2 variantes.
9. UGC-video: 3 formatos 9:16 de prompts/criativos.md — A (hook problema/solução), B (demonstração pura, 3 cortes com caption de 3 palavras), C (infográfico em movimento) × 2–3 hooks de texto = 6–9 vídeos.
10. Static-ads (static-ads-1/2/3): dissecação zona-a-zona de 3 ads vencedores do ad library (estrutural preserva, de marca troca) + guardas de fiabilidade no prompt (travar produto à foto real verbatim, copiar texto letter-for-letter, proibir extras, posições em grelha concreta). SEMPRE 3 variantes em paralelo.
11. Regras de consistência em todos os prompts: mesmo fundo/tom de luz (sistema visual, não fotos soltas), sem logos/marcas de terceiros, texto ≤ 6 palavras por overlay com painel sólido, safe zone do carrossel (terço do meio livre nas bordas), legível a braço de distância para 55–75 anos — se não couber, corta palavra, nunca encolher tipo.
12. Guardrails nos overlays: garantia/preço/specs idênticos em TODOS os frames; reviews reais ou "Dramatized customer story"; claims de saúde suavizados; produto mostrado = o que shipa.
13. Delegar ao Hermes (secção "Delegação Hermes") para a redação dos prompts por slot; o creative-director faz o QC da contact sheet (headlines são resultados? foto contradiz a legenda? texto na safe zone? valores coerentes? prova real?) e grava o creative-brief.

## Validation
- 1 prompt pronto por slot da seção 9 (nenhum slot em falta).
- 5 chaves presentes em cada prompt lifestyle/UGC + fecho anti-IA.
- Angles usam foto real (prompt de fotografia, não de geração IA).
- Textos dos overlays verbatim do copy-doc (≤ 6 palavras por overlay).
- Garantia/preço/specs idênticos em todos os frames (passagem de consistência).
- Plano de variância: 6–9 criativos (3 formatos de vídeo × 2–3 hooks + estáticos).
- QC da contact sheet passado (5 perguntas do método).

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, gerar manualmente os prompts dos slots críticos (hero-main, payoffs, static-ads) e marcar o restante como pendente.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: revisão humana prompt a prompt; nenhum prompt sem as 5 chaves (lifestyle) ou as guardas de fiabilidade (static-ads) vai para geração.
- Frame de QC reprovado: regenerar o frame antes de entregar — qualquer falha nas 5 perguntas da contact sheet bloqueia o slot.

## Checklist
- [ ] Kit de marca travado (1 dos 4) antes dos prompts
- [ ] Lista de slots derivada da classificação (seção 2)
- [ ] 1 prompt por slot com ratio, luz, fundo e copy verbatim
- [ ] Hero-main como Benefit Stack com foto real + painel translúcido
- [ ] 5 chaves + fecho anti-IA em todos os prompts lifestyle/UGC
- [ ] Angles com foto real (2 variantes cada)
- [ ] Static-ads com dissecação zona-a-zona + guardas de fiabilidade
- [ ] Consistência: mesmo fundo/luz, safe zones, texto ≤ 6 palavras, valores iguais
- [ ] Plano de variância 6–9 criativos (vídeo A/B/C × hooks)
- [ ] QC da contact sheet passado e creative-brief gravado

## Delegação Hermes
- slug sugerido: growth-creative-brief-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-creative.prompt.md (slots + dissecações + copy verbatim + 5 chaves + estrutura de saída: 1 prompt por slot)
- comando: bash workflows/executors/hermes-exec.sh -t growth-creative-brief-<slug> -f /tmp/aiox-prompts/<slug>-creative.prompt.md -d /root/homefy -T 30
- timeout sugerido: 30 min
- leitura do result.json: campo "status" — SUCCESS (fazer QC da contact sheet e gravar), PARTIAL (revisão humana slot a slot), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
