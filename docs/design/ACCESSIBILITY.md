# Pebbi — accessibility and adaptive behavior

[DESIGN.md](../../DESIGN.md) owns exact palette/type/spacing. [Components](COMPONENTS.md) owns state presentation; [Screens](SCREENS.md) binds PB coverage. WCAG ratios are useful measurable baselines, while the shipped macOS app also needs native accessibility testing. Static HTML or token lint is not proof of VoiceOver compliance.

## Perceivable without color, sound, illustration or animation

Ordinary text meets 4.5:1 minimum; qualifying large text 3:1; essential control outlines, focus and state glyphs 3:1 against adjacent colors. Use named root tokens and approved pairings. Decorative shadows are not a boundary. Pastel plate text is plum ink, never white. Muted text uses a tested token without blanket opacity. Do not place text on glaze gradients or photographs. Fields and buttons maintain opaque backs over material chrome.

Measured token contrast and exact pair definitions are recorded in [verification.json](verification.json). Token lint only checks declared component text/background pairs; separate geometry checks cover outlines/focus. Increase Contrast uses opaque planes, stronger native borders and no dependence on shadows. Reduce Transparency removes blur without changing layout. OS accent/focus colors can supersede brand styling to respect accessibility settings.

Canonical statuses use icon + readable label; a waveform is supplemental. Failed vs cancelled vs interrupted, and dictation review vs insertion complete, must remain distinguishable in grayscale. Every meaningful graphic has a concise text equivalent. Decorative mascots are hidden when adjacent status duplicates the information. No success state is conveyed by a smile alone.

## Keyboard and focus

- Every operation has a keyboard-accessible path from Home or the menu bar, including expanding the perch, stopping capture, cancelling a task and reviewing an approval. Global shortcut choices must be configurable and conflicts explained; do not claim a universal reserved key combination.
- Tab/Shift-Tab follow visible logical order. Native list arrow-key navigation and selection conventions remain intact. Full Keyboard Access does not expose decorative objects as controls. A visible skip/jump-to-content affordance is appropriate on public web pages.
- Focus ring: two-point outer ring, two-point solid surface-colored gap, no clipping by parent rounded masks. Light uses primary, dark uses butter; on accent objects the neutral gap preserves separation. Focus is not selection.
- Modal sheets hold keyboard focus in the sheet, announce title/context, and return focus to the invoking control. Escape cancels/dismisses safely; never approves. Destructive sheets start on the description or safe action, not a preselected destructive default. App-wide stop shortcuts remain accessible where the OS allows.
- Background status changes do not focus a window, move the insertion caret, reorder a focused row or switch Spaces. Explicit focus-taking activation is distinguished from a glance/status shortcut.
- After an async row removal, move focus to the next logical row or list heading and announce what happened. After a failed action keep focus near the error and preserve input.
- Dictation remembers its original target but revalidates the currently authorized field immediately before insertion. Focus loss returns to review; never send keystrokes to an unverified new target.

## VoiceOver and assistive technology semantics

Use native roles, labels, values, help and actions. Suggested readable names: “Pebbi, research assistant”; “Cancel task: Review this document”; “Stop speaking”; “Stop sharing: selected window”; “Review approval: send message”; “Connection: disconnected.” The underlying task state remains canonical data; human-readable names may be natural language. Icon-only actions have names, not inferred symbol descriptions. Secrets and hidden document content are never included in accessibility hints.

Announce state transitions once and group related updates. Use an appropriate interruption priority only for user-critical capture/takeover or immediate safety failures; ordinary progress should not interrupt reading. Do not announce every token, audio frame or percentage tick. Provide a transcript and task event list that can be read at the user's own pace. Record unread completion if Focus/call rules suppress notifications. Respect VoiceOver's reading position instead of forced autoscroll.

For source citations, accessible text names the source and what it supports. Tables have associated headers. File preview fallback names type, access state and alternative “Open in default app”; whole-document processing completeness is visible as text, not inferred from a thumbnail. A visible memory edit/forget control must also expose the same action to AX.

## Text scaling, localization and hit targets

Nominal body is 15 points; captions 12; no essential warning lives only in a caption. Provide 100–200% application text scaling and adapt to OS text/accessibility settings. Use intrinsic sizing and platform font metrics; test actual 200%, not browser zoom alone. Expand controls and rows before truncating labels. Body prose can wrap; task titles, permission scopes and destructive consequences cannot be ellipsized. Middle-truncated paths expose full selectable content and full AX value.

Use at least 28 × 28-point compact targets, 44 × 44 for primary, microphone, stop and approval actions. Hit padding must not overlap another actionable target. Keep at least 8 points between distinct high-consequence controls. A small visual glyph may have a larger invisible hit area. Drag-only operations have a menu/keyboard alternative. Hover-only controls, timing-dependent gestures and double-click-only primary actions are prohibited.

Reserve enough width for longer localization; use leading/trailing alignment and mirror spatial navigation when appropriate without mirroring text or asymmetric brand art arbitrarily. No hard-coded English string measurement for layout. Do not globally letterspace non-Latin scripts. Number/currency/date display follows locale; stored canonical values are unchanged.

## Window, notch and multi-display safety

Home reference size 1180 × 780 points; responsive thresholds and exact spacing live in root DESIGN.md. Start with three regions only when they fit. Below 1080 collapse the inspector; below 840 collapse the sidebar. At 640 × 480 use a single scrollable content pane with accessible navigation. If available screen bounds are smaller, fit inside the visible frame and keep close/back/stop reachable. At 200% type use content-fit thresholds even on a nominally wide display.

A top-edge perch is optional. It must work on external and notchless displays below the menu bar with no fake notch. Never place a control beneath a camera housing or overwrite menu-bar items. If insufficient top-edge room exists, use the menu-bar entry and ordinary Home window. Convert coordinates per display; respect Retina/non-Retina scaling, display arrangement, visibleFrame, safe area and Spaces. When a display disappears, re-anchor on an available display without taking focus. A walkthrough target offscreen or in another Space is reported, not guessed.

Avoid capture overlays that intercept pointer events outside the intentional control. Drawn annotations have a clear dismiss path and a text-only equivalent. If the user cannot use visual pointing, expose the same step as accessible instructions and target name in Home.

## Native testing matrix required before release

Test keyboard-only with Full Keyboard Access; VoiceOver with speech and braille-compatible semantics where available; reduced motion; reduced transparency; increased contrast; both appearance modes; 100%, 150%, 200% text; Retina and non-Retina; notched and notchless; external display removal; narrow visible frame; long/localized strings; mouse/trackpad; mic denied, revoked and changed; sleep/wake; and offline/provider-unavailable paths.

Critical task: start from menu bar with no notch; read task state; deny an approval; interrupt speech without cancelling work; review dictation; change focus; confirm no unintended insertion; stop capture; inspect a failed task and retained outputs. Test all without seeing the mascot, hearing a sound or relying on motion. Report actual results with environment and assistive-tech version; never mark these passed from this design specification alone.

## Documentation artifact accessibility

The brand board is English semantic HTML with labeled figures, meaningful headings, real document anchors, keyboard focus, no custom widget scripting and no app-like live controls. Pictured actions are noninteractive text and explicitly captioned as design references. Both light/dark product compositions are visible together; no theme-toggle behavior is implied. It has no external fonts, images or scripts and no animation. At narrow widths the layout stacks; the pictured product is a schematic and does not establish an iOS/mobile app. Inline SVGs have unique title/description IDs; decorative reuse is hidden from the accessibility tree.
