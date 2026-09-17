# Local Azure onboarding — current feature specification

**Status: documentation only. Do not implement until the owner explicitly resumes development.** This document specifies one future feature, not the full historical app. It supersedes the managed-backend, mandatory Pebbi account, locked-model and subscription assumptions in the earlier documentation.

## Decision and boundary

Pebbi is an open-source native macOS app. Each user brings their own Azure API key, endpoint and model deployments. The app will connect directly from their Mac to their Azure resource. There is no Pebbi-operated backend, Supabase, Render, Vercel, Entra application account, Stripe subscription or hosted usage service in this design.

**On-device application does not mean on-device Azure inference.** UI, settings, orchestration and local data stay on the Mac; an authorized Azure inference request sends the necessary input to Azure, which processes it remotely and bills the user's Azure account. Do not advertise this as offline AI, no network access, or data that never leaves the device.

Current implementation scope, once authorized: first-launch onboarding with a **Custom Azure setup** section, secure local save/load, editing and reset. There is currently no application or onboarding screen to modify, so a future implementation may add the smallest launchable SwiftUI/AppKit shell needed to exercise this feature. It must not implement the whole older product, backend, browser automation, microphone capture or audio generation merely to add configuration.

## First-launch journey

1. On launch, read the app's versioned Azure connection profile from its own macOS Keychain item. Do not infer setup completion from a Boolean alone.
2. If no profile exists, show onboarding. Use the original Pebbi mascot, cream/sea-glass/clay/lilac palette, system rounded headings and accessible native controls.
3. Explain the direct-Azure connection and user-paid Azure usage before collecting credentials. There is no Pebbi sign-up or payment screen.
4. Show **Custom Azure setup**, with the fields below. Do not request microphone, screen-recording or Accessibility permission just to enter configuration.
5. Validate locally as the user edits. Do not send a key to a server or probe a deployment on launch, typing, blur or local Save.
6. Enable **Save setup** only when all required local fields and explicitly enabled role bindings are valid. Persist the complete profile atomically as specified below.
7. On confirmed save/read-back, show **Azure setup saved — connection not tested**. Do not show “models verified”, “voice ready” or a pretend working chat.
8. On later launches, a valid saved profile skips first-run setup. **Settings → Azure connection** always allows editing or reset.
9. If Keychain is locked/denied/unavailable, show a recoverable credential-access state. Do not erase credentials, create a replacement profile, or silently treat the user as a fresh install.
10. If the profile is malformed or from an unsupported newer schema, preserve it and offer an explanatory repair/reset path. Do not silently overwrite an unknown version.

## Fields and defaults

| Field | Control / requirement | Behaviour |
| --- | --- | --- |
| Azure API key | Required native secure text field | Never echo to logs, analytics, screenshots, command arguments, crash context or model prompts. Optional reveal requires a deliberate user action and returns to masked state. |
| Endpoint URL | Required native text field | User provides their Azure inference resource/base URL. Show examples using only placeholder hosts, never a real developer endpoint. |
| API family | Explicit choice in advanced connection settings | Azure OpenAI v1 or a documented classic Azure operation family. Save the selection; do not guess transport from a deployment name. |
| API version | Only required for a selected versioned/classic transport | Preserve exact user value. A v1 profile does not need a dated API-version value. |
| Reasoning / tasks deployment | Required editable text field | Used for future text, reasoning and screen-understanding adapters if supported by the chosen deployment. |
| Realtime conversation deployment | Optional enabled-role section | Intended for bidirectional speech-to-speech, not assumed equivalent to ordinary text generation. |
| Speech-to-text deployment | Optional enabled-role section | Used for transcription/dictation through a compatible transport. |
| Speech generation deployment | Optional enabled-role section | Used for text-to-speech when separately selected; not mandatory when the chosen realtime model produces speech itself. |

Use labels such as **Azure deployment name** and help text explaining that a deployment identifier can differ from the catalog model name. Accept user-chosen identifiers; do not force Astra or the previously selected audio models. Example suggestions are not defaults, a verified catalog or proof of access. Do not require a separate model for every role when a compatible deployment can serve more than one.

Each optional role has a clear enable/disable control. Disabled roles do not block Save and must not be presented as ready. Enabling a role requires its deployment identifier and a declared transport selection suitable for that role. A string alone does not establish model capability.

A shared key and endpoint are the normal path. Under **Use a different Azure connection for this role**, optionally allow a role-specific key, endpoint and API-family/version override. The inherited connection is clearly displayed. A fully disabled role has no retained override; disabling an enabled role warns if it will remove separately entered credentials. Do not silently copy a key to a different host.

Changing a shared connection must show which roles inherit it. Existing edited role overrides remain scoped to their own explicit endpoint. No fallback to the repository owner's endpoint, shared credential, model or local LiteLLM service is permitted.

## Local data contract

This is a proposed native data model, not an HTTP API or an implemented schema:

- `schemaVersion`: integer, initially 1.
- `profileId`: locally generated UUID, unrelated to a Pebbi account.
- `primaryConnection`: exact endpoint value, API family, optional version and secret key.
- `roleBindings`: `reasoning`, `realtimeConversation`, `speechToText`, `speechGeneration`; each contains enabled state, exact deployment name, declared transport and optional connection override.
- `savedAt`: local save timestamp; not a provider-verification timestamp.
- `validationStatus`: initially `savedUnverified`. No catalog lookup, save, handshake or accepted session update may produce a live-success status.

Store the entire small versioned profile, including the key and any overrides, in **one app-scoped, non-synchronizing macOS Keychain generic-password item**. This avoids splitting secret changes and completion flags across unrelated stores. Use a stable app service/account identity; never enumerate, import or clear other apps' credentials. Do not use UserDefaults, a tracked JSON file, `.env`, SQLite or an unencrypted Application Support file for the key. Ordinary non-sensitive appearance preferences may use UserDefaults separately.

A save validates first, writes one complete replacement Keychain item atomically, then checks the result. On failure keep the previous valid profile and remain in the editor with a sanitized error. A read-back uncertainty remains an uncertainty: re-read before retrying, do not claim completion or destroy a possibly committed profile. No separate onboarding-complete flag can override the actual credential state.

On an edit, the UI may use a clear **Keep saved key** state instead of exposing the secret. A blank untouched password field must not silently erase the saved key. **Replace key** is explicit; invalid replacement cannot alter the stored profile. Cancelling edits leaves the previous profile untouched.

Reset requires confirmation explaining that only Pebbi's Azure connection configuration is removed. Delete only this app's item, verify the result, clear in-memory secrets, and return to onboarding. Do not delete user workspaces, other credentials or Azure deployments. Uninstall/reinstall can leave macOS Keychain items intact; describe “first launch” as absence of a valid saved profile, not a guarantee that every reinstall erases it.

## Endpoint and credential safety

- Require an absolute HTTPS URL and a valid hostname. Reject URL userinfo, fragments, malformed percent escapes and key/token-bearing query parameters.
- Preserve the source identifier; show an actionable validation error rather than silently repairing a malformed URL, deployment name or API-version token. Do not truncate a full Azure operation URL into an assumed base.
- Explain the exact configured destination and role before any future network test/use. Treat unsupported endpoint families as unsupported, not as a reason to send credentials speculatively.
- Recognize only implemented, documented Azure endpoint families, including appropriate sovereign-cloud hosts if actually supported. Custom proxies, arbitrary endpoints and private-network routing are outside this first feature unless separately reviewed and explicitly added. Do not claim support for every Azure catalog or project URL.
- A future request builder must compose the operation from the explicit API family and validated base without duplicate `/v1`, lost query parameters, or deployment-name substitutions.
- Azure keys go only in the documented authorization header for that selected Azure operation. Never put a key into a URL, request body, model message or query string. Do not forward credential-bearing requests across redirects to another origin.
- Keep system TLS verification enabled. No insecure fallback, permissive certificate delegate, globally disabled sandbox/security setting or trust-all connection mode.
- No telemetry, background discovery, account registration, cloud sync or managed billing is part of setup. The app never uploads the connection profile to a Pebbi service.

## Validation and network boundaries

**This single feature requires local configuration validation, not working voice/chat pipelines.** Successful Save proves persisted input, not Azure access. Do not add a misleading Test Connection button whose only check is a model listing or one unrelated request.

If live connection verification is separately authorized later, use a deliberate **Test selected role** action with destination and possible Azure-charge disclosure. Send bounded synthetic input only, never microphone or private screen data for an onboarding test. Verify each role with its actual modality/operation and label the exact tested scope; a reasoning response cannot certify dictation or audio generation. Show unsupported transport, permission failure, deployment not found, throttling, network/offline and TLS errors honestly with no key or full secret-bearing request in the message.

A later adapter must verify model capabilities before enabling a feature. Changing a connection/deployment invalidates any prior verification. The older three locked models and their resource-specific audit results are historical examples only; they neither constrain nor certify another user's deployment.

## UI, copy and accessibility

- Heading: **Make Pebbi yours.** Section: **Custom Azure setup**.
- Explanation: **Connect your own Azure resource. Your key stays in this Mac's Keychain. AI requests go directly to Azure and may incur charges in your Azure account.**
- Endpoint help: **Use the endpoint for your Azure inference deployment, not a portal or project-management URL.**
- Model help: **Enter the deployment name configured in Azure. It may differ from the model's catalog name.**
- Primary action: **Save setup**. Secondary: **Cancel** when editing; close/quit remains available during first run without pretending setup completed.
- Saved message: **Azure setup saved. Connection not tested.**
- No-key/no-profile status: **Set up your Azure connection to enable AI features.**
- Denied Keychain copy: **Pebbi could not access its saved connection. Unlock or allow access, then try again. Your saved setup has not been intentionally removed.**
- Reset action: **Remove Azure setup** with **Remove** and **Cancel** choices.
- Use SecureField semantics, persistent visible labels, keyboard navigation, accessible error associations and native focus behaviour. Never expose an API key through an accessibility label or status announcement.
- Keep the established expressive Pebbi materials and mascot. Decoration yields to readable fields; advanced transport/per-role options disclose progressively. Respect light/dark, increased contrast and reduced motion. No animation implies a live connection.

## Acceptance checklist for the later implementation

| ID | Required evidence |
| --- | --- |
| BYOK-001 | A clean app credential state opens onboarding; no hosted service or Pebbi account is required. |
| BYOK-002 | Required key, endpoint and reasoning deployment validate locally; invalid Save never modifies persisted state. |
| BYOK-003 | User-selected deployment names round-trip unchanged; optional role disabling and explicit connection overrides work without silent fallback. |
| BYOK-004 | Valid Save persists the complete versioned profile in this app's non-synchronizing Keychain item; no secret is in ordinary files/preferences/logs. |
| BYOK-005 | Relaunch with a valid profile skips onboarding; Settings can edit it, keep or replace a key, or cancel without mutation. |
| BYOK-006 | Missing/locked/denied/corrupt/newer-version credential states are distinguished; write/read-back failures preserve data and do not claim success. |
| BYOK-007 | Confirmed Reset removes only Pebbi's profile and returns to onboarding; cancellation changes nothing and deletion failure is reported. |
| BYOK-008 | Opening, typing and saving issue zero network requests and trigger no microphone/screen/Accessibility permission prompts. |
| BYOK-009 | Saved-but-untested status is truthful; there are no fake audio, transcription, chat or deployment-success claims. |
| BYOK-010 | Endpoint validation rejects insecure or secret-bearing URLs and unsupported input without silently rewriting it; future authenticated redirects cannot leak keys. |
| BYOK-011 | Keyboard and VoiceOver can use every field, enabled-role section and action without revealing secret text; light/dark and compact windows remain legible. |
| BYOK-012 | README/license/agent instructions match this local BYOK scope; no backend, login, Stripe, Supabase or Render dependency is introduced. |

Tests use conspicuously synthetic credentials and isolated temporary Keychain service identities. Never test against the owner's saved Azure key or delete a real profile. Later implementation requires actual native build/tests and interactive first-launch/edit/reset evidence on a Mac; none has run for this documentation change.

## External requirements and exclusions

Needed later: a compatible Swift/macOS development environment; user-entered Azure credentials and compatible deployments for actual inference; Apple signing/notarization only for a separately authorized trusted distribution release. No Render/Supabase/Vercel/Azure Container Apps account, custom domain, server database, managed login or payment provider is needed for this feature.

Not included: full agent/task runtime, live voice or transcription implementation, browser extension, permissions automation, backend provisioning, production release or an assertion that all Azure model modalities work. Those require separate scope and real tests. The repository is licensed under [MIT](../../LICENSE); preserve third-party notices and avoid claims that the Pebbi name is trademark-cleared.
