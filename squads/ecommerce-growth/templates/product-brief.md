# Product Brief (squad ecommerce-growth) — [NOME DO PRODUTO]

> **Fonte canônica: `ecom-stack/templates/product-brief.md`**
> Este ficheiro é a versão de trabalho do squad. As secções 1–9 mantêm os mesmos
> números e campos do contrato original para compatibilidade com os workflows e
> tasks; as secções 10–12 são campos de OUTPUT do squad (positioning, hipóteses
> validadas, controlo do artefacto). Em caso de divergência, prevalece o original.
>
> Preencher ANTES de pedir a landing page OU os criativos.
> Criar cópia de trabalho: `python3 ecom-stack/cli/cli.py brief novo <slug>`
> (grava em `ecom-stack/research/landers/<slug>-brief.md`).

## 1. Dados base
- **Slug/nome curto**:
- **Nicho**: (casa & utilidades / beleza & cuidados pessoais)
- **Mercado-alvo** (países do teste): (ex.: US, CA, AU, NZ, UK — UK separado)
- **URL do produto no Shopify** (obrigatório — tem de existir antes do Liquid):
- **Preço de venda**: €   | **Preço riscado**: €
- **Custo do produto + envio**: €   | **Margem estimada**: %
- **Prazo de entrega prometido**: (ex.: 6–9 dias úteis com rastreio)

## 2. Classificação do produto (método EcomAlchemist — decide a sequência de criativos)
- [ ] **High-consideration** (saúde/beleza com claims, preço alto, comprador cético)
      → galeria PDP completa: 9–11 frames (hero → recognition → pivot → mechanism →
      payoffs → how-easy → for/not-for → proof → offer)
- [ ] **Low-stakes** (barato, visual, impulso — maioria de casa/utilidades)
      → galeria curta: hero + payoffs + how-to + comparação + prova + oferta

## 3. Público e promessa
- **Avatar 1** (principal): idade, género, contexto, frase típica
- **Avatar 2** (se houver):
- **Avatar 3** (se houver):
- **Pain central** (o problema que o produto resolve — 1 frase, linguagem do cliente):
- **Desejos ranqueados** (o resultado que cada avatar quer, por ordem de intensidade —
  escreve as headlines dos frames de payoff):
  1.
  2.
  3.
- **Objeções principais** (cada uma TEM de ser respondida por uma imagem ou secção):
  1.
  2.
  3.

## 4. Referências escolhidas (Winning Hunter / ad library)
| Componente | URL | O que vou copiar |
|---|---|---|
| Homepage | | |
| Landing page (PDP) | | |
| Hero section (screenshot) | | |
| Ads vencedores para clonar (ad library, filtrar por spend) | | 3–6 frames de referência |

- **Receita estimada da loja alvo**: $/mês (valida que a página converte)

## 5. Oferta e bundles (ligar a produtos/variants REAIS do Shopify)
- **Bundle 1** (1 unidade): preço / preço riscado
- **Bundle 2** (mais popular): preço / preço riscado
- **Bundle 3** (melhor valor): preço / preço riscado
- **Painel de oferta grátis**: o que está incluído em cada bundle (só se REAL —
  nunca inventar gifts) / valor riscado
- **Garantia**: (dias — tem de bater certo com a política da loja em TODOS os frames)

## 6. Copy
- **Benefício principal (headline)**: resultado em linguagem "you", 4–8 palavras
- **Benefícios (máx. 5, escaneáveis)** — cada um = 1 frame de payoff:
  1.
  2.
  3.
  4.
  5.
- **Como funciona (3 passos, 2 palavras por passo)**:
  1.
  2.
  3.
- **FAQ (4–6 perguntas reais, responde objeções da secção 3)**:
  1.
  2.
  3.
  4.

## 7. Guardrails de claims (preencher obrigatoriamente)
- [ ] Nenhum preço/desconto/prazo/garantia sem confirmação na loja ou no fornecedor
- [ ] Claims de saúde/beleza suavizados ("designed to help with", não "cura/trata")
- [ ] Sem logos de imprensa/endorsements inventados
- [ ] Reviews = reais da loja OU "Dramatized customer story" legível
- [ ] Specs (medidas, materiais, tempos) verificados — senão BLOCKED

## 8. Assets e identidade
- **Kit de marca** (travar 1 antes de gerar criativos):
  [ ] clinical-clean  [ ] bold-hype  [ ] premium-elegant/warm  [ ] earthy-natural
- **Fotos reais do produto** (mín. 1, para recortar com rembg e embutir nos frames):
- **Logo**:
- **Cores da marca**: principal / acento / fundo

## 9. Slots de criativos necessários (página + ads)
- [ ] `hero-main` — Benefit Stack (foto real em uso + painel translúcido)
- [ ] `recognition-1/2` — avatares a reconhecer o problema (só high-consideration)
- [ ] `payoff-1/2/3` — 1 imagem por desejo ranqueado
- [ ] `infographic-mech` — Mechanism Explainer (cutaway + glow)
- [ ] `how-to` — How-To Steps
- [ ] `vs-alternative` — comparação
- [ ] `angle-1/2/3` — ângulos reais do produto (foto, não IA)
- [ ] `lifestyle-1/2` — hiper-realistas (5 chaves), 2 variantes
- [ ] `ugc-video` — vídeo 9:16 para ads e página
- [ ] `static-ads-1/2/3` — clones de ads vencedores (3 variantes)

---
## 10. Posicionamento (OUTPUT — task `create-positioning`)
- **Statement de posicionamento** (1 frase: para <avatar>, <produto> é o <categoria>
  que <diferenciador>, ao contrário de <alternativa>):
- **Categoria/ângulo de entrada** (o "momento do cliente" escolhido — uma pessoa
  específica + um momento específico, nunca "para todos"):
- **Diferenciador principal** (o que ataca o gap dos concorrentes — da secção de
  gaps do research-report):
- **Alternativa atacada** (salão/cabeleireiro, pilhas de produtos, métodos manuais —
  nunca nomes de marcas):

## 11. Hipóteses validadas (OUTPUT — tasks `research-product` / `research-market`)
- **Pain validado por evidência** (citação + fonte + data — do research-report):
- **Desejo dominante** (o #1 da secção 3, confirmado nos dados):
- **Ângulo criativo vencedor esperado** (a queixa dos concorrentes que os nossos
  ads vão resolver):
- **Score do gate (≥70/100)**: procura /20 · gap /20 · fornecedor /20 ·
  compliance /20 · prova criativa /20 → TOTAL
- **Veredito da pesquisa**: [ ] GO  [ ] NO-GO  (ref research-report.md)

## 12. Controlo do artefacto
- **Origem**: (manual / painel ecom-stack / output de task do squad)
- **Preencido por / data**: 
- **Status**: [ ] rascunho  [ ] pronto para `create-copy`  [ ] pronto para
  `create-page-spec` / `build-landing-page`  [ ] aprovado humanamente
- **Próxima task do workflow**:
