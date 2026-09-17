# Pebbi — information architecture

Normative destination and ownership map. [Contract](../CONTRACT.md) and [Requirements](REQUIREMENTS.md) govern behavior; [App flows](APP-FLOWS.md) governs transitions; [Screens](../design/SCREENS.md) and [DESIGN.md](../../DESIGN.md) govern visual composition and tokens. This is a native SwiftUI/AppKit information architecture, not a web route specification.

## Identity and nouns

| Noun | Meaning | Must not be confused with |
| --- | --- | --- |
| HeyPebbi | Project/company-facing identity; selected domain `heypebbi.com` | A second app or proven registered legal entity |
| Pebbi | App name and default assistant's name | A separate runtime provider |
| Pebbis | Persistent task assistants with individual profiles | Temporary task processes or shared accounts |
| Home | Full native workspace and overview destination | Perch-only interaction or a web dashboard |
| Conversation | Durable message context with drafts and task references | A task state machine |
| Task | Logical requested work with attempt lineage | Every voice utterance or notification |
| Attempt | One execution with canonical task state and journal | A retry that overwrites earlier evidence |
| Memory | User-approved durable fact or preference | All original messages or provider training |
| Workspace | A Pebbi's managed local artifact boundary | Unrestricted Mac storage |
| Suggestion | Read-only-researched, source-backed proposed task | Already authorized work |
| Routine | A local repeat-task definition with run history | A cloud worker running after Quit |
| Connection | Account-labeled authorized adapter and discovered tools | Permission to use all writes or every app |
| Approval | Version-bound decision on an operation/scope | OS permission, identity sign-in or model readiness |
| Perch | Compact top-edge native presentation | A hardware-notch requirement |

## Top-level navigation

The Home window sidebar uses these exact destinations, in this order: **Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections, Settings**. Search is a native control, not an extra top-level destination. Sidebar selection and keyboard focus remain distinct.

| Destination | First content | Primary actions | Secondary destinations | Empty/error treatment |
| --- | --- | --- | --- | --- |
| Home | Selected Pebbi, pending input/approvals, running/queued work, recent unread results | Talk, Type, Open result, Review request | Specific conversation/task | No work: invite a first request; offline retains local content |
| Pebbis | Stable pinned-first collection with name, job, original face and text status | New Pebbi, Open conversation | Profile, Memory, workspace, Routines | Default Pebbi stays available; archived filter; failed save retains form |
| Conversations | Searchable local list grouped/filterable by Pebbi with read/archive/pin indicators | New conversation, Search, Mark read/unread | Chat, task detail, preview | No matches differs from no history; missing history offers disclosed fresh conversation |
| Files | Managed artifacts and imported attachments with origin/type/modified date | Preview, Open, Export, Show in Finder | Producing task/conversation | No files explains how to attach/create; unreadable file preserves provenance |
| Suggestions | One sourced proposal and counter/navigation, or opt-in explanation | Approve, Adjust, Skip | Source preview, source preferences, queued task | Not opted in, research running, no useful proposal and connection unavailable are distinct |
| Routines | Definitions with Pebbi, schedule/timezone, canonical state and next due | New, Run now, Pause, Resume | Editor, run history, result | No routine explains app-open execution; blocked/paused reason and next action visible |
| Connections | Built-in catalog, configured accounts and custom MCP | Connect, Reconnect, Add custom, Disconnect | Scopes/tools/grants | Unconfigured adapter visible as unavailable; disconnected is not hidden |
| Settings | Last category or General on first visit | Category-specific controls | Account, privacy, support/update | Local categories work offline; server sections show unavailable, not empty fabricated data |

Home attention priority is deterministic: unresolved risky/unknown external outcomes; actionable approvals; other input/connection blockers; running work; queued work; unread results. Within a group preserve creation order unless user explicitly reorders queue. No continuous reorder by task animation or fluctuating status.

## Native surfaces and navigation ownership

| Surface | Purpose | State it owns | What it cannot do |
| --- | --- | --- | --- |
| Menu bar menu | Reliable notchless entry, Show Home, current status, Settings, Quit | Native menu presentation only | Hide all access when Dock/perch is disabled |
| Compact perch | Selected Pebbi and unobtrusive voice/task status | Expanded/collapsed presentation and display policy | Change conversation/task identity on hover |
| Expanded perch | Quick conversation/composer, attention and open-in-Home | Same selected context as Home | Cover billing/approval or steal background focus |
| Home window | Full native navigation and split panes | Sidebar selection, selected Pebbi/conversation, window placement | Become a web-shell implementation |
| Chat pane | Messages, live progress, source/result cards and draft | Per-conversation scroll anchor/draft/attachments | Reassign an unsent draft on Pebbi switch |
| Preview pane | One selected artifact/source | Per-conversation preview ID/position | Run embedded scripts/macros or grant folder authority |
| Task detail | Full journal, approval history, outputs, Retry/Stop | Expanded sections, selected attempt | Mutate a terminal attempt into a new run |
| Approval card/sheet | Exact action preview and decisions | Currently inspected action version | Persistently approve high-risk classes or capture credentials |
| Guidance overlay | Anchored pointer/marks and accessible step controls | Current visible step/geometry | Block the user's app outside explicit controls or click by itself |
| Takeover indicator | Current target/action scope and Stop | Current control-lease presentation | Hide real pointer movement under a background claim |
| System browser | Auth, hosted billing, public links, selected browser automation | External browser session under actual provider rules | Accept credentials via an ordinary Pebbi text field |
| Native pickers/settings | Permission, file scope, device and save choices | OS-owned grant/selection | Be bypassed to make a demo look unattended |

**Surface transfer rule:** the view is a projection of the same selected IDs. Moving between Home and perch commits draft/view state and attaches the new presentation to those IDs. It cannot duplicate message submission, task creation or attachment import. There may be only one active editing owner for a conversation draft at a time; other presentations mirror it rather than race it.

## Object graph and persistence boundaries

- Account has device sessions and server usage/entitlement records; it isolates a local account store. Sign-out locks this store; sign-out is not local deletion.
- Account's local store has Pebbis. A Pebbi has a profile, workspace, memory scope, conversations and routine definitions. Shared/global preference memories are explicitly scoped; no implicit cross-Pebbi fact sharing.
- Conversation has messages, drafts, attachment references, read/archive/pin flags, scroll anchor and preview selection. A message may reference zero or more task events/artifacts but is never itself a task state.
- Logical task has immutable original request and attempt lineage. Attempt has canonical task state, ordered journal, input/context manifest, grants/approvals, source evidence, output artifacts and reconciliation status.
- Suggestion has sources, proposal version, chosen Pebbi and user decision. Approval references exactly one version and creates one logical task idempotently.
- Routine has confirmed schedule/timezone, next due, state, failure streak and task-run history. Archiving/restoring a Pebbi never silently reactivates routines.
- Artifact has managed location or explicit granted reference, media/type metadata, provenance, producing attempt and validation. Deleting a conversation does not silently delete unrelated exported files; show actual affected scope.
- Connection has origin/account, canonical state, scopes and discovered tool inventory. Credentials live in Keychain; exported configuration contains names/metadata only, never secrets.
- Approvals reference user, connector/app, tool class, resource, expiry and action version. Changing destination/content invalidates the relevant approval.

Storage formats/foreign keys belong to [Data model](../engineering/DATA-MODEL.md); these relationships specify user-visible ownership. No local object above acquires server synchronization by being shown on an account screen.

## Conversation pane anatomy

Reading order: Pebbi name/job and conversation title; canonical task/status summary; messages oldest to newest; jump-to-latest when needed; attachment tray; composer; send/talk controls; optional preview. Within assistant result: concise outcome, artifacts, citations, limitations, expandable work history. Approval/recovery card belongs beside the relevant task, with Home attention linking to it.

Message and task cards show who owns the work, whether it is still running/waiting/terminal, and whether the result is unread. A read flag never stands in for success. Long histories load around a stable message anchor, not an index that jumps when older messages arrive. Background replies cannot force bottom scroll.

Draft ownership key is account + conversation. Include text, attachment references, optional voice recovery text and edit cursor/selection where safely restorable. Persist before navigation or close; restore after relaunch. If a conversation is missing, offer recovery rather than assigning draft to whichever chat is visible.

## Pebbi profile anatomy

1. Identity: name, job and original appearance.
2. Context: memory review and relevant workspace boundary.
3. Work: conversations, running/queued tasks and outputs.
4. Routines: definitions, next due, state and failure reason.
5. Management: pin, archive/restore and explicit deletion.

Do not expose implementation-file shortcuts as the primary profile experience. Memory editing is a native UI; an implementation prompt file is not a substitute. Profile edits affect future work; amendment of active work uses a follow-up and retains original request.

## Settings categories

| Category | Contents | Scope/default behavior |
| --- | --- | --- |
| General | Launch behavior, Dock visibility, Home behavior | Device-local; no daemon after Quit |
| Appearance & displays | Original Pebbi appearance, perch display policy, permitted motion choices | Device-local; accessible global OS preferences respected |
| Voice & audio | Voice choice/explicit preview, input/output devices, fallback consent | Device-local selection; actual capability health shown |
| Dictation | Language preference, review-first toggle, explicit dictionary editing, transcript retention | Review-first default; no global typing observation |
| Shortcuts | Home/talk/dictation/hands-free recorder, conflict validation and reset | Device-local; key recorder never submits work |
| Notifications | Task cues, suggestion invitation, Quiet mode and available system suppression | Routines silent; lock-screen content redacted |
| Permissions | Actual Microphone, Screen Recording, Accessibility, Notifications status | OS truth, separate from connection/model state |
| Privacy & data | Context controls, memory/suggestion consent, retention, private sessions, local export/delete | Local paths work offline; scope distinctions explicit |
| Account & usage | Identity/device sessions, plan, reserved/consumed usage, hosted billing, server export/delete | Server authoritative; no fabricated pricing/zero usage |
| Grants | Inspect/revoke bounded action grants by app/connector/resource/expiry | High-risk fresh approvals never appear as blanket grants |
| Support & Updates | Diagnostics preview/export, support, version, release notes, check/download/install | No telemetry submission without consent; signed updates only |

Connections remains a top-level destination; Settings may deep-link to it but must not create an inconsistent second connection editor.

## Focus, keyboard and dismissal hierarchy

- Native top-level navigation follows predictable sidebar → content → optional preview ordering. Tab order follows visible reading order; icon-only controls have accessible names.
- During active foreground takeover, Escape first stops that takeover and follows its cancellation/reconciliation path; it never approves or cancels unrelated work. Otherwise Escape acts on the highest current interaction: shortcut recorder cancel; topmost sheet/popover dismiss; walkthrough visible overlay dismiss; expanded perch close.
- Closing Home restores focus only after deliberate invocation and only if the previous app/window still exists. Background task/notification changes never activate a window or Space.
- Opening a composer explicitly focuses it. Voice hold never makes a background composer the dictation target. Native dictation insertion revalidates originating field immediately before action.
- On deleting/removing a focused item, focus moves to the next sibling, previous sibling if last, or owning section's primary action if empty. It never jumps to an unrelated Send button.
- A waiting approval is announced once as an available action. Stream token updates never repeatedly interrupt VoiceOver.
- Takeover Stop has a stable native button and configured keyboard path. All decisions remain operable without speech or mouse.
- Preserve input cursor/scroll/preview when toggling layouts. Reduced motion changes transition style, not navigation or semantics.

## Search and filtering rules

Local search covers Pebbi names/jobs, conversation titles/message text and indexed artifact text within current account permissions. Indicate whether a match comes from chat, memory or file. Search does not secretly upload the local corpus. Filters for Pebbi, archived, unread and type are visible and clearable; unsupported unindexed files are not falsely represented as searched. Opening a result highlights its match while preserving task state.

Quick spoken routing is not full-text search and must not choose by fuzzy name alone when names collide. Ask with name + job. A “missing conversation” is a broken reference state, not an empty successful search result.

## Empty, waiting and error placement

| Condition | Placement | Retained context | User path |
| --- | --- | --- | --- |
| No Pebbis beyond default | Pebbis collection | Default profile | Create manually or through conversation |
| No conversation history | Chat/list | Selected Pebbi | Start conversation |
| Search has no matches | Search content | Query and filters | Clear filters/edit query |
| Missing history reference | Relevant chat plus recovery link | Pebbi, known tasks, local draft | Create fresh linked conversation; inspect diagnostics |
| `waitingForApproval` | Task card + Home attention | Immutable preview and output | Review/allow/deny/stop |
| `waitingForInput` | Task card + Home attention | Concrete question and original goal | Answer/revise/stop |
| `waitingForConnection` | Task card + linked connection | Request, partials and source requirements | Reconnect/manual alternative/stop |
| Provider `unavailable` | Voice control and capability notice | Draft/transcript | Retry after repair or use actually available path |
| Dictation `failed` | Review recovery card | Recognized text and original target | Open retained draft/retry/cancel |
| Routine `paused` after failures | Routine row/profile | Failure streak and last result | Fix then Resume |
| Offline | Nonmodal Home banner and affected controls | All local state | Local browse/edit/export; later reconnect |
| Unknown external outcome | Persistent prominent task warning | Intent and evidence | Reconcile; do not auto-retry |
| Unconfigured billing/release/support | Relevant card/page | Current known configuration | Explain required operator configuration; no dummy action |

## Requirement-to-destination index

| PB | Primary destination | Required supporting surface |
| --- | --- | --- |
| PB-001 | Installer/Home | Menu bar, Quit confirmation |
| PB-002 | Settings → Account & usage | System-browser sign-in, device list |
| PB-003 | Settings → Permissions | Point-of-use permission card |
| PB-004 | First-run setup | Safe tutorial, profile preview |
| PB-005 | Home | Menu bar, perch, preview |
| PB-006 | Settings → Shortcuts | Global invocation and origin-safe composer |
| PB-007 | Conversation | Perch voice control and transcript |
| PB-008 | Conversation → Add screen context | Native scope picker/indicator |
| PB-009 | Conversation task detail | Guidance overlay and text steps |
| PB-010 | Dictation review | Origin/destination receipt |
| PB-011 | Pebbis → Profile | Create/edit/archive controls |
| PB-012 | Conversations | Search, native context menu, preview |
| PB-013 | Pebbi profile → Memory | Proposed-memory and compaction cards |
| PB-014 | Composer/Files | Preview, native file picker |
| PB-015 | Conversation → Task detail | Home work status and artifacts |
| PB-016 | Home work list | Per-Pebbi ordered queue |
| PB-017 | Task approval/recovery | Grants, Stop/takeover indicator |
| PB-018 | Task detail | Native app target and takeover indicator |
| PB-019 | Connections → Browser | Scope chooser and dedicated browser window |
| PB-020 | Conversation result | Source detail and artifact preview |
| PB-021 | Files | Workspace/overwrite/execution preview |
| PB-022 | Connections catalog | System-browser OAuth and scope detail |
| PB-023 | Connections → Add custom | Remote/local form and tool review |
| PB-024 | Suggestions | Source preview, adjustment dialog |
| PB-025 | Routines | Schedule editor, run history, Pebbi profile |
| PB-026 | Home attention | Native notifications and unread markers |
| PB-027 | Settings → Account & usage | Hosted Checkout/Portal |
| PB-028 | Affected capability card | Usage/connection repair links |
| PB-029 | Settings | Device picker, voice preview, shortcut recorder |
| PB-030 | Settings → Privacy & data/Account & usage | Native export picker, deletion confirmation |
| PB-031 | Settings → Privacy & data | Context manifest/private-session indicator |
| PB-032 | Every destination | VoiceOver semantics and keyboard controls |
| PB-033 | Settings → Appearance & displays | All native windows and overlays |
| PB-034 | Settings → Voice & audio | Interruption/fallback card |
| PB-035 | Home recovery | Task reconciliation and local drafts |
| PB-036 | Settings → Support & Updates | Signed installer/update controls |
| PB-037 | Settings → Support & Updates | Diagnostic preview and send confirmation |
| PB-038 | Home/task view | Nonintrusive capacity/wait status |
| PB-039 | Public/account web pages | Verified download/support/auth links |
| PB-040 | Release evidence outside end-user navigation | Acceptance coverage and real evidence manifest |

PB-040 is a release obligation, not a fake end-user “all tests passed” screen. The implementation must produce its evidence through the verification system, not a decorative dashboard.
