# Support, diagnostics and user-safe recovery

Status: **support operating specification; no live support channel or SLA is asserted**. A verified operator contact, support destination and assigned owners are [external inputs](EXTERNAL-INPUTS.md) required for LG-SUPPORT/LG-WEB. Do not invent an email address, staffed team, response promise or ticket receipt. [OPERATIONS](OPERATIONS.md) owns incidents; [PRIVACY-AND-DATA](PRIVACY-AND-DATA.md) owns data handling.

## User-facing support entry points

Settings exposes Support, documentation, release notes, privacy, account and a previewable diagnostics export. Contextual error cards provide one clear recovery action and Support with a safe correlation ID. Menu bar/perch must not cover support/account/billing sheets. A web support page provides an actual tested primary destination and a verified fallback; if neither is configured, state unavailable and preserve local diagnostic export. The original brand board is not a support site.

Use the canonical user nouns Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections and Settings. Keep the tone calm, specific and honest. Explain what happened, what remains safe and what the user can do. Do not blame the user, promise a fix already applied or suggest buying a plan when the real problem is an unconfigured provider.

Examples of acceptable recovery copy, to adapt to actual state:

- “Microphone access is off. You can keep typing. Open System Settings to enable voice.”
- “Voice is unavailable for this account configuration. Your conversation is saved; no replacement model was used.”
- “I couldn't confirm whether that message was sent. I won't send it again until we check.”
- “The insertion destination changed. Review your text and choose the field again.”
- “This routine runs while Pebbi is open. Missed work after Quit was not run.”
- “The local export is ready. The account export is still pending.”

These are wording examples, not a report of current app behavior.

## Diagnostic collection contract

1. The user chooses a bounded interval and can enter reproduction notes. Show app/backend/extension/config version where available, OS/architecture, capability state, safe error code, durations/state transitions and correlation IDs.
2. Exclude prompts, chat/file contents, raw screen/audio, clipboard contents, full URLs/query parameters, home paths/usernames, credentials, signing material and other accounts. Application/window titles can contain sensitive content and are excluded or deliberately redacted too.
3. Run redaction before writing the export, not only before network send. Preview the actual sanitized bundle. Redactor failure blocks export/send until unsafe fields are removed; do not retain a raw intermediate archive.
4. Local export works offline and does not send a ticket. Outbound support submission needs a fresh preview and explicit approval. A failed upload preserves only the safe local artifact and never says sent. Retry is idempotent where supported and retains the same submission identity.
5. Verify receipt by reading the exact target ticket/submission status or trustworthy provider receipt. A click or accepted API call is not proof the support system received a usable bundle. Missing service input remains BLOCKED.
6. Apply approved support storage/access/retention and user deletion requests. Operator downloads need a documented purpose and access audit. Do not attach raw customer data to a public issue or build-agent context.

A user may separately choose to provide a screenshot or document for a specific case; give a redaction preview and minimal-scope warning. Never make passwords, API keys, MFA codes, payment details, broad screen recording or a complete home-directory archive prerequisites for help.

## Triage intake

Ask only for information missing from safe diagnostics: observed versus expected action, exact safe error, app version, supported OS/architecture, affected capability, whether an external action may already have occurred and reproduction steps using test content. Confirm what is user-observed versus operator-reproduced. Do not ask the user to repeat retrievable diagnostics or disclose private model endpoint names in a public ticket.

Classify a case by boundary before suggesting changes:

| Symptom | First safe check | Forbidden shortcut / escalation |
| --- | --- | --- |
| Can't sign in / another device still active | System-browser result, verified account, device/session revocation and network. | Never ask for password/MFA/token or approve auth for the user. Escalate identity with correlation ID. |
| Mic/screen/AX denied | Actual OS permission and capability-specific explanation; unrelated typed/local use. | No TCC database edits, permission auto-clicking or disabling OS security. |
| Voice/dictation unavailable | Selected role/deployment status, safe error, account entitlement; known deferred inputs. | No catalog-based assurance, fake audio transcript or model substitution. Azure voice inputs are USER-DEFERRED until reopened. |
| Wrong focus / dictation not inserted | Preserve review text; compare original target with current field, secure-input and AX state. | Never repeat insertion blindly or paste into whichever app is active. |
| Task stuck / unknown send | Inspect task/attempt/wait state and immutable effect receipt; read exact target. | No generic Retry if outcome unknown; escalate to reconciliation. |
| Routines not running while closed | Explain app-open local execution, next eligible run and explicit Run now. | Never promise cloud execution or install a daemon as a workaround. |
| Quota/billing discrepancy | Server reservation/consumption state and authoritative Stripe account/event history. | No client-edited credits, invented refund/price/entitlement or unapproved transaction. |
| Missing conversation/file | Ownership, archive/search filters, source existence, safe store/export recovery. | Never silently replace store with empty data, scan unrelated folders or claim cloud sync can restore it. |
| Browser not connected | Chrome/Brave version, extension/helper install, selected tab/origin scope and native-host authentication. | No ordinary-profile remote-debugging port, all-tab grant or login credential guessing. |
| Crash/update won't install | Exact signed build/channel, compatibility, sanitized crash and normal Gatekeeper result. | No unsigned build, disabled Gatekeeper/notarization/Sparkle check or blind database downgrade. |
| Privacy/security concern | Stop affected collection/action and preserve minimal restricted evidence. | Do not request secrets to prove exposure or publish sensitive evidence; immediate security/privacy escalation. |

## Severity and ownership

- **Security/privacy/data-integrity:** unauthorized access/disclosure, duplicate protected effect/charge, data corruption or unsafe update. Contain immediately, assign security/incident owner, stop affected admission/distribution, preserve redacted evidence and follow OPERATIONS. No ordinary backlog routing.
- **Critical functional outage:** sign-in, selected model, core native interaction, installation or account/billing control unavailable across affected users. Assign service/native operator; identify scope and safe alternatives without false readiness.
- **Single-user recoverable failure:** permission/device/connection or workspace-specific issue with data preserved. Follow bounded recovery, exact-target verification and clear escalation if it fails.
- **Usability/accessibility defect:** broken VoiceOver/focus/contrast/Stop can be release-blocking regardless of user count; assign accessibility/native owner and test the actual assistive flow.
- **Question/feedback:** answer using current verified product behavior and published approved policy; avoid inventing availability/pricing.

Each incident has one accountable coordinator and explicitly assigned native/backend/integrations/billing/security/privacy owners as needed. Response/notification deadlines follow approved service/legal commitments; no commercial SLA is defined here. Release safety does not wait for a customer-count threshold.

## Support-assisted recovery and approvals

Support can guide a user through native Settings, inspect sanitized diagnostics and suggest a scoped recovery. It cannot grant standing tool authority, manipulate account rows manually, issue financial compensation without authorization, remotely operate secure screens or disable safety to satisfy “do it all.” Any outbound reply, uploaded diagnostic, destructive cleanup or protected action requires the appropriate user/operator approval.

Before any consequential repair: record exact target, intended change, backup/recovery implications and user consent. Afterward read back exact state, check for unintended changes and communicate what was actually verified. If a tool cannot establish outcome, stop and report uncertainty. Preserve drafts and local work while investigating; do not force repeated login/reinstall/reset as a diagnostic ritual.

## Privacy and account requests

Authenticate the requester through the approved account flow; do not accept an email address alone as authority to export/delete account data. Route data-access/deletion/correction requests to the privacy owner, distinguish local versus server data and quote only the approved published deadlines/retained legal categories. A support worker cannot read a user's local conversations from the backend because no sync exists. Other offline Mac data and user exports cannot be remotely erased by this architecture.

Track request, verified identity, scope, deadline, processing state, receipt and disclosed exception with minimal content. Do not say all deleted when server work is pending or local copies remain outside scope. Protect export URLs and avoid forwarding account exports into tickets.

## Public support and release communication

Support/privacy/account/download pages must be accessible, original Pebbi-styled and truthful about availability, macOS 14.2+, verified architectures and actual releases. Explain local routines and provider availability without publishing private deployment details. No fake testimonials, approved price claims or download buttons for nonexistent artifacts.

Outage notices distinguish affected capability, known scope, safe workaround and current verified status. Only authorized operators publish notices; updates must not expose account identifiers or speculative root causes. Resolved means the real path and affected gates were re-tested, not merely a green health check. A signed corrective release notice states data compatibility and recovery actions plainly.

## Closure and launch evidence

Close a support case only after verified resolution or an explicit unresolved/blocker handoff with owner and user-visible next action. Record actual reproduction, redacted evidence, approved changes, exact readback, user impact and regression test/gate IDs. Do not claim the user confirmed a fix if they did not.

LG-SUPPORT requires actual tested entry points, assigned ownership/escalation, offline diagnostic export, seeded-secret redaction, preview/cancel/approved-send/readback, identity-safe privacy request handling and an exercised incident/rollback communication flow. Until those inputs and the implemented candidate are verified, the gate remains **BLOCKED**, not passed by this runbook.
