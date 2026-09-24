# Task: research-product

task: pesquisarProduto()
responsavel: product-researcher
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Executar o método de pesquisa evidence-based (ecom-stack/docs/metodo-pesquisa.md) para
um candidato a produto: passagem 1 (shortlist com score 0–100 nas 5 dimensões) e
passagem 2 (deep dive com veredito GREEN/AMBER/RED e CPA máximo). O product-researcher
decide com dados e evidência datada, nunca com intuição, e alimenta o tracker central
do projeto. O princípio do método: não é o produto que vence — é o problema que ele
resolve.

## Entrada
- parâmetros de pesquisa: nicho (casa & utilidades / beleza & cuidados pessoais), mercado-alvo (ex.: US) e faixa de preço (ex.: $29–59) — fornecidos pelo operador ou herdados do brief em edição
- product_brief (ecom-stack/templates/product-brief.md — consome seções 1 e 2 quando já existir rascunho)
- método: ecom-stack/docs/metodo-pesquisa.md e ecom-stack/prompts/pesquisa-produto.md (filtros Winning Hunter, prompt de análise do concorrente)
- tracker: ecom-stack/research/tracker.md (shortlist, deep dives, evidence log)
- template de registo: ecom-stack/research/landers/TEMPLATE-lander.md

## Saida
- research-report: ecom-stack/research/landers/<slug>-research.md (formato do template squads/ecommerce-growth/templates/research-report.md)
- tracker atualizado: score nas 5 dimensões (procura /20, gap /20, fornecedor /20, compliance /20, prova criativa /20), veredito e evidence log com link + data
- decisão TEST/SKIP em uma frase + CPA máximo calculado
- brief rascunho criado via CLI quando GREEN: `python3 ecom-stack/cli/cli.py brief novo <slug>`
- Produz no brief: seções 1 (dados base) e 2 (classificação do produto)

## Procedure
1. Confirmar nicho, mercado e faixa de preço; se ausentes, pedir ao operador antes de prosseguir.
2. Aplicar os filtros do Winning Hunter (prompts/pesquisa-produto.md §1): loja com receita estimada > $50k/mês e ≤ 12 meses de idade, 3+ anúncios ativos há mais de 30 dias, criativos dominantes UGC, preço $25–70 com bundle, solução visual (o produto "mostra" o benefício em 2 segundos).
3. Registar o candidato na shortlist do tracker (ecom-stack/research/tracker.md) com link + data de cada evidência.
4. Montar o prompt file da passagem 1 a partir do modelo "Passagem 1" de metodo-pesquisa.md: problema que resolve com citações reais de reviews/comentários, momento de uso, prova de spend, preço dos concorrentes e score 0–100.
5. Delegar ao Hermes (secção "Delegação Hermes") e ler o result.json do run.
6. Calcular o score nas 5 dimensões do método; aplicar o gate: ≥ 70 avança para a passagem 2, < 70 é descartado com motivo registado no tracker.
7. Na passagem 2, usar o prompt da Parte 3 do método: 5 queixas mais frequentes nas reviews 1–3★ das 3 lojas concorrentes principais (citações verbatim), economia (margem e CPA máximo a partir de custo + envio + AOV) e veredito GREEN/AMBER/RED com razões e riscos.
8. Em GREEN: criar o brief com `python3 ecom-stack/cli/cli.py brief novo <slug>`, preencher o research-report com as secções 1b/1c do método e encaminhar ao operador para os dados comerciais (preços, bundles, garantia).
9. Em AMBER/RED: registar no tracker e selecionar o próximo candidato ≥ 70. Conta gastar 2–4 passagens 2 até ao primeiro GREEN — é o método a proteger de produtos maus, não falha do pesquisador.
10. Nunca fabricar evidência: toda afirmação leva link + data; sem fonte, não entra no relatório.

## Validation
- Score 0–100 com as 5 dimensões preenchidas e gate ≥ 70 aplicado (metodo-pesquisa.md Parte 2).
- Veredito GREEN/AMBER/RED explícito, com razões, riscos e recomendação direta ("não anunciava" quando for o caso).
- CPA máximo calculado a partir de AOV, custo, envio e taxas; coerente com a sobrevivência a €20–50/dia de teste.
- Evidence log com link + data em cada linha do tracker.
- Research-report salvo em ecom-stack/research/landers/ e brief criado quando GREEN.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout aumentado em 50%; se repetir, marcar o candidato como "indeterminado" no tracker e avançar para o próximo.
- FAILED/REJECTED: halt — não emitir veredito sem execução válida; registar o erro no tracker e escalar ao operador com o hermes.log do run em .aiox/external-runs/<run>/.
- PARTIAL: saída vazia ou curta demais exige revisão humana obrigatória antes de qualquer decisão TEST/SKIP.
- Evidência insuficiente (reviews inacessíveis, spend indisponível, fornecedor sem política de refunds): não avance — faltam dados de entrada; reportar ao operador o que falta.

## Checklist
- [ ] Nicho, mercado e faixa de preço confirmados no relatório
- [ ] Candidato registado na shortlist do tracker com link + data
- [ ] Filtros do Winning Hunter aplicados e registados (receita, idade, anúncios 30+ dias, formato UGC)
- [ ] Score 0–100 nas 5 dimensões e gate ≥ 70 aplicado
- [ ] Passagem 2 com as 5 queixas mais frequentes citadas verbatim das reviews 1–3★
- [ ] CPA máximo calculado e coerente com o orçamento de teste de €20–50/dia
- [ ] Veredito GREEN/AMBER/RED explícito com razões e riscos
- [ ] Evidence log atualizado (link + data em cada fonte)
- [ ] Brief criado via CLI em caso de GREEN (`python3 ecom-stack/cli/cli.py brief novo <slug>`)

## Delegação Hermes
- slug sugerido: growth-research-product-<slug-do-produto>
- prompt file: /tmp/aiox-prompts/<slug>-research.prompt.md (montado a partir de metodo-pesquisa.md + dados do candidato do tracker)
- comando: bash workflows/executors/hermes-exec.sh -t growth-research-product-<slug> -f /tmp/aiox-prompts/<slug>-research.prompt.md -d /root/homefy -T 30
- timeout sugerido: 30 min
- leitura do result.json: campo "status" — SUCCESS (validar output.md e seguir a procedure), PARTIAL (revisão humana antes do veredito), FAILED ou TIMEOUT (failure handling acima), REJECTED (pré-check falhou: prompt vazio, workdir ilegível ou hermes ausente — corrigir a causa e reenviar)
