# Task: research-market

task: pesquisarMercado()
responsavel: market-researcher
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Mapear o nicho antes de escalar qualquer produto: tamanho e dinâmica do mercado,
tendências dos últimos 12 meses, sazonalidade, riscos de compliance do nicho e a
linguagem real do cliente (voice-of-customer). O market-researcher entrega as
palavras exatas dos compradores — é essa linguagem que a copy e os anúncios vão
usar para falar como o cliente, não como a marca.

## Entrada
- nicho e mercado-alvo (ex.: beleza & cuidados pessoais, US) — do operador ou do brief seção 1
- product_brief (ecom-stack/templates/product-brief.md — consome seção 1 quando existir)
- método: ecom-stack/docs/metodo-pesquisa.md (Parte 0: começar pelo problema; guardar link + data)
- tracker: ecom-stack/research/tracker.md (evidence log do nicho)
- contexto de produtos ativos do nicho em ecom-stack/research/landers/

## Saida
- market-report: ecom-stack/research/<nicho>-market.md com: dimensionamento, tendências 12 meses, sazonalidade, mapa de concorrência de nicho, riscos de compliance e bloco voice-of-customer
- voice-of-customer: 15–30 citações verbatim organizadas por tema (desejos, queixas, objeções, gírias) com link + data
- evidence log do nicho atualizado em ecom-stack/research/tracker.md
- Produz no brief: insumo para seção 3 (público) quando o relatório alimentar um produto específico

## Procedure
1. Confirmar nicho e mercado-alvo com o operador; definir 5–8 termos de busca (problema, não produto — ex.: "frizz hair morning routine", não "hair brush").
2. Coletar sinais em Google Trends (12 meses, comparar termos), Reddit (threads com queixas recorrentes), TikTok Creative Center e Meta Ad Library (marcas a gastar continuamente = nicho com margem), guardando link + data de cada fonte.
3. Dimensionar: estimativas de tamanho/dinâmica do nicho com fonte citada; quando não houver dado público, indicar a estimativa como direcional e explicar a base de cálculo.
4. Mapear sazonalidade e momentos de pico (meses, eventos) — alimenta o timing de lançamento.
5. Extrair voice-of-customer: copiar as palavras exatas dos compradores em 15–30 citações, agrupadas por tema, com o momento em que o problema acontece (acordar, preparar o jantar) — a cena que o criativo vai mostrar.
6. Levantar riscos de compliance do nicho (restrições de anúncio, claims proibidos, marcas registadas) — nichos de saúde/beleza exigem atenção redobrada.
7. Montar o prompt file de síntese e delegar ao Hermes (secção "Delegação Hermes"); o output estruturado vira o corpo do market-report.
8. Revisar o output: cada afirmação quantitativa precisa de fonte + data; citações verbatim conferidas contra as fontes coletadas.
9. Gravar o relatório em ecom-stack/research/<nicho>-market.md e registar as fontes no evidence log do tracker.

## Validation
- Mínimo de 15 citações voice-of-customer com link + data, agrupadas por tema.
- Toda afirmação quantitativa (tamanho, crescimento, spend) com fonte datada; estimativas direcionais identificadas como tal.
- Bloco de sazonalidade com meses de pico justificados por evidência.
- Riscos de compliance listados com o motivo (plataforma ou regulamento).
- Relatório gravado em ecom-stack/research/ e evidence log atualizado.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout em 50% maior; persistindo, entregar o relatório com as seções já coletadas marcando a síntese como pendente e escalar ao operador.
- FAILED/REJECTED: halt — corrigir a causa (prompt file vazio, hermes ausente) e reenviar; não publicar relatório sem execução válida.
- PARTIAL: revisão humana do output antes de gravar; completar as secções em falta manualmente a partir das fontes coletadas.
- Fontes indisponíveis (Reddit bloqueado, Trends sem dado para o termo): registar a limitação no relatório e compensar com mais fontes alternativas — nunca preencher o vazio com suposição.

## Checklist
- [ ] Nicho, mercado-alvo e termos de busca definidos no relatório
- [ ] Mínimo de 4 fontes de sinal coletadas com link + data (Trends, Reddit, TikTok CC, Ad Library)
- [ ] 15–30 citações voice-of-customer verbatim, agrupadas por tema
- [ ] Sazonalidade mapeada com meses de pico evidenciados
- [ ] Riscos de compliance do nicho listados
- [ ] Afirmações quantitativas todas com fonte datada
- [ ] Relatório gravado em ecom-stack/research/<nicho>-market.md
- [ ] Evidence log do tracker atualizado com as fontes do nicho

## Delegação Hermes
- slug sugerido: growth-research-market-<nicho>
- prompt file: /tmp/aiox-prompts/<nicho>-market.prompt.md (síntese estruturada das fontes coletadas, com as citações inline e instrução de formato markdown)
- comando: bash workflows/executors/hermes-exec.sh -t growth-research-market-<nicho> -f /tmp/aiox-prompts/<nicho>-market.prompt.md -d /root/homefy -T 30
- timeout sugerido: 30 min
- leitura do result.json: campo "status" — SUCCESS (revisar output.md e gravar o relatório), PARTIAL (completar secções em falta manualmente), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
