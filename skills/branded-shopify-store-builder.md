---
name: branded-shopify-store-builder
description: Build a branded Shopify storefront for a DTC ecommerce brand. Use when the user wants to launch or rebuild a Shopify store, build a product page that doesn't look like a Dawn template, customise theme sections in Liquid, or stand up a branded look in Accio. Covers two paths — fast (Accio AI agent + reference brands) and deep (custom Liquid sections + JSON templates).
---

# Branded Shopify Store Builder

## When To Use This Skill

Load this skill whenever the user wants to:
- Build a branded Shopify store from scratch
- Make a product page look like a $1M/mo DTC brand instead of a Dawn template
- Use Accio AI to scaffold a store
- Write custom Liquid sections for a hero, feature grid, specs table, FAQ, comparison, CTA banner, etc.
- Apply a per-product layout via JSON templates (`template_suffix`)
- Pick a palette + typography system that reads "premium" not "generic"
- Decide between page-builder apps (PageFly, GemPages) and native theme sections

This skill assumes USA-targeted DTC brands, USD currency, and the Dawn theme as base.

---

## The Two Paths

There are two approaches. Pick one, or use them in sequence (Path 1 to scaffold fast, Path 2 to push the look further):

| Path | Time | Skill Needed | Output Quality |
|---|---|---|---|
| **1. Accio AI agent (fast path)** | 60 min | Just write prompts | Branded if prompted right |
| **2. Custom Liquid sections (deep path)** | 1-2 days | Liquid + CSS + JSON | Premium / fully bespoke |

The deep path beats Accio only when you (a) want a single hero product page that converts at premium-brand level, or (b) want reusable branded sections you can drop onto every future product via the Theme Customizer.

---

## Path 1 — Accio AI Agent (Fast Path)

### Tool
[Accio](https://www.accio.com/) — AI agent that builds a Shopify-compatible storefront from a brand brief + reference screenshots.

### 5-Step Workflow
1. **Write the brand brief** (product, niche, audience, price, tone, inspiration brands)
2. **Feed reference screenshots** — 5-10 images from real branded competitors
3. **Iterate section by section** — homepage → product page → policy pages
4. **Connect Shopify + custom domain** (Shopify Basic $39/mo, Namecheap domain $9/yr)
5. **Layer conversion apps** — Loox, Vitals, Klaviyo, Canva Pro

### Reference Brands To Show Accio
Each one nails a different part of the branded DTC playbook. Screenshot these and feed them in:

| Brand | Steal This |
|---|---|
| **Phero** (pheromone perfume) | Video review carousel with play+mute icons, 94/87/98% result donuts, "Why Choose Us" comparison checklist, "Transform Your Essence" 3-product grid |
| **Lux Cove** (LED beauty device) | Press bar (L'OREAL · COSMOPOLITAN · FOX · VOGUE), "vs Competition" feature table, 30-day result donuts, before/after slider |
| **Reviva** (LED facial sculptor) | "Glowing skin in 5 minutes" 5-step ritual, FAQ accordion, "Women Who Transformed" verified review grid, $44.99 50% OFF urgency, "BEST SELLER · 10,000+ SOLD" pill |
| **CurrentBody** (Skin LED Mask Series 2) | Editorial layout, asymmetric hero, italic accents on emotional words, premium beauty vs techy gadget |

### The 8 Design Patterns Every Branded Store Needs
1. Video review carousel (3-6 customer videos with play + mute icons)
2. Result % donuts (94% / 87% / 98% above the fold)
3. Press bar (logo strip — small features still count)
4. vs Competition table (your brand all green ✅ vs "Others" all red ❌)
5. 5-step ritual timeline (numbered, daily-use)
6. Verified review grid (photo reviews + "Verified Buyer" badge)
7. BEST SELLER + sold count ("BEST SELLER · 10,000+ SOLD" pill)
8. Scarcity + 50% OFF (countdown banner + "Only X left in stock")

### Master Accio Brief (Copy + Paste)

```
Build me a fully branded Shopify storefront for a US-based DTC brand.

PRODUCT: [your product, e.g. 7-in-1 LED Facial Sculptor]
NICHE: [e.g. premium at-home skincare device]
TARGET CUSTOMER: US women, 28-55, $50K+ income, buys premium beauty
PRICE POINT: $44.99-$79.99 (positioned as 50% OFF a $99 anchor)
BRAND TONE: Premium, scientific, warm, results-driven, feminine but not pink
INSPIRATION: Match the look + section order of these reference brands
(screenshots attached): Phero, Lux Cove, Reviva, CurrentBody.

HOMEPAGE MUST INCLUDE:
1. Hero: short headline + supporting line + primary CTA + hero product image
2. Press bar: "AS SEEN IN: VOGUE, COSMOPOLITAN, FORBES, FOX"
3. 3 result donuts: 94% / 87% / 98% with one-line benefit each
4. Video reviews carousel: 4-6 placeholders with play + mute icons
5. "Why Choose [Brand] vs Others" comparison table (green checks vs red X's)
6. "Transform Your [outcome]" 3-product grid
7. 5-step ritual timeline ("Glowing skin in 5 minutes")
8. Verified review grid with photos + 5 stars + "Verified Buyer" badge
9. Founder story block with photo
10. FAQ accordion (8-10 questions)
11. Sticky footer with email signup

PRODUCT PAGE MUST INCLUDE:
- BEST SELLER + sold-count badge ("10,000+ SOLD")
- 50% OFF urgency badge with strikethrough $99 → $44.99
- "Only [X] left in stock" scarcity counter
- 6-8 product images + 1 GIF of product in use
- 5 benefit bullets with icons
- 3-tier pricing (1 unit / 2 units / 3 units)
- Photo reviews (40+) + average star rating
- FAQ accordion repeated below
- Sticky add-to-cart on mobile

OUTPUT: Shopify-compatible store. Mobile-first. Page load <2s.
American English copy. USD currency.
```

### Section-Specific Re-Prompts

**Press bar:** Add a press bar directly under the hero. Light grey background, dark logos. Use: VOGUE, COSMOPOLITAN, FORBES, FOX, GLAMOUR. Center-aligned. Mobile: 2 rows of 2-3 logos. Caption above: "AS SEEN IN".

**Result donuts:** Add a 3-column section with circular percentage donuts. Numbers: 94%, 87%, 98%. Below each: short benefit. Brand-green fill. Animate on scroll.

**vs Competition table:** Build a comparison table titled "Why Choose [Brand] vs Others". Two columns: [Brand] (green checks) vs "Other Brands" (red X's). 7 rows: Clinically Proven Results / FDA Cleared / Money-Back Guarantee / Free US Shipping / Fast Visible Results / Premium Materials / 24/7 Support.

**Scarcity + urgency:** On the product page, above the price, add: "🔥 BEST SELLER · 10,000+ SOLD" (red pill). Below the price: "⏳ Only 12 left in stock — order before midnight for free US shipping." Above the strike-through price: "50% OFF TODAY ONLY".

**FAQ accordion:** Add 10 expandable questions: 1) Does it really work? 2) How fast will I see results? 3) Is it safe? 4) What's the return policy? 5) How long does shipping take? 6) Do I need a charger? 7) Can I use it daily? 8) Will it work for sensitive skin? 9) What's in the box? 10) Money-back guarantee terms. Warm, confident tone.

---

## Path 2 — Custom Liquid Sections (Deep Path)

When Accio output isn't bespoke enough — or when you want a hero product page that looks like a $5M/yr brand and reusable sections you can drop onto every future product — write the Liquid yourself.

### High-Level Approach
Shopify themes have two layers:
- **Default sections** that ship with Dawn (image-with-text, multicolumn, etc.) — these look generic and corporate
- **Custom sections** — Liquid files written from scratch with their own HTML, CSS, and `{% schema %}` for Theme Customizer settings

The right move is to build 7 custom sections rather than fight Dawn's defaults, then assign them to one product via a custom JSON template (e.g. `product.led-mask.json`) so that product alone uses this layout while every other product still uses standard Dawn.

### The 4-File Pattern Per Section
Every custom section is the same 4-file structure:

```
sections/custom-feature-grid.liquid     ← the section itself (HTML + Liquid + schema)
assets/section-custom-feature-grid.css  ← scoped styles
templates/product.led-mask.json         ← assigns which sections render on the page
config/settings_schema.json             ← (only if you need new global theme settings)
```

### The Three Parts of a `.liquid` Section

```liquid
{{ 'section-custom-feature-grid.css' | asset_url | stylesheet_tag }}

<section class="custom-feature-grid">
  <h2>{{ section.settings.heading }}</h2>
  {% for block in section.blocks %}
    <div class="feature-card">
      <h3>{{ block.settings.title }}</h3>
      <p>{{ block.settings.description }}</p>
    </div>
  {% endfor %}
</section>

{% schema %}
{
  "name": "Custom Feature Grid",
  "settings": [
    { "type": "text", "id": "heading", "label": "Heading", "default": "Why it works" }
  ],
  "blocks": [
    {
      "type": "feature",
      "name": "Feature card",
      "settings": [
        { "type": "text", "id": "title", "label": "Title" },
        { "type": "richtext", "id": "description", "label": "Description" }
      ]
    }
  ],
  "presets": [{ "name": "Custom Feature Grid" }]
}
{% endschema %}
```

The `{% schema %}` block at the bottom is the magic — it tells the Theme Customizer (Shopify Admin → Online Store → Customize) what knobs to expose. The `"presets"` key is what makes the section show up in the "Add section" picker so you can drop it onto any page.

### The 4 Things That Make It Look Branded (Not Dawn)

#### 1. Define a brand system upfront, then apply it consistently
Before writing any section, pick a palette and typography pair tied to the brand positioning. Example for a "premium beauty" brand:

| Token | Value | Use |
|---|---|---|
| Warm tan | `#b89968` | CTAs, accents |
| Rose blush | `#e8b5a8` | Highlights, gradient backgrounds |
| Cream | `#faf6f0` | Section backgrounds (swap from default white) |
| Charcoal | `#2c2826` | Body text — never pure black, which looks harsh |
| Playfair Display italic | Headings | Emotional accents ("Real results, in real time") |
| Inter | Body + UI | Clean sans-serif baseline |

Inspiration: CurrentBody's Skin LED Mask Series 2 page, Reviva. Premium beauty, not techy gadget. Every section's CSS uses the same palette tokens so the page reads as one brand rather than 7 disconnected blocks.

#### 2. Write your own CSS rather than overriding Dawn's
Dawn's CSS uses `--color-foreground` style tokens designed for theme-wide consistency, but they fight you when you want a custom look. Instead, scope each custom section's CSS to its own section class (`.custom-feature-grid`, `.custom-hero-banner`) and write its own colour values. Avoids global side-effects on other pages and lets each section have a strong opinion.

```css
.custom-feature-grid {
  background: #faf6f0;
  padding: 80px 24px;
}
.custom-feature-grid .feature-card {
  background: #fff;
  border: 1px solid #e8b5a8;
  border-radius: 16px;
  padding: 32px;
  transition: transform 0.3s ease;
}
.custom-feature-grid .feature-card:hover {
  transform: translateY(-4px);
}
```

#### 3. Add editorial details Dawn defaults don't have
Things that make a page feel premium vs templated:
- Italic Playfair accents on emotional words (`<em>Real results, in real time</em>`)
- Generous padding (80–120px vertical between sections vs Dawn's tight 40px)
- Subtle hover transitions on cards
- Asymmetric layouts in the hero (image left, text right but offset, not centred)
- No big colourful buttons — quiet `#b89968` tan CTAs that look considered
- Inline SVG icons in the spec table rather than emoji or stock icon fonts

#### 4. Make every section Customizer-editable
Every custom section exposes its key text/images/colours through the schema, so the brand owner can edit copy in the Customizer without touching code. The feature grid lets you add/remove/reorder feature cards by drag-and-drop in the admin UI — same as Dawn's native sections.

### How Sections Compose Into One Page
The product uses `templates/product.led-mask.json`, a JSON manifest listing which sections render in which order:

```json
{
  "sections": {
    "main": { "type": "main-product" },
    "hero": { "type": "custom-hero-banner", "settings": {} },
    "features": { "type": "custom-feature-grid", "settings": {}, "blocks": {} },
    "specs": { "type": "custom-specs-table", "settings": {} },
    "how-to": { "type": "custom-how-to-steps", "settings": {} },
    "comparison": { "type": "custom-comparison-table", "settings": {} },
    "faq": { "type": "custom-faq", "settings": {} },
    "cta": { "type": "custom-cta-banner", "settings": {} }
  },
  "order": ["main", "hero", "features", "specs", "how-to", "comparison", "faq", "cta"]
}
```

Then set `template_suffix: "led-mask"` on the product via the Shopify Admin API. That product alone uses this layout. Every other product still uses Dawn's standard `product.json`.

### The 7 Custom Sections To Build (Reference Pack)
For a branded DTC product page these are the 7 sections that earn their keep:

| # | Section | Purpose |
|---|---|---|
| 1 | `custom-hero-banner` | Asymmetric hero with product image + headline + CTA |
| 2 | `custom-feature-grid` | 3-4 benefit cards with icons + short copy |
| 3 | `custom-specs-table` | Product specs in a clean table with inline SVG icons |
| 4 | `custom-how-to-steps` | 5-step ritual / how-to-use timeline |
| 5 | `custom-comparison-table` | Your brand vs "Others" with checks/X's |
| 6 | `custom-faq` | Accordion with 8-10 questions |
| 7 | `custom-cta-banner` | Final urgency banner with discount + scarcity |

Because every section has `"presets"` in its schema, all 7 are now available to drop onto any product or page in your store via the Theme Customizer — not just the hero product.

### Why Path 2 Beats The Alternatives

- **vs. just typing into the description field:** Description text is unstyled HTML inside the theme's body container — no proper sections, no Customizer editing, no responsive grid. Looks like a Word document.
- **vs. a page builder app (PageFly, GemPages):** Those add 200kb+ of JavaScript, slow your page, and lock content inside a third-party app you have to keep paying for. Native sections are pure Liquid + CSS, render server-side, zero runtime cost.
- **vs. just using Dawn defaults:** Dawn is intentionally generic so it works for any product. To stand out you have to either pay for a premium theme (~$200) or write custom sections — the latter gives you total control.

---

## Apps To Layer On Top (Either Path)

| App | Tier | What It Does |
|---|---|---|
| Shopify | Required ($39/mo Basic) | Platform + checkout |
| Accio | Recommended | AI store builder |
| Loox | Essential ($9-30/mo) | Photo + video reviews |
| Vitals | Essential ($30/mo) | 40+ tools (sticky ATC, countdown, currency, upsells) |
| Klaviyo | Required (free under 250 contacts) | Email + SMS flows |
| Canva Pro | Required ($15/mo) | Banner + GIF + thumbnail design |
| Google Banana Pro (Google AI Studio) | Essential | Logo + product infographics — see `dtc-infographic-generator` skill |

---

## Pro Tips

- Don't ask Accio for a "nice store." Show it $1M/mo brand screenshots and say "build this look for my product."
- If you're going to write custom Liquid, define the brand system (palette + fonts) BEFORE you write any section. Otherwise each section drifts and the page looks disjointed.
- Cream backgrounds (`#faf6f0`) instead of pure white feel premium. Pure black text feels harsh — use charcoal (`#2c2826`).
- 80-120px vertical padding between sections beats Dawn's 40px every time.
- `template_suffix` is the unlock for per-product page layouts without touching every other product.
- Your conversion will jump 30-50% just from layering 10-15 Banana Pro infographics into the product page — generate those before you optimise ads.
