# Task: create-offer

task: criarOferta()
responsavel: offer-strategist
responsavel_type: Agente
atomic_layer: Organism

## Purpose
Construir a oferta comercial do produto: bundles 1/2/3 com âncoras de preço, painel
de oferta grátis (apenas se REAL — nunca inventar gifts), garantia alinhada com a
política real da loja e mecanismo de risk reversal. A oferta é o que transforma
tráfego pago em margem: decide se o produto sobrevive a €20–50/dia de teste.

## Entrada
- product_brief (ecom-stack/templates/product-brief.md — consome seções 1, 2 e 3; produz seção 5 completa)
- política de devolução e garantia da loja Shopify (Settings → Policies — confirmada pelo operador; verificável com `python3 ecom-stack/cli/cli.py doctor` para acesso à loja)
- dados de custo: custo do produto + envio por unidade (fornecedor, registado no tracker)
- competitors-report: ecom-stack/research/landers/<slug>-competitors.md (ofertas e preços da concorrência)
- template: squads/ecommerce-growth/templates/offer-brief.md
- método: ecom-stack/docs/metodo-pesquisa.md Parte 0 item 4 (verificar o dinheiro primeiro: CPA máximo)

## Saida
- offer-brief: ecom-stack/research/landers/<slug>-offer.md (formato squads/ecommerce-growth/templates/offer-brief.md)
- brief seção 5 preenchida: Bundle 1/2/3 (preço e riscado), painel grátis (só se real), garantia em dias
- CPA máximo e margem por bundle documentados
- Produz no brief: seção 5 (oferta e bundles)

## Procedure
1. Confirmar os números base do brief seção 1: preço de venda, preço riscado, custo do produto + envio, margem estimada. Sem custo real de fornecedor, não avançar — pedir ao operador.
2. Calcular a economia: margem por unidade = preço − custo − envio − taxas; CPA máximo = margem − margem de segurança (ex.: AOV $69, margem $39 → CPA máx ~ $20). Verificar se sobrevive a €20–50/dia de teste com AOV $25–70.
3. Desenhar 3 bundles com desconto crescente por unidade: Bundle 1 (1 unidade — entrada), Bundle 2 (mais popular — âncora principal), Bundle 3 (melhor valor — maior desconto por unidade). Preços riscados só quando o preço riscado é uma referência real e defensável.
4. Painel de oferta grátis ("INCLUDED WITH THIS PURCHASE"): incluir APENAS itens confirmados como reais com o fornecedor ou já existentes na loja — caso contrário, remover o painel por completo (regra dura: nunca inventar gifts). Valor riscado só com base real.
5. Garantia: copiar os dias exatos da política de devolução da loja (Settings → Policies); a garantia prometida nunca excede a política real e tem de bater certo em TODOS os frames e secções da página.
6. Risk reversal: escrever a caixa de garantia (risco zero acima do CTA final) respondendo à maior objeção de compra do avatar principal.
7. Conferir cada objeção da seção 3 contra a oferta: preço (bundle), confiança (garantia), envio (prazo prometido) — a oferta responde objeções, não só desconta.
8. Delegar ao Hermes (secção "Delegação Hermes") para redigir o offer-brief; revisar os números contra o brief e gravar; atualizar a seção 5 do brief.
9. Fazer a passagem de consistência: preço, riscado, garantia e prazo iguais em bundle 1/2/3, painel grátis e caixa de garantia.

## Validation
- Margem do bundle popular ≥ 25% após produto + envio (alvo do blueprint §7); margem mínima > 15% nos demais.
- Garantia em dias idêntica à política real da loja (fonte: Settings → Policies, confirmada com operador).
- Painel grátis: 0 itens inventados — cada item tem confirmação real registada.
- CPA máximo documentado e coerente com o plano de teste de €20–50/dia.
- Consistência total: mesmos preços/garantia/prazo em todos os pontos do offer-brief.
- Seção 5 do brief preenchida e pronta para create-copy e create-page-spec.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, o offer-strategist redige o offer-brief manualmente a partir dos números confirmados.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: revisão humana obrigatória dos números antes de gravar; um valor comercial errado na oferta é defeito bloqueante.
- Política de garantia não confirmada pelo operador: BLOQUEAR a task — não escrever dias de garantia sem fonte; escalar ao operador.
- Custo de fornecedor ausente: BLOQUEAR — sem custo real não há CPA máximo; devolver a research-product.

## Checklist
- [ ] Números base confirmados (preço, custo, envio, taxas) com fonte
- [ ] Margem e CPA máximo calculados por bundle
- [ ] 3 bundles com desconto crescente e preços riscados defensáveis
- [ ] Painel grátis com itens 100% reais (ou removido por completo)
- [ ] Garantia idêntica à política real da loja, com fonte
- [ ] Caixa de risk reversal respondendo à maior objeção do avatar
- [ ] Cada objeção da seção 3 respondida por um elemento da oferta
- [ ] Passagem de consistência feita (preço/garantia/prazo iguais em tudo)
- [ ] Seção 5 do brief preenchida e offer-brief gravado

## Delegação Hermes
- slug sugerido: growth-create-offer-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-offer.prompt.md (números confirmados + objeções + política de garantia + estrutura do offer-brief)
- comando: bash workflows/executors/hermes-exec.sh -t growth-create-offer-<slug> -f /tmp/aiox-prompts/<slug>-offer.prompt.md -d /root/homefy -T 20
- timeout sugerido: 20 min
- leitura do result.json: campo "status" — SUCCESS (conferir cada número contra o brief e gravar), PARTIAL (revisão humana dos valores), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
