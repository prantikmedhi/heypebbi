# Pebbi — components and state semantics

Normative styling comes from [DESIGN.md](../../DESIGN.md); canonical state strings come from [CONTRACT](../CONTRACT.md). Screens: [SCREENS](SCREENS.md). The static [brand board](brand-board.html) is a reference composition, not functioning software.

## Native component contract

SwiftUI/AppKit own semantics, focus, text selection, menus, sheets, traffic lights, resizing and accessibility. Do not replace native text entry with canvas, snapshots or WebViews. Brand styling changes material and composition, not expected macOS behavior. Nominal sizes are points; all text-bearing components grow vertically with text scale.

| Component | Anatomy and treatment | Interaction / state / accessible behavior |
|---|---|---|
| App sidebar | Labeled destinations in canonical order; selected row uses sea-glass + ink and a leading selection glyph | Selected is distinct from keyboard focus; unread badge also has an accessible count; no color-only navigation |
| Home shelf | One large named Pebbi, its job, shortcut hint and a short invitation; modest colored workspace objects | Decorative mascot excluded from AX; paired name is text; no endless idle animation; task content begins immediately below |
| Pebbi tile | Appearance, name, job, task-state summary and context menu; opaque sea-glass/lilac/clay/butter face plate | Name, not appearance, identifies the assistant; selected tile has check + border; appearance cannot hide waiting approval |
| Task row | Task title, owning Pebbi, exact status, last verified step, start/update time, contextual controls | Activity title remains stable; no fabricated percentage; keyboard expands to event detail; Cancel task stays available when applicable |
| Conversation row | Title, Pebbi, readable excerpt, unread indicator, pin glyph, timestamp | Archive and pin are discoverable in menu; unread is semantically announced; a pinned conversation is not a running task |
| Transcript | Continuous reading plane, speaker labels, selectable text, linked sources and output attachments | Streaming paragraphs remain stable; VoiceOver announces bounded chunks, not each token; follow-live has an opt-out; history loading preserves position |
| Composer | Multiline native text field, explicit attachment, voice and send actions; current capture scope above input | Return/send behavior disclosed; Shift-Return adds line break; unconfigured voice action is disabled with a readable explanation and typing stays available |
| Perch | Compact Pebbi silhouette, subsystem icon + label, expand and stop affordances when relevant | Never depends on hover; expands on explicit activation; keyboard equivalent via menu bar and shortcut; no focus theft for status updates |
| Voice capsule | Mic icon, state label, duration only when measured, input/output device and Stop speaking when relevant | Waveform requires real audio; never show a fabricated live waveform while unavailable; interruption is separate from task cancellation |
| Dictation tray | Target application/field summary, capture control, selectable transcript, Insert and Cancel | Target change invalidates insertion readiness; reviewing is not completed; explicit focus recheck before insertion; transcript retained on insert failure |
| Scope strip | Capture icon, exact selected window/tab/app and Stop sharing | Always visible during capture/control, even when inspector closes; sensitive field redaction or blocking has a text explanation |
| Approval sheet | Requesting Pebbi, action verb, app/connector, bounded resource, exact preview, consequence and scope/expiry | Default focus on explanation or Deny, never the destructive action; preview scrolls but action row stays visible; Escape denies/dismisses without implicit permission |
| Task inspector | Current task, event timeline, linked outputs, approvals and stop/retry controls | Event rows distinguish requested, attempted and verified; timestamps and attempt identifiers are selectable; newest events do not steal focus |
| Guided pointer | Narrow outline, anchored text bubble, current step, Pause / Resume / Exit | No full-screen animation; target missing becomes a recoverable paused view; keyboard-accessible equivalent instructions remain in Home |
| Capture picker | Native-compatible thumbnail list with window/app names and a single explicit selection | Not preselected to all displays; share begins only after confirmation; unavailable/sensitive windows are explained rather than silently skipped |
| Connection row | Service name in text, connection state, scope summary, last check if known, Manage | No copied service logos are needed for initial design; provider identity and destination are visible before system-browser OAuth |
| Suggestion slip | Proposed action, reason, evidence and bounded scope; butter note with no busy indicator | Read-only until explicit approved execution; dismiss is easy; proposal never animates as if work already started |
| Routine card | Name, owner Pebbi, schedule/timezone, next eligible local run, state and recent outcomes | Must say “Runs while Pebbi is open”; paused/blocked/archived are text states; catch-up count never implies a backlog flood |
| File row | Filename, type, workspace-relative location, source task and preview affordance | External paths carry a scope boundary label; long path has middle truncation only with full copyable/accessibility text |
| Error panel | What failed, what was confirmed, what remains, retry or alternate path, disclosure for redacted details | Opaque neutral plane, danger icon/text; no giant sad mascot, animation or generic “Oops”; never erase partial output |
| Empty state | Small grounded illustration, literal explanation and one useful action | True empty and failed-to-load are different; never populate a real user list with sample tasks or fake Pebbis |
| Notice | Icon, short title, action, dismiss if noncritical; warm surface with readable border | Not the only location of an approval, capture warning or failure; critical content remains in the relevant record |
| Plan comparison | Nest, Studio, Constellation in aligned rows; exact server-fed price/currency/period/limits | Unconfigured prices say “Pricing unavailable”; no invented discount, recommended badge or checked entitlement |

## Control-state matrix

The following applies to buttons, row actions, chips, disclosures and fields. Native controls may have platform-specific decoration while keeping these semantics.

| State | Visual response | Input and accessibility |
|---|---|---|
| Default | Opaque fill, legible label, meaningful outline on a neutral plane | Labeled role; compact target at least 28 × 28, major/stop/approval target 44 × 44 |
| Hover | Darker action fill or a native row highlight; tooltip only for secondary clarification | Never reveals the sole route to a required action; no layout movement |
| Pressed | Immediate tint/one-point ledge compression; high-risk controls never bounce | Commit on release within bounds; dragging out cancels; no delay to accommodate animation |
| Keyboard focus | Two-point contrasting outer ring with two-point surface-colored gap | Full Keyboard Access works; ring independent of hover/selection; focus survives async updates |
| Selected | Check/selection glyph plus fill and accessible selected value | Group relationship conveyed; selectable chips are not confused with status chips |
| Busy | Small progress glyph + explicit action/state label; preserve width where possible | Repeated submission disabled only for that action; Cancel or applicable stop remains reachable |
| Disabled | Readable muted token text, native unavailable appearance and no press ledge | Reason is in helper text or an enabled explanation control; disabled controls are not the only path to recovery |
| Invalid | Danger icon + inline specific error; retain entered text | Error linked to field; announce once after validation; focus first invalid field after attempted submit |
| Read-only | Normal reading contrast and selectable content; no editable affordance | Accessible read-only trait; Copy can remain enabled |

Primary action light states use `button-primary`, `button-primary-hover`, `button-primary-pressed`; dark action uses `button-primary-dark`, with native pressed overlay only if contrast remains compliant. The dark secondary uses a raised neutral plate and sea-glass text. A focus ring on pastel fill uses a neutral gap so the ring never disappears into a same-colored fill. Destructive styling always includes an explicit verb. Text links are underlined in prose; navigation labels need selection semantics rather than universal underlines.

## Task axis — exact strings, no invented task lifecycle

Task appearance must be derived from verified events, not the voice pose. Retry creates a new attempt; terminal results cannot turn back into running for that same attempt. An interrupted attempt is visibly unresolved until reconciliation. All states use a literal status label in the inspector; compact labels below are human-readable mappings only.

| Canonical state | UI label | Glyph / material / Pebbi pose | Available primary affordance |
|---|---|---|---|
| `queued` | Queued | Stacked-line glyph; neutral tray; idle face | Inspect queue; cancel queued task |
| `running` | Running | Activity track; sea-glass tag; intent eyes | Inspect verified steps; Cancel task |
| `waitingForApproval` | Approval needed | Hand/shield glyph; butter slip; level attentive face | Review request; Deny is equally discoverable |
| `waitingForInput` | Your input needed | Reply glyph; lilac tag; attentive face | Open exact question; provide input or cancel |
| `waitingForConnection` | Connection needed | Broken-link glyph; butter tag; neutral concerned face | Open named connection; cancel |
| `cancelling` | Cancelling | Stop-square and bounded native busy indicator; neutral pose | Inspect; no false promise that already-triggered side effects were undone |
| `cancelled` | Cancelled | Stop-square with static label; neutral plate | Inspect retained outputs; start a new attempt if requested |
| `succeeded` | Completed | Check glyph; sea-glass tag; one small smiling settle | Open verified output; exact state remains `succeeded` in data |
| `failed` | Failed | Error glyph; danger text on neutral tray; concerned face | Read last confirmed step; retry as a new attempt if safe |
| `interrupted` | Interrupted | Broken progress line; butter tag; paused face | Review/reconcile before retry; never silent replay |

A task progress meter is indeterminate unless the denominator is known and meaningful. Multi-step count is labeled “verified steps,” not percent complete. Concurrent task rows retain owner and task identity; a combined count does not replace per-task cancellation and approvals. A follow-up has a visible queue/attachment destination rather than silently mutating another in-flight task.

## Voice axis — independent of task execution

| Canonical state | Visual + copy | User control / mascot |
|---|---|---|
| `idle` | Mic off glyph, Ready to talk only when capability is genuinely ready | Start voice / type; still smiling Pebbi |
| `connecting` | Link-progress icon, Connecting voice | Cancel connection attempt; attentive pose, no audio waveform |
| `listening` | Mic-on icon, Listening, persistent device/scope disclosure | End voice; measured waveform if available; listening pose |
| `thinking` | Processing icon, Thinking | Stop speaking is not misleadingly shown before speech; interrupt session as supported; glance-up pose |
| `speaking` | Speaker icon, Speaking; synchronized transcript | Stop speaking; speaking pose follows actual output energy, no mandatory sound |
| `interrupted` | Speaker-stop icon, Speech interrupted | Continue by typing or speaking; static paused pose; tasks continue unless separately cancelled |
| `unavailable` | Slashed mic, Voice unavailable; exact configuration/provider reason | Type instead / open device or connection settings; quiet neutral pose |
| `failed` | Error icon, Voice failed; preserve transcript | Retry voice / type; concerned pose; never replace with a working fixture |

`idle` is not permission to open the mic in the background. Start/control behavior follows the product flow and consent. A provider outage cannot look like listening. The contract's unresolved realtime deployment remains unavailable in real builds until a successful live check; pictured listening on the brand board is explicitly labeled a design reference, not proof.

## Dictation axis — separate transcript and insertion truth

| Canonical state | UI label / material | Required visible fact and next action |
|---|---|---|
| `idle` | Dictation ready / neutral | Show intended target if known; start capture only on explicit action |
| `capturing` | Capturing / clay mic tile | Mic active, elapsed capture if measured, selected device; Stop capture and Cancel |
| `transcribing` | Transcribing / neutral busy | Audio capture stopped; transcript may be partial; Cancel remains reachable |
| `reviewing` | Review dictation / lilac header | Full editable transcript and original target; Insert and Cancel |
| `inserting` | Inserting / neutral busy | Current verified target app/field; prevent duplicate insertion while pending |
| `completed` | Inserted / check + sea-glass | Only after confirmed insertion; identify destination; keep copyable transcript |
| `cancelled` | Dictation cancelled / stop glyph | No insertion claim; handling of captured content follows retention settings |
| `failed` | Dictation failed / danger icon | Distinguish capture, transcription and insertion failure; preserve recoverable transcript; offer Copy without claiming insertion |

If focus changes, stay/revert to `reviewing` with “Target changed—choose where to insert.” Do not silently type into the newly focused app or claim completion after mere clipboard write. Mic indicator, transcript and insertion state remain understandable without animation.

## Connection and routine axes

| Axis / canonical state | Label and visual | Required action/context |
|---|---|---|
| Connection `disconnected` | Disconnected, broken-link icon, neutral | Connect; show scopes before OAuth or local launch |
| Connection `connecting` | Connecting, bounded busy glyph | Cancel; system-browser return guidance; no “Connected” confetti |
| Connection `ready` | Connected, check + sea-glass | Manage/revoke; scope summary; readiness must be verified |
| Connection `expired` | Sign in again, clock-link + butter | Reauthorize; describe blocked dependent tasks |
| Connection `degraded` | Limited connection, partial-link + butter | Explain specifically which operation is unavailable; no universal success check |
| Connection `failed` | Connection failed, error glyph | Redacted reason, retry/test; preserve configuration |
| Routine `active` | Active, clock + sea-glass | Next eligible local run and “while Pebbi is open”; Pause |
| Routine `paused` | Paused, pause glyph + neutral | Resume; distinguish from app sleeping |
| Routine `blocked` | Blocked, lock/link + butter | Resolve exact permission/connection/input; no busy animation |
| Routine `archived` | Archived, archive glyph + neutral | Read retained history; restore only if supported by product flow |

These tables cover all canonical state values. No animation, color or human-readable label changes the machine vocabulary.

## Approval, stop and takeover grammar

- `allowOnce` → **Allow once**. Always show the exact upcoming action. `allowForScope` → **Allow for this scope**, only for eligible low-risk operations and with bounded resource + expiry. `deny` → **Deny**.
- Fresh previews and approvals are mandatory for payments, credentials, destructive bulk actions, publishing and outbound messages. Never offer scope-wide authorization for these classes. Passwords and secrets are not displayed in previews or stored in illustration samples.
- **Stop speaking**, **Stop sharing**, **Pause walkthrough**, **Cancel dictation** and **Cancel task** have separate labels and semantics. “Stop” alone is acceptable only when adjacent context makes the exact operation unmistakable and the accessibility name remains specific.
- Native semantic desktop action must name its target app. Foreground CGEvent takeover uses an unmistakable opaque butter banner: “Pebbi will control the foreground pointer and keyboard.” Preview scope, action and explicit takeover approval; provide a persistent stop path that is not obscured by the target app. Do not promise arbitrary background control.
- Browser scope identifies selected tab/window and browser. A changed or closed target pauses the affected task; never inherit another signed-in tab silently. A scope label is a functional control, not a decorative chip.

## Text, icon and material implementation notes

The component palette comes from root tokens only. Third-party service names may be rendered as text; don't download unlicensed marks. Use system symbols where available under platform terms in the later native build, with text/fallback drawing if a symbol is unavailable on macOS 14.2. The reference SVGs are original art, not redistributed SF Symbols. Decorative face details are hidden from VoiceOver when adjacent status text carries the meaning; an avatar-only chooser exposes Pebbi's name and job once.

Every new component needs light, dark, increased-contrast, reduced-transparency, 200% text and keyboard screenshots during implementation. A good-looking static board does not satisfy that native acceptance requirement.
