# Prompt — Gerar landing page de produto (Kimi Code)

> Cole este prompt na Kimi Code (ou Claude Code) com o `product-brief.md` preenchido
> e os prints/links das 3 referências. Substitui os valores entre {{ }}.

---

You are building a Shopify dropshipping product landing page that must convert cold
traffic from Meta and TikTok ads into buyers.

## Product data
[PASTE THE FILLED product-brief.md HERE]

## Design references (3 sources — do not copy any single one wholesale)
1. Homepage reference: {{REF_HOMEPAGE_URL}} — borrow: {{WHAT_TO_BORROW}}
2. Landing page reference: {{REF_LANDING_URL}} — borrow: {{WHAT_TO_BORROW}}
3. Hero section reference: {{REF_HERO_URL}} — borrow: {{WHAT_TO_BORROW}}

## Hard requirements
- Mobile-first (390px is the primary viewport), then scale to desktop.
- Single CTA focus: "Add to Cart". No nav menu, no links to other pages.
- Section order: announcement bar → hero (image, benefit headline, star rating,
  bundle selector with 3 options, price anchored, CTA, trust badges) → benefits
  (max 5, icon + title + 1 line) → UGC video (15–30s placeholder) → how it works
  (3 steps) → image gallery (infographic + angles + lifestyle) → 3 reviews with
  verified-buyer badge → comparison table (us vs others) → FAQ (5 questions that
  answer real objections) → guarantee box above final CTA → footer (minimal).
- Sticky add-to-cart bar appears after scrolling past the hero.
- Load target: < 2.5s on 4G; hero image < 200KB.
- Style: premium but warm. Off-white background (#F5F6F2), near-black text (#111),
  ONE accent color used only for CTAs, badges and key highlights. No gradients.
- Every image placeholder must be a named slot (hero-main, angle-1/2/3,
  lifestyle-1/2, infographic-1, ugc-video, review-avatar-1/2/3) so assets can be
  generated and swapped programmatically.
- Copy voice: direct, benefit-first, second person. Short sentences. No exclamation
  marks except in the announcement bar. UK/US English.
- The page must be a single self-contained HTML file with inline CSS/JS.

## Output
One complete HTML file. After the code, list: (1) the image slots with exact aspect
ratios and sizes needed, (2) any sections where a reference couldn't be matched and
you improvised.
