# Native macOS implementation contract

**Proposed specification, not implemented code.** Governs PB-001, PB-003, PB-005–PB-010, PB-014, PB-018, PB-029, PB-031–PB-038. [CONTRACT](../CONTRACT.md) and canonical security policy take precedence. [ARCHITECTURE](ARCHITECTURE.md) defines ownership; [TOOLS](TOOLS.md) defines tool envelopes.

## 1. Native app and window model

`PebbiApp` is a SwiftUI application with an AppKit application delegate for lifecycle bridging. The app remains a normal Dock application with a Home window, Settings scene and menu-bar item. Closing Home hides that window; Quit ends local work and helpers. Neither a hidden Home window nor menu-bar mode is evidence the app has quit.

`WindowCoordinator` is `@MainActor` and owns:

- Home: resizable `NSWindow` with native title bar/toolbar and SwiftUI content. Restore frame only after clamping to a current screen's usable area. Sidebar nouns are exactly Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections, Settings.
- Perch: compact nonactivating `NSPanel`, top edge of the user-selected display. No keyboard focus until the user clicks an input control or explicitly invokes the compose shortcut. For editable text, intentionally activate a normal focusable surface; do not smuggle keystrokes out of another app.
- Menu-bar item: `NSStatusItem`, usable without a notch, with Home, capture, voice/dictation controls and Quit. Never obscure Apple menu/status items to imitate hardware.
- Guidance: transparent borderless panels bound to the captured display/window, ignoring mouse events by default. A separate native accessible inspector exposes the same step, target and Resume/End controls. An overlay alone is not an accessible control.
- Approval: native sheet when Home is active, otherwise a notification/perch indication which the user opens. Never steal focus to approve. Approval requires a deliberate native UI action and exact preview, not a voice transcription interpreted as consent.

Use `NSScreen.safeAreaInsets`, auxiliary top areas where available and visible frame to place the perch; notch presence is a geometry input, not an assumption. Do not hard-code a MacBook size. On notchless/external screens the perch docks below the menu bar. Observe screen-parameter and workspace notifications; never place windows with only stored pixel positions.

Keep authored ceramic Pebbi artwork, rounded system typography and root DESIGN.md color/material tokens. SwiftUI/native AppKit controls supply semantic behavior. Tactility does not justify custom text fields, inaccessible painted buttons or a monochrome/minimalist replacement. Animate from current presentation state; interrupted expand/collapse reverses without a jump. Reduced Motion substitutes static/cross-fade transitions; Reduce Transparency uses solid materials; Increase Contrast strengthens boundaries. Do not run indefinite decorative animation when idle.

### Proposed presentation interfaces (pseudocode, not Swift implementation)

```text
WindowCoordinator.showHome(reason: userGesture | shortcut | restoredWindow)
WindowCoordinator.showPerch(displayId, activateInput: false)
OverlayController.present(annotationSet, captureGeometryId)
OverlayController.invalidate(reason: moved | spaceChanged | scopeRevoked)
ShortcutController.register(binding, action) -> registered | conflict | invalid
```

No UI interface accepts raw tool payloads for execution. A user gesture becomes a coordinator command with an ingress ID.

## 2. Shortcuts, focus and text insertion

Use native global hot-key registration for discrete shortcuts (Carbon `RegisterEventHotKey` where supported by the pinned SDK), with native menu equivalents. No global keylogging or always-on event tap just to listen for a shortcut. Recorder detects reserved/system conflicts and displays a conflict instead of quietly stealing the key. Permission requirements of any fallback must be disclosed separately.

`FocusSnapshot` is an ephemeral value containing `focusToken` UUID, app bundle ID, PID plus process start identity, window ref, focused AX element ref, selected-text range if exposed, `focusRevision`, `capturedAt`, and a secure-field flag. Do not retain the field's contents unless insertion needs an exact user-approved replacement range.

Dictation starts from the current target snapshot, then presents reviewing text before insertion by default. Auto-insert is a separate preference with a scope-specific warning, not permission to target a changed app. Before insert, verify process identity, frontmost app, focused element and original range/value revision; any mismatch returns `focusChanged`, moves back to `reviewing` and offers Copy or Choose target. Never activate the original app behind the user's back.

Insertion ladder:

1. For a writable nonsecure text element, use supported AX selected-text/value mutation with the exact selection/range, then read the resulting range/value to verify.
2. If unsupported, offer Copy. A user may explicitly choose Paste with a fresh foreground takeover approval. Clipboard snapshot/restore is best-effort and only when the change count still matches Pebbi's own write; do not overwrite a new clipboard value set by the user or another app. Sensitive text must not be retained in clipboard history by Pebbi.
3. Never simulate arbitrary typing with CGEvent without takeover consent, never type into secure/credential/permission/payment controls, and never retry insertion after a timeout unless read-back proves nothing was inserted.

Insertion is one journaled tool effect under its audio owner (audio_event_receipts and the audio-owned approval/effect FKs in DATA-MODEL.md), not a synthetic agent task. Before dispatch, cancellation makes no target edit. Racing an admitted insertion stops further work and reconciles inserted/unchanged/unknown; never claim nothing happened or auto-undo across user edits. Stop dictation cancels capture/transcription, not this or another Pebbi's task. Escape in dictation review discards that draft after the native flow's normal unsaved-content behavior; it does not broadcast task cancellation.

## 3. TCC permission model

`PermissionService` tracks independent observations, not a single “all permissions granted” Boolean:

| Capability | Platform observation / request | Denied or revoked behavior |
|---|---|---|
| Microphone | AVFoundation authorization status and user-triggered request; usage description | Voice/dictation unavailable; typed chat remains; settings link, no repeated prompts |
| Screen capture | CoreGraphics preflight/request with ScreenCaptureKit scope selection; availability guards | No screen stream; explain how to reopen system settings and re-check; typed/DOM features can remain |
| Accessibility | `AXIsProcessTrustedWithOptions`, prompt only after user intent | AX tools blocked; DOM read-only or manual guidance where authorized |
| Notifications | UserNotifications authorization/settings | In-app unread badges still work; no assumption a notification was shown |
| Browser/connector | Separate app/extension/OAuth permission, not TCC | Disconnect only that capability; preserve task and precise reconnect action |

These permissions do not authorize one another. Screen recording is not input control. Accessibility trust is broad OS capability but tool scope remains bounded by Pebbi policy. The app is responsible for honest disclosure that a non-sandboxed application can possess broader user-account access than a chosen workspace.

Re-check permission immediately before sensitive operations and on foreground/wake. An observation can change after checking: adapter errors still fail closed. Never automate System Settings permission toggles, OS authorization prompts or credential fields. User approval within Pebbi does not bypass TCC, browser consent or provider OAuth.

Developer ID/hardened runtime configuration must enumerate actual required entitlements, usage descriptions and code-signing requirements at build time; do not preemptively add disable-library-validation, JIT, Apple Events automation or unrelated protected-resource entitlements. Developer ID/hardened runtime is not the App Sandbox. See canonical security policy for the approved final signing profile.

## 4. AX-first desktop driver

`AXDriver` confines `AXUIElement`, `AXObserver` and run-loop state to one dedicated serial worker thread. The actor façade submits jobs and returns copied `Sendable` snapshots. Use bounded `AXUIElementSetMessagingTimeout` calls; proposed limit is two seconds per remote request, with an eight-second overall inventory budget. Limit inventories to 500 nodes, depth 12 and 256 KiB of text; return `truncated: true` plus a continuation scoped to the same generation rather than pretending the tree is complete.

Refs are UUIDs resolving inside the driver's registry, bound to `{appBundleId, processIdentity, windowRef, treeGeneration}`. Never serialize AX pointers, backend native IDs or “click element 7” as durable identifiers. Process restart, missing element, window close and tree replacement invalidate them. An observer notification invalidates relevant snapshots; a lack of notification does not prove stability, so re-resolve and check role/action/geometry immediately before a mutation.

Allowed semantic operations are narrowly enumerated: inventory, inspect a ref, supported AXPress, AXSetValue on an ordinary writable nonsecure value, select a supported menu/select option, supported scroll increment/decrement and focused insertion. AXPress on a background window may work, fail, raise that app or trigger app-specific behavior. Report the observed behavior, not a blanket claim of background automation.

Background protocol:

1. Read current frontmost app/window and relevant target identity.
2. Inspect target role, enabled state and supported actions; deny sensitive fields/actions and out-of-scope targets.
3. If there is evidence the semantic action will need activation or the app's behavior is unverified, return `requiresTakeover` rather than trying a coordinate fallback. Maintain a tested compatibility record per app version, not a guessed universal rule.
4. For a permitted background semantic action, execute once and read back the exact target. If the app unexpectedly activates, stop the sequence, release the lease and disclose that focus changed. Do not forcibly restore focus while the user is interacting.
5. `cannotComplete`/timeout after a mutation is `unknown`, not an invitation to repeat. Re-inventory and reconcile; if the effect cannot be determined, ask the user.

A closed/minimized/occluded app may expose an AX tree while its screenshot cannot be captured, or expose no useful tree at all. A background window's accessible controls need not accept actions. Apps with custom-rendered UI may have incomplete roles. Missing support remains a product limitation with explicit takeover/manual alternatives, never a fake success.

## 5. Explicit CGEvent takeover

`TakeoverController` is the only component allowed to post mouse/keyboard events. ToolBroker supplies an approved immutable intent and a lease, not a raw model command.

A native takeover preview specifies app/window/display, action list or bounded interaction, reason semantic control failed, and that the real pointer/focus will move. `allowOnce` covers only that displayed interaction. Interactive takeover lease: at most 60 seconds of active use, always visible in the perch, revoked by Stop control, Escape, session lock, display/Space change, user input conflict or app switch away from the approved target. No routine or standing scope grant can silently start a takeover.

One global foreground-input lease blocks competing Pebbis and dictation insertion. Immediately before each event, verify lease generation, target frontmost identity, geometry freshness and sensitive-control exclusions. If activation is part of consent, use AppKit/NSRunningApplication activation explicitly; after activation, re-observe before posting. Never send a stale queued sequence once focus changes.

Physical user activity suspends further automated events. Use a disclosed event observation path only while takeover is active, avoid recording key content, and distinguish synthetic events with an event source tag. If reliable interruption observation cannot be established with available permissions, do not offer unattended sequences; require step-by-step user control. Escape must remain a local emergency stop even when network is offline. Do not install an unbounded global keyboard logger.

Post down/up pairs safely; on cancellation release any Pebbi-held modifiers/buttons and stop immediately. Do not restore an old cursor position if the user moved the pointer. A timeout after posting is uncertain; verify the actual control or ask, never repeat the click. `CGEvent` coordinates are global Quartz display coordinates, not capture pixels or SwiftUI-local points.

## 6. Coordinate spaces and generation safety

Every screenshot/overlay/action carries `geometryId` and `captureId`. `DisplayGeometry` snapshots:

- ephemeral `displayId` UUID mapped to current `CGDirectDisplayID`, persistent display UUID where available, mirror group, rotation and generation;
- AppKit global frame (points, bottom-left origin), visible frame and safe-area regions;
- Quartz global display bounds (top-left-oriented desktop coordinates), never assumed to equal physical pixel dimensions;
- capture source rect, actual raster dimensions, actual nonpadding content pixel rect and transforms; window content vs frame bounds distinguished;
- `backingScaleFactor`, capture scale and timestamps for diagnostics, not as interchangeable values;
- target window identity and current geometry revision.

For an axis-aligned display, AppKit-to-Quartz mapping uses the **matched display's observed bounds**, not `NSScreen.main` and not the union desktop height. In proposed mathematical notation:

```text
u = (appKitX - appKitDisplay.minX) / appKitDisplay.width
v = (appKitDisplay.maxY - appKitY) / appKitDisplay.height
quartzX = quartzDisplay.minX + u * quartzDisplay.width
quartzY = quartzDisplay.minY + v * quartzDisplay.height
```

Map all four rectangle corners and take the transformed bounds; a rectangle's lower-left Y is not its top-left Y. Displays left/above the primary can have negative coordinates. `NSScreen.main` changes with keyboard focus and is not the stable coordinate origin. Rotation/mirroring must be handled by the recorded transform of the actual capture source; no blanket second rotation of an already upright SCK frame.

Capture mapping is separate. Normalize a point relative to `contentPixelRect` (subtract letterbox origin, divide by content size), then apply the recorded `pixelToQuartz` affine transform constructed from the SCK selected source rect and current display/window bounds. ScreenCaptureKit frame attachments (`contentRect`, scale information and status) must be interpreted in their SDK-documented units before constructing that transform. Do not multiply both backing scale and capture scale. If the mapping cannot be established or dimensions/status disagree, return `invalidGeometry`, not a guessed click.

Overlays use Quartz-to-AppKit inverse mapping, then convert into their panel coordinates. Browser DOM CSS coordinates have an additional independent mapping; browser-native DOM actions avoid that conversion altogether. See [BROWSER-AUTOMATION](BROWSER-AUTOMATION.md).

Any display reconnect, resolution/scale/rotation change, mirror change, Space switch or target move invalidates affected geometry and pixel action intents. On hardware uncertainty, recapture. Coordinate takeover requires a capture no older than two seconds **and** unchanged target/geometry generation. Fresh timestamp alone does not authorize a click. Guidance tied to a semantic ref can be re-anchored after fresh observation; unanchored strokes freeze with an outdated indication until recaptured.

## 7. Capture scope, lifetime and exclusions

The user chooses one window, one display, or a selected rectangle within a display. Prefer the system ScreenCaptureKit content-sharing picker available to the deployment target; availability-guard newer refinements. Continuous “watch this” is a separate, visible capture session, never enabled by an ordinary question. Capture scope is bound to the selected source ID; window close does not fall back to full-display capture.

`CaptureService` owns a scope lease, `SCStream` or availability-supported screenshot operation, and bounded frame storage. Capture only after permission and a local purpose. Exclude Pebbi overlays/approvals from its own stream where platform filtering supports it. If exclusion or source scope cannot be enforced, pause capture and explain rather than upload unintended content. Protected windows can be black or absent; report `protectedContent`/unavailable instead of claiming to understand them.

Concrete default lifetime rules (may be shortened by canonical security policy):

- One-shot capture consumes one complete, valid frame and tears down the stream immediately.
- Continuous scope expires after ten minutes unless the user renews it; Stop, lock, sleep, sign-out, task cancel or permission revoke ends it sooner. Idle continuous scope does not imply audio or desktop input permission.
- At most three raw frames are resident. Drop superseded frames rather than queueing them; processing references retain only the selected frame.
- Raw capture and derived OCR transient text expire within 30 seconds after the last authorized consumer, and immediately at scope revoke; invalidate handles so late consumers fail. ARC/deallocation and clearing owned buffers are best-effort memory hygiene, not a guarantee of forensic secure erasure.
- No raw capture written to SQLite, diagnostics, temporary previews, crash breadcrumbs or autosaved conversations. Keep redacted scope metadata and result references only. If the user explicitly chooses Save/Attach screenshot, create a normal durable file with separate disclosure, storage/retention controls and provenance.
- Sending selected frames to the reasoning backend is an explicit feature disclosure, not local-only analysis. Stream/session UI identifies what is shared. Do not claim reliable automatic detection of all sensitive pixels; provide source selection, local exclusion/review and immediate Stop.

No password/secret extraction, protected-content bypass, camera capture, or ambient always-on screenshot history. VoiceOver descriptions may explain the scope but must not read sensitive raw OCR by default.

## 8. Audio engine and independent state machines

`VoiceController` owns canonical voice states; `DictationController` owns canonical dictation states. They persist separate audio_operations/audio_event_receipts through Store and share a single device microphone resource lease. Starting casual voice/standalone dictation allocates audioOperationId/audioAttemptId, never a task queue row. BackendClient maps only audio-role wire taskId/attemptId to those UUIDs; sourceTaskId/sourceAttemptId remain actual agent-result provenance. A voice stream may coexist with the same Pebbi's Astra task; dictation can run while that task is running or waiting. One provider stream per audio owner remains enforced. Voice uses the realtime role, dictation uses the transcription role; do not create an automatic transcription-plus-TTS replacement for an unavailable realtime model.

`AudioEngineBridge` serializes AVAudioEngine graph setup/teardown and device changes outside the realtime callback. A realtime tap must not allocate unbounded memory, await an actor, run logging, write SQL or perform network IO. Copy into a bounded preallocated buffer/ring; a worker converts/resamples to negotiated provider format and sends bounded frames. Overflow is surfaced as a capture interruption; never silently drop sustained audio and pretend the transcription is complete.

Bind audio frames to `{audioOperationId, audioAttemptId, voiceSessionId or dictationSessionId, generation, sequence}` in controller memory. Session IDs/tokens are volatile mappings to the audio aggregate, never task IDs/FKs or reusable restored authority. Persist semantic/terminal receipts with the owner cursor atomically, not raw frames. To start dictation while voice holds the microphone, require a native review to end that voice input session, then release/acquire the lease; no automatic hidden voice resume. Changing input/output device increments generation, rebuilds conversion, and renegotiates as necessary. Do not assume built-in microphone sample rate or channel layout. Bluetooth profile changes can change quality, route and timing; display the actual device and reconnect status. Device removal, sleep, lock or mic revoke stops capture immediately and requires explicit recovery. Do not resume listening merely because a device returns.

Speech-stop: atomically increment playback generation, stop/flush scheduled output, request remote response cancellation if supported and ignore late audio frames. It does not set task `cancelling`. Task Cancel stops further tool dispatch, cancels model work, reconciles in-flight effects and separately stops speech describing that task. Muting output does not mean the microphone is off; controls and accessible labels must distinguish these states.

Real-time provider/deployment errors remain `unavailable`/`failed`; text remains usable through the configured reasoning path when available. Never demonstrate prerecorded fixture speech as a live deployment test.

### Native credential, usage and management boundaries

IdentityService stores the one-time `RegisterDeviceResponse.deviceToken` in an app-restricted, non-synchronizing Keychain item keyed by accountId/deviceId, not install.json, SQLite, UserDefaults, logs, clipboard or tool context. Create the API/SECURITY account-authenticated enrollment nonce challenge, perform ordinary Entra auth-code + PKCE with returned nonce, `prompt=login`, configured signed `auth_time` and local callback state validation, and send `enrollmentId`/`enrollmentIdToken` only in the registration body, never an ID-token API bearer. Follow challenge one-use, freshness and lost-response/re-enrollment semantics; do not reuse an old bearer with a new installationId to evade revocation. Missing/locked Keychain item blocks device-bound calls and requests explicit native reauthentication; there is no fallback to just X-Pebbi-Device-Id. SQLite holds only deviceCredentialKeychainRef for the credential. Cache the opaque backend `accountId`; never derive it from `sub`, compare native/API subjects literally, or link identities by email/name. Backend identity uses pinned issuer/tenant + verified immutable `oid` (and signed `tid` where provided); no raw token/claim dump or new tenant identifier is added to local accountMetadata. Never share device credentials with the browser extension/native host, execution supervisor, code/MCP environment or Azure. Session mint uses bearer + device ID + device credential; WebSocket authorization uses its separately issued role/owner/device-bound short-lived session token and public X-Pebbi-Device-Id, never X-Pebbi-Device-Token or an account bearer.

On sign-out/revocation/account deletion, close audio/provider streams, advance accountEpoch, invalidate device authorization and remove the relevant Keychain credential under the identity policy. Local purge covers audio receipts, drafts and staged bytes as well as conversations. An interrupted enrollment response does not authorize recovering a credential from logs/cache; use the backend's fresh interactive recovery path. Confirmed credential loss, including the last device, uses explicit accessible native review of the exact same-installation target and `replaceDeviceId` plus fresh nonce-bound OIDC proof; the backend atomically revokes old/creates new credentials, never requiring another working device forever or accepting old bearer alone. Backend identity input remains an external gate if configured signed `auth_time`, nonce/login behavior or cross-audience account mapping is unverified.

Native context indicators/compaction read the reasoning `tokenBudget` delivered by GET /v1/capabilities; provider capacity and operator safe budgets are not a number inferred from the model label. Missing/unverified/unsupported estimator data blocks new reasoning but keeps typed drafts/native editors usable. Actual metered usage is backend GET /v1/usage, not a local estimated-token charge. Exact budget fields, estimator and error behavior belong to API.md; runtime budgeting and required negative tests are in AGENT-RUNTIME.md.

Typed/conversational Pebbi creation and routine management use the explicit command/draft/review interfaces in AGENT-RUNTIME.md. Home and VoiceOver expose editable native review and Save/Enable/Cancel controls; model output can prefill but never click/forge them. Setup, OAuth, browser pairing, permissions, grants, protected-effect approvals and private Save consent remain native authority. A transcribed “allow” is not allowOnce/allowForScope.

Audio encoders/decoders use API.md's reassembled-message limits: text/control/context/transcript JSON ≤256 KiB including envelope/escaping; audio.append/voice.output.audio ≤32 KiB serialized plus ≤16 KiB decoded PCM. Bound each data frame to 32 KiB and cumulative reassembly before parsing; RFC 6455 fragmentation does not enlarge the message budget. Preserve code points, no silent final-transcript truncation, reject oversized/invalid input explicitly and retain reviewable text where available. CJK/emoji/escaped and fragmented-message tests are required; scalar-count schema limits are not byte validation.

## 9. Documents, previews and OS lifecycle

Use native NSOpenPanel/NSSavePanel, UniformTypeIdentifiers, PDFKit, Quick Look and Apple Vision before extra dependencies. [DATA-MODEL](DATA-MODEL.md) owns file versions and extraction coverage; previews operate on the exact immutable artifact version selected by the user, never a live source that can change under approval.

Quick Look/PDF rendering can parse hostile files and may use OS caches. Do not promise that closing a preview purges every system cache. Offer a plain-text safe view when rendering is unavailable or risk warrants it. Do not automatically launch scripts, resolve external document macros, navigate embedded links or execute HTML attachments. Active HTML/code is previewed as text by default; browser opening is an explicit separate user action.

On sleep/lock: stop capture/audio/takeover, checkpoint agent attempts, interrupt unclosed audio owners and abandon unfinished artifact drafts; suspend scheduling. Recovery never automatically restarts audio capture or replays dictation insertion. On wake: re-evaluate permissions, network, clocks and generation; perform one routine catch-up per routine, never a backlog flood. On Quit: stop accepting ingress, mark/cancel live attempts durably, close child IPC, terminate/reap owned process groups, close streams and database. If a remote effect cannot be reconciled before bounded shutdown, persist uncertainty for next launch. Do not delay Quit indefinitely or report a terminated process as a rolled-back operation.

## 10. Required tests and real-device checks

| Test ID | Injection/action | Required observation |
|---|---|---|
| NAT-01 | Launch, close Home, menu-bar reopen, Quit | Focus rules hold; Quit leaves no app-owned helper or routine running |
| NAT-02 | Deny/revoke each TCC permission independently | Specific unavailable capability; no repeated prompts; unaffected features usable |
| NAT-03 | AX target disappears/restarts/minimizes/raises unexpectedly | Ref invalidation, no duplicate action, honest background limitation |
| NAT-04 | CGEvent takeover plus user pointer/key input, Escape and app switch | Further events stop; held synthetic keys released; no secret key logging |
| NAT-05 | Mixed Retina/non-Retina, negative-origin display, rotated/mirrored screen | Transform round-trip within one capture pixel; safe bounds; target matches before any input |
| NAT-06 | Move window or change Spaces after capture and before action | `staleTarget`/`invalidGeometry`; no event emitted |
| NAT-07 | Secure field; change dictation focus/selection; duplicate insertion result | No secret entry; review/Copy recovery; inserted exactly once or uncertainty exposed |
| NAT-08 | Stop speaking while a task writes an approved file | Playback stops; task continues and file outcome is journaled |
| NAT-09 | Remove Bluetooth microphone/output, sleep, revoke mic | Bounded buffers, no crash; no hidden recording after wake |
| NAT-10 | End capture during OCR/upload preparation; expiry; protected window | Stale handles fail; memory refs released; no raw data in DB/log export |
| NAT-11 | VoiceOver, full keyboard, Reduce Motion/Transparency, increased text size | Every control/guide available semantically; no motion-only status; no clipping |
| NAT-12 | Unsupported model deployment | Correct canonical state; no silent substitute; local UI stays responsive |
| NAT-13 | Voice with no task → same-Pebbi task → verified result context → speech stop | Separate audio owner, uninterrupted independent task, correct sourceTaskId provenance and no queued audio attempt |
| NAT-14 | Dictation while task waits + voice owns mic | Explicit voice-input end, one mic owner, no task-slot consumption; no automatic voice resume |
| NAT-15 | Locked/missing/revoked device Keychain item, wrong account/device pairing | No device-bound request with ID/bearer alone; no credential in DB/extension/logs; native recovery only |
| NAT-16 | Typed management Save/Enable; spoken “allow”; private script Save then Run | Native deliberate controls required; separate privacy Save and per-run execution approval; forged model consent rejected |

Tests must use a purpose-built accessibility fixture app as well as representative real apps; mocked AX success cannot certify arbitrary background support. Actual Apple Silicon and Intel hardware, Chrome and Brave, multiple displays and audio device switching are release evidence obligations, not claims made by this document.

Implementation reference entry points: [Accessibility](https://developer.apple.com/documentation/applicationservices/axuielement), [ScreenCaptureKit](https://developer.apple.com/documentation/screencapturekit), [AppKit](https://developer.apple.com/documentation/appkit), [AVAudioEngine](https://developer.apple.com/documentation/avfaudio/avaudioengine). Verify the exact available APIs against the pinned SDK and deployment target; newer documentation is not permission to raise the runtime minimum.
