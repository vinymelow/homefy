---
name: clone-link-to-my-shopify
description: Given ANY URL or uploaded HTML/JSX file, faithfully replicate the entire landing page as a Shopify product page that LOOKS like the source — same DOM structure, class names, CSS rules, components, and visual weight per section. Transcribes each source section into Liquid (not template-fills) with only dynamic bits — text, images, prices, variant ids — lifted into editable settings and blocks. Every image, video, headline, button, and toggle is swappable in the theme editor. Add-to-Cart, variant picker, and checkout wired to Shopify's real cart. Mobile-first, SEO-ready. Handles JS-rendered sources (React apps, Claude bundler exports, Next.js) by unpacking the bundle and walking the JSX tree. Use whenever the user pastes a URL, uploads HTML, or says "clone this", "make this for my store", "rip this page", "replicate this landing page", "build me a page like this", "I want this in my shop", or pastes a URL with little context. Use even if they don't say "Shopify".
---

# Clone any landing page into the user's Shopify store

## Setup — fill this in first

Before running this skill the first time, set `STORE_DOMAIN` below to your Shopify domain (e.g. `your-store.myshopify.com`). The skill operates exclusively on this store and refuses to touch any other.

`STORE_DOMAIN = "your-store.myshopify.com"`

The deliverable is: a real Shopify product + a custom product template + custom theme sections. The user gets a live URL where everything works (cart, variants, checkout), every piece of media is swappable in the theme editor, and the page looks like the source on phone, tablet, and desktop.

## Phase 0 — Pre-flight

1. Call `switch-shop` with `STORE_DOMAIN`. Skip only if already done in this conversation.
2. Call `get-shop-info` to confirm the connection.
3. Detect the active theme via `graphql_query`:
   ```graphql
   query { themes(first: 5, roles: [MAIN]) { nodes { id name role } } }
   ```
   Capture the MAIN theme's `id`. Confirm it's Online Store 2.0 by checking for a `sections/` folder via `themeFiles`. If not OS 2.0, switch to the **Page Fallback** flow at the end and tell the user why.
4. **Duplicate the live theme — non-negotiable.** Shopify's MCP refuses writes to MAIN themes (this is a platform-side guard, not a permission setting). Don't ask the user, just do it: call `themeDuplicate` and use the new draft `id` as the write target for the entire build. Tell the user once: *"I've duplicated your live theme into a draft called `<name>`. I'll build into the draft; you publish when it looks right."* Capture both ids — `live_theme_id` (read-only reference) and `draft_theme_id` (write target). **Exact mutation shape** (the payload field is `newTheme`, not `theme` or `duplicatedTheme` — wrong field names cost two round trips per build):

   ```graphql
   mutation DupeTheme($id: ID!, $name: String!) {
     themeDuplicate(id: $id, name: $name) {
       newTheme { id name role }
       userErrors { field message }
     }
   }
   ```
5. **Re-duplicate after every publish.** Once the user publishes a draft, that draft becomes the new live theme and writes to it are blocked again. Every time you resume work after a publish, the first thing you do is duplicate the (now-live) theme into a fresh draft and swap `draft_theme_id`. This will come up often during the bug-fix loop in Phase 10.
6. Establish a unique slug from the source URL (e.g. `clone-nightlift-001`). All files, sections, templates, the asset stylesheet, and the product handle use this slug so the user can find and delete the whole bundle later.

## Phase 1 — Source extraction (transcribe, don't classify)

The single biggest failure mode of an earlier version of this skill was Phase 1 saying "classify each section into one of these 10 types" — that collapsed every unique source design into a generic template and the cloned page came out as a watered-down version of the source. Don't classify. **Transcribe.** Walk the source DOM and capture each section's actual markup tree, then in Phase 5 reproduce that tree in Liquid.

### 1.1 Get a usable copy of the source

- **HTML page (URL)**: `web_fetch` with `html_extraction_method: markdown` for readable content AND a second fetch retaining raw HTML for the DOM structure. If the page is server-rendered, you have what you need.
- **JS-rendered page (URL)**: `web_fetch` will return a near-empty shell with `<div id="root"></div>` plus script tags. Don't try to work from that. Switch to the Claude in Chrome tools (`mcp__Claude_in_Chrome__navigate`, then `mcp__Claude_in_Chrome__get_page_text` / `mcp__Claude_in_Chrome__read_page`) which render JavaScript and return the real DOM. Alternative: ask the user to "Save Page As → Webpage, Complete" in their browser and upload the result.
- **Claude.ai standalone HTML bundler exports** (`<script type="__bundler/manifest">` + `<script type="__bundler/template">` in the head): these look like HTML but the actual JSX lives base64+gzipped inside the manifest. Unpack it:
  ```python
  import re, base64, gzip, json, pathlib
  src = pathlib.Path('PATH_TO_UPLOAD').read_text()
  manifest = json.loads(re.search(r'<script type="__bundler/manifest">(.*?)</script>', src, re.DOTALL).group(1))
  # find the application/javascript entry whose UUID is referenced as type="text/babel"
  for uuid, entry in manifest.items():
      if entry.get('mime') == 'application/javascript' and entry.get('compressed'):
          jsx = gzip.decompress(base64.b64decode(entry['data'])).decode('utf-8')
          pathlib.Path('/tmp/source.jsx').write_text(jsx)
  ```
  Then walk the JSX component tree the same way you'd walk a DOM tree — every component definition becomes a section, every `<div>` inside a component is markup, every `{prop.value}` or hardcoded string is a candidate for an editable setting.
- **Direct HTML/JSX upload**: read it. Skip Chrome and bundler unpacking.

### 1.2 Extract design tokens (more thorough than the old version)

From the raw HTML/CSS, capture:
- Every `<link rel="stylesheet">` — `web_fetch` each one and concatenate.
- Every inline `<style>` block in the head and body.
- Every `:root` CSS custom property (the source's design tokens).
- Every `@font-face` rule (self-hosted fonts — flag for substitution).
- Every `@import url(...)` to Google Fonts / Bunny / Adobe.
- For each visible element (sections, headings, buttons, cards, pills, badges, prices, inputs): the computed-or-inline `font-family`, `font-size`, `line-height`, `color`, `background`, `border`, `border-radius`, `padding`, `margin`, `gap`, `box-shadow`. You need enough to reproduce the look pixel-close, not just "fonts and colors."

Save the full tokens file at `/tmp/source-tokens.css` — Phase 2 turns it into the asset stylesheet.

### 1.3 Walk the DOM and dump a per-section spec

For each visually-distinct section in the source (separated by full-width background changes, large vertical gaps, or explicit `<section>` boundaries), write a JSON spec to `/tmp/section-NN.json` with:

```json
{
  "slug": "hero",
  "source_tag": "section.hero-grid",
  "title_for_humans": "Hero — gallery + buy box",
  "markup": "...verbatim outerHTML of the section, with text content and image URLs preserved...",
  "dynamic_fields": [
    {"path": "h1", "kind": "text", "default": "The Complete Trauma Healing Toolkit"},
    {"path": "p.product-sub", "kind": "richtext", "default": "Printable worksheets..."},
    {"path": ".rating .stars", "kind": "rating", "default": 4.8},
    {"path": ".price-row .price", "kind": "price", "binds_to": "product.selected_or_first_available_variant.price"},
    {"path": ".gallery img", "kind": "image_picker", "binds_to": "product.media", "repeat": true},
    {"path": ".tier-card", "kind": "block", "block_type": "tier", "fields": [...]},
    {"path": ".cta-button", "kind": "text+url", "binds_to": "form 'product'"}
  ],
  "classes_used": [".hero-grid", ".gallery", ".buy-box", ".tier-card", ".price-row", ".rating-row"],
  "responsive_intent": "2-col desktop, 1-col mobile; gallery stacks above buy box on mobile"
}
```

The `markup` field is what makes the clone faithful — it's the actual source HTML, not a paraphrase. The `dynamic_fields` array is what makes it editable — every node that holds variable content gets a setting or block in Phase 5.

**Slug-naming convention** (just for tidy filenames, NOT for forcing the section into a template): give each section a short kebab-case slug that describes its role — `hero`, `problem-aware`, `whats-inside`, `value-stack`, `tiers`, `bought-together`, `creator-story`, `guarantees`, `reviews`, `faq`, `final-cta`, `sticky-atc`, etc. If a section doesn't match any common name, invent one (`workshop-cards`, `before-after-band`).

### 1.4 Extract product data

Title, vendor, type, variant structure (options, values, per-variant price + compare-at), currency. Use JSON-LD `Product` schema as a tiebreaker only — it's often stale. For pricing-tier landing pages (Starter / Popular / Complete), capture the **exact** tier names with their em-dashes preserved (`Starter — Feel Safe First`, not `Starter - Feel Safe First`) — these become the Shopify variant titles and the tier-comparison Liquid looks them up by exact match.

### 1.5 Currency

If non-USD, ask the user once whether to convert or keep numeric values in their store currency.

## Phase 2 — Design token resolution

1. Build a token map from the source's `:root` custom properties verbatim — if the source has `--bg: #f6f0e7`, your asset CSS has `--{slug}-bg: #f6f0e7`. Don't invent generic token names. Preserve every variable from the source so the cloned page reads visually identical.
2. Capture the source's typography pairings exactly: the heading font, body font, mono/eyebrow font (if any), and the weights actually used. The source may use one font for headings and a contrasting one for body — preserve that contrast.
3. Font fallback map. If the source uses a self-hosted or paid font you can't legally reuse, substitute the closest Google Font and disclose:
   - Sohne, Söhne → **Inter**
   - Tiempos, Charter → **Lora**
   - Cormorant Garamond, GT Sectra, Tiempos Headline → **Cormorant Garamond** (free on Google)
   - Founders Grotesk, Söhne Breit → **Manrope**
   - GT America → **Inter Tight**
   - Untitled Sans → **Inter**
   - Custom display sans → **Space Grotesk**
   - Custom serif → **Fraunces**
4. Capture every component-level CSS rule that affects visible appearance: `.hero-card`, `.tier-card`, `.tier-card[data-popular="true"]`, `.value-card`, `.value-card[data-bonus="true"]`, `.badge`, `.pill`, `.review-card`, `.faq-item`, etc. Re-namespace each class to your slug (`.hero-card` → `.{slug}-hero-card`) but preserve every property exactly. These become the bulk of your asset stylesheet.
5. Report all substitutions in the final summary.

## Phase 3 — Asset migration

Every external image and video MUST live on Shopify's CDN before the page goes live. Hotlinks fail (403, Referer blocks, expired signed URLs).

1. For each image: try direct ingestion via `fileCreate` (or `create-product`'s `images` array). If it fails or returns < 1KB (likely an error page), retry via `stagedUploadsCreate` → upload bytes → `fileCreate`. If still failing, generate a gray placeholder labeled with the section name and flag for user replacement.
2. Capture the resulting Shopify CDN URL AND the MediaImage GID (`gid://shopify/MediaImage/...`).
3. For videos: YouTube/Vimeo → keep the embed URL. Self-hosted MP4/WebM → `stagedUploadsCreate` with `resource: VIDEO` → `fileCreate`. Capture the file GID. If upload fails, generate a poster image placeholder with a play overlay; tell the user to upload manually in the theme editor.
4. **Explicit verification step**: after upload loop, confirm every asset has a CDN URL. Halt and list any missing assets to the user before proceeding.
5. Generate paraphrased alt text for every image (descriptive, keyword-light, never lifted from source).

## Phase 4 — Product creation

1. Rewrite ALL copy. Paraphrase title, description, button labels, feature copy, testimonial text. Never lift verbatim — IP risk and Meta ad rejection risk.
2. Strip competitor brand names, trademarks, "as seen on [outlet]" name-drops the user doesn't have rights to.
3. Sanitize tags: drop any tag that's a competitor name or trademark.
4. Idempotency: before creating, run `search_products` with `title:"<proposed title>"`. If a match exists, surface to user and ask whether to update or duplicate.
5. Call `create-product` with:
   - `status: DRAFT`
   - `title`, `descriptionHtml` (minimal — landing page lives in the template, not here), `productType`, `vendor`, `tags`
   - `options`: array of option names (`["Size", "Color"]`)
   - `variants`: each with `price`, `compareAtPrice`, `sku`, `optionValues`, `inventoryItem: { tracked: true }`
   - `images`: featured + gallery, each with `altText`
   - SEO: `seo.title` (≤60 chars, paraphrased), `seo.description` (≤155 chars, paraphrased)
   - `handle`: explicit, derived from slug
6. Per-variant image linking: if source has variant-specific imagery (color swatches etc.), pass `mediaId` on each variant referencing the uploaded MediaImage GID.
7. Add to a `Cloned imports` collection (create if missing via `create-collection`). Ask the user if they want it in additional collections.

## Phase 5 — Build the custom theme template + sections

This is what makes the page look like the source AND lets the user swap media without code. Use `themeFilesUpsert` to write Liquid sections, one shared CSS asset, and a custom product template.

### The shared CSS asset (single source of truth for the look)

Create exactly one file: `assets/{slug}-styles.css`. It holds the full design system — color tokens, font imports, every component class. Every section just references it.

Why one asset and not inline `<style>` per section: section files have a hard byte ceiling on `themeFilesUpsert` calls, the user gets one file to retheme later, and the browser caches it across page loads. This was the single biggest unlock during the Trauma Healing Toolkit build — sections went from 600-line monsters to 80-line markup files.

Shape:

```css
/* {slug}-styles.css — full design system for the cloned page */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --{slug}-bg:          #ffffff;
  --{slug}-surface:     #faf8f3;
  --{slug}-ink:         #1a1a1a;
  --{slug}-ink-muted:   #5a5a5a;
  --{slug}-accent:      #...;
  --{slug}-accent-deep: #...;
  --{slug}-btn-bg:      var(--{slug}-ink);
  --{slug}-btn-fg:      #ffffff;
  --{slug}-radius:      14px;
  --{slug}-radius-btn:  999px;
  --{slug}-font-heading: 'Inter Tight', system-ui, sans-serif;
  --{slug}-font-body:    'Inter', system-ui, sans-serif;
  --{slug}-font-mono:    'JetBrains Mono', ui-monospace, monospace;
}

.{slug}-container { max-width: 1180px; margin: 0 auto; padding: 0 clamp(16px, 4vw, 32px); }
.{slug}-section   { padding: clamp(40px, 8vw, 96px) 0; background: var(--{slug}-bg); }
.{slug}-btn       { /* button base */ }
.{slug}-hero      { /* ... */ }
/* every component class lives here */
```

Use `oklch()` for colours if the source palette has any subtlety — sRGB hex flattens warm cream / sage / dusty rose into mud. `oklch(0.96 0.018 82)` is the warm cream from the Trauma build.

### Universal section structure

Every section file is small markup that pulls the shared stylesheet and then writes a few scoped overrides. Filename: `sections/{slug}-{section-type}.liquid`.

```liquid
{{ '{slug}-styles.css' | asset_url | stylesheet_tag }}

<section class="{{slug}}-section {{slug}}-{{section_type}}" id="shopify-section-{{ section.id }}-inner">
  <div class="{{slug}}-container">
    <!-- section-specific markup using section.settings.heading, .image, .video, etc. -->
  </div>
</section>

<style>
  /* Scoped overrides ONLY — global rules live in the asset file.
     Dawn (and most themes) paint h1-h4 in a near-invisible color-scheme
     variable that overrides anything you set globally. You MUST re-assert
     heading colour and background scoped to this section's id, or your
     headings will render as faint ghosts on the live page. */
  #shopify-section-{{ section.id }} { background: {{ section.settings.bg_color | default: 'var(--{slug}-bg)' }}; }
  #shopify-section-{{ section.id }} h1,
  #shopify-section-{{ section.id }} h2,
  #shopify-section-{{ section.id }} h3,
  #shopify-section-{{ section.id }} h4 { color: {{ section.settings.text_color | default: 'var(--{slug}-ink)' }}; }
</style>

{% schema %}
{
  "name": "Clone — Hero",
  "settings": [
    { "type": "text", "id": "heading", "label": "Headline", "default": "Welcome" },
    { "type": "richtext", "id": "subhead", "label": "Subheadline", "default": "<p>Short subhead.</p>" },
    { "type": "image_picker", "id": "image", "label": "Hero image" },
    { "type": "video", "id": "video", "label": "Hero video (optional, overrides image)" },
    { "type": "url", "id": "video_url", "label": "External video URL (YouTube/Vimeo)" },
    { "type": "text", "id": "cta_label", "label": "Button text", "default": "Shop now" },
    { "type": "url", "id": "cta_link", "label": "Button link (leave blank to add this product to cart)" },
    { "type": "color", "id": "bg_color", "label": "Background", "default": "#ffffff" },
    { "type": "color", "id": "text_color", "label": "Heading colour", "default": "#1a1a1a" }
  ],
  "presets": [{ "name": "Clone — Hero" }]
}
{% endschema %}
```

`image_picker` and `video` schema types render a file-picker in Shopify's theme editor — the user clicks, uploads, done. This is the swappable-media requirement. Every block that renders a visual (card icon, value-stack tile, testimonial avatar, comparison row image) gets its own `image_picker` setting so the user can swap them without touching code.

### Schema rules that will burn you if you miss them

Shopify's schema validator is strict, the error messages are unhelpful, and a single bad schema rejects the whole `themeFilesUpsert` call.

- **Section `name` ≤ 25 characters.** "Frequently bought together" (27) gets rejected — shorten to "Bought together". Block `name` has the same limit.
- **Setting `id`s must be globally unique within the section.** A text setting `id: "badge_text"` and a colour setting `id: "badge_text"` will both be accepted at upload and then one silently wins — usually the wrong one. Always namespace: `badge_text` (string) + `badge_text_color` (colour).
- **`text`, `richtext`, `url` settings can't have blank string defaults.** `"default": ""` is rejected. Supply a real fallback ("Add to cart", `<p>Subhead.</p>`, `"/"`) even if the user will overwrite it.
- **`range` settings need `min`, `max`, `step`, and `default` — all required.** Default must be a multiple of step from min.
- **`block.shopify_attributes`** must be emitted on every block container in the Liquid (`<div ... {{ block.shopify_attributes }}>`). Without it the theme editor's hover-to-edit doesn't find the block and the user can't click into it.
- **`max_blocks: 50` is the platform ceiling.** Anything higher is rejected.

### Per-source-section transcription procedure

For each `/tmp/section-NN.json` spec from Phase 1.3, produce one Liquid section file. The procedure is the same regardless of whether the source section is a hero, a tier comparison, a reviews grid, a creator story, or something nobody's ever built before:

**Step 1 — copy the source markup verbatim into the Liquid file**, then re-namespace the CSS class names by prefixing your slug. So source `<div class="hero-card">...</div>` becomes Liquid `<div class="{{slug}}-hero-card">...</div>`. Don't simplify the DOM tree. Don't collapse wrappers. If the source has three nested divs around a heading, your Liquid has three nested divs around a heading. Visual fidelity comes from the markup structure as much as the CSS.

**Step 1.5 — separate content from design placeholder.** This is the single most-skipped step in the whole procedure, and the one that produces the angriest "I can't edit this" follow-ups. When you read the source, a lot of what looks like real content is actually mock data the designer put in so the page would render. Your job is to map the placeholder to its real role in Shopify, not to transcribe the placeholder pixels.

Three patterns recur:

- **Galleries / product imagery → bind to `product.media`, do not transcribe the placeholder images.** If the source has a hero gallery with mock product photos (or worse, hand-drawn placeholder SVGs / paper-sheet React components / lorem-ipsum-tier mockup tiles), that whole block is "the product image area." Your Liquid renders `product.featured_media` as the main image and loops `product.media limit: 8` for the thumbnails with click-to-swap JS. Only render the placeholder as a fallback inside `{%- if product.media.size == 0 -%}`. The merchant uploads images in Products → Media; this section displays them automatically. Same rule for variant-card thumbnails, "frequently bought together" card images, related-products grids: if it visually represents a *Shopify-managed product*, bind it, don't transcribe it.

- **Product-card grids → use a `product` block setting per card.** When the source has an upsell row, bundle row, related items row, or any other set of cards that each represent a sellable product, give each block a `{ "type": "product", "id": "linked_product" }` setting. Auto-fill the card's title/price/compare-at/image/url from `all_products[block.settings.linked_product]`. Provide a per-block `image_picker` override and manual text fields as fallback when no product is linked. The user picks real Shopify products in the editor; the cards become real upsells, not text strings.

- **Decorative backgrounds (gradients, color blocks, pattern fills) → always pair with an `image_picker` override.** Every section that has a styled background — a gallery container with a cream→rose gradient, a final-CTA card with a sage→lavender wash, a creator-story block with a soft pink panel — gets an `image_picker` setting whose Liquid renders as `background: url(...) center/cover` when set, falling back to the original CSS gradient/colour when blank. If you used an image, layer a low-opacity overlay div on top so headline text stays readable.

The mock content in the source (the React `<PaperA />` components, the placeholder photos, the lorem-ipsum product titles) renders ONLY as the empty-state fallback. The Shopify-managed value (product.media / linked product / uploaded image) is the default render.

**Step 2 — for each dynamic field listed in the section spec, replace the source's hardcoded value with a Liquid output**:

| Source pattern | Replace with | Schema setting |
|---|---|---|
| Heading text (`<h1>Title</h1>`) | `{{ section.settings.title }}` | `text` |
| Paragraph / rich body (`<p>Multi line copy</p>`) | `{{ section.settings.body }}` | `richtext` |
| Inline image (`<img src="...">`) used decoratively (icon, illustration, accent) | `{{ section.settings.image \| image_url: width: 800 \| image_tag }}` with `{%- else -%}` placeholder div for unset | `image_picker` |
| Product gallery (main + thumbs, OR any block that displays the product visually — even if source uses mock SVGs / paper-sheet placeholders) | `product.featured_media` + `for media in product.media` loop with click-to-swap JS; render the source's placeholder only inside `{%- if product.media.size == 0 -%}` | nothing in schema — driven by `product.media` |
| Card representing a sellable product (upsell, FBT, related item, bundle slot) | `{%- assign p = all_products[block.settings.linked_product] -%}` then `{{ p.title }}`, `{{ p.price \| money }}`, `{{ p.featured_image \| image_url ... }}`, link to `{{ p.url }}` | block setting `product` named `linked_product`, plus an `image_picker` override and manual text fields as fallback |
| Decorative section background (CSS gradient, color block, pattern) | `style="{% if section.settings.bg_image != blank %}background: url('...') center/cover no-repeat{% else %}<original-gradient>{% endif %}"` — add a translucent overlay div when an image is set so text stays readable | `image_picker` named `bg_image` |
| Price (matches one variant) | `{{ product.selected_or_first_available_variant.price \| money }}` | nothing |
| Compare-at price / "was" price | conditional on `compare_at_price > price` | nothing |
| Variant tier cards (Starter/Popular/Complete) | `{%- assign matched = product.variants \| where: 'title', block.settings.match_variant \| first -%}` then `{{ matched.price \| money }}` and `?variant={{ matched.id }}` | block setting `match_variant` (text, default = exact variant title with em-dashes preserved) |
| CTA button label | `{{ section.settings.cta_label }}` | `text` |
| CTA button link | `{{ section.settings.cta_link }}` (with `\| default: '...'` fallback) | `url` |
| Star rating value | `{{ section.settings.rating }}` rendered as `★` × rounded value | `range` (min 0, max 5, step 0.1) |
| Toggle / featured / popular state | `{% if block.settings.is_popular %}data-popular="true"{% endif %}` | `checkbox` |
| Two-toned title with italic emphasis word | three text settings concatenated as `{{ part_1 }} <em>{{ part_2 }}</em>{{ part_3 }}` | three `text` settings |
| Disabled / X-mark feature in tier card | preserve as `<li data-yes="false">` with strike or muted styling | included in features list, parsed per-item with yes/no separator (see below) |
| Repeated child element (cards, list items, review tiles, FAQ items) | wrap loop in `{% for block in section.blocks %}...{% endfor %}` with one schema block type per repetition pattern | `blocks` |

**Step 3 — for repeated children, define one block type per repetition pattern, with one block-level setting per dynamic field in that child.** Example: a value-stack card with image, title, meta, value, and a bonus flag becomes a block with `image_picker`, `text`, `text`, `text`, `checkbox` settings. Render the loop in the Liquid as `{%- for block in section.blocks -%}...{%- endfor -%}`. Always emit `{{ block.shopify_attributes }}` on the block's container `<div>`.

**Step 4 — for binary feature states (✓ included vs ✗ not-included on tier cards), encode the yes/no per item.** The cleanest pattern uses a per-line marker convention in the features textarea: lines starting with `-` mean "not included", everything else is "included":

```liquid
{%- assign lines = block.settings.features | newline_to_br | split: '<br />' -%}
{%- for line in lines -%}
  {%- assign txt = line | strip -%}
  {%- if txt != '' -%}
    {%- if txt | slice: 0, 1 == '-' -%}
      <li data-yes="false">{{ txt | slice: 1, txt.size | strip }}</li>
    {%- else -%}
      <li data-yes="true">{{ txt }}</li>
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}
```

Then in CSS: `[data-yes="false"] { opacity: .5; }` and `[data-yes="false"]:before { content: "✗"; }`. This faithfully reproduces tier cards where Starter has 4 items crossed out and Complete has 0.

**Step 5 — preserve every visual element the source has, even the small ones.** If the source has a "MOST CHOSEN" badge floating above a card → keep it. If the source has a quantity selector → keep it. If the source has a 3-icon trust row at the bottom of the hero → keep it. If the source has a bundle-total card with checkboxes per item → keep it. If the source has a star-rating breakdown bar chart in reviews → keep it. The skill's job is to make this editable in Shopify, not to redesign it.

**Step 6 — only after all of the above, write the schema.** One setting per dynamic field, one block type per repetition pattern, presets that populate with the source's actual content so the user sees the cloned page immediately after assigning the template. Apply all the schema rules above (≤25 char names, unique ids, non-blank defaults).

**Step 7 — mobile responsive audit.** Source CSS that's been re-namespaced and dropped into the asset stylesheet almost always contains layout primitives that depend on viewport width. They look fine on desktop and break on phones — and the breakage is usually not subtle (overlapping content, fixed elements blocking the buy box, hero images bleeding off the page). Before claiming done, grep the asset CSS for each of the following and decide whether each one needs a mobile-breakpoint override:

- **`position: sticky`** — fine on desktop, usually broken on mobile when the layout stacks to one column. The element keeps trying to stick while its parent is now full-width content above other content, and it ends up floating over whatever comes next as the user scrolls. Default fix: add `@media (max-width: 980px) { .{slug}-sticky-thing { position: static !important; top: auto !important; } }`. The viewport breakpoint should match wherever the source's grid switches from multi-col to single-col.
- **`position: fixed`** on non-overlay elements — same problem. Sticky bars are fine fixed at the bottom; a "fixed" hero card or sidebar is not.
- **Hard-coded large `vh` heights** (`min-height: 90vh` on a hero) — fine on desktop, can produce a hero taller than the phone screen with the CTA hidden below the fold. Reduce to `auto` or `min-height: clamp(420px, 70vh, 720px)` at mobile breakpoints.
- **`aspect-ratio` on a wide container** (e.g. `aspect-ratio: 1.05 / 1` on a hero grid) — fine when there's room for two columns, awkward when stacked. Reset to `aspect-ratio: 1/1` or `auto` on mobile.
- **Calculated `padding-bottom` on body or wrappers** to reserve space for a fixed sticky bar — only valid at the mobile breakpoint where the sticky bar shows; outside that breakpoint it leaves dead space.
- **`max-width` set on inline imagery without `height: auto`** — can produce stretched or squashed images on mobile when the container width changes.
- **Grids that drop to `1fr` at one breakpoint but contain content sized for the multi-col layout** — re-check max-widths on text content, font-sizes on hero h1 (Cormorant Garamond at 54px feels huge on a 380px-wide phone — `clamp(34px, 4.2vw, 54px)` is your friend).

Open the cloned product preview in Chrome at 375px width (iPhone SE) and 414px width (iPhone Plus). Scroll. If anything overlaps, jumps, or hides the buy box, that's where the override goes.

### Source-side patterns that frequently get under-built (don't drop these)

Sections that look "simple" in the source but easily become impoverished in the clone:

- **Gallery overlay arrows** (left / right floating buttons for prev/next image) — these matter, build them.
- **Badge pills floating over a card** (e.g., "DIGITAL · PRINTABLE PDF", "MOST CHOSEN", "BONUS") — position them with `position: absolute` over the card, don't drop them.
- **Soft gradient backgrounds on gallery containers** (cream → lavender, etc.) — preserve them.
- **Bottom trust grid in the hero** (3–4 columns of small icon + label + description) — separate component from the rest of the hero.
- **Quantity selector** (− 1 + control) — small but expected. Use a hidden form input + JS increment.
- **ATC button with inline price** ("Add to Cart — $34") — concatenate label + price in the button.
- **Review summary block** (big rating number + star-bar breakdown + recommend %) — full visual element, not just the card grid.
- **Review cards with bold headline + body** (not just a quote) — preserve the typographic hierarchy.
- **Founder-portrait area in creator story** (gradient block or photo, sized as a real column) — don't centre the text and skip the portrait.
- **FBT with per-item checkboxes + bundle-total card** — not just a thumbnail row. Each card gets a `product` picker (links to a real Shopify product) AND an `image_picker` override. The bundle total recalculates live in JS as the user toggles checkboxes.
- **Inside-the-bundle as a 2-column with copy left + icon-pill grid right** — not a flat list.
- **Tier cards with both ✓ and ✗ feature states** — don't render everything as ticks.
- **Hardcoded gallery placeholders that should be the product image area** — if the source has hand-drawn SVG worksheet previews, React paper-sheet components, mock product photos, or any other content that's *visually standing in for the product image*, bind that area to `product.media` (Step 1.5). The placeholder renders ONLY when `product.media.size == 0`.
- **Sticky / fixed positioning that breaks on mobile** — see Step 7 audit. The source's `position: sticky` is almost always desktop-only; add a mobile-breakpoint override or the gallery / sidebar / sticky bar will float over the buy-box content as the user scrolls.
- **Sections with a styled background but no swap option** — every gradient panel, color block, or decorative wash should expose an `image_picker` so the user can drop their own background photo in without touching CSS.

### The custom product template

Create `templates/product.{slug}.json` via `themeFilesUpsert`:

```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "blocks": { },
      "block_order": ["variant_picker", "buy_buttons", "description"],
      "settings": { "media_size": "large" }
    },
    "clone-hero":         { "type": "{slug}-hero",         "settings": {} },
    "clone-social-proof": { "type": "{slug}-social-proof", "blocks": {} },
    "clone-features":     { "type": "{slug}-features",     "blocks": {} },
    "clone-mechanism":    { "type": "{slug}-mechanism",    "blocks": {} },
    "clone-video-demo":   { "type": "{slug}-video-demo",   "settings": {} },
    "clone-testimonials": { "type": "{slug}-testimonials", "blocks": {} },
    "clone-comparison":   { "type": "{slug}-comparison",   "settings": {} },
    "clone-faq":          { "type": "{slug}-faq",          "blocks": {} },
    "clone-guarantee":    { "type": "{slug}-guarantee",    "blocks": {} },
    "clone-footer-cta":   { "type": "{slug}-footer-cta",   "settings": {} }
  },
  "order": [
    "main", "clone-hero", "clone-social-proof", "clone-features",
    "clone-mechanism", "clone-video-demo", "clone-testimonials",
    "clone-comparison", "clone-faq", "clone-guarantee", "clone-footer-cta"
  ]
}
```

**Important**: `main` stays — that's the theme's real product form with the real Add-to-Cart, variant picker, and price. Clone sections live *around* it.

Assign the template to the product via `productUpdate` setting `templateSuffix: "{slug}"`.

### Writing files to the theme — batching

`themeFilesUpsert` accepts multiple files per call but the inline JSON payload has a soft size limit; in practice batches of 3–5 small section files (or 1 large asset + 1–2 sections) go through reliably, while ≥10 files in one call frequently truncate or 413. Plan the uploads as:

1. First call: `assets/{slug}-styles.css` alone (it's the biggest single file).
2. Second–fourth calls: 3–5 section `.liquid` files each.
3. Final call: `templates/product.{slug}.json` (must be last — it references section types that have to already exist).

If a call comes back with a Liquid parse error, only the failing file needs to be re-sent; the others in the same batch were rejected too, so re-upload them with the fix.

### Liquid gotchas that cost real time

These are the ones that crashed the live preview and required a re-duplicate + republish cycle in the Trauma build. Avoid them up front.

- **`{% form %}` tag arguments can't be piped.** This crashes the section render and shows a blank white area where the form should be: `{% form 'product', product, id: 'product-form-' | append: section.id %}`. Pipe filters aren't allowed inline in tag args. Assign first: `{%- assign tht_form_id = 'product-form-' | append: section.id -%}` then `{% form 'product', product, id: tht_form_id %}`.

- **Don't `{% render %}` snippets you didn't write.** Dawn snippets like `icon-padlock`, `icon-checkmark`, `icon-arrow` exist on Dawn but not on every theme — and the cloned product page may end up on a different theme later. Use inline SVG for icons. Snippets you do create yourself should live under `snippets/{slug}-*` so they can't collide with the theme's own snippets.

- **Money filter quirks.** `money_without_trailing_zeros` returns empty for some currencies (GBP, JPY) which leaves a visible empty rectangle if you've styled the price badge with a background. Two fixes, use both: switch to `money`, and add `.price-badge:empty { display: none !important; }` to the asset CSS as a belt-and-braces guard. Always test with the store's actual currency, not USD.

- **Dawn's color-scheme cascade wins.** Even if you set `h2 { color: var(--{slug}-ink); }` in the asset file, Dawn's `.color-scheme-1 h2 { color: rgba(var(--color-foreground), …); }` overrides it because Dawn's selector is more specific. The scoped `#shopify-section-{{ section.id }} h1, h2, h3, h4` rule in the universal section structure exists exactly to win this fight. Don't skip it "just for this one section" — you'll come back and add it.

- **Section background inherits from the theme's color scheme if you don't set one.** This is what causes the "why is my hero blue?" moment: Dawn paints the section background with the active color scheme's `--color-background`. Always set `#shopify-section-{{ section.id }} { background: …; }` explicitly in the scoped override block, even if the section looks fine in your local mockup.

- **Theme files are immutable after publish.** Once the user publishes, you can't write to that theme any more — every subsequent edit must go into a fresh duplicate. See Phase 0 step 5.

## Phase 6 — Functional CTAs and cart

Every CTA in every cloned section uses this anchor + JS pattern. AJAX add-to-cart with graceful redirect fallback. Works on any theme.

```liquid
<a href="#" class="{{slug}}-cta"
   data-product-id="{{ product.selected_or_first_available_variant.id }}"
   data-clone-cta>
  {{ section.settings.cta_label | default: 'Add to cart' }}
</a>

<script>
  document.querySelectorAll('[data-clone-cta]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const id = btn.dataset.productId;
      try {
        const res = await fetch('/cart/add.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: [{ id, quantity: 1 }] })
        });
        if (!res.ok) throw new Error('add-to-cart failed');
        if (window.theme && typeof window.theme.openCartDrawer === 'function') {
          window.theme.openCartDrawer();
        } else {
          document.dispatchEvent(new CustomEvent('cart:open'));
          setTimeout(() => {
            if (!document.querySelector('.cart-drawer.is-open')) window.location.href = '/cart';
          }, 400);
        }
      } catch {
        window.location.href = '/cart';
      }
    });
  });
</script>
```

The Liquid output re-renders on variant change, so when the user changes variant in `main`, clone CTAs automatically use the new variant ID.

### Sticky mobile CTA — always ship one

Every cloned product page gets a sticky mobile add-to-cart bar — it's not optional. Mobile conversion drops measurably without it because the hero CTA scrolls off-screen and the user has to scroll back to buy. Build it as its own section (`sections/{slug}-sticky-mobile-atc.liquid`) and add it as the last entry in the template `order` array so it sits at the page bottom in the source. Fixed-position bar on mobile, hidden on desktop, appears after scrolling past the hero:

```html
<div class="{{slug}}-sticky-cta" data-clone-cta data-product-id="{{ ... }}">
  Add to cart — {{ product.selected_or_first_available_variant.price | money }}
</div>

<style>
  .{{slug}}-sticky-cta { display: none; }
  @media (max-width: 749px) {
    .{{slug}}-sticky-cta {
      display: block; position: fixed; bottom: 0; left: 0; right: 0;
      padding: 14px 16px; background: var(--{{slug}}-c-btn-bg);
      color: var(--{{slug}}-c-btn-text); text-align: center;
      font-weight: 700; z-index: 9999;
      box-shadow: 0 -2px 12px rgba(0,0,0,.08);
      opacity: 0; transform: translateY(100%); transition: .25s;
    }
    .{{slug}}-sticky-cta.is-visible { opacity: 1; transform: translateY(0); }
  }
</style>

<script>
  const sticky = document.querySelector('.{{slug}}-sticky-cta');
  const hero = document.querySelector('.{{slug}}-hero');
  if (sticky && hero) {
    new IntersectionObserver(([e]) => {
      sticky.classList.toggle('is-visible', !e.isIntersecting);
    }).observe(hero);
  }
</script>
```

## Phase 7 — SEO and structured data

1. SEO title and meta description on the product (`seo.title` ≤60, `seo.description` ≤155) — paraphrased.
2. Product JSON-LD — Shopify's `main-product` section emits this on most themes. Verify; only add a second if missing. Use Liquid objects (`product.title`, `product.featured_image`) so values stay in sync.
3. Open Graph + Twitter cards — Shopify auto-generates. Verify featured image is set correctly.
4. Canonical URL — Shopify handles automatically. Don't override.
5. Alt text on every image — already done in Phase 3.
6. Heading hierarchy — exactly one `<h1>` per page (the product title in `main`), `<h2>` for each section heading, `<h3>` for sub-items. Don't emit stray `<h1>`s in cloned sections.
7. Internal links — drop references to source-site products you don't have. Paraphrase competitor names in comparisons to generic category descriptors ("other splints", "leading alternatives").

## Phase 8 — Performance

1. Above-fold images: `loading="eager" fetchpriority="high"`. Use Shopify's image filter at responsive sizes: `{{ image | image_url: width: 1500 }}` + `srcset`.
2. Below-fold images: `loading="lazy" decoding="async"`.
3. Videos: `preload="metadata"`, `poster="{{ poster | image_url: width: 1500 }}"`, `playsinline muted` for iOS autoplay.
4. Fonts: `@import` with `display=swap` so text renders in fallback immediately.
5. No heavy JS libraries. The CTA script + IntersectionObserver are the only scripts shipped.
6. Avoid layout shift: every `<img>` has explicit `width` and `height` attributes (Shopify's image filter supplies them).

## Phase 9 — Mobile + desktop UX rules

Apply across every section:

- Mobile-first CSS. Defaults are mobile. `@media (min-width: 750px)` for tablet, `(min-width: 990px)` for desktop.
- Tap targets ≥ 44×44px. Button padding minimum `14px 24px`.
- Body `font-size: clamp(15px, 2.5vw, 17px)`. Never below 14px on mobile.
- `line-height: 1.5` body, `1.2` headings.
- No horizontal scroll. Mentally test at 360px width — every section fits.
- Section spacing: `padding: clamp(40px, 8vw, 96px) clamp(16px, 4vw, 32px)`.
- No fixed pixel widths except logos and icons.
- Hero text overlay on image: gradient scrim (`background: linear-gradient(to top, rgba(0,0,0,.5), transparent)`).
- FAQ: native `<details>`. Carousels: CSS scroll-snap, no JS libraries.

## Phase 10 — Verification

Before reporting done:

1. `web_fetch` the live product URL (`https://STORE_DOMAIN/products/{handle}?_ab=0&_fd=0&_sc=1` for draft preview, or `?preview_theme_id=...` if working on duplicate theme). Confirm:
   - HTTP 200
   - Custom template loaded (slug appears in class names)
   - Hero heading appears in HTML
   - At least one CDN image URL appears
   - Page weight < 2MB (heavier = something wrong)
2. `HEAD` request each uploaded image URL to verify accessibility.
3. Check that every section listed in the section specs from Phase 1.3 appears in the rendered markup by its namespaced class. If `section-04` was a tier-comparison with `<div class="tier-card" data-popular="true">`, grep the rendered HTML for `{{slug}}-tier-card` and confirm three of them exist with one carrying `data-popular="true"`.
4. **Visual diff against the source.** Open both the source URL/HTML and the cloned preview side by side. For each section in your Phase 1.3 spec, eyeball: is the layout the same? Are the badges / pills / arrows / quantity selectors / per-item checkboxes / X-marks / rating breakdowns / founder portrait blocks all present? Walk through every entry in the "Source-side patterns that frequently get under-built" list and confirm none were dropped. If you have the Claude in Chrome tools, use `mcp__Claude_in_Chrome__navigate` + screenshot to capture the rendered preview and compare. If something is missing, fix it before claiming done — don't make the user post screenshots back at you saying "why doesn't this match what I sent you?"
5. **Mobile responsive check.** Open the preview at 375px width (iPhone SE) and 414px width (iPhone Plus). Scroll the hero, scroll past the sticky bars, scroll through the tier comparison and the FBT row. Anything that overlaps, floats over the buy-box, leaves blank space, or hides content under another element is a Step 7 audit miss — add the mobile-breakpoint override before claiming done.
6. **Editability sweep.** For every section, open it in the Shopify theme editor and confirm: every visual element (gallery image, card image, decorative background, upsell product) has an editable setting attached to it. If you find any hardcoded image, gradient, or product reference that the merchant can't swap from the editor, that's a Step 1.5 miss — go back and add the setting.
5. If any check fails, report which one and the most likely fix.

## Phase 11 — Hand-off summary

Summarize for the user in this order:

1. **Live preview URL**.
2. **Admin product URL**: `https://STORE_DOMAIN/admin/products/{numeric-id}`.
3. **Theme editor URL** to swap media: `https://STORE_DOMAIN/admin/themes/{theme-id}/editor?previewPath=/products/{handle}`. Explain every image, video, headline, and button label is editable here without code.
4. **Files created** (so the user can find/delete them later): list every section file, the template file, the shared asset stylesheet (`assets/{slug}-styles.css`), and any snippets.
5. **What was paraphrased** vs the source.
6. **What was substituted** (fonts, placeholder images, removed competitor names).
7. **Currency note** if non-USD source.
8. **Out-of-scope items** the user handles separately:
   - Reviews — install Loox / Judge.me / Stamped (the social-proof section leaves a slot)
   - Email capture — Klaviyo or Shopify Email
   - Live chat — Tidio or Shopify Inbox
   - Tracking pixels — verify Meta/TikTok pixels are on the theme already
   - Trust badges — add via theme editor in the `guarantee` section's image_picker slots
9. **Next step**: ask whether to flip from DRAFT to ACTIVE. Only after explicit yes, call `update-product` with `status: ACTIVE`.

## Failure modes and fallbacks

- **Theme is not OS 2.0** → switch to Page Fallback below. Tell user upgrading to OS 2.0 unlocks the full skill.
- **`themeFilesUpsert` denied** → connection needs `write_themes` scope. Point user to Settings → Apps → reconnect Shopify.
- **Source page JS-rendered, `web_fetch` returns blank** → ask user to paste rendered HTML, or work from screenshots, or try `?_escaped_fragment_=` / AMP version.
- **Hero video exceeds Shopify's file size limit (1GB)** → keep external embed; user compresses and uploads in theme editor.
- **Source uses paid fonts** → substitute per Phase 2 map and disclose.
- **Source has working chat/quiz/configurator** → out of scope without app installs. Note in summary.

## Page Fallback (non-OS-2.0 themes)

If theme isn't OS 2.0:

1. Create a Shopify **page** (`/pages/{slug}`) instead of a custom product template.
2. Page body is a single self-contained HTML+CSS+JS bundle with all sections inline.
3. Media swap: use page metafields (`custom.hero_image`, `custom.hero_video`, etc.) referenced from the page body via Liquid. Create metafield definitions via `metafieldDefinitionCreate`. User updates media by editing metafield values in page admin (less elegant than theme editor, but works).
4. CTAs link to `/products/{cloned-product-handle}` instead of adding to cart inline (page isn't a product page).
5. Everything else (responsive, SEO, performance) is identical.

## Sensitive verticals — guardrails

If the source page (or the product you're cloning into) is in any of these categories, the cloned page MUST include a disclaimer FAQ entry and the copy MUST be claim-free. This protects the user from ad-platform rejections (Meta/TikTok auto-reject medical claims) and from regulatory risk:

- **Mental health / trauma / addiction recovery**: include an FAQ entry titled "Is this a substitute for professional mental health care?" with the answer "No. This is for educational and self-reflection purposes only and is not a substitute for professional diagnosis or treatment. If you are in crisis, please reach out to a qualified professional or a local crisis service." Strip any "heal", "cure", "treat" verbs from the rewritten copy.
- **Supplements / functional food / nootropics**: include an FAQ entry "Are these claims FDA-evaluated?" with the standard disclaimer ("These statements have not been evaluated by the FDA. This product is not intended to diagnose, treat, cure, or prevent any disease."). Avoid before/after framing.
- **Skin / hair / body**: avoid clinical-outcome language. "Visibly smoother" is fine, "clinically proven to reduce wrinkles" is not unless the source cites a study and you keep the citation.
- **Pregnancy, fertility, perimenopause / menopause**: include a "consult your clinician" note in the FAQ. The voice is "you're not crazy" / informational — not diagnostic.

When in doubt, default to educational framing. The user can soften the disclaimer wording later in the theme editor; missing it entirely is the failure mode that gets ads rejected.

## Strict rules — never violate

- Never lift source copy verbatim. Always paraphrase.
- Never reproduce competitor brand names, logos, or trademarks.
- Never reuse paid/licensed fonts from the source.
- Never flip a product to ACTIVE without explicit user confirmation.
- Never hardcode media URLs — every image and video is a section setting the user can swap.
- Never hardcode hero thumbnails — the gallery loops `product.media`, no exceptions.
- Never write to a live (MAIN role) theme. Always duplicate first; re-duplicate after every publish.
- Never use `money_without_trailing_zeros` for a non-USD store without testing it first.
- Never `{% render %}` a snippet you didn't ship in this build (no relying on Dawn snippets).
- Never operate on any store other than `STORE_DOMAIN`.

## Default behavior when user pastes a URL or uploads HTML

If the user pastes a URL or uploads an HTML/JSX file with no other instruction, respond with:

> "Cloning [source] into your store. I'm duplicating your live theme into a draft, building the product + custom template + sections into that draft, and pausing before publishing — that way nothing changes on your live store until you click publish. I'll transcribe each section from the source (not template-fill), so the cloned page reads visually identical with editable text and swappable images. Roughly 10–20 tool calls depending on section count. Starting now."

Then begin Phase 0 immediately. Don't ask whether to duplicate — duplication is mandatory because Shopify refuses writes to live themes, and asking the user a question they can't say no to is wasted turns. Don't ask whether to "classify into one of these section types" — there are no types, only what the source has.

## Iteration loop after the first publish

The first publish is almost never the last. Expect the user to come back with screenshots and "fix the X" requests — invisible headings, blue hero background, empty price badge, hardcoded thumbnails, font swap. Each round looks like this:

1. **Re-duplicate the now-live theme** (Phase 0 step 5) — the previously-draft theme is now live and locked.
2. **Identify the smallest set of files to change.** If it's a visual issue (colour, spacing, typography), it's almost always the asset stylesheet alone. If it's a Liquid issue, it's one section file. Only touch what's needed.
3. **Upload the patched files** to the new draft.
4. **Tell the user**: "Pushed to a fresh draft called `<name>`. Preview it, and if it looks right, publish." Include the theme preview URL so they don't have to hunt for it.
5. **Wait for their confirmation** before assuming the fix landed. The Shopify Admin's preview can serve stale assets for a minute after upload.
