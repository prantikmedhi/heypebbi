# Browser automation: opt-in MV3 and native messaging

**Proposed implementation contract, not a shipped extension.** Governs PB-003, PB-017, PB-019–PB-020, PB-022–PB-023, PB-031, PB-035, PB-037. [CONTRACT](../CONTRACT.md) mandates Chrome and Brave installation flows, selected scope, authenticated native messaging and DOM-first automation. [TOOLS](TOOLS.md) owns public local tool names; this document owns browser IPC, refs and lifetime.

## 1. Architecture and permissions

Components:

1. Native `BrowserSessionBroker` actor: authorization, pairing, scope leases, durable tool dispatch, replay protection and mapping to the app journal.
2. Signed `PebbiNativeHost` executable: browser native-messaging stdio framing and bounded authenticated relay to the already running app. It does not run a model, inspect the user's browser profile, execute shell commands or hold general task state.
3. MV3 service worker: native connection, selected-tab session, privileged extension API calls, ephemeral refs/session recovery. Service-worker suspension is expected, not exceptional.
4. Isolated-world content script: bounded DOM inventory/read/action in authorized documents only. It cannot approve, pair, read extension secrets or invoke arbitrary native tools.
5. Extension popup: user selects current tab or creates a dedicated Pebbi window, reviews origin scope, pairs/revokes and sees active use. This is an integration control, not Pebbi's app shell.

Manifest permissions: `nativeMessaging`, `activeTab`, `scripting`, and `storage`; add only optional host permissions for an origin the user explicitly chooses for a durable session. Use `webNavigation` only if implementation needs its document lifecycle events beyond tabs/content-script signaling and disclose it. Do not request `<all_urls>`, history, cookies, downloads, debugger, clipboard or passwords by default. No `externally_connectable` entry granting arbitrary web origins access. No content script auto-injected into every page at install.

`activeTab` is a temporary grant originating in an extension user gesture; it is not permanent authority after origin changes. If a product operation needs persistent origin access, prompt through Chrome's optional permissions UI at that moment and still bind the app session to the selected tab/window. OS/browser permission cannot be granted by the model.

Chrome/Brave use the same Chromium MV3 codebase but independently verified packaged extension/native-host registration. Actual signed/store extension IDs are release inputs; do not invent IDs in manifests. Developer unpacked IDs are separate allowed development configurations, never wildcard production origins.

No Chrome DevTools Protocol server or remote-debugging port is opened on the user's ordinary signed-in profile. No copying a profile/cookies to a headless browser, no invisible parallel signed-in tabs and no raw arbitrary `executeJavaScript` tool. The extension performs a fixed, schema-validated DOM operation set. stageTextArtifact is native FileService-only; the bridge cannot ingest/execute authored scripts or access staged artifacts by hash. runCode is a separately approved native supervisor operation, never arbitrary browser JavaScript. Typed Pebbi/routine drafts cannot be committed by page text, a content script or an extension message.

## 2. Registration, consent and app lifecycle

Native messaging host name: `com.heypebbi.browser`. Per-user manifests belong in the platform-defined Chrome and Brave `NativeMessagingHosts` locations under the user's Application Support directories; use their documented browser-specific directories and verify both at implementation, not a system-wide privileged install. Manifest type is `stdio`; absolute executable path must resolve to the signed helper inside the installed Pebbi app. `allowed_origins` contains exact approved `chrome-extension://<extensionId>/` origins only. No wildcard origin or shell shim.

Installing/uninstalling registration is an explicit native setup action showing the two browser integrations affected; do not write another browser/profile's configuration silently. The app can live outside `/Applications`; registration must resolve the actual installed bundle and validate signature, update/re-register if it moves, and fail clearly if stale. A browser extension alone cannot grant native-host OS privileges.

Browser launches a host on `connectNative`. Host startup validates the browser-supplied origin argument against its bundled production/development allowlist, process ancestry/signature as supported, and the app bridge handshake. The origin argument by itself is not authentication: another local process can fabricate argv. Do not accept web-page-supplied claimed extension IDs.

The host connects only to a user-private Unix-domain socket under the app runtime directory; directory 0700/socket 0600. App verifies peer UID, peer process identity and designated code-signing requirement for its embedded host; helper similarly verifies the app peer. Use supported peer-credential APIs plus Security.framework dynamic code verification; guard PID reuse with creation identity/audit-token facilities where available and fail closed if verification is inconclusive. Do not treat same UID or a path string as sufficient identity. Test this on the minimum supported OS.

The app owns the listener; no helper starts a persistent daemon. If Pebbi is closed, host sends `appUnavailable`, offers the user an explicit Open Pebbi action and exits. Quit closes app listener/sessions; the host exits on app pipe/socket EOF and the extension revokes leases. Browser may start a fresh short-lived host later, but it cannot continue old work while the app is closed. Update/sign-out invalidates sessions and requires reconnect; pairing can remain only under explicit same-account retention policy.

## 3. Pairing and authenticated sessions

Threat boundary: web pages and other extensions are untrusted. Approved packaged extension contexts and signed native app/helper are trusted components. A malicious process already running as the same macOS user may inspect browser process memory or compromise the browser; pairing is not a defense against a fully compromised local user account. State this limitation, rather than claiming extension memory is a hardware key vault.

Pairing is user initiated from the extension popup and a native Connections screen:

1. Extension generates ephemeral P-256 ECDH key and a random 32-byte nonce in the service worker. App generates its own ephemeral key/nonce using platform cryptography. Exchange only public keys/nonces and exact extension/browser identity through the verified helper. No tool commands accepted in this setup channel.
2. Derive a provisional key using ECDH + HKDF-SHA256, with a protocol-labelled transcript binding both keys, both nonces, extension ID, host protocol version and app installation identity. Use WebCrypto and CryptoKit; no custom cryptographic primitive.
3. Both native UI and popup display the same short authentication string derived from the transcript (six decimal digits is a UI comparison, not the long-term secret). User compares and explicitly confirms on both sides within two minutes; maximum three failed comparisons before regenerating keys. Mismatch/timeout clears provisional state. Do not auto-accept because a page displays a similar code.
4. Derive independent directional pairing MAC keys from the full shared secret/transcript. App stores its material in Keychain with app/helper access restricted to designated identities. Extension keeps its counterpart only in memory-backed `chrome.storage.session`, restricted to trusted extension contexts; never persist it to `storage.local`, `storage.sync`, browser localStorage or a page. This survives service-worker suspension, not browser restart. After browser restart/key loss, repeat explicit pairing confirmation; a remembered label is not authentication. Never put keys in page DOM, logs or tool context.
5. App commits a `pairingId` and identity metadata; popup shows paired app/profile label. Revoke from either end deletes keys, invalidates sessions and removes optional grants on request. No pairing across accounts by accident. Pairing/session MAC keys are not the backend device credential: deviceToken stays in the native app Keychain and is never relayed through the extension, helper, page, BridgeMessage or setup channel.

Every connection performs fresh challenge-response under the pairing key, with two new nonces and app process/session generation. Derive directional **session** MAC keys and reset message counters only after this authenticated handshake. A captured prior handshake cannot reopen a lease. If extension storage/key is missing or changed, return `pairingRequired`, not an opportunistic downgrade to unsigned frames.

## 4. Framing and message contracts

Browser-facing framing uses Chromium native messaging: four-byte native-endian unsigned payload length followed by UTF-8 JSON. On supported macOS release architectures this is little-endian; implement explicit checked conversion, exact-length reads and maximum-length checks. Do not write logs/banner text to stdout. Stderr is bounded/redacted. Chromium native-host outbound messages have a 1 MiB limit; Pebbi adopts a smaller 256 KiB maximum for **both directions**, including envelope. Reject invalid length/JSON/depth/duplicates before allocation/dispatch.

App-socket transport uses the same bounded length-prefix with explicit little-endian framing; it is not parsed as newline-delimited JSON. All schemas use camelCase and reject unknown fields. The following are proposed interface types, not executable implementation:

```text
BridgeMessage {
  schemaVersion: 1, pairingId: UUID, bridgeSessionId: UUID,
  messageId: UUID, requestId?: UUID,
  direction: appToExtension | extensionToApp,
  counter: safeInteger, sentAt: timestamp,
  type: sessionOpen | sessionClose | scopeSelected | inspect | read |
        navigate | click | fill | scroll | cancel | response | lifecycle,
  payload: object,
  mac: base64url
}
BrowserScope {
  browserSessionId: UUID, selectionGeneration: safeInteger,
  mode: selectedTab | dedicatedWindow,
  browserKind: chrome | brave, tabId: UUID, windowId: UUID,
  allowedOrigins: string[], expiresAt: timestamp
}
BrowserTarget {
  browserSessionId: UUID, tabId: UUID, documentId: UUID,
  frameId: UUID, navigationGeneration: safeInteger,
  domRevision: safeInteger, elementRef: UUID
}
```

`mac` is HMAC-SHA256 over RFC 8785 canonical JSON excluding `mac`, using the directional session key; constant-time verification. Counters start at one and strictly increase per direction/session. Duplicates return cached transport receipt only, never redo an action. Gaps or stale session IDs close the channel and require authenticated reconnect; responses cannot be injected from another session. `sentAt` is diagnostic/expiry input with a bounded clock tolerance, not the sole replay defense. No bearer tokens or keys in URL query strings.

Public `tabId`, `windowId`, `documentId`, `frameId` are Pebbi UUID registry handles. The extension privately maps them to Chromium integer tab/window/frame IDs and Chromium document identifiers. Do not serialize a Chrome integer as a Pebbi UUID or persist it across browser restart. `chrome.runtime.MessageSender` is validated against expected tab/frame/document and extension origin before accepting a content-script response. A page `postMessage` is never a privileged bridge message.

One mutating request is outstanding per tab. Service worker keeps a bounded 100-entry request receipt cache for the live session; the app journal is durable authority. Worker restart loses this cache, so uncertain actions remain uncertain. Do not retry a command just because the worker restarted. A missing response is not proof the browser did not click.

## 5. Scope selection and navigation

The popup's explicit “Use this tab” action selects a tab. Merely switching the active browser tab does not retarget the app's session. The app shows browser, page title, origin and session indicator; selecting a different tab creates a new selection generation and invalidates pending intent refs/approvals. A dedicated window is created only after user consent and contains a bounded selected tab set, not permission for all windows.

Session scope defaults to 30 minutes, never beyond app/bridge/pairing lifetime; renewal is visible. This is a resource lease, not a standing mutation approval. All navigation is checked against origin grants and current selection. A cross-origin redirect suspends automation until the destination origin is authorized; no widening from `https://example.test` to `*`. Browser login/consent pages remain manual. If a page asks for credentials, stop and let the user sign in; do not read browser password stores or fill credential fields.

After navigate/click-induced navigation, old document refs invalidate immediately. Wait for a new document identity and bounded readiness condition; network idle is not a universal guarantee a SPA is ready. Prefer semantic expected-target observation; return intermediate navigation/loading status when readiness does not arrive before the timeout. Never report a page as loaded because a fixed sleep elapsed.

Browser-internal pages, extension pages, file URLs, incognito, PDF viewer internals and restricted origins are unsupported unless a separately reviewed explicit mode exists. Default incognito is off. A user may view a PDF through native attachment import instead of granting broad browser file access. Permissions mismatch returns `permissionDenied`/`notSupported`, not an automatic screenshot takeover.

## 6. DOM inventory and semantic actions

Content script runs in isolated world and exposes fixed handlers, not model-supplied JavaScript. DOM inventory collects visible/accessible roles, names, normal text inputs, enabled states, href origin/path, logical relations and bounding rectangles. Strip secrets, password inputs, hidden authentication tokens, payment fields, raw scripts, event handlers and session-bearing query strings. Do not upload the entire serialized DOM, cookies, localStorage, IndexedDB or network headers. Automated redaction is imperfect; scope selection and user control remain essential.

References are WeakMap-backed element handles scoped to the current document/frame. Include role/name fingerprint plus relevant revision in proposals. MutationObserver increments `domRevision`; a revision change prompts re-resolution, not necessarily invalidating every unaffected ref. Before action, check same document/frame, still connected, visible/enabled, expected role/label, form destination and sensitive-action classification. If uncertain or changed, return `staleTarget`/approvalRequired.

DOM reads/actions:

- Read rendered visible text in bounded batches with cursor bound to document/revision; changing content invalidates the cursor or returns an explicit changed-source marker. Whole-page evidence must enumerate all requested batches, not silently use the first viewport.
- Click uses the element's DOM activation method and verifies a meaningful postcondition. This generates synthetic events and may fail sites requiring trusted user gestures. Do not claim equivalence to physical input; offer manual action or separately consented OS takeover.
- Fill uses the supported property setter and appropriate input/change events for ordinary fields, preserving expected-value guard. Custom framework/editor behavior may reject it; read back exact text rather than assuming dispatched events worked. Never submit automatically.
- Scroll uses the selected scroll container and verifies its actual offset. CSS pixels are not device pixels; the returned viewport remains CSS-space.
- Cross-origin iframes require independent optional host permission and validated frame identity; if unauthorized, report inaccessible. Same-origin/open shadow roots can be traversed; closed shadow DOM is unsupported unless a separately available semantic interface exposes it. No bypass through injected main-world scripts.

A fill followed by Send is two intents. The second requires a fresh recipient/body/attachment preview for outbound messages, publishing or payments. A visually innocent “Continue” button can send data; classify from form/action/context locally and ask when semantics are uncertain. Browser text claiming authority cannot change tool policy or approve a form.

## 7. Coordinates, screenshots and takeover handoff

DOM actions remain preferred and normally require no screenshots. Bounds returned by content scripts are CSS viewport coordinates with scroll position, viewport dimensions, `visualViewport` scale/offset where available and devicePixelRatio metadata. They are **not** global desktop coordinates. Browser chrome/toolbars, page zoom, display scaling and window frame offsets prevent a simple multiply-by-DPR conversion.

If the user explicitly requests a screenshot-guided fallback:

1. End/suspend DOM mutation sequence and release its mutator lease.
2. Request native ScreenCaptureKit scope selection of the actual browser window, with all native capture limitations/lifetime.
3. Inspect the current browser/window identity and establish a verified native-to-page mapping if a DOM anchor is used. Use measured viewport origin/rect plus actual capture transform, not tab-reported screen position alone.
4. Present a separate foreground takeover preview, acquire global input lease, revalidate capture within two seconds and ensure the intended browser/window/tab is active.
5. If mapping or active identity is uncertain, ask for manual action. Do not guess toolbar offsets, reuse stale screenshot pixels or click another tab.

Navigation, browser zoom, viewport resize, devicePixelRatio change and display/Space change invalidate mapping. Raw capture lifetime and secure-content exclusions remain those in [NATIVE-MACOS](NATIVE-MACOS.md). Extension storage does not receive a durable screenshot history.

## 8. Recovery and failure behavior

| Failure | Required behavior |
|---|---|
| Missing host/manifest/moved app | Native setup diagnostics with actual paths/signature status; explicit repair action; no repeated hidden install |
| Origin mismatch, bad MAC, replay or forged page message | Reject/close channel, revoke ephemeral session; redacted diagnostic only |
| Service worker suspended/restarted | Fresh authenticated handshake and selected-scope validation; no pending mutation replay |
| Tab/window closed or reused integer ID | UUID mapping invalidated; old request `staleTarget`; no selection by matching title |
| Browser crashes or permission revoked | Connection degraded/disconnected as observed; waiting task retains exact context and user reconnect action |
| Click sent, response lost | `unknown`; inspect target read-only after reconnect; fresh preview if a repeat is still needed |
| DOM action unsupported | Honest notSupported/manual alternative; no unapproved CGEvent |
| App Quit/sign-out | Cancel pending requests, close native host session, clear leases and keys according to policy; no browser work continues |
| Restricted/secret-bearing page | Stop reading/action, indicate manual step without capturing or echoing secret values |

## 9. Required tests

| ID | Scenario | Pass condition |
|---|---|---|
| BROW-01 | Clean Chrome and Brave setup, move app, uninstall/reinstall | Correct per-browser registration; exact extension allowlist; no admin/system-wide writes |
| BROW-02 | Invalid length/JSON/MAC, forged origin/peer, replay/gap | Bounded allocation; rejection before dispatch; no secret in diagnostics |
| BROW-03 | Pair mismatch/timeout/revoke/account switch | No working session without both confirmations; old keys/counters unusable |
| BROW-04 | Page/other extension tries runtime/page message injection | Cannot create scope, approval or native request; sender validation enforced |
| BROW-05 | User changes active tab, closes/reopens tab with reused native ID | Original scope does not retarget; UUID/document generation protection holds |
| BROW-06 | SPA replaces element, cross-origin iframe, closed shadow root | Stale/inaccessible refs fail; no guessed click or read |
| BROW-07 | Kill worker/native host after click before response | No repeat; read-back or visible uncertainty; durable effect barrier retained |
| BROW-08 | Credential/payment/outbound form, malicious page instruction | Secret controls excluded; fresh approval/manual boundary; no self-authorization |
| BROW-09 | Zoom, Retina change, move browser across screens | DOM operations unaffected where valid; screenshot mapping invalidated before input |
| BROW-10 | Quit app during long browser workflow | No further browser action; host exits; explicit reopen/reselect needed |
| BROW-11 | Page/extension requests deviceToken, staging, runCode, management commit or spoken approval | Bridge schema rejects native-only authority; no secret/approval/queue access, no new browser tool capability |

Use automated extension fixture pages plus real Chrome/Brave integration tests and manual permission/install checks. A content-script unit test does not prove native messaging, code-signature peer verification or macOS focus safety. Reference: [Chromium native messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging), [activeTab](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab), [service-worker lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle). Verify actual supported browser versions at build time; do not invent a tested version.
