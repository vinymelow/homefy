# Guia prático — usar o ecom-stack no dia a dia

Fluxo completo de trabalho, do zero até ao primeiro produto publicado. Cada fase diz **o que fazes tu**, **o que faço eu** (Kimi) e **os comandos**.

## Visão geral do ciclo

```
Fase 1  Pesquisa (Winning Hunter) ──► brief do produto
Fase 2  Landing page (eu gero, tu publicas no tema duplicado)
Fase 3  Criativos (slots da landing + anúncios)
Fase 4  Campanha (Ads Manager manual, €20–50/dia × 3 dias)
Fase 5  Ler métricas ──► matar (CPA>€35) ou escalar (CPA<€15) ──► voltar à Fase 1
```

---

## Fase 1 — Pesquisa e brief (tu)

1. No Winning Hunter → **Landers** → filtra por nicho (casa/utilidades ou beleza) + países US/CA/AU/NZ/UK → ordena por receita
2. Escolhe 1 produto: anúncios ativos há 30+ dias, preço €20–70, loja com tráfego
3. Identifica as **3 referências**: homepage da loja concorrente + melhor PDP + melhor hero section
4. Cria o brief — duas formas, igualmente válidas:
   - **Dashboard web** (mais fácil): `python3 dashboard/server.py` → abre `http://IP_DO_VPS:8000/?key=CHAVE` no browser → wizard "Novo brief" → preenches o formulário e grava direto em `research/landers/`
   - **CLI**: `python3 cli/cli.py brief novo nome-do-produto` → cria o ficheiro vazio a partir do template, preenches no editor

5. Preenches o brief — **a forma mais fácil de editar ficheiros no VPS é o VS Code Remote-SSH** (ver caixa abaixo)
6. Envia-me o brief (cola o conteúdo aqui no chat ou faz upload do ficheiro) + as 3 URLs

> **Dica essencial — VS Code Remote-SSH:** instala a extensão "Remote - SSH" no teu VS Code (ícone verde canto inferior esquerdo → Connect to Host → `root@179.198.193.119`). O VS Code abre a pasta `/root/ecom-stack` diretamente — editas briefs, configs e vês ficheiros como se fossem locais, sem scp nem nano. Passa a usar isto para toda a edição.

## Fase 2 — Landing page (eu gero, tu publicas)

1. Eu gero a landing page preenchida a partir do `templates/landing-page.html` + brief + referências (aqui no chat, ficheiro pronto)
2. Tu substituis no VPS (com o Remote-SSH é só colar no ficheiro) e validas abrindo o HTML no browser
3. **Publicação na Shopify** (primeira vez, manual):
   - Shopify Admin → **Online Store → Themes** → ⋯ no tema MAIN → **Duplicate** (regra de ouro: nunca escrever no MAIN)
   - No tema duplicado → **Customize / Edit code** → criar uma nova **page template** (JSON) + secções Liquid, colando os blocos da landing page
   - Ou via API com `curl` (quando quiseres automatizar: o token do `.env` permite criar assets no tema duplicado)
4. Revisão mobile (390px) no preview do tema → publica o tema duplicado só quando a página estiver certa

## Fase 3 — Criativos (eu gero, tu aprovas)

1. Eu gero as imagens/vídeos para cada slot do brief (hero-main, angle-1..3, lifestyle, infographic, ugc-video…) com as regras do `docs/metodo-criativos.md`
2. Tu fazes QC: texto dentro das safe zones, claims suavizadas, produto idêntico ao real
3. Guardas em `assets/creatives/` — os nomes têm de casar com os slots da landing page

## Fase 4 — Campanha (tu, manual por agora)

1. Meta Ads Manager: campanha de conversões (Purchase), 3–5 criativos, US/CA/AU/NZ/UK, orçamento €20–50/dia × 3 dias
2. TikTok Ads Manager: idem (ou começa só por uma plataforma se o orçamento for apertado)
3. Pixel verificado a disparar (teste de compra com o Shopify Bogus Gateway antes de lançar)

## Fase 5 — Decisão (tu, no fim do dia 2–3)

| Métrica | Ação |
|---|---|
| CTR < 1% ao fim do dia 2 | **Mata** — criativo não prende atenção |
| CPA > €35 sem compras | **Mata** — oferta/página não converte |
| CPA < €15 | **Escala** — +20% orçamento/dia |
| CPA €15–35 | Mantém + testa 2 criativos novos |

Depois: volta à Fase 1 com o próximo produto. O `python3 cli/cli.py anuncio plano <slug>` imprime este plano sempre que precisares.

## Comandos de rotina (no VPS)

```bash
python3 cli/cli.py status          # estado geral do projeto
python3 cli/cli.py doctor          # ligação à Shopify ok?
python3 cli/cli.py brief listar    # briefs existentes
python3 cli/cli.py anuncio plano <slug>   # plano de teste do produto
```

## O que ainda não está automatizado (por decisão)

- **Publicação no tema** — primeira vez é manual (duplicar + edit code); automatiza-se quando o fluxo estiver maduro
- **Meta/TikTok Ads** — manual no Ads Manager até ~€50/dia; a API entra na fase de escala
- **Criativos via CLI** — o comando `criativo` é um esqueleto; a geração real faz-se aqui no chat (eu gero, tu aprovas)
