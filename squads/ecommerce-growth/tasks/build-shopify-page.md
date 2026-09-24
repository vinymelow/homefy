# Task: build-shopify-page

task: construirPaginaShopify()
responsavel: shopify-engineer
responsavel_type: Agente
atomic_layer: Page

## Purpose
Converter o landing-page-spec (e a página estática aprovada) em implementação Shopify:
seções Liquid com schema válido, template JSON de produto, snippets e assets com
prefixo único, tudo editável no Theme Editor e nada hard-coded. A task PREPARA o
pacote completo com instruções de atribuição; a publicação só acontece após aprovação
humana explícita (publish_requires_human_approval: true no squad.yaml).

## Entrada
- product_brief (ecom-stack/templates/product-brief.md — REQUER seção 1: URL do produto no Shopify; sem ela a task não inicia)
- landing-page-spec: ecom-stack/research/landers/<slug>-page-spec.md
- página estática validada: ecom-stack/templates/<slug>.html (output de build-landing-page)
- ligação à loja: `python3 ecom-stack/cli/cli.py doctor` (verifica .env e ligação Shopify)
- master prompt: ecom-stack/prompts/loja-completa.md PASSO 4 (regras NON-NEGOTIABLE de implementação)
- checklists: squads/ecommerce-growth/checklists/shopify.md e performance.md

## Saida
- pacote Liquid/JSON: ficheiros de secções (sections/<slug>-*.liquid), snippets (snippets/<slug>-*.liquid), assets (assets/<slug>-*.css/js) e templates/product.<slug>.json — em .aiox/external-runs/<run>/artifacts/
- instruções de instalação: ecom-stack/research/landers/<slug>-shopify-prep.md (ficheiros criados, ordem de upload, atribuição do template ao produto via template_suffix)
- relatório de validação de sintaxe e de responsividade
- Entrada para: audit-shopify (validação técnica no tema duplicado)

## Procedure
1. Pré-check duro: confirmar a URL do produto no brief (seção 1) e a ligação à loja com `python3 ecom-stack/cli/cli.py doctor`. Se a URL falta, halt e devolver ao operador — o produto tem de existir na loja antes do Liquid.
2. Confirmar que a página estática passou na audit-page; divergências de guardrails bloqueiam a conversão.
3. Duplicar o tema live ANTES de qualquer escrita (regra de ouro: nunca escrever no MAIN; re-duplicar após cada publish). A duplicação é executada pelo operador ou via Admin API com o token do .env — registando live_theme_id e draft_theme_id.
4. Gerar uma secção Liquid por módulo do spec, com schema válido e presets: nada de merchant-facing hard-coded — headings, preços, bundles, garantia, reviews, FAQ e imagens vêm de section settings, blocks, metafields e do objeto product ao vivo.
5. Manter header, announcement bar, footer, navegação, cart drawer e fontes do tema EXATAMENTE como estão; a página renderiza dentro do layout normal do tema (sem {% layout none %}, sem header/footer duplicados, sem fontes novas).
6. Arquitetura OS 2.0 nativa: JSON templates, snippets partilhados, CSS/JS scoped com prefixo único do slug; sem React/Vue/Tailwind/page builders/jQuery.
7. Comércio real: variant switching, preços ao vivo, product form nativo, refresh do cart drawer, sticky mobile ATC, quantity rules — sem carrinho fake. Botões usam AJAX add-to-cart com fallback para /cart.
8. Validar sintaxe de cada ficheiro (Theme Check se disponível no ambiente; caso contrário revisão estrutural + validação de schema: nomes de secção ≤ 25 caracteres, ids de settings únicos, defaults não vazios, max_blocks ≤ 50, block.shopify_attributes em todos os blocos).
9. Preparar o template product.<slug>.json com as secções na ordem do spec e escrever as instruções de atribuição (template_suffix no produto); listar a ordem de upload (assets primeiro, secções em lotes de 3–5, template por último).
10. Entregar o pacote em .aiox/external-runs/<run>/artifacts/ + o prep doc ao operador. PUBLICAÇÃO = aprovação humana explícita primeiro; a task termina no pacote pronto para preview no tema duplicado.

## Validation
- Theme Check (ou revisão estrutural equivalente) sem erros de sintaxe Liquid.
- Teste de nada hard-coded descrito no prep doc: mudar o preço no admin tem de mudar a página; trocar imagem no Theme Editor tem de trocar na página.
- Header/footer/cart drawer reais presentes no preview (desktop e mobile).
- Secções reordenáveis e editáveis no Theme Editor (settings, blocks e metafields).
- Responsivo 320–430px sem overflow, alvos ≥ 44px, safe-area insets.
- Zero escrita no tema MAIN; tema alvo é sempre um duplicado.

## Failure handling
- TIMEOUT: repetir 1 vez com timeout 50% maior; persistindo, entregar as secções já geradas com a lista das pendentes no prep doc.
- FAILED/REJECTED: halt — escalar ao operador com o hermes.log.
- PARTIAL: não entregar pacote incompleto; completar as secções em falta antes de fechar o prep doc.
- Doctor falhar (sem .env ou token inválido): BLOQUEAR — seguir ecom-stack/docs/integracoes-cli.md com o operador; nenhuma chamada à API sem credenciais válidas.
- Tema não OS 2.0: escalar ao operador com a alternativa de page fallback (página /pages/<slug> com metafields) descrita em prompts/loja-completa.md.

## Checklist
- [ ] URL do produto no brief confirmada (seção 1) e doctor OK
- [ ] Tema duplicado (nunca MAIN); ids do live e do draft registados
- [ ] Uma secção Liquid por módulo do spec, com schema válido e presets
- [ ] Zero valores comerciais hard-coded (settings/blocks/metafields/product)
- [ ] Header/footer/fonts/cart drawer do tema intocados
- [ ] Sticky mobile ATC e variant switching funcionais (AJAX + fallback)
- [ ] Sintaxe validada (Theme Check ou revisão estrutural documentada)
- [ ] templates/product.<slug>.json na ordem do spec + instruções de atribuição
- [ ] Pacote em .aiox/external-runs/<run>/artifacts/ + prep doc gravado
- [ ] Nenhuma publicação: aguardando aprovação humana explícita

## Delegação Hermes
- slug sugerido: growth-build-shopify-<slug>
- prompt file: /tmp/aiox-prompts/<slug>-shopify.prompt.md (spec + página estática + master prompt do PASSO 4 de loja-completa.md + regras de schema + proibição explícita de publicar)
- comando: bash workflows/executors/hermes-exec.sh -t growth-build-shopify-<slug> -f /tmp/aiox-prompts/<slug>-shopify.prompt.md -d /root/homefy -T 45
- timeout sugerido: 45 min
- leitura do result.json: campo "status" — SUCCESS (validar sintaxe e fechar o pacote), PARTIAL (completar ficheiros em falta), FAILED/TIMEOUT (failure handling acima), REJECTED (corrigir pré-check e reenviar)
