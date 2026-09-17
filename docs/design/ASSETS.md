# Pebbi — original reference assets and provenance

**All artwork below was newly authored for HeyPebbi in this documentation task using original SVG path geometry.** No third-party logo, avatar, photograph, paid asset, external image-generation call or downloaded font was used. This is a source/provenance statement, not trademark clearance. [Brand](BRAND.md) explains usage; [DESIGN.md](../../DESIGN.md) owns exact token values.

## Asset manifest

| File | Native vector canvas | Source / intended use | Delivery limits |
|---|---|---|---|
| [logo-mark.svg](assets/logo-mark.svg) | 320 × 280 | Author-generated original flat sea-glass silhouette, plum face, clay thumbprint; avatars/identity | Full face at 24 pt and above; review optical rendering before production |
| [logo-mark-mono.svg](assets/logo-mark-mono.svg) | 320 × 280 | Author-generated silhouette with transparent facial cutouts; single-color template | `currentColor` fill; platform template tint for menu bar; inspect at 16/18/24/32 pt |
| [wordmark.svg](assets/wordmark.svg) | 872 × 260 | Author-generated custom rounded path lettering spelling lowercase heypebbi | Not a font; never retype to approximate it; preserve viewBox and aspect ratio |
| [app-icon-reference.svg](assets/app-icon-reference.svg) | 512 × 512 | Author-generated cream icon field plus original ceramic mascot | Reference artwork only; no ICNS, asset catalog, signed app or App Store approval implied |
| [mascot-ceramic.svg](assets/mascot-ceramic.svg) | 320 × 280 | Author-generated glazed companion with token-derived highlights and contact shadow | Illustration for Home/onboarding/identity; do not use as evidence of live activity |
| [mascot-expression-sheet.svg](assets/mascot-expression-sheet.svg) | 1160 × 930 | Author-generated 12-pose reference atlas with canonical example state captions | Static poses; identical state strings across axes remain distinct in contracts |
| [pocket-world.svg](assets/pocket-world.svg) | 720 × 560 | Author-generated original still life: Pebbi, lilac memory tab, clay note/voice dish, butter ground | Identity illustration only, not a screenshot or working product visualization |

Every SVG is self-contained XML with title, description and viewBox. No scripts, embedded rasters, remote URLs, linked CSS/fonts or externally referenced SVG content. Illustrative glaze uses gradients of existing root colors and opacity; native UI text does not inherit those gradients. The monochrome mask intentionally uses white/black as alpha-mask mechanics, not new brand palette colors.

## Static board

[brand-board.html](brand-board.html) embeds all displayed vector artwork and CSS. It opens locally without a server or network; document links resolve within this repository. It has no JavaScript, app state, account logic, network request or fake click handler. Internal navigation and document links are real links; pictured buttons/composers are noninteractive specimens. Light Home, dark Conversations, approval and notchless perch studies are all labeled design references. All task/conversation content is explicitly illustrative, not fabricated live evidence. The example email uses a reserved example domain.

The original board composition is a wide editorial identity spread: asymmetrical hero still life, material-color row, paired light/dark native studies, a larger approval/perch scene, expression strip and type specification. It is not a cloned third-party landing page, app shell or equal three-feature-card grid. At narrow widths it reflows for documentation reading; this does not specify an iPhone app.

## Fonts and rights

Native UI requests the installed system font through platform APIs, with rounded design where supported. Documentation HTML uses `ui-rounded, system-ui, sans-serif` and `ui-monospace, monospace`. No Apple font files are included. No external font is fetched, so there is no external OFL font dependency or missing license file. SVG wordmark is original drawn path lettering and renders without a font. Expression captions use installed system fallback; the shapes themselves are font-independent.

These author-generated assets are supplied as project reference source files for the repository owner. No third-party art license is asserted or required by their construction. Repository licensing and trademark clearance remain the owner's decisions; do not infer that the selected name/domain is legally cleared merely because new art was drawn. Native system symbols, if later used in the app, are accessed through platform APIs under applicable platform terms and are not included in this asset set.

## Production work not implied by this reference delivery

- Produce and optically inspect every macOS icon size; supply the actual AppIcon asset catalog/ICNS only during implementation/packaging.
- Rebuild illustration rendering as appropriate for SwiftUI/AppKit image resources, preserving accessibility descriptions or hiding redundant decoration.
- Verify transparent cutouts and template tint on both menu-bar appearances, high contrast and notched/notchless hardware.
- Native control symbols need OS-availability fallback; do not redistribute downloaded SF Symbols or Apple fonts.
- Real screens need native screenshot/accessibility/performance tests; the HTML board and SVG parse checks are documentation evidence only.

## Reproducibility and validation

All files are editable plain text. Palette literal snapshots in assets and board derive from root DESIGN.md, not an independent color authority. Regenerate/review derived illustrations if tokens change. [verification.json](verification.json) records token lint, coverage, link, SVG and browser checks, with explicit limits. No generated asset or test figure should be promoted into a fake production result.
