# Ecom Stack — Loja Shopify reativada (dropshipping assistido por IA)

Projeto para relançar a loja Shopify depois de 3 anos, com pesquisa de produtos no
Winning Hunter, landing pages geradas com Kimi Code, criativos gerados por IA e
testes de anúncios em **US · CA · AU · NZ · UK**.

Nichos em foco: **casa & utilidades** + **beleza & cuidados pessoais**.
Orçamento de teste: **€20–50/dia por produto, 3 dias por teste.**

## Arquitetura do projeto

```
ecom-stack/
├── README.md                     ← este ficheiro
├── docs/
│   ├── blueprint-pagina-de-vendas.md   ← estrutura da página (método do vídeo)
│   ├── metodo-criativos.md            ← SOP de criativos (síntese dos docs do tutor)
│   ├── integracoes-cli.md             ← o que é real: APIs vs "CLIs"
│   └── tutor/                         ← material original do tutor (referência)
│       ├── How To Build Your Store (STEP BY STEP GUIDE).docx
│       ├── clone-static-ad.md
│       └── branded-shopify-store-builder.md
├── skills/                       ← skills do tutor, prontas a instalar no teu agente
│   ├── clone-link-to-my-shopify/     ← clonar qualquer página para o Shopify
│   ├── hyperreal-image/              ← imagens hiper-realistas (5 chaves)
│   └── product-pdp-image-builder/    ← galeria PDP método EcomAlchemist
├── research/
│   └── landers/                  ← referências do Winning Hunter (3 por produto)
│       └── TEMPLATE-lander.md
├── templates/
│   ├── landing-page.html         ← template base mobile-first (este projeto)
│   └── product-brief.md          ← preencher por produto antes de gerar a página
├── prompts/
│   ├── pesquisa-produto.md       ← prompts de análise de concorrentes
│   ├── pagina-vendas.md          ← prompt para gerar a landing page
│   ├── loja-completa.md          ← cadeia completa: homepage + PDP + publicação
│   └── criativos.md              ← prompts de imagem/vídeo para ads
├── cli/
│   └── cli.py                    ← comando único: python3 cli/cli.py <comando>
├── config/
│   └── config.example.env        ← copiar para .env e preencher credenciais
└── assets/creatives/             ← imagens e vídeos gerados
```

## O fluxo de trabalho (ordem de execução)

**Fase 1 — Pesquisa (tu, com Winning Hunter)**
1. Winning Hunter → Landers → filtrar por nicho → anotar páginas com receita estimada alta.
2. Para cada produto candidato, escolher 3 referências: melhor homepage, melhor landing
   page, melher hero section (mobile!). Registar em `research/landers/TEMPLATE-lander.md`.
3. Ver ad library dos concorrentes filtrado por maior spend → guardar os melhores criativos.

**Fase 2 — Página de vendas (Kimi Code)**
4. Preencher `templates/product-brief.md` com os dados do produto e as 3 referências.
5. Página única: usar o prompt em `prompts/pagina-vendas.md`.
   Loja completa (homepage + PDP + publicação): usar a cadeia em
   `prompts/loja-completa.md` — é o método exato do guia passo-a-passo do tutor
   (caso Flovir: produto $100K/mês, homepage de pulsetto.tech, PDP de pettichat.com,
   hero de nordicstretch.com).
6. Validar em mobile (390px). Guardar o HTML do produto em `templates/`.

**Fase 3 — Produto na loja**
7. Importar o produto no Shopify (fornecedor: USA Drop, CJ, Zendrop — o que usares).
   ⚠️ O produto TEM de existir na loja antes da conversão para Liquid.

**Fase 4 — Criativos**
8. Gerar imagens/vídeos seguindo o SOP em `docs/metodo-criativos.md`
   (clonagem de ads vencedores + 5 chaves hiper-realistas + galeria PDP
   EcomAlchemist). Os prompts base estão em `prompts/criativos.md`.
   Regra de ouro: produto real recortado nunca regenerado; 3 variantes por ad;
   QC em contact sheet antes de publicar.

**Fase 5 — Publicar e testar**
9. Converter HTML → Liquid no Shopify (tema duplicado) e substituir os placeholders.
10. Lançar campanha de teste (ver `docs/integracoes-cli.md` para Meta/TikTok).

## Comandos da CLI

```bash
python3 cli/cli.py ajuda                  # lista todos os comandos
python3 cli/cli.py brief novo <produto>   # cria product-brief para um produto
python3 cli/cli.py brief listar           # lista briefs existentes
python3 cli/cli.py criativo imagem <slug> # gera imagem a partir do brief (com .env)
python3 cli/cli.py status                 # estado do projeto e próximos passos
```

A CLI é um esqueleto funcional — os comandos de criativos e anúncios só funcionam
depois de preencheres `config/.env` com as tuas chaves (ver `docs/integracoes-cli.md`).

## Regras do jogo

- 3 dias de teste por produto, depois decide com dados (métricas no blueprint).
- Sem paixão por produto — o Winning Hunter + os números escolhem.
- Uma página por produto, mobile-first, um só CTA.
- Tudo o que for repetido 2 vezes vira template/prompt neste projeto.
