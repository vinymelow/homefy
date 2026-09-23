# Prompt chain — Loja completa (adaptado do guia passo-a-passo do tutor)

> Genérico: substitui {{PRODUCT_URL}}, {{REF_*}} e {{BRAND}}. Baseado no caso Flovir
> do tutor (docs/tutor/How To Build Your Store.docx): produto $100K/mês, homepage de
> uk.pulsetto.tech, PDP de pettichat.com, hero de nordicstretch.com.
> Ferramentas: o guia usa ChatGPT → Claude Design → Claude Co-Work. Usa o equivalente
> que tiveres (Kimi, Claude, GPT — a cadeia é igual).

## PASSO 1 — Encontrar as lojas (Winning Hunter)

1. winninghunter.com → **Stores** → filtrar por nicho → ordenar por receita.
2. Escolher o produto-alvo (loja concorrente forte).
3. Escolher as 3 referências de estrutura:
   - **Homepage**: a loja com a melhor homepage (ex. do tutor: uk.pulsetto.tech)
   - **PDP**: a loja com a melhor página de produto (ex.: pettichat.com)
   - **Hero da PDP**: screenshot do hero de compra com bundle (ex.: nordicstretch.com)
4. ⚠️ Referência = estrutura, movimento e ritmo visual. NUNCA copiar logo, imagens,
   copy, reviews, claims ou código — e nunca inventar claims comerciais (preços,
   garantias, prazos, endorsements). O que não for verificado vira placeholder editável.

## PASSO 2 — Prompt "master prompter" (gerar o prompt de design)

```
Act as a master prompter for an AI design tool with 10+ years of experience building
premium direct-response ecommerce pages. I want you to build me a prompt to create a
page for this product: {{PRODUCT_URL}} using this page's EXACT layout, the way it
moves and works: {{REF_URL}}. It must be phone and mobile friendly.
```

O output será um prompt gigante. Esse prompt gigante é o que vai para o gerador
de design no PASSO 3. Repetir para cada uma das 3 referências.

## PASSO 3 — Gerar os 3 ficheiros HTML conceito

Colar cada output no gerador de design (Claude Design, ou pedir à Kimi Code).
Regras que o prompt final deve impor (o tutor inclui todas — manter):
- Mobile-first; breakpoints testados de 320px a 1440px
- Uma ideia por secção, ritmo da página de referência preservado
- Todos os valores comerciais (preço, desconto, garantia, prazo, stock) como props
  editáveis — nada hard-coded, nada inventado
- Slots de mídia nomeados (galeria, hero, UGC, infográficos)
- Secções repetidas vindas de arrays/blocks, não markup duplicado
- Acessibilidade (WCAG AA), reduced-motion, performance (<2s)
- Sem iframe da página de referência, sem código copiado

Gerar **3 ficheiros separados** (não juntar — corrompe):
1. `{{slug}}-homepage.html` (fluxo completo da homepage, ~17 secções no caso Flovir)
2. `{{slug}}-pdp.html` (galeria + sistema de compra + storytelling + reviews + FAQ)
3. Hero da PDP atualizado com o screenshot do terceiro referencial (só a secção
   hero/purchase: galeria com thumbnails, bundle selector, painel de oferta/grátis,
   accordions) — sem tocar nas secções abaixo

## PASSO 4 — Master prompt para o agente de código publicar no Shopify

```
You are a senior Shopify theme architect, Liquid engineer, frontend engineer, ecommerce
UX designer, conversion strategist, accessibility specialist, performance engineer and
QA lead with 10+ years of experience building production Shopify stores.
Implement a complete homepage and product detail page directly inside my existing
Shopify theme, based on these HTML design prototypes: [homepage HTML] + [PDP HTML].

NON-NEGOTIABLE:
- Nothing merchant-facing is hardcoded: no headings, prices, variant IDs, bundle
  values, promotions, guarantees, reviews, FAQ, images, colors or menus in code.
  Everything comes from theme settings, blocks, metafields, live product data or menus.
- Keep the existing header, announcement bar, footer, navigation, cart drawer and
  fonts EXACTLY as they are. Both pages render inside the normal theme layout.
  No {% layout none %}, no duplicate header/footer, no new fonts.
- Native OS 2.0 architecture: one Liquid section per module (with valid schemas and
  presets), shared snippets, JSON templates, scoped CSS/JS with a unique prefix.
  No React/Vue/Tailwind/page builders/jQuery.
- Real commerce: variant switching, live prices, native product form, cart drawer
  refresh, sticky mobile ATC, quantity rules, no fake cart.
- Homepage and PDP as separate templates; PDP assigned to the product via
  template_suffix. No hardcoded product handles or IDs.
- Mobile-first: no overflow at 320–430px, touch targets ≥44px, safe-area insets.
- Verify with Theme Check and report desktop/tablet/mobile test results honestly.
Deliver the full implementation, exact files created/modified, and template
assignment instructions. Do not return only a plan.
```

## Checklist pós-publicação (do tutor)

- [ ] Header/footer reais visíveis no preview das duas páginas (desktop + mobile)
- [ ] Nenhum valor comercial hard-coded (testar: mudar preço no admin → muda na página)
- [ ] Tema publicado a partir de um **duplicado**, nunca no tema live direto
- [ ] Theme Check sem erros; consola limpa
- [ ] Secções reordenáveis/editáveis no Theme Editor
- [ ] Pixel Meta/TikTok a disparar nos eventos certos

## Alternativa automatizada — skill clone-link-to-my-shopify

Se quiseres clonar uma página específica diretamente para o Shopify com menos passos
manuais, existe a skill `skills/clone-link-to-my-shopify/SKILL.md` (usa Shopify MCP:
duplica tema → transcreve secção a secção → escreve Liquid editável → verifica).
Nota: ela pressupõe acesso MCP à tua loja; sem isso, segue a cadeia de prompts acima.
