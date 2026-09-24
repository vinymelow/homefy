# Agents do Ecommerce Growth Squad

Os 10 agents do squad `ecommerce-growth` (manifest: `squads/ecommerce-growth/squad.yaml`,
arquivos em `squads/ecommerce-growth/agents/`). Eles são especialistas de
domínio orquestrados pelo AIOX e executados via Hermes (ver
`docs/hermes-integration.md`).

## Princípio de autoridade separada

Cada tipo de decisão pertence a um único papel — nenhum agente acumula
autoridade fora do seu domínio:

| Decisão | Autoridade |
|---|---|
| Pesquisa de mercado/produto, dados, evidências | research agents (market-researcher, product-researcher) |
| Copy, mensagens, headlines, claims de texto | copywriter |
| Arquitetura de página, UX, spec visual | ux-designer |
| Código: HTML/Liquid/Shopify, integrações técnicas | shopify-engineer |
| Veredito de qualidade: QA PASS/FAIL, gates | qa-specialist |
| Orquestração: escolher a próxima task, compor a cadeia | ecommerce-master |

Cro-specialist e creative-director têm autoridade técnica de auditoria (CRO e
criativos, respectivamente), mas o veredito final de qualidade é sempre do
qa-specialist, e a decisão de orquestração é sempre do ecommerce-master.

## Os 10 agents

| Agent | Papel | Autoridade | Handoffs |
|---|---|---|---|
| **ecommerce-master** | Orquestrador do squad. Seleciona tasks, monta a cadeia (pesquisa → oferta → copy → página → QA), decide retry/halt com base no `result.json` | Orquestração e priorização; não executa produção | Upstream: operador humano. Downstream: todos os specialists; recebe vereditos do qa-specialist |
| **market-researcher** | Pesquisa de mercado e nicho: tendências, demanda, sinais de concorrentes (ex.: Winning Hunter, ad libraries) | Evidências de mercado; não define oferta nem copy | Upstream: ecommerce-master / product-brief. Downstream: product-researcher, offer-strategist |
| **product-researcher** | Pesquisa de produto: análise do candidato, fornecedores, referências (landers), viabilidade | Dados e referências do produto | Upstream: ecommerce-master / market-researcher. Downstream: offer-strategist, ux-designer (referências) |
| **offer-strategist** | Estratégia de oferta e posicionamento: preço, bundle, garantia, ângulo, avatar | Arquitetura da oferta (dados reais do brief; nunca inventar preços/garantias) | Upstream: research agents. Downstream: copywriter, creative-director |
| **copywriter** | Copy da página e mensagens: headline, bullets, CTA, seções de objeção | Todo texto de venda; claims só com base no brief aprovado | Upstream: offer-strategist. Downstream: ux-designer (copy vai para a spec), qa-specialist |
| **ux-designer** | Spec da landing page: estrutura de seções, hierarquia mobile-first, slots de criativo | Arquitetura da página e spec visual; não escreve código final nem copy | Upstream: copywriter + referências do product-researcher. Downstream: shopify-engineer |
| **shopify-engineer** | Implementação: HTML da landing page, conversão para Liquid/Shopify, integrações via API | Código e assets técnicos; não publica sem aprovação humana | Upstream: ux-designer. Downstream: qa-specialist |
| **creative-director** | Brief e direção de criativos: ângulos, slots, clonagem de ads de referência, QC de imagens/vídeos | Direção criativa e QC de criativos | Upstream: offer-strategist / product-brief. Downstream: qa-specialist, operador (aprovação de publicação) |
| **cro-specialist** | Auditoria CRO: funil, fricção, objeções, propostas de teste A/B | Diagnóstico CRO e recomendações; não aplica mudanças sozinho | Upstream: página publicada em ambiente de teste / qa. Downstream: ux-designer, shopify-engineer, ecommerce-master |
| **qa-specialist** | Veredito de qualidade: checklists (copy, ux, shopify, performance, cro, launch), smoke tests, QA PASS/FAIL | Gates de qualidade — único agente que emite PASS/FAIL; bloqueia avanço e publicação | Upstream: qualquer producer (copywriter, ux-designer, shopify-engineer, creative-director). Downstream: ecommerce-master (retry/halt), operador humano |

## Regras comuns a todos os agents

1. **Segurança e segredos.** Nunca ler, exibir ou transcrever valores de
   `ecom-stack/config/.env` ou de `~/.hermes/`; usar apenas placeholders em
   qualquer artefato. Não aceder à rede além do necessário para a task (a task
   `smoke-test-project-structure` é explicitamente só leitura local).
2. **Claims de e-commerce.** Nunca inventar preços, descontos, garantias,
   prazos de envio ou prova social — tudo deve derivar do Product Brief
   aprovado. Claims sem evidência são reprovados no gate de QA.
3. **Governança.** Respeitar os limites de `modelGovernance` (budget, max
   iterations, timeouts, checkpoints) e o contrato do executor: cada task vira
   um run com `result.json`, e um status diferente de `SUCCESS` segue a
   política de retry/halt (ver `docs/workflows.md`).
4. **Escopo.** Ficar dentro da própria autoridade: research não escreve copy,
   copywriter não altera código, ninguém além do qa-specialist emite veredito,
   e **nenhum agente publica** em Shopify/Meta/TikTok — publicação exige
   aprovação humana explícita (regra crítica do `AGENTS.md`).
5. **Artefatos.** Produzir saída no formato esperado pelo consumidor downstream
   (templates em `squads/ecommerce-growth/templates/`) e registrar o run em
   `.aiox/external-runs/` para auditoria.
