# Sources, dates and evidence boundaries

Reference review date: 2026-09-17. A link is evidence only for what its retrieved material says, not proof of tenant access or a tested private product. A later build must recheck version-sensitive interfaces.

| Source | What it supports | What it does not establish |
| --- | --- | --- |
| [Clicky public repository](https://github.com/farzaa/clicky) and [license](https://github.com/farzaa/clicky/blob/main/LICENSE) | Older native menu-bar app, push-to-talk, screenshot explanation and pointing; MIT source reuse conditions | Current private HeyClicky source or exact model routing |
| [HeyClicky homepage](https://www.heyclicky.com/) | Public positioning, talk/dictation/agents, screen permission statements | Measured reliability, verified privacy behavior or Pebbi's commercial terms |
| [HeyClicky changelog](https://www.heyclicky.com/changelog) | Advertised v1.0.49/v1.0.50 persistent assistants, Home, files, memory, MCP, suggestions, routines and control permissions | Firsthand app testing or permission to reproduce its distinctive visual assets |
| [HeyClicky privacy policy](https://www.heyclicky.com/privacy-policy) | Provider/data-processing disclosures as published | A suitable policy for Pebbi without implementation and legal review |
| [Azure model catalog](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure?pivots=azure-openai) | Published model families and constraints | Callable deployments in a user's subscription |
| [Azure Realtime WebSockets](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/realtime-audio-websockets) | Voice/transcription session formats and transport patterns | A promise that a selected model works on a particular resource |
| [Azure Responses](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses) | Responses request, streaming and tool patterns | End-to-end native agent operation |
| [Entra OIDC](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc), [ID-token claims](https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference), [optional claims](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) | Standard signed nonce verification, interactive sign-in and `auth_time` claim semantics | A preconfigured Pebbi tenant, custom enrollment-only assertion issuer or successful live enrollment |
| [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) | Native interaction and accessibility foundations | A mandate for minimalist styling |
| [ScreenCaptureKit](https://developer.apple.com/documentation/screencapturekit) | Native screen-capture framework | Permission bypass or universal capture access |
| [Apple notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) | Distribution requirements | A signing identity or successful notarization |
| [Sparkle documentation](https://sparkle-project.org/documentation/) | Signed macOS update framework | A deployed feed, trusted signing key or working rollback |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills), [memory](https://code.claude.com/docs/en/memory) | Project agent/skill schemas and CLAUDE.md imports | Support for non-Claude models through third-party gateways or automatic bypass of approvals |
| [Google DESIGN.md](https://github.com/google-labs-code/design.md) | Design token document format and linter | Visual quality or native UI performance by itself |

## Tested facts available to this specification

The owner authorized an endpoint audit on 2026-09-17. Astra returned a sentinel through direct Azure and an existing private LiteLLM route. Real streaming audio checks failed for the locked audio deployment names: realtime operation unsupported; dictation deployment not found after a session accepted configuration. See [AI model status](../engineering/AI-MODELS.md). The raw audit is intentionally not copied into this repository because it contains local infrastructure identifiers.

## Recommendations rather than external facts

Pebbi's brand, feature contracts, stack choices, schemas, operational budgets, plan names and acceptance criteria are project design decisions. They are not represented as vendor benchmarks, legal advice, approved pricing or measurements of an implemented app. The brand and domain were selected by the owner; registration and trademark clearance are still separate processes.
