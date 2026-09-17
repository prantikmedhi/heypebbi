# Pebbi documentation map

## Current scope — read these first

**Docs and repository updates only. Development is on hold.** The next authorized feature is a native first-run Custom Azure setup section with user-owned credentials and per-role deployment choices. There is no Pebbi backend, Supabase, Render, Vercel, managed customer account or billing dependency.

| Current authority | Purpose |
| --- | --- |
| [CONTRACT.md](CONTRACT.md) — current section | Local BYOK decision and precedence over historical designs |
| [LOCAL-AZURE-ONBOARDING.md](product/LOCAL-AZURE-ONBOARDING.md) | Complete first-launch flow, fields, Keychain persistence, endpoint safety, settings/reset and BYOK-001 through BYOK-012 acceptance |
| [AGENTS.md](../AGENTS.md) | Documentation hold and bounded future implementation conduct |
| [BUILD-PROMPT.md](agents/BUILD-PROMPT.md) | One-feature implementation prompt; execute only after explicit authorization |
| [ORCHESTRATION.md](agents/ORCHESTRATION.md) | Scoped native/UI/Azure-client/reviewer roles |
| [Claude support](../.claude/README.md) | Current project-local entry points; no global configuration changes |
| [MIT license](../LICENSE) | Open-source terms for original software/documentation |

**The app and settings are local; Azure inference is remote.** Saving a configuration is not a live model-access test. There is no application implementation or deployment in this repository yet.

## Current visual references

The original expressive Pebbi identity remains current: [DESIGN.md](../DESIGN.md), [brand direction](design/BRAND.md), [components](design/COMPONENTS.md), [motion](design/MOTION.md), [accessibility](design/ACCESSIBILITY.md), [asset provenance](design/ASSETS.md), and [brand board](design/brand-board.html).

[Screen studies](design/SCREENS.md) and the brand board include earlier full-product compositions. Reuse their visual language, not their old account/billing/backend assumptions or feature scope. The new onboarding specification owns its layout, fields, status and acceptance.

Original art: [logo](design/assets/logo-mark.svg), [monochrome mark](design/assets/logo-mark-mono.svg), [wordmark](design/assets/wordmark.svg), [app icon reference](design/assets/app-icon-reference.svg), [ceramic mascot](design/assets/mascot-ceramic.svg), [expressions](design/assets/mascot-expression-sheet.svg), [pocket world](design/assets/pocket-world.svg).

## Historical design library — not a build queue

These are preserved to avoid losing prior work and source evidence. Their full PB roster, hosted identity, backend routes, fixed models, subscriptions and release mandates are **superseded**, not prerequisites for the current feature. Each product/engineering/operations document is marked accordingly. Machine-readable history has an explicit scope annotation.

| Historical collection | Documents |
| --- | --- |
| Product exploration | [Product](product/PRODUCT.md), [PB requirements](product/REQUIREMENTS.md), [old flows](product/APP-FLOWS.md), [information architecture](product/INFORMATION-ARCHITECTURE.md), [copy](product/COPY.md) |
| Native/full-agent concepts | [Architecture](engineering/ARCHITECTURE.md), [macOS](engineering/NATIVE-MACOS.md), [runtime](engineering/AGENT-RUNTIME.md), [tools](engineering/TOOLS.md), [data](engineering/DATA-MODEL.md), [browser](engineering/BROWSER-AUTOMATION.md) |
| Managed-service design | [Stack](engineering/TECH-STACK.md), [API prose](engineering/API.md), [OpenAPI](engineering/openapi.json), [tool envelope](engineering/schemas/tool-envelope.schema.json), [security](engineering/SECURITY.md), [connections](engineering/CONNECTIONS.md), [billing](engineering/BILLING.md) |
| Prior decisions/evidence | [Model audit](engineering/AI-MODELS.md), [decisions](engineering/DECISIONS.md), [review resolutions](engineering/REVIEW-RESOLUTIONS.md) |
| Historical complete-product gates | [Acceptance](quality/ACCEPTANCE.md), [testing](quality/TESTING.md), [PB coverage](quality/coverage.json), [old build ledger](agents/build-state.template.json) |
| Former operations plan | [External inputs](operations/EXTERNAL-INPUTS.md), [release](operations/RELEASE.md), [operations](operations/OPERATIONS.md), [privacy](operations/PRIVACY-AND-DATA.md), [support](operations/SUPPORT.md) |

The older resource-specific Azure audit does not certify any user's deployment and does not lock their choices. The hosted OpenAPI is not a request to generate or deploy a server.

## Documentation integrity and sources

- [Manifest](manifest.json) identifies the current feature/acceptance IDs and labels its legacy roster separately.
- [Documentation checker](../scripts/validate_docs.py) checks links, files and retained historical-contract consistency. Its PB/REST counts are historical, not completion of current BYOK acceptance.
- [Contract fixtures](../scripts/validate_contracts.py) still validate old managed-service shapes, not app functionality or current onboarding.
- [Earlier validation record](quality/DOCUMENTATION-VALIDATION.md) records previous specification checks, not new implementation evidence.
- [Reference comparison](reference/HEYCLICKY-COVERAGE.md), [source index](reference/SOURCES.md), and [third-party notices](../THIRD-PARTY-NOTICES.md) preserve attribution and evidence boundaries, not current scope expansion.

No Swift app, backend, infrastructure deployment, paid resource, inference call or signed release has been created by the current documentation revision.
