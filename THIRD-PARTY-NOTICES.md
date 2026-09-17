# Third-party notices and asset provenance

The current repository contains original project documentation, original Pebbi vector reference assets and documentation validation tooling, offered under the [MIT license](LICENSE). No application implementation is included yet. It does not bundle the Clicky app, Apple fonts, licensed commercial typefaces, Azure/OpenAI models, or application dependencies.

## Clicky reference

The public [farzaa/clicky repository](https://github.com/farzaa/clicky) identifies its code as MIT licensed, copyright 2026 Farza. The latest commercial HeyClicky implementation is separate and private. If implementation reuses any MIT source or substantial portion, preserve its copyright and MIT permission notice in the redistributed source/app notices and inventory the reused files. A link or product feature comparison does not require adopting its brand. No permission to copy trademarks or proprietary later features is inferred.

## Platform and design tooling

- Apple platform frameworks and system fonts are used under the applicable Apple agreements; do not extract or redistribute SF fonts from a developer machine.
- [Google DESIGN.md](https://github.com/google-labs-code/design.md) is the referenced design-token specification. Its validation CLI is fetched as a development tool and is not vendored here.
- Claude Code's agent/skill file formats are referenced through official documentation; the project instructions themselves are newly authored for Pebbi, not copies of global skill libraries.
- Runtime dependencies named in the stack are proposed, not installed or redistributed by this docs commit. Implementation must produce an SBOM and license inventory from actual locked versions.

## Original Pebbi art

See [asset provenance](docs/design/ASSETS.md). SVGs and the brand board are design references, not legally cleared trademarks, notarized app icons or evidence of a working app. Preserve editable originals when exporting runtime assets.
