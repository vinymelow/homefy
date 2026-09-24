# Knowledge Map — Squad ecommerce-growth

> Mapa do conhecimento existente no Homefy → consumidores do squad.
> **REGRA: referências, não cópias.** Os artefactos do squad apontam para estes
> caminhos; nada é duplicado para dentro do squad (exceção: os templates do
> squad, que são versões de trabalho referenciando a fonte canônica).
> Atualizado em 24/09/2026.

| Conhecimento (caminho) | Tipo | Usado por (agents/tasks/templates) | Como |
|---|---|---|---|
| `ecom-stack/prompts/pesquisa-produto.md` | Prompt (pesquisa) | tasks: `research-product`, `research-market`, `analyze-competitors` · agents: `market-researcher`, `product-researcher` · template: `research-report.md` | Filtros do Winning Hunter (Landers), prompt de análise do concorrente e regras de registo; alimenta a passagem 1/2 do método |
| `ecom-stack/prompts/pagina-vendas.md` | Prompt (página) | tasks: `create-page-spec`, `build-landing-page` · agents: `ux-designer`, `copywriter` · template: `landing-page-spec.md` | Prompt base para gerar a landing page a partir do product-brief preenchido; hard requirements (mobile-first, CTA único, ordem das secções, slots nomeados) |
| `ecom-stack/prompts/loja-completa.md` | Prompt (cadeia loja) | tasks: `build-shopify-page` · agents: `shopify-engineer` · template: `landing-page-spec.md` | Cadeia homepage + PDP + master prompt de publicação no Shopify (OS 2.0, nada hard-coded, tema duplicado) |
| `ecom-stack/prompts/criativos.md` | Prompt (criativos) | task: `generate-creative-brief` · agents: `creative-director` · template: `creative-brief.md` | Prompts base por tipo de slot (hero, lifestyle, infográfico, ângulo), 3 formatos de vídeo 9:16 (A/B/C), regras de consistência |
| `ecom-stack/docs/blueprint-pagina-de-vendas.md` | Método/blueprint | tasks: `create-copy`, `create-page-spec`, `audit-page`, `audit-cro` · agents: `copywriter`, `ux-designer`, `cro-specialist` · templates: `landing-page-spec.md`, `launch-report.md` | Filosofia das 3 referências, sistema visual da galeria, ordem das 17 secções, 5 correções de copy, guardrails, métricas de validação (kill/scale) |
| `ecom-stack/docs/metodo-criativos.md` | Método/SOP | task: `generate-creative-brief` · agents: `creative-director` · template: `creative-brief.md` | SOP de produção: clonagem zona-a-zona, 5 chaves de hiper-realismo, classificação high/low-stakes, 6 arquétipos de infográfico, QC por contact sheet |
| `ecom-stack/docs/metodo-pesquisa.md` | Método/SOP | tasks: `research-product`, `research-market` · agents: `market-researcher`, `product-researcher` · template: `research-report.md` | Método evidence-based: 4 fundamentos, score do gate ≥70/100 (5 dimensões), passagem 1 (shortlist) e passagem 2 (deep dive), economia do teste |
| `ecom-stack/docs/guia-uso.md` | SOP operacional | tasks: `prepare-launch`, `smoke-test-project-structure` · agents: `ecommerce-master` | Fluxo dia a dia das 5 fases (pesquisa → página → criativos → campanha → decisão), comandos de rotina, VS Code Remote-SSH |
| `ecom-stack/docs/setup-vps.md` | SOP infra | agents: `shopify-engineer`, `qa-specialist` · task: `audit-shopify` | Setup das integrações (Shopify obrigatória; Meta/TikTok adiadas), scopes da Admin API, regra MAIN read-only, checklist de integrações |
| `ecom-stack/docs/integracoes-cli.md` | Referência técnica | agents: `shopify-engineer` · tasks: `build-shopify-page`, `audit-shopify` | O que é real vs. esqueleto nas integrações da CLI; consulta quando uma API falhar |
| `ecom-stack/templates/product-brief.md` | Template (CONTRATO CENTRAL) | TODAS as tasks e agents — contrato de entrada do workflow | Fonte canônica do Product Brief; o squad usa `squads/ecommerce-growth/templates/product-brief.md` (mesmas 9 secções + outputs do squad, com cabeçalho de referência) |
| `ecom-stack/templates/landing-page.html` | Template (código) | tasks: `build-landing-page`, `build-shopify-page` · agents: `ux-designer`, `shopify-engineer` · template: `landing-page-spec.md` | Padrão visual/estrutura real das landing pages (13 secções + sticky ATC, slots nomeados) — base da spec e da conversão Liquid |
| `ecom-stack/templates/escova-alisadora.html` | Exemplo real (código) | agents: `ux-designer`, `shopify-engineer` | Landing page real preenchida (low-stakes, beleza) — referência de como os slots ficam com conteúdo |
| `ecom-stack/research/landers/TEMPLATE-lander.md` | Template | tasks: `research-product`, `analyze-competitors` | Ficha de análise do lander (3 referências, notas mobile 390px, veredito) |
| `ecom-stack/research/landers/escova-alisadora-brief.md` | Exemplo real | agents: todos (contexto de produto) | Product Brief preenchido real — exemplo de brief low-stakes aprovado |
| `ecom-stack/research/tracker.md` | Tracker | tasks: `research-product`, `prepare-launch` · template: `research-report.md` | Product validator: shortlist com scores, deep dives (GREEN/AMBER/RED), evidence log (link + data) — registo obrigatório dos candidatos |
| `ecom-stack/skills/clone-static-ad.md` | Skill | agent: `creative-director` · template: `creative-brief.md` | Clonagem de ads estáticos vencedores (dissecação zona-a-zona, 3 variantes, guardas de fiabilidade) — método dos `static-ads-*` |
| `ecom-stack/skills/hyperreal-image.skill` | Skill | agent: `creative-director` · templates: `creative-brief.md` | Geração de imagens hiper-realistas — origem das 5 chaves (lifestyle/UGC) |
| `ecom-stack/skills/product-pdp-image-builder.skill` | Skill | agent: `creative-director` · templates: `creative-brief.md`, `landing-page-spec.md` | Galeria PDP método EcomAlchemist — sequência de frames high/low-st consideration, 6 arquétipos de infográfico |
| `ecom-stack/skills/clone-link-to-my-shopify.skill` | Skill | agent: `shopify-engineer` · task: `build-shopify-page` | Clonar qualquer página para Shopify via transcrição secção a secção em Liquid editável |
| `ecom-stack/skills/branded-shopify-store-builder.md` | Skill | agents: `ux-designer`, `shopify-engineer` | Módulos branded opcionais (press bar, donuts, carrossel de reviews) para quando o produto escalar |
| `ecom-stack/cli/cli.py` | CLI (Python) | tasks: `prepare-launch` (anuncio plano), `smoke-test-project-structure`, `research-product` (brief novo) | Ponto de entrada operacional: status, brief novo/listar, criativo (esqueleto), `anuncio plano <slug>` (plano de teste do launch-report), doctor, painel |
| `skills/` (raiz: copywriting/ creative/ cro/ ecommerce/ research/ shopify/ + skills avulsas) | Skills por domínio | agents correspondentes ao domínio (copywriter→copywriting, creative-director→creative, cro-specialist→cro, ...) | Espelho de `ecom-stack/skills/` organizado por domínio; diretórios por domínio são staging para skills novas do squad |
| `workflows/executors/hermes-exec.sh` | Script (ponte de execução) | workflows do squad · task: `smoke-test-project-structure` | Único caminho de execução delegada AIOX → Hermes; contrato de artefactos em `.aiox/external-runs/` e de status SUCCESS/PARTIAL/FAILED/TIMEOUT/REJECTED |
| `.aiox-core/` (core-config.yaml, schemas/, development/) | Framework/governança | todo o squad (via squad.yaml + validate-squad.js) | Orquestração AIOX: manifest schema, validação do squad, modelGovernance (orçamento/timeouts), source of truth dos agents para as projeções de IDE — não editar à mão |
| `AGENTS.md` + `README.md` (raiz) | Regras/arquitetura | todos os agents | Regras críticas (segredos, MAIN read-only, ecom-stack intocável, execução via hermes-exec, deploy só com aprovação) e visão AIOX → Hermes |

## Notas de uso
- Caminhos relativos à raiz do repo (`/root/homefy`). Nada da lista acima deve
  ser copiado para dentro do squad — citar o caminho no artefacto.
- Evidência de pesquisa (links + datas) regista-se em
  `ecom-stack/research/tracker.md`, nunca em cópias locais.
