# Connections, OAuth and MCP contract

Status: implementation specification, not an installed connector catalog. [CONTRACT](../CONTRACT.md) fixes scope; [SECURITY](SECURITY.md) owns trust policy, [TOOLS](TOOLS.md) the broker, and [API](API.md) the Pebbi service wire. Connections are local, per-account records. No backend connector-sync endpoint is added.

## Product contract

Connections supports built-in adapters and custom remote/local MCP connections. A built-in catalog is a reviewed manifest of actual adapters, not a list of provider logos implying working integrations. Each visible entry must declare identity, supported read/write operations, auth method, requested scopes, privacy/data destination, current capability snapshot and disconnect/revoke behavior. If external app registration or credentials are missing, show the item as not connected and explain the requirement; a fixture is never `ready` in production.

Connector state is exactly `disconnected`, `connecting`, `ready`, `expired`, `degraded`, `failed`. An account may have multiple explicitly named connections to the same provider; never guess which identity should send a message or receive a file. Suggestions read only user-selected connected scopes; routines use existing valid grants and still request fresh high-risk approvals.

## Local record and secret boundary

The native DATA-MODEL owns concrete tables. A connection's logical contract includes a UUID connection identity, owning account, kind (`builtIn`, `remoteMcp`, `localMcp`), display name, reviewed adapter/version, canonical state, provider account identity, granted scopes, bounded resource allowlist, permission/capability version and expiry. Local configurations may contain an exact endpoint or executable location chosen by the user; repository docs never contain personal endpoints or tokens.

SQLite holds only nonsecret metadata and Keychain references. OAuth tokens, API keys, pairing secrets and optional endpoint credentials stay in Keychain. Tool output, model context, telemetry and support export must omit them. The Pebbi backend device credential is a **separate** non-synchronizing Keychain item scoped to app/account/device; it is not an OAuth connector credential and must never be inherited by MCP children or forwarded to a connector. Pebbi enrollment authorization nonces and `enrollmentIdToken` proofs stay only in bounded attempt/request memory. The ordinary native-client-audience ID token is body-only proof for Pebbi device registration, never generic API or connector bearer authentication; the account API access token is independent. Connector authentication/`ready` state cannot establish Pebbi device authorization or recent interactive enrollment proof. Connector OAuth tokens remain local unless a specific, separately authorized server operation truly requires one; this API inventory provides no general token-upload route. Do not invent one or route native OAuth through a server just for convenience.

## State transitions and failure behavior

| From / trigger | Result | Required behavior |
| --- | --- | --- |
| `disconnected` + user chooses Connect | `connecting` | Display destination and scopes before system browser consent or local process launch. |
| Valid OAuth exchange / validated MCP handshake and capability snapshot | `ready` | Confirm actual authenticated provider identity and supported read operation; config parsing alone is insufficient. |
| Consent cancelled or denied | `disconnected` | Delete one-time OAuth state/verifier and provisional secret; do not keep retrying. |
| Expired/revoked credential | `expired` | Single-flight documented refresh if possible; otherwise reconnect. No repeated background login windows. |
| Valid auth but partial/provider-limited capability | `degraded` | Advertise only verified working capabilities; fail affected tools without guessing a replacement connection. |
| Invalid endpoint, malicious schema, protocol failure or unrecoverable auth error | `failed` | Safe reason, bounded retry only if appropriate; quarantine changed capability manifests. |
| User disconnects from any state | `disconnected` | Cancel in-flight work, revoke local grants and server credential where provider supports it, clear Keychain secret and stop owned child process. |
| App Quit / account sign-out | Transport closed | Stop processes and revoke ephemeral leases. Persist credential only according to sign-out choice, never continue routine execution. On next open revalidate before `ready`. |

A failed/revoked tool places its task in `waitingForConnection` when reconnect is actionable, or `failed` with evidence when not. Do not display “working” while silently polling forever. Connection state is not a task state.

## OAuth flow for built-in and remote connections

Use the provider's current documented OAuth method. Native public-client adapters use authorization code + PKCE `S256`, system browser, exact registered redirect, one-time state and short-lived verifier. Request only the scopes needed for the selected connector features; read-only setup is the default, write scopes require explicit explanation and consent. A client-secret-only provider is not made safe by embedding its secret in the app: it needs an explicitly designed authorized backend component or remains unavailable.

Validate discovery issuer, protected resource/audience, origin, redirect URI and token endpoint. Do not take OAuth configuration directly from untrusted MCP prose. Verify authenticated account after exchange; show it before connection completion. Do not automatically reuse a token against a different server/audience even if its hostname looks related. Tokens never travel in URL query strings. Refresh once through a per-connection lock and atomically rotate stored material; invalid_grant becomes `expired`, not a silent new account login.

Consent UI is not authorization to invoke every tool. Actual calls still need registered tool schemas, capability checks, bounded resources and the required action preview. Disconnect stops local access immediately; if remote revocation is offline/unsupported, clearly distinguish local removal from unconfirmed provider revocation and link to the provider's account controls.

## Remote MCP

Prefer MCP Streamable HTTP for new supported integrations. Pin an actual compatible protocol/SDK revision during implementation; no made-up revision is a requirement. Use the documented initialization handshake, verify negotiated protocol version and server identity, send the initialized notification, then discover bounded `tools/list` capability pages. Record a digest/version of tool definitions before any call. Older transports are supported only by an explicitly tested adapter, never silently switched to bypass auth.

- HTTPS only by default; optional localhost/LAN connections require separate explicit type/host/port approval and the SSRF controls in SECURITY.
- Apply auth to the configured resource only. Do not forward app Entra access tokens, `X-Pebbi-Device-Token`, enrollment ID-token proofs, authorization nonces or audio-session tokens to an MCP server. Discovery/redirects obey issuer/origin/resource validation, bounded retries and no cross-origin credential forwarding.
- For Streamable HTTP, preserve only a server-issued session identifier after authenticated initialization; bind it to the connection and supported protocol. Session identifiers are not standalone authorization and cannot be reused across accounts/servers. Handle server restarts/session expiry by reinitializing; do not replay tool calls automatically.
- Every tool call uses a bounded JSON-RPC ID associated with the immutable local `toolCallId`, timeout, cancellation token and tool schema version. Accept responses only for pending calls. Unexpected IDs, invalid JSON-RPC or conflicting duplicate responses fail the connection safely.
- Enforce message ≤1 MiB, tool arguments ≤64 KiB, at most 200 discovered tools, schema nesting at most 32 levels and bounded pagination; expose only the user-approved subset to the model. Restrict remote JSON Schema refs/recursion. Never render tool descriptions as privileged instructions.
- Capability/schema/tool-name change invalidates relevant persistent grants. New destructive or outbound tools remain unavailable until reviewed. Names are namespaced by connection UUID so one server cannot shadow a built-in trusted tool.
- MCP cancellation is best-effort, not proof an external action was undone. Unknown write outcome must be reconciled against the exact target before retry; read requests may retry once only if their adapter classifies them as safe and the deadline permits.
- MCP protocol features that request sampling, elicitation, roots, resources or command execution do not acquire authority automatically. Default deny unimplemented/server-initiated features. Elicitation requiring secrets or payment goes to the user, not model context; sampling consumes a new approved local model budget and cannot choose another model/provider. Where reasoning is used it requires the delivered compatible `tokenBudget` and current ID; a connector cannot invent missing provider capacity, estimator support or safe input limits.

## Local MCP processes

Local MCP is not an OS sandbox. Explain that a selected executable runs as the logged-in user. Use the app's reviewed catalog or an explicit user-selected absolute executable and argument vector; no model-provided shell string, `curl | sh`, automatic package install or hidden sudo. Display executable/source, arguments, workspace, expected network use and requested environment references before launch.

Spawn directly with a minimal allowlisted environment. Resolve Keychain references only at launch and pass only that connector's required secret material through a supported protected channel; never inherit the whole process environment or all OAuth tokens. Do not put secrets in process arguments. Fix working directory to an approved workspace. Close stdin/terminate the owned process group on disconnect, cancellation when supported, account switch and Quit; enforce bounded shutdown and kill only children Pebbi owns. No LaunchDaemon, login item or process that intentionally outlives Quit.

Use documented stdio framing and negotiated protocol; cap stdout/stderr and sanitize diagnostics. Tool output is inert text/data, not shell code. If the executable changes, loses trust or needs new privileges, invalidate readiness and standing grants before relaunch. Code signing/hash checks are integrity signals, not evidence that arbitrary code is harmless.

## Built-in adapter acceptance contract

An adapter is production-available only after all these hold:

1. Real provider registration and scopes are authorized, with actual sign-in, authenticated identity read-back and revocation/refresh tested.
2. Every advertised tool has a closed input schema, read/write risk classification, bounded resource mapping, cancellation/timeout policy and exact-target verifier.
3. Outbound messages, publishing, purchases, credentials and destructive bulk actions require fresh preview/approval; idempotent provider operation IDs are used where supported. Missing provider idempotency means unknown-outcome reconciliation, not blind replay.
4. Pagination/count assertions are validated; export/search does not claim completeness from one truncated page. Rates/backoff follow provider limits without background retry floods.
5. Connection failure/revocation/scope change while a task is queued or awaiting approval is exercised. Pending approval cannot dispatch under the old account or schema.
6. Consent, signed-in provider identity, scopes and disconnect controls are available through native accessible Settings/Connections UI. No implementation may satisfy the catalog requirement with a nonfunctional placeholder and call it live.

## Required connection tests

Test malicious discovery URLs, DNS rebinding, cross-origin redirects, private address encodings, forged JSON-RPC IDs, tool-description injection, schema expansion, unknown server features, missing OAuth verifier, callback replay, conflicting account identities, refresh races, scope removal, duplicate writes, cancel during write, local process exit/output flood and Quit termination. Verify connector processes, outbound headers, tool context and diagnostic exports never receive Pebbi device/enrollment/audio-session credentials; disconnect/reconnect cannot mint a replacement Pebbi device from a stale account bearer. Live connector tests and deterministic fixtures must be reported separately. Domain selection, a configured endpoint and a successful initialization are not a complete end-to-end connector pass.
