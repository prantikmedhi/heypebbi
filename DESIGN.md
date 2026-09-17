---
version: alpha
name: HeyPebbi — Pocket-world tactility
description: An expressive native companion with ceramic character, tactile trays, and clear human control.
colors:
  primary: "#176B62"
  sea-glass: "#9CDBCB"
  cream: "#FFF8E9"
  surface: "#FFFCF6"
  clay: "#F2A18A"
  lilac: "#CFBCEB"
  butter: "#F4D878"
  ink: "#35283E"
  muted: "#6B5B70"
  edge: "#88768E"
  danger: "#A53545"
  night: "#231D2B"
  night-surface: "#302737"
  night-raised: "#3D3145"
  night-ink: "#FFF3DB"
  night-muted: "#CCBED1"
  night-edge: "#AC98B4"
  primary-hover: "#11534D"
  danger-soft: "#FFC4BB"
typography:
  display:
    fontFamily: "ui-rounded, system-ui, sans-serif"
    fontSize: 64px
    fontWeight: 750
    lineHeight: 1.04
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "ui-rounded, system-ui, sans-serif"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  section:
    fontFamily: "ui-rounded, system-ui, sans-serif"
    fontSize: 22px
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body-large:
    fontFamily: "system-ui, sans-serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  body:
    fontFamily: "system-ui, sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  label:
    fontFamily: "ui-rounded, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "0em"
  caption:
    fontFamily: "system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.01em"
  perch:
    fontFamily: "ui-rounded, system-ui, sans-serif"
    fontSize: 13px
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "0em"
  code:
    fontFamily: "ui-monospace, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
rounded:
  xs: 6px
  control: 12px
  tile: 20px
  tray: 28px
  pill: 999px
spacing:
  micro: 4px
  tight: 8px
  control: 12px
  base: 16px
  group: 24px
  section: 32px
  world: 48px
components:
  home-light:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.tray}"
    padding: "{spacing.section}"
  home-dark:
    backgroundColor: "{colors.night}"
    textColor: "{colors.night-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.tray}"
    padding: "{spacing.section}"
  tray-light:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.tile}"
    padding: "{spacing.group}"
  tray-dark:
    backgroundColor: "{colors.night-surface}"
    textColor: "{colors.night-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.tile}"
    padding: "{spacing.group}"
  inspector-dark:
    backgroundColor: "{colors.night-raised}"
    textColor: "{colors.night-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.tile}"
    padding: "{spacing.base}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.cream}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.cream}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  button-primary-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  button-primary-dark:
    backgroundColor: "{colors.sea-glass}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
    height: "44px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  button-secondary-dark:
    backgroundColor: "{colors.night-raised}"
    textColor: "{colors.sea-glass}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  button-disabled:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  button-disabled-dark:
    backgroundColor: "{colors.night-raised}"
    textColor: "{colors.night-muted}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  destructive:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.cream}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  destructive-dark:
    backgroundColor: "{colors.danger-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  input-light:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  input-dark:
    backgroundColor: "{colors.night-raised}"
    textColor: "{colors.night-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "{spacing.control}"
  selection-light:
    backgroundColor: "{colors.sea-glass}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "{spacing.tight}"
  approval-chip:
    backgroundColor: "{colors.butter}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "{spacing.tight}"
  speech-chip:
    backgroundColor: "{colors.clay}"
    textColor: "{colors.ink}"
    typography: "{typography.perch}"
    rounded: "{rounded.pill}"
    padding: "{spacing.tight}"
  memory-chip:
    backgroundColor: "{colors.lilac}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "{spacing.tight}"
  task-chip:
    backgroundColor: "{colors.sea-glass}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "{spacing.tight}"
  caption-light:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: "{spacing.micro}"
  caption-dark:
    backgroundColor: "{colors.night}"
    textColor: "{colors.night-muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: "{spacing.micro}"
  perch-light:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.ink}"
    typography: "{typography.perch}"
    rounded: "{rounded.pill}"
    padding: "{spacing.control}"
    height: "44px"
  perch-dark:
    backgroundColor: "{colors.night-surface}"
    textColor: "{colors.night-ink}"
    typography: "{typography.perch}"
    rounded: "{rounded.pill}"
    padding: "{spacing.control}"
    height: "44px"
  focus-stroke-light:
    backgroundColor: "{colors.primary}"
  focus-stroke-dark:
    backgroundColor: "{colors.butter}"
  control-edge-light:
    backgroundColor: "{colors.edge}"
  control-edge-dark:
    backgroundColor: "{colors.night-edge}"
  identity-display:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.ink}"
    typography: "{typography.display}"
    rounded: "{rounded.tray}"
    padding: "{spacing.world}"
  window-title:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.tile}"
    padding: "{spacing.base}"
  section-title:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.section}"
    rounded: "{rounded.tile}"
    padding: "{spacing.base}"
  reading-body:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-large}"
    rounded: "{rounded.tile}"
    padding: "{spacing.group}"
  code-block:
    backgroundColor: "{colors.night}"
    textColor: "{colors.night-ink}"
    typography: "{typography.code}"
    rounded: "{rounded.xs}"
    padding: "{spacing.base}"
---

# HeyPebbi design system

## Overview

**Pocket-world tactility** is an expressive, non-minimalist identity for **HeyPebbi**, the project/company-facing brand; **Pebbi** is the native macOS app and default companion; persistent assistants are **Pebbis**. `heypebbi.com` is the selected domain, not evidence of registration or trademark clearance. [The canonical contract](docs/CONTRACT.md) controls scope and vocabulary.

The defining composition is a small ceramic companion resting among useful, colored objects: a sea-glass task tile, a folded butter permission slip, a lilac memory tab. Large sculptural color areas, rounded deliberate type, asymmetrical illustration and soft material edges create richness. Long reading and safety decisions sit on opaque, orderly planes. This is neither monochrome minimalism nor an indigo SaaS system. Do not imitate another companion's silhouette, face, copy or layout.

**Three material layers:** desk → tray → object. **Three levels of expression:** identity spreads may be abundant; Home reserves an expressive upper shelf above productive lists; approvals and errors suppress decorative motion and prioritize facts. Richness comes from authored composition, not more UI chrome. Native SwiftUI/AppKit controls retain their familiar behavior; HTML here is documentation only.

See [Brand](docs/design/BRAND.md), [Screens](docs/design/SCREENS.md), [Components](docs/design/COMPONENTS.md), [Motion](docs/design/MOTION.md), [Accessibility](docs/design/ACCESSIBILITY.md), and [Assets](docs/design/ASSETS.md). The [static brand board](docs/design/brand-board.html) is a design reference, never a shipped-product claim.

## Colors

Exact values live in the front matter. SVG and HTML reference artifacts contain literal snapshots of these tokens; other documents name tokens instead of maintaining competing palettes. No per-Pebbi color picker may create unreadable text pairs.

| Role | Light tokens | Dark tokens | Rules |
|---|---|---|---|
| Desk | `cream` / `ink` | `night` / `night-ink` | Opaque reading background; dark is warm plum, not inverted cream |
| Tray | `surface` / `ink` | `night-surface` / `night-ink` | One layer above desk |
| Raised inspector | `surface` / `ink` | `night-raised` / `night-ink` | Border still required where a control needs an edge |
| Main action | `primary` / `cream` | `sea-glass` / `ink` | One emphasized commit per decision group |
| Quiet text | `muted` | `night-muted` | Use on neutral planes only; never faded with blanket opacity |
| Control outline | `edge` | `night-edge` | Essential boundaries at least 3:1, not small text |
| Focus | `primary` | `butter` | Two-point outer ring plus two-point surface gap |
| Destructive | `danger` / `cream` | `danger-soft` / `ink` | Explicit verb and consequence, not merely red |
| Character/task tile | `sea-glass` / `ink` | Same opaque pair | General identity, not a success guarantee |
| Voice/object accent | `clay` / `ink` | Same opaque pair | Listening/speaking still have distinct icons and text |
| Memory/object accent | `lilac` / `ink` | Same opaque pair | Small labels, not a purple software theme |
| Attention/approval | `butter` / `ink` | Same opaque pair | Icon + reason + actionable label |

Text targets: at least 4.5:1 for ordinary text, 3:1 for qualifying large text, and 3:1 for meaningful non-text controls. This system exceeds 4.5:1 even for the main display pair. Computed examples: `cream` on `primary` 5.99:1; `ink` on `sea-glass` 8.80:1; on `clay` 6.72:1; on `lilac` 7.90:1; on `butter` 9.80:1. `night-muted` on `night-raised` 6.88:1. `edge` against `cream` 3.95:1 is for geometry, not body text. Always recompute for a changed pairing.

Do not put cream text on pastel accents. Color roles do not replace icons, state strings or accessible names. Illustrative glaze may mix token colors through opacity; text and safety UI may not use an untested translucent mixture. System Increase Contrast adds the specified opaque edge; Reduce Transparency removes material blur. System high-contrast colors may override brand selections when required for accessibility.

## Typography

The type posture is **soft voice, precise content**. Use platform rounded text for titles, labels and the perch; use the normal platform system face for long prose and dense tables. Native mapping: request system fonts through SwiftUI/AppKit with rounded design for rounded roles; never identify or bundle Apple's font files. Use platform fallback where rounded is unavailable. CSS `ui-rounded, system-ui, sans-serif` is deliberate documentation fallback, not a promise that every browser has the same rounded face.

| Token | Intended native point size / use |
|---|---|
| `display` | 64, identity board only; fluid web display may reduce to 40 |
| `headline` | 32, Home greeting and first-run title |
| `section` | 22, sections and inspector heading |
| `body-large` | 17, readable conversation option |
| `body` | 15, standard reading and forms |
| `label` | 14, controls and task titles |
| `caption` | 12, metadata, never the sole safety explanation |
| `perch` | 13, compact state text; expand rather than shrink |
| `code` | 13, monospace paths, commands and structured output |

Spec dimensions use `px` because the format requires CSS units. Treat one nominal token px as one native layout point, not one physical display pixel; retain native text metrics. The custom SVG wordmark is original outlined geometry, not a downloadable typeface. No external fonts are required, embedded, fetched or bundled. This avoids network dependence and Apple-font redistribution. Use bold and optical size, not all-caps paragraphs. Platform text rendering owns tracking for native body copy; the listed tracking is reference intent, not a reason to override script-specific shaping.

Provide application text scaling 100–200% and respect platform accessibility preferences. Row heights expand with text, localized labels wrap, numeric progress uses tabular figures only where alignment is necessary. A long filename may truncate in the middle with full accessible value and disclosure; a permission scope, error or destructive consequence must wrap without truncation.

## Layout

Home is **Operate** with an expressive shelf, not a marketing hero. Stable sidebar order: **Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections, Settings**. A persistent task inspector is secondary, never a substitute name for Conversations. Conversation and task are different objects.

Native Home default reference size is 1180 × 780 points. At 1080 points and wider: 208-point sidebar, flexible primary pane, optional 304-point task inspector, 24-point content gutters. At 840–1079: 180-point sidebar, inspector becomes a dismissible sheet or drill-in. At 640–839: sidebar collapses to a labeled toolbar control; content becomes a single reading column; task inspector is a navigable detail view with Back. Comfortable Home minimum is 640 × 480; if the display's visible area is smaller, permit a compact single-pane fallback with scrolling and never place close/stop off-screen. At large text sizes collapse columns based on measured content fit, not only these nominal thresholds.

The perch uses an ordinary top-edge panel on any display. Collapsed target is 176 × 44 points; expanded reference is 360 × 156. These are starting dimensions, not clipping bounds. Hardware notch geometry is excluded from interactive regions; do not draw controls into the sensor housing or cover system menu items. On a notchless/external display use the same panel below the menu bar; a persistent menu-bar item opens Home if the panel cannot fit. Respect each screen's visible frame, safe area, scale and active Space. No fake notch is drawn. Focus stays in the user's current app until an explicit activation needs input.

Spacing is a 4-point base: micro, tight, control, base, group, section, world. Compound density is content-driven. Rich identity sections can break the grid with illustrations; working rows, keyboard focus and text baselines may not. Sheet buttons remain visible when body scrolls. HTML board reflows below 900 CSS pixels and stacks below 600, with no horizontal document scroll at 320; its pictured native window is a labeled schematic, not a mobile-app specification.

## Elevation & Depth

Desk has no shadow. A tray uses a one-point outline and a soft offset shadow: light, `ink` at 10% opacity, x=0, y=8, blur=24; dark, `night` at 45%, x=0, y=8, blur=24 plus `night-edge` at full opacity wherever the boundary is essential. A floating panel uses x=0, y=12, blur=32 at the same source token with opacity 16% light / 55% dark. These are illustrative shadow recipes, not additional color tokens.

Objects may have a three-point underside ledge and an upper-left glaze highlight: `cream` at 45% in light, `night-ink` at 18% in dark. These effects belong to decorative ceramic illustration, not control text. Task content remains flat and legible. Approval sheets have opaque bodies; native modal treatment supplies separation. Never stack translucent reading surfaces or make contrast depend on the user's wallpaper. Reduce Transparency uses fully opaque backgrounds with unchanged layout.

## Shapes

A Pebbi is a low, asymmetrical river-stone body: high left shoulder, gentler right shoulder, wide flattened base, two small inset eyes and an upturned mouth. A clay thumbprint at the lower cheek and a short off-center glaze ridge distinguish the expressive mascot from a generic circular face. Flat logo geometry omits material details; it remains recognizable at small sizes. Do not deform the silhouette into a copied character or add limbs to explain ordinary status.

Native controls use continuous corners matching `control`; content objects use `tile`; trays use `tray`; status chips use `pill`; code and compact inset details use `xs`. Never give every item the same pill silhouette. Use system window corners, traffic lights and native resize behavior rather than replacing them with brand decoration. Illustration shadows are not hit areas. Icons have 1.75-point nominal strokes on a 20-point grid, optical alignment and 28-point minimum compact hit regions; high-priority controls use 44-point targets.

## Components

YAML component entries are atomic examples and theme pairs, not executable widgets. Only spec-supported properties appear. Border, shadow, focus, animation and state behavior are prose rules in [Components](docs/design/COMPONENTS.md). Every palette token is referenced by a component; edge tokens are deliberately background-only stroke swatches, not body-text examples.

`button-primary`, `button-primary-hover` and `button-primary-pressed` are separate states. Their dark equivalents preserve action contrast rather than mechanically inverting. Keyboard focus is independent of selection and hover. Pointer-down highlights immediately; release within bounds commits. Busy actions show exact verb and state, not an unrelated mascot loop. Disabled controls remain readable and have an explanation outside the disabled hit target.

Task state, voice state, dictation state, connection state and routine state are independent axes. Canonical strings and UI labels are exhaustively mapped in [Components](docs/design/COMPONENTS.md); [Screens](docs/design/SCREENS.md) binds them to PB-001 through PB-040. Never use a smiling Pebbi or green accent as proof of task success. Speech interruption does not cancel a task; **Stop speaking** and **Cancel task** are distinct controls. Privacy, pending approval, capture and takeover have persistent labeled affordances.

For every interactive component document default, hover, pressed, focus, disabled and busy, plus selected/error where meaningful. All icon actions have accessible names and shortcuts where appropriate; noninteractive decorations do not enter the accessibility tree. Full behavior for the mascot and native transitions is in [Motion](docs/design/MOTION.md).

## Do's and Don'ts

- Do build expressive pockets of color, ceramic illustrations and deliberate rounded type around clear native tools. Non-minimalist does not mean noisy reading surfaces.
- Do keep a stable companion silhouette, opaque text planes and predictable control placement in both themes.
- Do label disconnected providers honestly. Illustrations and static examples never establish live capability, billing entitlement or release readiness.
- Do use native menus, sheets, selection, focus and accessibility APIs. Do not implement the native app as a web shell because this reference board is HTML.
- Do give every color-based state an icon and text equivalent; expose exact scope before approval.
- Do keep stop, deny and recovery affordances visible during errors, sleep recovery and compact layouts.
- Do replace travel, parallax and squash with immediate state changes or brief crossfades for Reduce Motion. No ambient idle animation.
- Do not add generic indigo gradients, confetti, invented success rates, fake testimonials, copied avatars or a repeated three-feature-tile landing composition.
- Do not bundle Apple fonts, put secrets in mockups, invent plan prices, claim the selected domain is registered, or imply this reference board is application implementation.
