<p align="center">
  <img src=".github/assets/readme-cover.svg" width="1200" alt="HeyPebbi — a little presence. A lot off your plate. A sea-glass ceramic companion on a warm, colorful desk.">
</p>

<p align="center">
  <strong>a softer side of software.</strong><br>
  A voice-first Mac companion with a little character and a lot to help with.
</p>

<p align="center">
  <a href="docs/design/BRAND.md">the world</a> &nbsp; · &nbsp;
  <a href="docs/product/APP-FLOWS.md">the experience</a> &nbsp; · &nbsp;
  <a href="docs/engineering/ARCHITECTURE.md">the blueprint</a> &nbsp; · &nbsp;
  <a href="docs/agents/BUILD-PROMPT.md">build pebbi ↗</a>
</p>

<br>

## Your ideas don't arrive in neat little boxes.

They arrive mid-tab, mid-thought, halfway through something else.

**Pebbi is being designed to meet you there.** Talk an idea through. Share a window. Turn a ramble into writing. Hand over a task—and keep your place.

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>01 &nbsp; say it.</h3>
      Natural conversation.<br>
      Dictation where you work.<br>
      Less translating thoughts into clicks.
    </td>
    <td width="33%" valign="top">
      <h3>02 &nbsp; share the view.</h3>
      Screen context, when you choose.<br>
      Guidance that points to the thing.<br>
      A little less “which button?”
    </td>
    <td width="33%" valign="top">
      <h3>03 &nbsp; make room.</h3>
      Persistent Pebbis, files and memory.<br>
      Tasks with visible progress.<br>
      Important actions stay your call.
    </td>
  </tr>
</table>

<br>

## Sea-glass. Clay. A bit of mischief.

Warm paper. Rounded type. Glazed ceramic. A companion with an actual silhouette—not another glowing orb.

Colorful without shouting. Tactile without getting in the way. **Native to the Mac, not a website wearing a window.**

<p align="center">
  <img src="docs/design/assets/mascot-expression-sheet.svg" width="860" alt="Original Pebbi expression studies for idle, listening, working and failed states.">
</p>

<p align="center">
  <sub>same little pebble. different things on its mind.</sub><br><br>
  <a href="docs/design/BRAND.md">Brand story</a> &nbsp; / &nbsp;
  <a href="DESIGN.md">Colors &amp; type</a> &nbsp; / &nbsp;
  <a href="docs/design/brand-board.html">Visual studies</a>
</p>

<br>

## Open the sketchbook.

| Follow your curiosity | Find your way |
| :--- | :--- |
| **What is Pebbi?** | [The product](docs/product/PRODUCT.md) · [Every app flow](docs/product/APP-FLOWS.md) |
| **What does it feel like?** | [The screens](docs/design/SCREENS.md) · [Motion](docs/design/MOTION.md) · [Accessibility](docs/design/ACCESSIBILITY.md) |
| **What makes it work?** | [Native architecture](docs/engineering/ARCHITECTURE.md) · [Tech stack](docs/engineering/TECH-STACK.md) · [AI roles](docs/engineering/AI-MODELS.md) |
| **What keeps it trustworthy?** | [Security](docs/engineering/SECURITY.md) · [Privacy](docs/operations/PRIVACY-AND-DATA.md) · [Acceptance](docs/quality/ACCEPTANCE.md) |
| **Where is everything?** | [Complete documentation map](docs/README.md) · [Canonical contract](docs/CONTRACT.md) |

<br>

> [!NOTE]
> **Still in the sketchbook.** This private repository holds the complete build specification and original brand references—not a released app. Azure audio setup and other live-service inputs remain [explicitly gated](docs/operations/EXTERNAL-INPUTS.md).

<details>
<summary><strong>For the builders — one prompt, the whole picture ↗</strong></summary>

### Give this to a coding agent

Start at the repository root:

> Implement the complete Pebbi application described in `docs/agents/BUILD-PROMPT.md`. Follow `AGENTS.md` and all normative documents indexed by `docs/README.md`. Use the repository's specialist skills and agents where supported. Complete every PB requirement with real code, error handling, tests and evidence. Continue all unblocked work without routine clarification; preserve explicit security and external-input gates. Do not stop at scaffolding, substitute mock success, or claim a production release while live gates are blocked.

Claude Code: `/build-pebbi`. Reading the prompt alone does not authorize implementation. Credentials, permissions, signing and paid resources remain human-controlled prerequisites.

**Intended stack:** Swift 6 · SwiftUI / AppKit · ScreenCaptureKit · AVAudioEngine · SQLite / GRDB · TypeScript / Fastify · Azure · PostgreSQL.

**Locked AI roles:** `gpt-realtime-2.1` for voice · `gpt-live-transcribe` for dictation · `gpt-6-astra` for reasoning. [Actual access status](docs/engineering/AI-MODELS.md), not catalog assumptions.

### Verify this documentation pack

```sh
python3 scripts/validate_docs.py
npx -y @google/design.md lint DESIGN.md
uvx --from 'openapi-spec-validator>=0.7,<0.8' python scripts/validate_contracts.py
```

These validate the specification, not a working application.

### Agent entry points

[AGENTS.md](AGENTS.md) · [AGENT.md](AGENT.md) · [CLAUDE.md](CLAUDE.md) · [Specialist agents & skills](.claude/README.md)

</details>

<details>
<summary><strong>The fine print — sources, rights &amp; reality</strong></summary>

Original Pebbi brand artwork. Public product references are mapped in [HeyClicky coverage](docs/reference/HEYCLICKY-COVERAGE.md), with [sources and boundaries](docs/reference/SOURCES.md). No proprietary HeyClicky code or branding is included. Any future MIT-source reuse must retain its notices.

[Third-party notices](THIRD-PARTY-NOTICES.md) · [License](LICENSE). `heypebbi.com` is the selected domain, not a claim of registration or trademark clearance.

</details>

<br>

<p align="center">
  <img src="docs/design/assets/logo-mark.svg" width="48" alt="Pebbi"><br>
  <strong>small presence. big possibility.</strong><br>
  <sub>the heypebbi project</sub>
</p>
