# Prompts — Criativos de imagem e vídeo (PicsArt API / geradores IA)

Fluxo: (1) descarregar os melhores ads dos concorrentes (ad library filtrado por
maior spend, ou Winning Hunter) → (2) gerar prompts com a IA a partir dessas
referências → (3) gerar os assets → (4) validar consistência visual.

## 1. Gerar prompts de imagem a partir dos ads vencedores

```
Attached are the best-performing ad images from competitors selling [PRODUCT].
Also attached is my landing page structure with named image slots
(hero-main, angle-1/2/3, lifestyle-1/2, infographic-1, review-avatar-1/2/3).

For EACH slot, write one detailed image-generation prompt that:
- Recreates the style and composition of the strongest competitor ads
- Features MY product (describe it: [DESCREVER PRODUTO: cor, material, formato])
- Matches the slot's purpose (hero = bold promise, lifestyle = real use context,
  infographic = benefits as text overlays, angle = detail/material close-up)
- Specifies: aspect ratio, lighting (soft natural / studio), background
  (clean off-white #F5F6F2 or real environment), no watermarks, no brand logos

Output: one prompt per slot, numbered, ready to paste into an image generator.
```

## 2. Prompts base por tipo de slot (ajustar ao produto)

**Hero (1:1, mobile)**
```
Premium e-commerce product photography of [PRODUCT], centered, floating slightly
above a clean warm off-white background (#F5F6F2), soft natural shadow, crisp
details, [material] texture visible, shot on 85mm, high-end catalog style.
One short benefit phrase as bold minimal typography overlay at the bottom.
```

**Lifestyle (4:5 ou 1:1)**
```
Candid lifestyle photo of [PERSONA] using [PRODUCT] in [CONTEXT: kitchen /
bathroom / living room / office], natural daylight, shallow depth of field,
authentic "phone photo" feel, warm tones, not staged, no visible logos.
```

**Infográfico (4:5)**
```
Clean product infographic: [PRODUCT] shown at 3/4 angle with 4 callout lines
pointing to features ([FEATURE_1..4]), minimal sans-serif labels, warm off-white
background, orange accent (#FF5F1F) for callout lines, generous white space.
```

**Ângulo/detalhe (1:1)**
```
Macro detail shot of [PRODUCT_PART], showing [MATERIAL/FUNCTION], soft studio
lighting, neutral warm background, razor-sharp focus, premium product photography.
```

## 3. Vídeos de anúncio (9:16, 15–30s) — 3 formatos para testar

**Formato A — Hook problema/solução**
```
UGC-style video, vertical 9:16: a person struggling with [PROBLEM] in the first
2 seconds (frustrated expression), then [PRODUCT] appears and solves it,
end with quick result + text overlay of the offer. Natural light, handheld feel,
captions in bold sans-serif.
```

**Formato B — Demonstração pura**
```
Vertical 9:16 product demo: [PRODUCT] in use, 3 quick cuts showing
[USE_1] → [USE_2] → [USE_3], each with a 3-word caption overlay, upbeat pacing,
clean background, no talking head.
```

**Formato C — Autoridade/infográfico em movimento**
```
Vertical 9:16 motion infographic: product rotates slowly while feature callouts
animate in one by one, ending with price + guarantee frame. Minimal, premium,
off-white background, single orange accent.
```

## 4. Regras de consistência (o que mata criativos)

- Todas as imagens do mesmo produto: mesmo fundo/tom de luz — sistema visual, não
  fotos soltas.
- Nunca gerar com logos/marcas de terceiros.
- Texto sobre imagem: máx. 6 palavras por overlay, fonte única.
- 3 formatos de vídeo × 2–3 hooks de texto = 6–9 criativos por produto para o
  teste inicial (€20–50/dia aguenta 2–3 criativos em aprendizagem).

## 5. Comandos (via CLI do projeto)

```bash
python3 cli/cli.py criativo imagem <slug> --slot hero-main
python3 cli/cli.py criativo video <slug> --formato A
```
(os comandos exigem .env configurado — ver docs/integracoes-cli.md)
