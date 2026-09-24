# Task: create-customer-avatar

task: criarAvatarCliente()
responsavel: product-researcher
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Transformar a pesquisa em pessoas: 1 a 3 avatares acionáveis (brief seção 3) com
desejos ranqueados por intensidade, objeções principais e o momento exato em que o
problema acontece. Os avatares são o contrato que alimenta oferta (create-offer),
copy (create-copy) e criativos (generate-creative-brief). Regra do método: uma
pessoa específica + um momento específico — nunca "para todos".

## Entrada
- research-report: ecom-stack/research/landers/<slug>-research.md (reviews e queixas da passagem 2)
- market-report: ecom-stack/research/<nicho>-market.md (voice-of-customer por tema)
- competitors-report: ecom-stack/research/landers/<slug>-competitors.md (gaps e objeções dos concorrentes)
- product_brief (ecom-stack/templates/product-brief.md — consome seções 1 e 2; produz seção 3 completa)
- método: ecom-stack/docs/metodo-pesquisa.md Parte 0 (problema recorrente, momento em que acontece, palavras exatas)

## Saida
- avatares-doc: ecom-stack/research/landers/<slug>-avatars.md com 1–3 avatares (idade, género, contexto, momento de uso, frase típica verbatim, desejos ranqueados, objeções)
- brief seção 3 preenchida: Avatar 1/2/3, desejos ranqueados 1–3, objeções principais 1–3
- mapa objeção → resposta: cada objeção ligada à secção/imagem da página que a responde
- Produz no brief: seção 3 (público e promessa)

## Procedure
1. Consolidar as citações verbatim dos três relatórios de entrada, mantendo link + data de cada uma.
2. Agrupar as citações por padrão: quem reclama (demografia, contexto de vida), quando o problema acontece (momento do dia/rotina) e o que querem (resultado desejado).
3. Definir 1–3 avatares a partir dos maiores agrupamentos; cada avatar leva: nome-tipo (ex.: "a mãe ocupada"), idade, género, contexto, momento de uso específico e uma frase típica copiada verbatim de uma citação real.
4. Ranquear os desejos de cada avatar por intensidade (1 = o resultado mais gritado nas citações); justificar a ordem com volume/força das citações. Os desejos ranqueados escrevem as headlines dos frames de payoff.
5. Listar as 3 objeções principais (as que mais aparecem nas reviews e queixas) e mapear cada uma para a secção ou imagem da página que a responde — regra do brief: cada objeção TEM de ser respondida por uma imagem ou secção.
6. Verificar a regra "uma pessoa específica + um momento específico" para cada avatar; se um avatar ficar genérico ("qualquer pessoa que queira..."), reescrever com o momento concreto.
7. Para produtos low-stakes (brief seção 2), concentrar 1 avatar principal e simplificar; para high-consideration, validar 1–2 avatares de reconhecimento (frames recognition).
8. Delegar ao Hermes (secção "Delegação Hermes") para a síntese; revisar o output contra as citações e gravar o avatares-doc + seção 3 do brief.

## Validation
- Cada avatar sustentado por pelo menos 3 citações reais com link + data.
- Desejos ranqueados com justificativa de intensidade (não ordem arbitrária).
- As 3 objeções principais mapeadas para secção/imagem que as responde.
- Frase típica de cada avatar é verbatim de citação real, não inventada.
- Zero avatares genéricos: cada um tem pessoa específica + momento específico.
- Seção 3 do brief preenchida e coerente com a classificação do produto (seção 2).

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o product-researcher sintetiza manualmente a partir das citações consolidadas e marca a síntese Hermes como pendente no relatório.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log; não preencher a seção 3 sem execução válida.
- PARTIAL: revisão humana obrigatória; conferir cada avatar e desejo contra as citações de origem.
- Citações insuficientes para 3 avatares (< 3 por avatar): reduzir para 1–2 avatares bem sustentados e registar a decisão — nunca preencher com perfil imaginário.

## Checklist
- [ ] Citações dos três relatórios de entrada consolidadas com link + data
- [ ] 1–3 avatares definidos com idade, género, contexto e momento de uso específico
- [ ] Frase típica de cada avatar copiada verbatim de citação real
- [ ] Desejos ranqueados 1–3 com justificativa de intensidade
- [ ] 3 objeções principais mapeadas para secção/imagem que as responde
- [ ] Regra "pessoa específica + momento específico" verificada em todos os avatares
- [ ] Seção 3 do brief preenchida (avatares, desejos, objeções)
- [ ] Avatares-doc gravado em ecom-stack/research/landers/<slug>-avatars.md

## Delegação Hermes
- slug sugerido: growth-create-avatar-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-avatars.prompt.md (citações consolidadas por tema + estrutura obrigatória de saída: avatares, desejos ranqueados, objeções, mapa objeção→resposta)
- comando: bash workflows/executors/hermes-exec.sh -t growth-create-avatar-<slug> -f /tmp/aiox-prompts/<slug>-avatars.prompt.md -d /root/homefy -T 20
- timeout sugerido: 20 min
- leitura do result.json: campo "status" — SUCCESS (conferir avatares contra as citações e gravar), PARTIAL (revisão humana antes de gravar), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
