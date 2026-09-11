---
target: VDC Imóveis homepage (app/templates/index.html)
total_score: 28
max_score: 36
na_heuristics: 10
p0_count: 1
p1_count: 2
timestamp: 2026-08-07T19-00-37Z
slug: app-templates-index-html
---
## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3/4 | Hero carousel autoplays (6s) with only 8px dots as pause/status cue; form submit feedback ("Enviando...") is good but isolated. |
| 2 | Match Between System and Real World | 4/4 | Real neighborhood names, professional registries (CREA-BA, OAB-BA), no jargon. |
| 3 | User Control and Freedom | 3/4 | Favorite removal is instant, no undo — one accidental tap permanently loses a saved property. |
| 4 | Consistency and Standards | 2/4 | Confirmed twice: the same "Falar com consultor" action renders in 3 different visual weights across the page, and eyebrow-label color contradicts the design system's own contrast table (rendered evidence: 2.4:1 on white, DESIGN.md flags this exact combo as "never text"). |
| 5 | Error Prevention | 3/4 | Contact phone field has no input mask/pattern despite the same CEP-autofill pattern already existing in the admin panel's JS. |
| 6 | Recognition Rather Than Recall | 4/4 | Icon+label pairing; active-section highlighting in header nav via IntersectionObserver. |
| 7 | Flexibility and Efficiency of Use | 3/4 | Quick-filter chips and favorites are real accelerators, but identical/hardcoded for every visitor. |
| 8 | Aesthetic and Minimalist Design | 3/4 | Hero badge presents "1" as if a counted metric ("1 mesa só..."), which cuts against the brand's own "prova concreta, não promessa vaga" principle. Rendered evidence also found 10px functional text (below an 11px floor) on 11 status/type tags. |
| 9 | Error Recovery | 3/4 | No `:invalid`/error styling anywhere for the contact form — a blank required field falls back to the browser's unstyled native bubble. |
| 10 | Help and Documentation | n/a | Product substitutes a human consultant (WhatsApp/contact) for self-serve docs — not a gap for this surface. |
| **Total** | | **28/36** | **Good (78%)** |

## Design Specificity Verdict

**Mostly earned, not fully.** The typography/data system (IBM Plex Mono for every price, m², CRECI, credential) and the credential-forward content strategy (real neighborhoods, real professional registries, the "same table" specialties metaphor turning the tagline into literal layout) are specifically authored for this brand — they could not be dropped into a generic real-estate template unchanged. Against that, the hero skeleton (full-bleed photo, dark veil, centered headline, floating search card) and the property-card grammar are standard listing-site vocabulary. A visitor who only sees the hero could mistake this for a template; one who scrolls to specialties/seals/team could not.

**Deterministic scan** (live-rendered evidence, `detect.mjs` browser overlay): 29 anti-patterns grouped across ~13 distinct types not visible from static source alone — `low-contrast` (3.3:1 navy-on-gold-gradient text on the gold CTA button; 2.0:1 white text on the WhatsApp green button — both below the 4.5:1 floor), `undersized-ui-text` (10px on 11 status/type tags — "Destaque" ×6, property-type labels), `kicker-above-heading` (the eyebrow-above-h2/h3 pattern repeated 11 times identically), plus `clipped-overflow-container`, `gray-on-color`, `dark-glow`, `side-tab`, `gpt-thin-border-wide-shadow`, and one `ai-color-palette` hit. The static CLI scan (source-only) separately found 5 `layout-transition` warnings (animating `height`/`max-height`/`width` instead of `transform`) and 1 `bounce-easing` overshoot (`cubic-bezier(.34, 1.56, .64, 1)`).

**False positives / out of scope**: the `ai-color-palette` "purple gradient" hit is the official Instagram-brand gradient button, which DESIGN.md explicitly requires and forbids altering (third-party mark, same exception class as the WhatsApp green) — not a real slop pattern here. A `broken-image` hit in `admin/hero.html` is an admin upload-preview placeholder outside the reviewed homepage surface, not a customer-facing defect.

**Visual overlays**: no user-visible browser tab was available this session (no native browser tool exposed); evidence was gathered via a headless Playwright injection instead, so there is no `[Human]` tab to point to — the console summary above is the full evidence trail.

## Overall Impression

The page earns its positioning in words and in its credential-forward structure — CRECI/CREA/OAB numbers as first-class UI, real neighborhood names, a monospace data system that quietly signals "there's a laudo and a number behind this." But the visual execution dips at exactly the two moments where a "biggest purchase of your life" decision most needs reinforcement: the Team section (half the proof is unnamed placeholders styled identically to the named, credentialed members) and the mobile properties section (the WhatsApp/Instagram FABs sit directly on top of the primary "Falar com consultor" click target). The single biggest opportunity is closing that gap between what the copy promises and what the pixels currently deliver at the trust-critical moments.

## What's Working

1. **The mono/display/body type system is load-bearing, not decorative.** Prices, CRECI numbers, and specs consistently render in IBM Plex Mono against Archivo headlines (hero, cards, credentials alike) — exactly the "there's a number and a laudo behind this" signal the brand doc calls for, applied with real discipline.
2. **The specialties section literalizes the brand's own tagline.** Four icons resting on one shared gold rule turns "consultoria, engenharia e jurídico na mesma mesa" into an actual visual structure instead of an icon-grid with a caption.
3. **The WhatsApp/E-mail contact switch uses color as information, not decoration** — the sliding thumb's green vs. gold signals "instant channel" vs. "async channel" and replaces what used to be two competing boxes with one clear choice.

## Priority Issues

**[P0] Floating WhatsApp/Instagram buttons collide with the property-card conversion CTA on mobile**
- **Why it matters**: This is a lead-gen page; "Falar com consultor" on a specific listing is the highest-intent click available. At 390×844, the Instagram FAB bounding box overlaps the first property card's CTA bounding box at the properties section's default scroll rest position — confirmed both visually and via DOM rect intersection.
- **Fix**: Give the FAB stack a scroll-aware offset, or reserve a bottom-right exclusion margin on the property card CTA so it never sits under the fixed 56px circles.
- **Suggested command**: `$impeccable layout`

**[P1] Contrast and legibility failures across multiple components, several contradicting the design system's own documented rules**
- **Why it matters**: `.vdc-eyebrow` defaults to gold-500 and is used as real section-label text on white/off-white backgrounds in 5+ places ("Como trabalhamos," "Selecionados a dedo," "Prova, não promessa," "Quem está na mesa," "Não achou o imóvel ideal?") — DESIGN.md's own table states this exact combination measures 2.4:1 and is "decorative only, never text." Live-rendered evidence adds two more: the gold CTA button's gradient drops to ~3.3:1 for its navy text near the gold-700 end, and the WhatsApp button's white text on `#25D366` measures 2.0:1 — both below the 4.5:1 floor. Separately, 11 status/type tags ("Destaque," property-type labels) render at 10px, below an 11px legibility floor. PRODUCT.md claims "contraste AA/AAA verificado" for the site; this contradicts that claim in five-plus places.
- **Fix**: Swap the eyebrow default to `--vdc-navy-500` (already documented as an approved alternate in DESIGN.md §4.2) on light backgrounds; fix or shorten the gold-button gradient so the navy text stays above 4.5:1 across its full range; bump the 10px tag text to at least 11-12px.
- **Suggested command**: `$impeccable colorize`

**[P1] Keyboard focus can land on invisible or mid-fade content**
- **Why it matters**: All post-hero sections start at `opacity:0`, gated behind scroll-triggered animation. Tabbing through without manual scrolling (letting the browser's native "scroll focused element into view" do the work) lands focus on links and buttons while their ancestor section is still measured at `opacity: 0` or mid-fade — a sighted keyboard-only user sees their focus outline appear on invisible content, undermining an otherwise solid `:focus-visible` system.
- **Fix**: Don't gate interactive elements' visibility behind scroll animation — animate only decorative wrappers — or force full opacity on `:focus-within` regardless of scroll-trigger state.
- **Suggested command**: `$impeccable harden`

**[P2] Footer logo renders as a visible white box on the navy gradient**
- **Why it matters**: The logo file has a solid white circular background baked in. That's invisible against the white header but produces an obvious white square floating on navy in the (global, every-page) footer — DESIGN.md explicitly requires a white-monochrome variant on solid navy and explicitly forbids placing the mark inside a colored box.
- **Fix**: Export and use a true white/transparent logo variant for navy-background placements; keep the current colored-on-white PNG for light backgrounds only.
- **Suggested command**: `$impeccable polish`

**[P2] Team section's anonymous placeholders are visually undifferentiated from the named, credentialed members**
- **Why it matters**: The two unnamed roles are an intentional, documented placeholder (no invented names per PRODUCT.md) — but they render with the exact same avatar treatment, type scale, and credential-line format as Deyse Fontes/CREA-BA and Dr. José Ângelo/OAB-BA, in the section DESIGN.md itself calls the brand's most underused proof asset. Half the proof reads as filler at the exact moment a buyer is deciding whether to trust real people with their biggest purchase.
- **Fix**: Visually differentiate the placeholder cards (a subtle "vaga em preenchimento" tag, dashed avatar ring, or reduced-emphasis treatment) so the page is honest about team size without looking like unfinished content dressed as final.
- **Suggested command**: `$impeccable clarify`

## Persona Red Flags

**Jordan (first-timer)**: Landing on the Team section and seeing two of four cards with no name reads as either an unfinished site or a smaller company than "quatro especialidades reunidas" implies, at a first-visit credibility moment. The property-card spec row is icon-only with no text labels, so an unfamiliar visitor has to infer meaning from position alone.

**Sam (accessibility-dependent)**: Hit directly by both P1 findings — the eyebrow/gold-button/WhatsApp-button contrast failures (measured 2.0-3.3:1, all below the 4.5:1 AA floor) and the scroll-gated opacity-0 content that lets keyboard focus land on invisible or mid-fade elements.

**Casey (mobile)**: Hit directly by the P0 finding — the fixed WhatsApp/Instagram FABs overlap the property card's primary conversion CTA at the properties section's default scroll rest position, confirmed by DOM rect intersection at a real 390×844 viewport.

## Minor Observations

- Opening the mega menu puts two gold CTA buttons on screen simultaneously (megamenu "Ver imóveis" + hero "Buscar," still visible beneath the panel) — DESIGN.md documents gold as "one per screen."
- Property cards mix real photos with line-icon placeholder covers in the same grid with no "photo coming soon" signal, reading as unfinished rather than intentional (expected, given placeholder inventory per PRODUCT.md, but worth a visual cue).
- Favorite removal is instant and irreversible, no confirm/undo.
- Contact form phone input has no format mask, despite the same smart-input pattern already existing in the admin panel's CEP autofill.
- Static-scan-only findings (lower severity, `warning`): 5 instances of animating `height`/`max-height`/`width` instead of `transform` (layout-thrash risk); 1 bounce/elastic easing overshoot (`cubic-bezier(.34, 1.56, .64, 1)`).
- Additional live-rendered detector flags without a clear priority-issue home: `clipped-overflow-container` (hero section clips a positioned child), `gray-on-color` text on navy (×2), `dark-glow` (colored box-shadow glow on dark background), `side-tab` (3px top border pattern), `gpt-thin-border-wide-shadow` (1px border + 48px shadow blur, ×2), `hero-eyebrow-chip` pattern on the hero eyebrow.

## Questions to Consider

- If the mega menu can put a second gold button on screen next to the hero's, what actually enforces "one gold CTA per screen" in practice — is it checked before shipping, or just a note in a document nobody re-reads?
- Two of four "quatro especialidades reunidas" team members have no name — is that framed anywhere as "team growing," or does it just quietly read as smaller than the section header claims?
- Every section past the hero exists on the page only if a scroll event fires and the animation library loads successfully — has this been checked on a flaky connection, under "Print to PDF," or for a screen-reader user who jumps by landmark instead of scrolling?
