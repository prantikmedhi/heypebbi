# Documentation validation record

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

This record covers the specification and original brand references only. It is not application QA, native runtime verification, Azure readiness, signing or production deployment evidence.

## Checks exercised

- `python3 scripts/validate_docs.py --self-test`: checker logic self-tests passed.
- `python3 scripts/validate_docs.py`: required files, links/anchors, PB coverage, JSON references, SVG structure, agent/skill identities, canonical state enums and endpoint inventories passed at document integration.
- `npx -y @google/design.md lint DESIGN.md`: zero errors and zero warnings; tokens comprise 19 colors, 9 typography scales, 5 rounding levels, 7 spacing tokens and 35 component entries.
- OpenAPI 3.1 validation through `openapi-spec-validator` and JSON Schema 2020-12 checks through `jsonschema`: passed for the service API, component schemas and local tool envelope.
- `uvx --from 'openapi-spec-validator>=0.7,<0.8' python scripts/validate_contracts.py`: 20 synthetic static regression checks passed for device credential declarations, authored artifacts, immutable script identity, role/budget readiness and UTF-8 message bounds. These do not substitute for the corresponding runtime negative tests.
- YAML parsing: project agent and skill frontmatter parsed. Four specialist agents inherit the selected development model and normal permissions; five repository skills include the explicit build entry point.
- All PB-001 through PB-040 are represented in requirements, flows, screen treatments, acceptance and the machine-readable coverage ledger.
- Brand board rendered in headless installed Chrome through Playwright. Desktop and narrow layouts were inspected; no horizontal document overflow or JavaScript page errors were observed in the tested viewports. The board has no application JavaScript or live product behavior.
- Visual inspection confirmed the heypebbi wordmark, recognizable mascot construction and legible section hierarchy. Small reference labels were enlarged and the failure pose softened after review.

## What these checks cannot establish

Static schemas do not prove secure implementation, idempotent side effects or working native controls. The HTML board is not a SwiftUI app. No current app source, native build, backend service, browser extension implementation, identity tenant, payment configuration or notarized release exists in this docs-only commit. No new Azure resource was provisioned. The known audio-deployment blockers remain in [AI-MODELS.md](../engineering/AI-MODELS.md) and [EXTERNAL-INPUTS.md](../operations/EXTERNAL-INPUTS.md).

GitHub's documentation workflow repeats structural, schema and design checks on pushes and pull requests. Its actual run status—not this record—is the authority for the latest remote commit. Later code changes must satisfy [ACCEPTANCE.md](ACCEPTANCE.md) and the live/native/hardware gates, not merely preserve a green docs check.
