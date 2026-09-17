# Pebbi — current agent contract

## Stop at documentation unless implementation is explicitly requested

The owner most recently instructed: **update the documentation and repository only; do not work on the application now.** This repository has no implemented native app. Do not create app code, backend code, services, deployments, cloud resources, CI app builds or signing material during this documentation task.

## Current product decision

Read [CONTRACT.md](docs/CONTRACT.md) and [Local Azure onboarding](docs/product/LOCAL-AZURE-ONBOARDING.md). They supersede older hosted-service requirements. Pebbi is an open-source native macOS app with user-owned Azure API keys, endpoints and per-role model/deployment choices. No Pebbi backend, Supabase, Render, Vercel, managed Pebbi login, Stripe or hosted usage ledger is required or authorized.

App UI, configuration and future local execution stay on the user's Mac. **Azure inference is remote** and uses the user's Azure account; never call this offline AI or claim inputs never leave the device. The previous three fixed models are not required defaults for a BYOK user.

## Scope of a later authorized implementation

Implement only the onboarding configuration feature specified by BYOK-001 through BYOK-012. If no native app exists, add only the smallest launchable SwiftUI/AppKit shell needed to exercise it. Do not automatically implement the full historical PB-001 through PB-040 product or its backend.

Use [BUILD-PROMPT.md](docs/agents/BUILD-PROMPT.md) only after an explicit implementation request. `/build-pebbi` is a compatibility entry point to that bounded current feature, not permission to resurrect the old complete-product mandate. Repository skills and specialist roles are development aids, not runtime dependencies.

## Security and product invariants

- Save the user's complete small connection profile in this app's non-synchronizing macOS Keychain item. Never store keys in ordinary files, preferences, logs, prompts, repository content or command-line arguments.
- No fallback to developer credentials, a localhost LiteLLM proxy or an owner-operated cloud endpoint.
- Accept exact user-selected deployment identifiers and explicit compatible transport settings. Do not infer model capability or deployment access from its name or a catalog.
- Onboarding open/edit/local Save performs no network requests. Saved setup remains explicitly unverified. A later live test requires deliberate consent, bounded synthetic input and a compatible operation for that role.
- Preserve Keychain data across failed saves, denied reads and unknown schema versions. No global credential deletion, API-key recovery from other apps or permission bypass.
- Validate HTTPS destinations and prevent secret leakage through URLs, redirects, diagnostics or accessibility output. Preserve system certificate checks.
- Native controls, keyboard operation and VoiceOver are mandatory. Retain original colorful tactile Pebbi branding; do not substitute a web shell or minimalist generic settings page.
- No microphone, screen or Accessibility permission is needed merely to enter an Azure configuration.

## Documentation authority

Current authority is: explicit latest user request → [CONTRACT.md](docs/CONTRACT.md) current section → [LOCAL-AZURE-ONBOARDING.md](docs/product/LOCAL-AZURE-ONBOARDING.md) → this file → project-local specialization.

Earlier product/engineering/operations documents and machine-readable hosted-service contracts are retained with explicit historical markers. Their API routes, billing, Entra identity, deployment instructions, fixed models and all-product release gates are **not active dependencies or implementation orders**. The [documentation index](docs/README.md) labels what remains current. General visual tokens and original art remain usable; old UI compositions do not authorize old features.

## Verification and delivery

For documentation changes, run `python3 scripts/validate_docs.py`, the static schema checks and design lint when their files are touched; clearly distinguish historical-contract integrity from current feature acceptance. No document check proves a working app.

For a later implementation, use test-first behaviour slices and real native build/Keychain/first-launch/edit/reset verification. Do not claim a cloud Linux test certifies macOS UI or that synthetic credentials prove real Azure access. A build that only saves configuration is not a functioning voice assistant.

The repository is public and licensed under [MIT](LICENSE). Preserve license and third-party notices; do not change visibility or publish secrets. Follow the user's separately established development-workflow permissions. A failed cloud-agent repository lookup is not permission to silently switch workflows or start local development.

Finish with changed artifacts, actual checks and remaining limits. Do not provision, purchase, run inference, sign or release the app without the appropriate explicit authorization.
