---
name: product-research
description: Validar um produto candidato em profundidade — reviews 1–3★ dos concorrentes, pain points reais, economia do teste (margem e CPA máximo) e veredito GO/NO-GO (GREEN/AMBER/RED) antes de investir em landing page e criativos.
when_to_use: Passagem 2 (deep dive) sobre um candidato que passou o gate ≥70 da passagem 1, ou sempre que for preciso decidir TEST/SKIP num produto específico.
---

# Validação de produto — deep dive e GO/NO-GO

## Quando usar

- Deep dive de um candidato da shortlist (score ≥70).
- Decisão TEST/SKIP antes de preencher o product brief ou gastar orçamento de teste.
- Conta gastar 2–4 passagens 2 até ao primeiro GREEN — é o método a proteger de produtos maus, não falha do processo.

## Pré-requisitos

- Candidato escolhido da shortlist com score e evidências no `ecom-stack/research/tracker.md`.
- URLs das 3 lojas concorrentes principais e dados de spend (ad library / Winning Hunter).
- Estimativa de custo do produto + envio (fornecedor: USA Drop/CJ/Zendrop/AliExpress) e AOV alvo.

## Procedimento

1. **Reviews 1–3★ das 3 lojas concorrentes principais:** listar as 5 queixas mais frequentes com citações. Cada queixa é um ângulo de anúncio ou uma objeção a responder na landing page.
2. **Economia do teste:** com custo estimado + envio e AOV, calcular margem e CPA máximo (ex.: AOV $69, margem $39 → CPA máx ~$20). Verificar se sobrevive a €20–50/dia de teste.
3. **Compliance:** confirmar ausência de claims de saúde proibidos, marcas registadas e restrições de anúncio no nicho.
4. **Veredito GREEN / AMBER / RED com razões:** o que se gosta, o que não se gosta, riscos. Se não se recomenda, dizer claramente "não anunciava".
5. **Decisão GO/NO-GO:**
   - GREEN → preencher `ecom-stack/templates/product-brief.md` (secções 1b/1c incluídas) e seguir para landing page.
   - AMBER/RED → voltar ao tracker e escolher o próximo candidato ≥70.

## Outputs

- As 5 queixas mais frequentes com citações (alimenta objeções do brief, secção 3).
- Cálculo de margem + CPA máximo registado no tracker.
- Veredito explícito GREEN/AMBER/RED com razões — o veredito é o output principal.
- Em GREEN: `research/landers/<slug>-brief.md` preenchido a partir do template.

## Referências

- `ecom-stack/prompts/pesquisa-produto.md` — prompt de análise do concorrente (secção 2) e regras de registo (secção 3).
- `ecom-stack/docs/metodo-pesquisa.md` — Parte 3 (passagem 2) e veredito GREEN/AMBER/RED.
- `ecom-stack/templates/product-brief.md` — contrato a preencher em GREEN.
- `ecom-stack/research/landers/TEMPLATE-lander.md` — ficha por candidato.
- `skills/research/ecommerce-research.md` — passagem 1 que precede esta skill.

## Guardrails

- "Não anunciava" é um veredito legítimo e deve ser dito explicitamente — sem hesitação por empatia.
- Citações reais das reviews; nunca paráfrase inventada.
- Números de economia antes de emoção: CPA máximo calculado, não assumido.
- Sem evidência de spend (3+ anúncios ativos há 30+ dias) a prova de procura fica comprometida — sinalizar no veredito.
