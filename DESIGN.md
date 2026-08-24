# PumpRun Design System

## 1. Atmosphere & Identity

A working tool for a working trade. PumpRun feels like well-kept heavy equipment:
deep spruce green steel, warm paper paperwork, amber warning lights. Dense where
data lives (routes, invoices, filing clocks), spacious where decisions happen
(dashboards, pricing). The signature is the **spruce-on-paper pairing** — a dark
green chrome frame around light, calm content, with amber reserved exclusively
for money and urgency. Nothing glossy; this must look credible on a phone in a
truck cab and on a health-board desk alike.

## 2. Color

### Palette

| Role | Token | Value | Usage |
|------|-------|-------|-------|
| Brand/darkest | --spruce-900 | #0b2e24 | Topbar, hero gradient start |
| Brand/dark | --spruce-800 | #0f3d2f | Button hover, h3 text |
| Brand/primary | --spruce-700 | #14663b | Primary buttons, links, focus |
| Brand/tint | --spruce-100 | #dcefe4 | Route-stop chips, secondary hover |
| Surface/page | --paper | #faf9f6 | Page background |
| Surface/card | --card | #ffffff | Cards, tables |
| Text/primary | --ink | #17211c | Body, headings |
| Text/secondary | --ink-soft | #5b6a62 | Hints, captions, labels |
| Border/default | --line | #e6e3da | Card borders, dividers |
| Accent/money | --amber | #b45309 | Due badges, founding offer |
| Accent/money-bg | --amber-bg | #fef3c7 | Due badge background |
| Status/error | --red | #b91c1c | Overdue text, destructive |
| Status/error-bg | --red-bg | #fee2e2 | Overdue badge, error banners |
| Status/success-bg | --green-bg | #dcfce7 | Paid badge |

### Rules
- Amber is money/urgency only. Never decorative.
- Spruce green is interactive elements + brand chrome only.
- Status colors (red/green) appear only as text+background pairs from this table.
- No color outside this table. Extend the table first.

## 3. Typography

### Scale

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Hero display | 1.9rem | 800 | Home/pricing hero h1 |
| Stat numeral | 1.7rem | 800 | Dashboard stat tiles |
| Invoice total | 1.6rem | 800 | Public invoice total |
| H2 | 1.35rem | 700 | Card/section titles |
| H3 | 1.05rem | 700 | Sub-sections, plan names |
| Body | 1rem | 400 | Default |
| Table/body-sm | 0.93rem | 400 | Table cells |
| Button | 0.95rem | 700 | All buttons |
| Hint/caption | 0.83rem | 400 | Hints, meta |
| Kicker | 0.72rem | 700 uppercase, +0.12em tracking | Card section labels |

### Font Stack
- Primary: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif
  (intentional: zero webfont requests on a rural-connection tool; SF/Roboto render
  cleanly at small sizes). Accepted trade-off, not an oversight.
- Numerals in tables/invoice totals: `font-variant-numeric: tabular-nums`.

### Rules
- Sentence case everywhere; kickers are the only uppercase.
- Headings wrap rarely; apply `text-wrap: balance` to h1/h2.

## 4. Spacing & Layout

Base unit: 4px.

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | 4px | Icon-label gaps |
| space-2 | 8px | Inline groups, list items |
| space-3 | 12px | Default gaps |
| space-4 | 16px | Card inner padding (min) |
| space-5 | 20px | Card padding (default 1.15-1.25rem) |
| space-6 | 24px | Card groups |
| space-8 | 32px | Page section breaks |

### Grid
- Content container: max-width 56rem, centered, 1rem inline padding.
- Nav/footer inner: max-width 68rem (chrome reads wider than content).
- Breakpoints: single fluid layout; 480px inline-padding adjustment only.
- Full-bleed: topbar and footer span 100vw; content never does.

## 5. Components

### Card
- Structure: `<div class="card">` — white surface, 1px --line border, 12px radius, tinted shadow.
- Variants: `.pricecard` (pricing tier), `.pricecard.featured` (2px spruce border + tag).
- States: none interactive; static surfaces.
- Used on: every page. The primary layout primitive.

### Stat tile (`.stat`, `.statstrip`)
- Grid of number+label tiles; `.bad`/`.warn`/`.good` recolor the numeral.
- Empty state: renders 0 honestly.

### Button (`.btn`)
- Variants: default (spruce fill), `.secondary` (white + border), `.danger`,
  `.big` (full-width, larger). `<button>` and `<a>` share styles.
- States: hover darkens; **active/focus added this pass** (see §6/§8).
- Spacing: 0.55–0.95rem padding, 10px radius.

### Route stop (`ol.route li`)
- Numbered chip (spruce tint square), name + driver chip, trailing actions.
- Completed stops show status pill + PDF/invoice links + inline mark-paid form.

### Status pills (`.pill-*`, `.badge.due/.paid`)
- paid/completed: green pair; due: amber pair; pending: indigo; overdue: red.

### Forms
- Stacked labels, full-width inputs, 10px radius, spruce focus ring.
- Errors: `.errors` red banner; field-level errors listed below the form.

### Nav (`.topbar` + `.nav-inner`)
- Sticky, full-bleed spruce-900; brand + links + auth action; CTA pill for anon.

## 6. Motion & Interaction

- Micro transitions (150-200ms ease-out) on button/background color changes.
- **This pass adds**: `:active` press feedback (`translateY(1px)`), visible
  `:focus-visible` rings, `scroll-behavior: smooth`, and a
  `prefers-reduced-motion` guard that disables smooth-scroll.
- No decorative animation exists or will be added: motion signals state change only.

## 7. Depth & Surface

Strategy: **mixed** — borders define surfaces; one tinted, low-opacity shadow
(`--shadow`) lifts cards off the paper; hero uses a spruce gradient as the single
atmospheric band. No glass, no noise overlays — materials must survive a dirty
phone screen.

## 8. Accessibility Constraints & Accepted Debt

### Constraints
- WCAG 2.2 AA target: body contrast ≥ 4.5:1 (ink on paper = 14.9:1; hint on white = 5.5:1 ✓).
- Visible focus ring on every interactive element (`:focus-visible`, 3px spruce-tinted).
- Full keyboard reachability; skip-to-content link (added this pass).
- Tap targets ≥ 44px on mobile for primary actions.
- `prefers-reduced-motion` disables smooth scroll (only motion present).

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
|------|----------|--------------|--------------|
| System font stack (no brand webfont) | global | Zero webfont requests for rural connections; performance-first trade | Revisit if brand work justifies a self-hosted variable font |
| Inline `style=""` on 2-3 one-off banners | pricing.html, login/signup cards | One-off sections; not reusable patterns | Fold into classes if a 2nd instance appears |
| No privacy/terms pages | footer | Solo founder, no legal counsel yet | Before first paid annual invoice |
| Django default 500 page | global | Rare; branded 404 shipped this pass | With custom domain work |
| title5_kit_done / invoice pages carry own styles | standalone pages | Intentionally standalone (print/share contexts) | If brand audit flags drift |
