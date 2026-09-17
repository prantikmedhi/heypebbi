# HeyPebbi — brand and material direction

**Status:** original design reference; no app implementation or trademark clearance is implied. Exact tokens: [DESIGN.md](../../DESIGN.md). Product contract: [CONTRACT](../CONTRACT.md).

## Brand fact sheet

- Project/company-facing name: **HeyPebbi**. Native app: **Pebbi**. Default companion: **Pebbi**. Persistent assistants: **Pebbis**. Preserve the unusual double **b** and final **i**.
- Domain selection: `heypebbi.com`. It is not proof of availability, ownership or legal clearance.
- Canonical navigation: **Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections, Settings**. A conversation holds dialogue; a task is a separately tracked execution attempt.
- Pebbi is explicitly AI, not a human friend, therapist or employee. Warmth must not imply consciousness, infallibility or invisible access to the user's desktop.

## One direction: pocket-world tactility

Reading this as a native companion for people who speak, write, research and delegate on a Mac, with a cheerful creative-desk language. A small ceramic being sits among tangible objects, each object carrying a useful role. Sea-glass is the companion and task tile; clay is the voice object; butter is the permission slip; lilac is a memory bookmark. The scene feels arranged by a person, not assembled from identical SaaS cards.

**Expression dial:** high in identity illustration and onboarding; medium in Home and Pebbis; low in tool logs, approvals, billing and destructive decisions. **Density dial:** generous on first contact, moderate on Home, efficient in Conversations and Files. **Motion dial:** responsive and brief; no ambient loops. Low motion is not low personality: pose, material, composition and type remain expressive while static.

This brief is expressly non-minimalist. Keep the rich palette, visible object layering, personable mascot, sculptural asymmetry and rounded headings. Do not strip the brand down to a monochrome wordmark with one accent. Equally, do not use expression as an excuse for poor hierarchy, tiny copy, decorative metrics or an all-over texture behind text.

## The ownable shape

The silhouette has a raised left shoulder, sloping right crown, low broad base and a small side indentation. The face sits below the visual center so the crown reads as a ceramic object rather than an emoji circle. Two inset plum eyes, an asymmetrical upturn and a clay thumbprint make the mascot welcoming without a copied animal species. The glaze ridge sits upper-left; illumination always comes from there. No limbs, antennae, floating AI sparks, generic starburst or third-party character references.

The logo uses flat geometry. The hero mascot adds a glazed crown, underside ledge, contact shadow and cheek impression. The expression sheet changes eyes and mouth, not the underlying identity. Identity and accessibility remain recognizable without color.

## Logo system

[Logo mark](assets/logo-mark.svg): flat mark, primary companion silhouette, self-contained SVG. [Wordmark](assets/wordmark.svg): custom original lowercase **heypebbi** lettering drawn from round-ended paths. It is a brand drawing, not a typeface; use normal case HeyPebbi in prose. [App icon reference](assets/app-icon-reference.svg): a cream continuous-corner field containing the ceramic Pebbi. This is a vector art reference, not a signed app icon catalog or finished macOS packaging.

Clear space is one eye-to-eye interval around the mark; around the wordmark, one lowercase letter-stem height above/below and one bowl width at the sides. Flat mark minimum: 24 points for the full face; below that use [the monochrome small mark](assets/logo-mark-mono.svg), with pixel-level optical review at 16, 18, 24 and 32. Wordmark minimum 140 pixels wide on the web or 35 mm in print. Never stretch, add an outline to the wordmark, rotate the logo, replace its letters with system text, or place it on a busy photograph.

Use the colored mark on cream or a solid pale accent. On a dark background give the colored mark its own solid cream/sea-glass field or use the cream monochrome variant produced from the monochrome path. Monochrome template artwork follows native menu-bar rendering; it is not a permanently colored status icon. Assets do not contain any downloaded logo, stock image, external SVG use, linked font or network reference.

## Composition grammar

1. **Desk:** broad warm cream or dark plum ground, with one expressive still-life anchor. The board's display title is offset, not centered above equal tiles.
2. **Tray:** a bounded productive plane; content has a reading order, leading edge and visible action.
3. **Object:** a task slip, memory tab or voice capsule that carries actual semantic information. Do not scatter meaningless pills.
4. **Pebbi:** one primary actor per scene. Multiple Pebbis can appear in the team shelf, each with name and job. They do not multiply as decorative avatars in unrelated sections.
5. **Margin notes:** small editorial explanations outside pictured UI clarify that the composition is a design reference. Avoid fake numbers, usage charts and disconnected badges.

Home is an Operate surface. Its expressive shelf occupies the upper portion, then yields to task rows and recent conversations. Conversations is a Command / Inspect surface with a continuous transcript and contextual task rail. Connections and Settings are Configure surfaces. Suggestions is Explore with clearly labeled read-only proposals. Billing is Compare with aligned, source-fed plan details—not a promotional upsell carousel.

## Voice and microcopy

Warm, concise, truthful. Say what happened, what scope was used, and what can happen next. Avoid baby talk, guilt, exaggerated praise and pressure to keep interacting. The assistant may say “I can help you review this” but not “I can see everything.” Explain that screen access is explicit and scoped.

| Context | Preferred example | Avoid |
|---|---|---|
| Ready, with working capability | “What shall we work on?” | “Your superpowered AI workforce is ready” |
| Voice not configured | “Voice is unavailable. You can type instead.” | Animated listening with no live provider |
| Scoped screen capture | “Share this window with Pebbi?” | “Pebbi sees your screen” |
| Approval | “Send this message to Maya?” with recipient and full body | “Let Pebbi work its magic” |
| Real completion | “Saved the file in your selected workspace.” | “Done!” before verification |
| Interrupted work | “This task was interrupted. Review its last confirmed action.” | Automatically treating an interruption as a failure or success |
| Routine blocked | “This routine needs a connection.” | “You forgot to reconnect” |

Examples are design copy, not evidence that any action occurred. Do not invent recipients, financial amounts or live activity for production empty states.

## Light and dark material

Light resembles glazed sea-glass on a cream studio desk. Dark resembles the same objects on a plum felt tray; warm highlights remain, but page-sized glow and neon are prohibited. Accent chips keep opaque pastel fills and plum text in both themes. Long content uses neutral planes. Borders stay visible when shadows vanish or Increase Contrast is enabled. Review both themes side by side; dark is a designed composition, not CSS inversion.

## Type and provenance

Use native system rounded for display and interface labels, normal system text for paragraphs and native monospace for code. No Apple font files are bundled. Web references use `ui-rounded, system-ui, sans-serif`; non-Apple systems intentionally fall back. The outlined wordmark needs no fonts. No external font or license download is necessary for these deliverables. See [Assets](ASSETS.md) for source provenance and [Accessibility](ACCESSIBILITY.md) for scaling.

## Guardrails and approval questions

Before shipping any new illustration ask: does its silhouette still belong to Pebbi; does it explain a product role; does text remain legible; does its use imply a capability or outcome that has not occurred? Before shipping any surface ask: can it be operated by keyboard, with no mascot, no color, no sound and no animation?

The design reference does not approve plan prices, entitlements, model substitutions, trademark clearance or current release availability. Asset originality here means newly authored vectors without copied source material; legal trademark review is a separate operator task.
