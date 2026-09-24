# Task: create-positioning

task: criarPosicionamento()
responsavel: offer-strategist
responsavel_type: Agente
atomic_layer: Molecule

## Purpose
Destilar a estratégia em uma proposta de valor afiada: o que prometemos, para quem,
porque somos a escolha certa e por que agora. Consome os gaps dos concorrentes e os
desejos dos avatares para definir o ângulo principal de ataque (e 2–3 alternativos
para teste de criativos) e as provas de diferenciação. É a Molécula que segura a
coerência entre oferta, copy e página.

## Entrada
- avatares-doc: ecom-stack/research/landers/<slug>-avatars.md (desejos ranqueados, objeções)
- competitors-report: ecom-stack/research/landers/<slug>-competitors.md (matriz de gaps)
- offer-brief: ecom-stack/research/landers/<slug>-offer.md (o que a oferta entrega de concreto)
- product_brief (ecom-stack/templates/product-brief.md — consome seções 2, 3 e 5; produz o bloco de positioning)
- método: ecom-stack/docs/metodo-pesquisa.md Parte 0 item 3 (construir um ângulo melhor: mudar o momento do cliente, manter a função factual)

## Saida
- positioning-doc: ecom-stack/research/landers/<slug>-positioning.md com proposta de valor, ângulo principal, ângulos alternativos e provas de diferenciação
- bloco de positioning no brief (seção 3/6): proposta de valor em 1 frase + ângulo principal
- Produz no brief: bloco de positioning (proposta de valor e ângulo)

## Procedure
1. Identificar o gap central: a falha que nenhum concorrente resolve (da matriz de gaps) e que o produto + oferta resolvem de verdade.
2. Escrever a proposta de valor em uma frase: resultado principal (desejo #1 do avatar) + diferenciador verificável + para quem (avatar principal no seu momento específico). Forma guia: "Para [avatar no momento], [produto] é [categoria] que [resultado #1] — diferente de [alternativa], porque [prova]."
3. Definir o ângulo principal de comunicação (o gancho que abre hero e anúncios) e 2–3 ângulos alternativos para rodar nos testes de criativos (cada ângulo = um momento do cliente ou um desejo diferente).
4. Listar as provas de diferenciação: factos verificáveis que respondem "porquê tu" (gap resolvido, garantia real, bundle, mecanismo do produto) e cruzar cada uma com as objeções que neutraliza.
5. Verificar honestidade: remover qualquer diferenciador que não tenha prova real — positioning inflado destrói a conta de anúncios e a confiança na página.
6. Confirmar coerência com a classificação do produto (brief seção 2): high-consideration pede mecanismo e prova; low-stakes pede benefício visual direto.
7. Delegar ao Hermes (secção "Delegação Hermes") para as versões de redação; o offer-strategist escolhe a versão final, grava o positioning-doc e o bloco no brief.

## Validation
- Proposta de valor cabe em uma frase e menciona resultado + diferenciador + público.
- Diferenciador principal tem prova verificável registada (sem prova, fora).
- 2–3 ângulos alternativos distinguíveis entre si e testáveis em criativos.
- Cada objeção principal do avatar tem uma prova de diferenciação que a responde.
- Coerente com classificação high-consideration/low-stakes e com a oferta real.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o offer-strategist redige manualmente a partir do gap central e dos desejos ranqueados.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: revisão humana; validar cada claim de diferenciação contra uma fonte real antes de gravar.
- Gap central inexistente (concorrência sem fraquezas exploráveis): escalar ao operador com a matriz — pode ser sinal de nicho saturado; não inventar diferenciação.

## Checklist
- [ ] Gap central identificado a partir da matriz de concorrentes
- [ ] Proposta de valor em 1 frase (resultado + diferenciador + público)
- [ ] Ângulo principal + 2–3 alternativos definidos
- [ ] Provas de diferenciação com fonte verificável
- [ ] Cada objeção principal cruzada com uma prova
- [ ] Coerência com classificação do produto (seção 2) confirmada
- [ ] Positioning-doc gravado e bloco no brief atualizado

## Delegação Hermes
- slug sugerido: growth-create-positioning-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-positioning.prompt.md (gap central, desejos ranqueados, objeções, provas reais, ângulos a redigir)
- comando: bash workflows/executors/hermes-exec.sh -t growth-create-positioning-<slug> -f /tmp/aiox-prompts/<slug>-positioning.prompt.md -d /root/homefy -T 15
- timeout sugerido: 15 min
- leitura do result.json: campo "status" — SUCCESS (selecionar versões finais e gravar), PARTIAL (revisão humana das redações), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
