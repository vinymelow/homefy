# Task: analyze-competitors

task: analisarConcorrentes()
responsavel: market-researcher
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Dissecar a concorrência do produto em validação: concorrentes diretos (mesmo produto)
e indiretos (mesmo problema, solução diferente), com ofertas, preços, ângulos,
criativos dominantes e fraquezas nas reviews. O objetivo não é copiar a marca — é
encontrar as falhas que ela não resolve e transformar cada uma em ângulo de anúncio
ou objeção respondida na página. Saída obrigatória: as 3 referências estruturais do
brief (home, PDP, hero) vindas do Winning Hunter / ad library.

## Entrada
- produto candidato: ecom-stack/research/landers/<slug>-research.md (output de research-product)
- product_brief (ecom-stack/templates/product-brief.md — consome seções 1 e 4; produz seção 4 completa)
- método: ecom-stack/prompts/pesquisa-produto.md §2 (prompt de análise do concorrente) e ecom-stack/docs/metodo-pesquisa.md (Parte 0: prova, não clones; Parte 4: filtros)
- tracker: ecom-stack/research/tracker.md (evidence log)
- blueprint: ecom-stack/docs/blueprint-pagina-de-vendas.md §1 (critérios de referência: receita visível, mobile 390px, estrutura e movimento — nunca logo/copy/claims)

## Saida
- competitors-report: ecom-stack/research/landers/<slug>-competitors.md com a matriz de concorrentes e a tabela de gaps
- brief seção 4 preenchida: tabela de referências (Homepage / Landing page / Hero / Ads vencedores com URL + o que copiar) + receita estimada da loja alvo
- lista de 3–6 frames de ads vencedores para clonar (ad library, filtrado por spend)
- evidence log atualizado com link + data de cada concorrente
- Produz no brief: seção 4 (referências escolhidas)

## Procedure
1. Ler o research-report do produto e confirmar que ele passou no gate ≥ 70; sem isso, não gastar tempo em concorrência.
2. Listar 3–5 concorrentes diretos (vendem o mesmo produto) e 2 indiretos (resolvem o mesmo problema com outra solução); para cada um capturar: URL, receita estimada (Winning Hunter) com data, idade da loja, nº de anúncios ativos e dias no ar, formato dominante (vídeo/imagem UGC), preço, oferta/bundle, prazo de envio prometido e países visíveis nos comentários.
3. Para cada concorrente direto, aplicar o prompt de análise de prompts/pesquisa-produto.md §2: por que está a ganhar (hook, dor, oferta), ponto fraco a bater (página, envio, oferta, frescura do criativo), margem estimada ao custo real e veredito TEST/SKIP do ângulo dele.
4. Ler as reviews 1–3★ dos concorrentes diretos e extrair as 5 queixas mais frequentes por loja (citações verbatim + link) — cada queixa é um gap ou uma objeção a responder.
5. Montar a matriz de gaps: falhas que nenhum concorrente resolve (envio lento, qualidade, ângulo, garantia fraca) → oportunidades de oferta e criativo que nos deixam melhores que o original.
6. Escolher as 3 referências estruturais pelo método do blueprint §1: homepage da loja com melhor estrutura global, PDP da loja com melhor sistema de compra, hero da loja com melhor hero de compra — sempre com receita estimada visível e inspeção a 390px. Referência = estrutura e movimento; NUNCA logo, imagens, copy, reviews ou claims.
7. Selecionar 3–6 frames de ads vencedores no ad library filtrado por spend (spend contínuo = lucro) para clonar em generate-creative-brief.
8. Delegar ao Hermes (secção "Delegação Hermes") para a síntese da matriz; revisar o output contra as fontes e gravar o competitors-report.
9. Preencher a seção 4 do brief (URL + o que vou copiar, por componente) e registar tudo no evidence log com link + data.

## Validation
- Mínimo de 3 concorrentes diretos e 2 indiretos analisados com dados datados.
- Cada gap da matriz tem citação real de review (1–3★) com link.
- Seção 4 do brief com as 3 referências preenchidas (URL + o que copiar) e receita estimada com data.
- 3–6 frames de ads vencedores identificados com fonte no ad library.
- Nenhum dado inventado: preços, prazos e receitas conferidos na fonte no dia da análise.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, gravar o relatório com os concorrentes já analisados e marcar a síntese como pendente.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log; não preencher a seção 4 do brief sem execução válida.
- PARTIAL: revisão humana obrigatória; validar cada linha da matriz contra as fontes antes de gravar.
- Concorrente com dados inacessíveis (loja offline, ad library vazio): substituir por outro direto e registar a substituição no relatório.

## Checklist
- [ ] Mínimo de 3 diretos + 2 indiretos na matriz, com URL e data de análise
- [ ] Por concorrente direto: preço, oferta, prazo, ângulo, formato de criativo, receita estimada
- [ ] Análise §2 aplicada (por que ganha / ponto fraco / margem / veredito) a cada direto
- [ ] 5 queixas mais frequentes por loja citadas verbatim das reviews 1–3★
- [ ] Matriz de gaps com oportunidades mapeadas para oferta e criativo
- [ ] Seção 4 do brief preenchida (3 referências + o que copiar + receita estimada)
- [ ] 3–6 frames de ads vencedores listados para clonar
- [ ] Evidence log atualizado (link + data em cada fonte)

## Delegação Hermes
- slug sugerido: growth-analyze-competitors-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-competitors.prompt.md (modelo §2 de prompts/pesquisa-produto.md + dados brutos de cada concorrente + citações de reviews)
- comando: bash workflows/executors/hermes-exec.sh -t growth-analyze-competitors-<slug> -f /tmp/aiox-prompts/<slug>-competitors.prompt.md -d /root/homefy -T 30
- timeout sugerido: 30 min
- leitura do result.json: campo "status" — SUCCESS (revisar output.md contra as fontes e gravar), PARTIAL (revisão humana linha a linha), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
