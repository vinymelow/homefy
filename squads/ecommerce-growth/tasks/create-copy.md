# Task: create-copy

task: criarCopy()
responsavel: copywriter
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Escrever a copy completa da página de vendas: headline principal em linguagem "you"
(4–8 palavras, resultado), 5 benefícios escaneáveis, 3 passos de como funciona
(2 palavras por passo), FAQ de 4–6 perguntas que respondem objeções reais, título e
meta description. Tudo dentro dos guardrails de claims — a copy que quebra regras
da Meta/FTC mata a conta de anúncios antes do primeiro teste.

## Entrada
- product_brief (ecom-stack/templates/product-brief.md — consome seções 2, 3, 5 e 7; produz seção 6 completa)
- positioning-doc: ecom-stack/research/landers/<slug>-positioning.md (proposta de valor e ângulos)
- offer-brief: ecom-stack/research/landers/<slug>-offer.md (preços, bundles, garantia — copy usa só valores reais)
- avatares-doc: ecom-stack/research/landers/<slug>-avatars.md (desejos e frases verbatim para voz)
- método: ecom-stack/docs/blueprint-pagina-de-vendas.md §4 (as 5 correções de copy) e §5 (guardrails)
- guardrails: seção 7 do brief (checklist obrigatório de claims)

## Saida
- copy-doc: ecom-stack/research/landers/<slug>-copy.md com headline, benefícios, how-to, FAQ, título da página, meta description e announcement bar
- brief seção 6 preenchida: benefício principal, 5 benefícios, 3 passos, FAQ
- Produz no brief: seção 6 (copy)

## Procedure
1. Ler os guardrails da seção 7 do brief e tratá-los como checklist de passa/falha: nenhum preço/desconto/prazo/garantia sem confirmação; claims de saúde/beleza suavizados; sem logos de imprensa inventados; reviews reais ou "Dramatized customer story"; specs só verificadas.
2. Escrever a headline principal: RESULTADO em linguagem "you", 4–8 palavras — nunca problema, nunca feature. O problema aparece uma única vez na página (hero/recognition).
3. Escrever os 5 benefícios escaneáveis (ícone + título + 1 linha): cada benefício = 1 desejo ranqueado do avatar; regra dura — cada desejo aparece exatamente 1 vez, sem repetição entre headline, benefícios e frames.
4. Escrever o how-to em 3 passos com labels de 2 palavras por passo (ex.: "Passa · Seca · Brilha"), na voz direta e em segunda pessoa.
5. Escrever o FAQ com 4–6 perguntas reais que respondem as objeções da seção 3; a pergunta sobre garantia repete os dias exatos da política da loja; nicho de saúde/beleza inclui hedge ("designed to help with", nunca "cura/trata").
6. Escrever announcement bar (único sítio com exclamação permitida), título da página (= benefício, não nome genérico) e meta description de ~160 caracteres.
7. Aplicar as 5 correções do blueprint §4 em cada peça: headline = resultado; sem duplos negativos ("clear head", não "no pills to fog your head"); sem repetição; confiança + diferenciação ("porquê tu"); trust + honesty (hedge em claims reversíveis).
8. Regras de estilo: voz direta, benefit-first, segunda pessoa, frases curtas, UK/US English, zero exclamações fora da announcement bar.
9. Delegar ao Hermes (secção "Delegação Hermes") para variações; o copywriter escolhe as versões finais, grava o copy-doc e preenche a seção 6 do brief.

## Validation
- Headline com 4–8 palavras, em "you", expressando resultado (contar as palavras).
- 5 benefícios, cada um ligado a 1 desejo, sem desejo repetido na página.
- How-to com 3 passos e labels de 2 palavras.
- FAQ com 4–6 perguntas cobrindo as objeções da seção 3 (cada objeção respondida na FAQ ou noutra secção identificada).
- Zero exclamações fora da announcement bar; zero claims de cura/tratamento.
- Todos os valores comerciais (preço, desconto, garantia, prazo) idênticos aos do offer-brief.
- Passa no checklist checklists/copy.md do squad.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o copywriter escreve as peças manualmente a partir da proposta de valor e dos desejos ranqueados.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: revisão humana peça a peça; nenhuma claim sai sem passar no checklist da seção 7.
- Guardrail impossível de cumprir (ex.: produto de saúde cujo único ângulo é claim proibido): escalar ao operador com alternativas honestas — nunca relaxar o guardrail.

## Checklist
- [ ] Guardrails da seção 7 verificados como passa/falha
- [ ] Headline 4–8 palavras, "you", resultado (contagem feita)
- [ ] 5 benefícios escaneáveis, 1 por desejo, sem repetição
- [ ] How-to 3 passos com labels de 2 palavras
- [ ] FAQ 4–6 perguntas respondendo as objeções reais da seção 3
- [ ] Garantia no FAQ com os dias exatos da política da loja
- [ ] Zero exclamações fora da announcement bar
- [ ] Valores comerciais idênticos ao offer-brief (preço/garantia/prazo)
- [ ] Seção 6 do brief preenchida e copy-doc gravado

## Delegação Hermes
- slug sugerido: growth-create-copy-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-copy.prompt.md (proposta de valor, desejos ranqueados, objeções, valores reais da oferta, guardrails verbatim, peças a redigir)
- comando: bash workflows/executors/hermes-exec.sh -t growth-create-copy-<slug> -f /tmp/aiox-prompts/<slug>-copy.prompt.md -d /root/homefy -T 20
- timeout sugerido: 20 min
- leitura do result.json: campo "status" — SUCCESS (aplicar as 5 correções e gravar), PARTIAL (revisão humana peça a peça), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
