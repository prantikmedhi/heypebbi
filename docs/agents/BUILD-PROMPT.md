# Future build prompt — local Azure onboarding only

**ON HOLD: the owner currently requests documentation and repository updates only. Do not execute this prompt unless implementation is explicitly authorized later.** This supersedes the previous one-prompt full-app build request. No application has been created by this change.

## Paste only when ready to authorize implementation

> Implement only the native local Azure onboarding feature in `docs/product/LOCAL-AZURE-ONBOARDING.md`, satisfying BYOK-001 through BYOK-012. Follow the current sections of `AGENTS.md` and `docs/CONTRACT.md`. Inspect the actual repository first; preserve existing application code if it exists. If there is no app yet, create the smallest launchable SwiftUI/AppKit macOS shell needed for first-run setup, local validation, secure Keychain persistence, Settings editing and confirmed reset. Let users supply their own Azure key, endpoint and per-role deployments. No hosted backend, Supabase, Render, Vercel, Pebbi login, billing, telemetry or hardcoded owner credentials. Do not implement unrelated historical PB requirements. Preserve the expressive Pebbi branding and native accessibility. Use test-first behaviour slices, run actual native checks, review secret handling and document results. Saved configuration is not verified model access; Azure inference is remote, not offline. Keep optional live tests bounded, explicit and separate from Save. Do not provision or release anything merely to finish this feature.

## Required deliverable when resumed

A working, locally runnable onboarding feature and its tests—not just fields in a mockup. Show the first-launch/no-profile path, validation, save/relaunch, editing, reset, denied/locked Keychain recovery and honest saved-unverified state. There is no requirement to implement voice generation, transcription or a task engine in this single change.

Read the feature specification for the exact profile, key preservation and role rules. Current acceptance IDs are BYOK-001 through BYOK-012. The old [PB ledger](build-state.template.json), hosted OpenAPI, server enrollment and billing fixtures are historical records, not this feature's completion checklist.

## Execution limits

Use a compatible verified Swift/macOS toolchain. Follow the owner's selected development workflow; if repository access or a Mac runner is unavailable, report it rather than silently switching or inventing build output. Tests use isolated fake profiles and app-owned temporary Keychain identities, never the owner's actual credentials.

Do not change system permissions, read other apps' secrets, deploy infrastructure, create paid resources, publish a signed release or invoke an inference request without applicable authorization. No server or platform account is needed to validate local setup. Apple signing/notarization belongs to a separately authorized distribution task.

## Final report

Report the actual feature artifact, build/test evidence, launch instructions, tested persistence/recovery cases, unrun hardware/Keychain/live checks and any blocker. Do not call the feature the complete Pebbi assistant. Do not claim real model capability from a saved deployment string or a fixture.
