# Pebbi — screen treatments and complete PB coverage

**Documentation-only design reference.** No rendered example is proof of implementation, live provider operation or release readiness. Canonical requirements and exact lifecycle strings are fixed by [CONTRACT](../CONTRACT.md). Exact tokens are in [DESIGN.md](../../DESIGN.md); full axis mappings and shared control anatomy are in [Components](COMPONENTS.md). See [Motion](MOTION.md) and [Accessibility](ACCESSIBILITY.md) for defaults that apply to every screen.

## Shared screen shells

- **Home / Operate:** native titlebar, stable sidebar, expressive Pebbi shelf, task list and recent conversations; optional task inspector. It is not a centered marketing page or an analytics dashboard.
- **Pebbis / Explore + Configure:** named companion tiles followed by a native detail editor; each Pebbi has job, appearance, memory, conversations, workspace and routines. Avatar color never replaces name or state.
- **Conversations / Command + Inspect:** searchable sidebar/list, readable transcript, multiline composer, citations/attachments, contextual task detail. A conversation is not a task.
- **Files / Inspect:** scope-aware native list and preview. **Suggestions / Explore:** read-only proposals with explicit approval to execute. **Routines / Configure:** local schedules and outcomes. **Connections / Configure:** status/scope catalog. **Settings / Configure:** native grouped panes with clear settings search/disclosure.
- **Perch / Glance:** optional compact top-edge surface with exact state, privacy controls and explicit expansion. Menu-bar and Home paths are equivalent; no hardware notch is required.
- **Decision sheet:** opaque neutral reading plane, requesting Pebbi identity, complete action preview, explicit safe/dangerous decisions, persistent footer actions. Decoration yields to the consequence.
- **Public page / Learn or Configure:** small original brand header, conventional headings, readable legal/support/download/account content; no faux native controls.

Canonical sidebar order and visible names are **Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections, Settings**. Screen names after an arrow below are subordinate views, not new global navigation nouns. All shells support native Back/dismiss, window close, keyboard and VoiceOver. Each PB section is normative design coverage; related sections may share the same surface.

## Adaptive shell rules

All dimensions are native points. At 1080+ Home width, allow sidebar + content + optional inspector. At 840–1079, inspector is sheet/drill-in; at 640–839, sidebar becomes labeled navigation and all content is one column. On a smaller visible screen, fit the window and scroll rather than losing a control. At larger text sizes, collapse columns sooner based on fit. Never horizontally scroll an ordinary form to reach its action footer. Dense code/table previews may scroll within their labeled container with a keyboard alternative.

Top-edge placement uses the actual visible frame and safe geometry of the selected display. On notchless displays the perch sits below the menu bar; if no safe space exists, use menu-bar/Home. Notifications and background task updates never steal focus or switch Spaces. Every compact scene provides an explicit Open Home route. Light/dark composition uses paired root tokens, not inverted imagery. Approval, capture, stop and failure indicators always outrank decorative mascot display.

## Screen-by-screen requirement treatments


### PB-001 — Native installation, launch, update and quit

**Surface:** Installation / Home / Settings → Updates.

- **Composition:** Use a branded cream introduction beside a large ceramic Pebbi, then native installation and launch affordances. After launch, Home replaces the introduction with the real empty-state shelf. Update status is a quiet native settings group, not a celebratory takeover.
- **State and truth:** Show verifying, available or unavailable update information only when known; installation and version labels are real release data. Quit explains any active work and closes all app-owned activity. Closing Home is distinct from quitting Pebbi.
- **Access, focus and fit:** First-run title is initially announced; native traffic lights remain native. On a small display, illustration shrinks or leaves the first viewport before explanatory text or Quit becomes inaccessible.

### PB-002 — Account sign-in, sign-out and device sessions

**Surface:** Home → Account entry / Settings → Account.

- **Composition:** A split first-run composition pairs a clay accent companion with a plain sign-in explanation and a single system-browser action. Signed-in view is a native device-session list with this-device identification, timestamps when known and per-device revoke controls.
- **State and truth:** Show waiting for browser, cancelled sign-in and error as distinct explanatory views without inventing a wire account state. Sign-out clarifies local versus server-held data; do not replace local conversations with a fake cloud-sync promise.
- **Access, focus and fit:** Returning from system browser does not bury error text or focus a destructive action. Device names and revoke consequences wrap. No credentials are entered into a brand illustration or custom fake browser.

### PB-003 — Permission onboarding and denied/revoked recovery

**Surface:** Settings → Permissions / contextual permission sheet.

- **Composition:** Lay permissions out as a stepped vertical checklist: capability, why it is needed, current OS status and a concrete next action. Use sea-glass only for an actually granted capability and a butter attention icon for recovery.
- **State and truth:** Ask for microphone, screen recording or Accessibility just in time. Denied and revoked states preserve typed/manual alternatives and name the specific system setting. Do not simulate an OS permission dialog or suggest permission is already granted.
- **Access, focus and fit:** Focus starts at the reason, then the contextual action. Native system prompt owns its focus. Long recovery steps remain selectable and scroll vertically; all steps can be completed from Home without a perch.

### PB-004 — Personalization interview and first Pebbis

**Surface:** Home → Personalization / Pebbis.

- **Composition:** Use a conversational interview with an illustrated companion at one side and a single question on an opaque tray. A preview shelf shows named Pebbis with proposed jobs and appearances; each proposal can be edited or skipped.
- **State and truth:** Clarify that Pebbis are AI assistants. Nothing begins working merely because a tile appears. Unknown answers remain unset, not confidently inferred. Memory capture has a clear inspect/edit path and can be declined.
- **Access, focus and fit:** Keyboard advances native fields; Back preserves entered answers. At narrow width, preview tiles become a horizontal list only if fully keyboard navigable, otherwise a vertical stack; no mandatory swipe or carousel.

### PB-005 — Menu bar, top-edge perch and full Home window

**Surface:** Menu bar / perch / Home.

- **Composition:** Home is the expressive desk: named Pebbi on an upper shelf, then real task rows and recent conversations. The perch compresses this identity into a face, subsystem icon and state label; menu-bar artwork is a monochrome template mark.
- **State and truth:** Perch and Home share real state, not independent toy animations. Tasks, voice and capture can coexist; preserve separate labels. Expand explicitly; do not open Home merely because background work completed.
- **Access, focus and fit:** Collapsed 176 × 44 and expanded 360 × 156 are reference starts, not clipping bounds. Below a notchless menu bar use a plain anchored panel. Menu-bar and keyboard routes expose everything if the panel is unavailable.

### PB-006 — Global shortcuts and focus-safe activation

**Surface:** Settings → Shortcuts / perch activation.

- **Composition:** A native shortcut-recording row shows command name, current binding, conflict status and Restore default. Use a small lilac keycap accent but ordinary legible text for binding and scope.
- **State and truth:** Distinguish a status glance from explicitly opening a composer that needs focus. Conflicts, unavailable global registration and recording cancellation are visible; never claim an invented universal system shortcut.
- **Access, focus and fit:** Capture a shortcut only while its recorder is active; Escape exits recording. VoiceOver names modifiers and keys. Activation must preserve the previous app/caret unless the chosen action explicitly takes input focus.

### PB-007 — Real-time spoken conversation and typed equivalent

**Surface:** Conversations / voice capsule / Home composer.

- **Composition:** Transcript is the main reading plane. A clay voice capsule sits near the composer with mic/speaker glyph, exact voice label, device and stop control. The mascot is expressive but never substitutes for the selectable transcript.
- **State and truth:** Present every voice state: `idle`, `connecting`, `listening`, `thinking`, `speaking`, `interrupted`, `unavailable`, `failed`. Typed input stays first-class. A blocked deployment reads Voice unavailable, not a fake live waveform.
- **Access, focus and fit:** Stop speaking is not Cancel task. Interrupting speech changes only the voice axis unless the user separately cancels work. Full Keyboard Access reaches typing and voice controls; compact layout preserves the stop control before decoration.

### PB-008 — Explicit screen capture scope and screen understanding

**Surface:** Conversations → Share screen / scope strip.

- **Composition:** Use a native-compatible window/display picker with real names and thumbnails only after authorized discovery. The chosen target becomes a persistent opaque scope strip adjacent to the conversation and in the perch.
- **State and truth:** User selects exact scope before capture. Show capture active, target lost, permission denied/revoked and stopped explicitly. A new target requires renewed scope selection; never silently capture every display.
- **Access, focus and fit:** Stop sharing is always reachable. Sensitive-region blocking has a text explanation. Picker is a labeled keyboard-navigable list; small windows use a one-column target list and readable source name rather than tiny thumbnails.

### PB-009 — Drawing, pointing and resumable guided walkthroughs

**Surface:** Target overlay + Home → Walkthrough detail.

- **Composition:** Outline only the relevant target with a small anchored explanatory bubble. Keep progress, Pause walkthrough, Resume and Exit in a separate stable control strip. Mirror every step as accessible text in Home.
- **State and truth:** Paused guidance retains its step and target identity. A missing, moved or closed target becomes an explicit recovery prompt; do not draw an arrow at stale coordinates or auto-click the next plausible control.
- **Access, focus and fit:** Overlay avoids intercepting unrelated clicks and never obscures a password/permission target. Reduced motion uses static outlines. On another Space/display, report target location and let the user navigate rather than force-switching.

### PB-010 — Dictation, review and focus-safe insertion

**Surface:** Dictation tray / Conversations → Dictation review.

- **Composition:** The tray has a clay capture header, a generous editable transcript, a persistent original-target label and a clear Insert action. Review text gets more space than the mascot. Copy is an honest alternative to insertion.
- **State and truth:** Show `idle`, `capturing`, `transcribing`, `reviewing`, `inserting`, `completed`, `cancelled`, `failed`. At focus mismatch remain/return to reviewing. Completed means insertion verified, not a clipboard write or a finished transcription.
- **Access, focus and fit:** Stop capture and Cancel are separate from Insert. Recheck exact target before writing; failed insertion preserves transcript. Review body scrolls above a fixed action footer. Text-only/keyboard flow is complete without audio animation.

### PB-011 — Persistent Pebbi creation, editing and appearance

**Surface:** Pebbis → New Pebbi / Pebbi detail.

- **Composition:** Use an expressive specimen shelf plus a native inspector for name, job, appearance, workspace, memory, conversations and routines. Appearance choices are authored glaze plates and poses, not unlimited untested text colors.
- **State and truth:** Editing a Pebbi does not delete its identity or silently redirect an active task. Show saving/validation failures without discarding edits. Display current task ownership and a clear edit versus create distinction.
- **Access, focus and fit:** Avatar selectors expose name/appearance and selected value with a check. Jobs and names wrap. At compact widths editor becomes a full detail page with Back; creative shelf never displaces Save/cancel or error details.

### PB-012 — Conversations, search, archive, unread and pinning

**Surface:** Conversations / search results / archived conversations.

- **Composition:** Use an efficient native list with title, Pebbi, excerpt, pin and unread indicators. Search sits above the list; results show matching context, not opaque ranking scores. Transcript remains an independent reading pane.
- **State and truth:** Empty results differ from unloaded/error results. Archive and restore preserve context. Pin/unread changes are visible and announced; do not turn conversation pinning into task priority.
- **Access, focus and fit:** List selection and search focus are stable during streaming. Context-menu actions also have discoverable toolbar/menu equivalents. One-column layout drills from list to conversation with Back and retained scroll position.

### PB-013 — Memory inspect, edit, forget and context compaction

**Surface:** Pebbis → Memory / Conversations → Context detail.

- **Composition:** Lilac identifies a memory bookmark, while the actual entries are a legible native list with source, scope and edit/forget controls. Context compaction appears as an explanatory transcript marker with inspectable summary.
- **State and truth:** Clearly distinguish saved memory from temporary conversation context and compacted summary. Forget previews the bounded effect; failures remain visible. Never imply that compacted context is an exact verbatim record or all data was erased remotely.
- **Access, focus and fit:** Full memory content is selectable and keyboard editable. Confirm destructive scope; return focus after removal. At narrow widths show entry details on a separate page rather than squeeze memory into a tiny tooltip.

### PB-014 — Attachments, whole-document reading and previews

**Surface:** Conversations → Attachments / Files → Preview.

- **Composition:** Attachment rows show filename, type, size when known, read state and preview action. Whole-document reading shows scope/completeness as text. Quick Look/native preview occupies a neutral plane, separate from decorative tiles.
- **State and truth:** Partial extraction, unsupported/encrypted file, unreadable page, oversized file and complete reading have honest labels. A visible thumbnail is not proof the whole document was processed. Preserve useful extracted text and source/page references.
- **Access, focus and fit:** Drag-and-drop has an Open-file alternative. Preview has keyboard close/back and accessible filename. Dense pages may zoom within their region; attachment list and action controls still fit the window.

### PB-015 — Agent task execution and truthful live progress

**Surface:** Home → Task detail / Conversations → Task inspector.

- **Composition:** Task title and owner anchor a verified-event timeline. Use an indeterminate activity line until a meaningful denominator exists; distinguish proposed, executing and verified steps. Outputs are linked artifacts, not celebratory placeholders.
- **State and truth:** All ten task states in Components are reachable visual treatments. `succeeded` requires verified result; `failed` preserves last confirmed action. Live tool errors and unavailable dependencies cannot be masked by a smiling mascot.
- **Access, focus and fit:** Cancel task and approval links remain in a stable footer/toolbar. Streaming updates do not reorder focused rows or announce every token. Compact inspector is a full-page detail, not an overlay covering its own stop control.

### PB-016 — Concurrent Pebbis, queues and race-free follow-ups

**Surface:** Home → Task list / Pebbis → Queue.

- **Composition:** Group task rows by explicitly named Pebbi when useful, with visible queue order, attempt state and follow-up destination. A compact header summarizes active/queued work from actual data, never decorative metrics.
- **State and truth:** Queued versus running is explicit. A follow-up states which logical task or conversation it attaches to; a conflicting operation shows waiting information rather than simultaneous fake progress. Each pending approval belongs to one named task.
- **Access, focus and fit:** Keyboard can inspect/cancel each task independently. Preserve scroll and selection when other Pebbis update. At narrow widths keep owner and title together; reduce optional timestamp detail before hiding task identity.

### PB-017 — Approval, stop, cancellation and recovery

**Surface:** Decision sheet / task inspector / recovery detail.

- **Composition:** Use an opaque butter-titled approval slip with exact actor, action, target, scope/expiry and full preview. Allow once, eligible Allow for this scope and Deny have clear separate affordances; no default approval through Return.
- **State and truth:** Fresh approval is required for payments, credentials, destructive bulk actions, publishing and outbound messages. Show `cancelling` until settled, then verified outcome; retain side-effect facts. `interrupted` recovery requires reconciliation before retry.
- **Access, focus and fit:** Deny and Cancel task stay visible with long previews. Escape never approves. Safe initial focus, 44-point actions, full accessible consequences and one-column footer wrapping protect narrow/large-text use.

### PB-018 — Native desktop control and takeover boundaries

**Surface:** Conversations → Desktop action / takeover banner.

- **Composition:** Action preview names the exact target app, resource and intended operation. A persistent butter banner distinguishes explicit foreground takeover from semantic native actions; it must not look like ordinary background task decoration.
- **State and truth:** Accessibility denial, absent target, unsupported semantic action and takeover request have separate recovery copy. CGEvent fallback requires explicit approval because it affects the foreground pointer/keyboard. Never promise arbitrary background clicks.
- **Access, focus and fit:** Provide a reliable stop path even when the controlled app covers Home. Do not take over secure/permission/password interfaces. Overlay boundaries are keyboard/AX-readable; text wraps rather than concealing which app will receive input.

### PB-019 — Browser DOM tools and user-selected sessions

**Surface:** Connections → Browser / Conversations → Browser scope.

- **Composition:** Show Chrome and Brave installation paths for the opt-in extension and native helper, each as conventional native setup rows. Session picker lists the user-selected tab or dedicated window and a persistent target label.
- **State and truth:** Connection state uses the canonical connection axis. Missing helper, wrong browser, closed tab, changed scope and denied action are visible. No remote-debugging-port onboarding for an ordinary signed-in profile; no fabricated browser success.
- **Access, focus and fit:** DOM-first actions name the element and target. Focus/takeover changes are explicit, not hidden behind a browser icon. Compact picker uses readable tab titles and origin text with full accessible URL as appropriate.

### PB-020 — Web research with source-grounded results

**Surface:** Conversations → Research result / source inspector.

- **Composition:** Research results use readable prose, attached citation markers, source title/origin/date where known and an inspectable evidence panel. No invented progress bars, trust scores, favicon collections or fake source cards.
- **State and truth:** Distinguish fetched evidence, unavailable source, partial coverage and inference. Failed access leaves a visible limitation, not fabricated quotation. Task completion refers to the bounded research result, not guaranteed truth.
- **Access, focus and fit:** Citations are named keyboard links and do not rely on tiny superscript targets. Source panel becomes a separate detail view at small widths. Preserve original text selection and offer normal open-source navigation.

### PB-021 — Files, workspace boundaries and code execution

**Surface:** Files / Pebbis → Workspace / task output inspector.

- **Composition:** Use a native file list with location breadcrumb, active workspace and preview. Code execution is a clearly scoped task detail with command, working directory, expected outputs and redacted actual log—not a fake embedded terminal demo.
- **State and truth:** Outside-workspace requests require explicit boundary approval. Unavailable runtime, execution failure and verified artifact creation are distinct. A proposed filename or generated code block is not proof the file exists or ran.
- **Access, focus and fit:** Paths are copyable with full accessible values. Destructive edits preview scope; stop applies to active execution. Compact layouts prioritize filename, boundary and status over decorative file tiles.

### PB-022 — Built-in connection catalog and OAuth lifecycle

**Surface:** Connections → Catalog / connection detail.

- **Composition:** Catalog rows group recognizable service names with descriptions and scopes; use original generic glyphs or text, not copied brand marks. Detail shows requested access, account identity when authorized and disconnect/revoke controls.
- **State and truth:** Cover `disconnected`, `connecting`, `ready`, `expired`, `degraded`, `failed`. Show system-browser authentication and cancelled return honestly. Ready requires a real check; expired credentials identify dependent waiting tasks.
- **Access, focus and fit:** Consent scopes wrap in ordinary prose with keyboard scroll. Focus returns from browser to a stable status region. Narrow view is list → detail with Back, never a dense grid of logo-only buttons.

### PB-023 — Custom remote/local MCP connections

**Surface:** Connections → Add custom connection.

- **Composition:** A native segmented choice distinguishes remote endpoint from local process. Remote form shows origin/transport/auth; local form shows executable, arguments and environment variable names with secret fields masked. A read-only tool list follows successful discovery.
- **State and truth:** Connection lifecycle follows the same six canonical states. Test and Save are distinct; validate endpoints and launch scope. Explain that tool allowlisting is not an OS sandbox. No secret values in test logs or preview artwork.
- **Access, focus and fit:** Use native labeled fields, inline errors, safe clipboard treatment and accessible mask disclosure. Long commands get a selectable wrapped preview; no horizontal form overflow. Local execution needs clear user consent.

### PB-024 — Read-only personalized suggestions and approve-to-run

**Surface:** Suggestions → Proposal detail.

- **Composition:** Butter slips carry proposed action, why it may help, source evidence and named Pebbi. Detail is a readable proposal with Dismiss and Review action; no running glyph before approved execution.
- **State and truth:** Suggestions remain read-only and cannot create tasks or external side effects merely by being visible. After approval, show a linked task with canonical task state rather than silently replacing the proposal with success.
- **Access, focus and fit:** No guilt copy, countdown urgency or hidden dismissal. Keyboard can inspect evidence and approve through the normal sheet. Compact layouts keep action scope and source next to the proposal, not in hover-only metadata.

### PB-025 — Routines, local scheduling, wake and retry policy

**Surface:** Routines → List / routine editor / history.

- **Composition:** Routine rows show name, Pebbi, schedule/timezone, next eligible local run and literal “Runs while Pebbi is open.” Editor uses native time/day controls and a readable action/approval scope preview.
- **State and truth:** Cover `active`, `paused`, `blocked`, `archived`. Show one catch-up after wake, not a flood of overdue jobs. Retry and approval policy remain visible; a routine can be blocked while its history contains succeeded tasks.
- **Access, focus and fit:** Pause and inspect history are keyboard-accessible. Device sleep/local-only limitations are not buried in a tooltip. At small widths edit schedule and action as stacked sections; keep save/cancel and timezone visible.

### PB-026 — Notifications, Focus/call suppression and unread delivery

**Surface:** Settings → Notifications / Home unread / Conversations.

- **Composition:** Notification preferences explain native alerts, sound and unread retention separately. Home and Conversations use a restrained unread badge and history entry; completion never launches a mascot celebration over another app.
- **State and truth:** When Focus/call policy suppresses a notification, preserve unread delivery in-app. Sensitive details can be hidden. Do not use an app-rendered imitation of a system alert to bypass notification permission.
- **Access, focus and fit:** Notification activation opens the exact task/conversation only on user intent. Badges have accessible counts and a text route to unread items. No color-only dots; narrow layouts retain the unread distinction.

### PB-027 — Plans, metering, reservations and billing changes

**Surface:** Settings → Plan and usage / system-browser billing.

- **Composition:** Present Nest, Studio, Constellation in an aligned native comparison with real server-fed price/currency/period/allowance. Usage separates consumed, reserved and available where authorized data supports it, with timestamps and explanatory labels.
- **State and truth:** Unconfigured pricing/entitlements say unavailable. No invented approved price, promotional percentage or completed checkout. Hosted Checkout/Portal opens in system browser; pending change and confirmed server-authoritative result are different views.
- **Access, focus and fit:** Billing consequences and renewal terms are readable and not obscured by ceramic art. Keyboard and VoiceOver get table headers. At narrow widths use labeled stacked plan sections, not clipped pricing columns.

### PB-028 — Quota limits and graceful provider unavailability

**Surface:** Home / Conversations / Settings → Plan and connections.

- **Composition:** A neutral status panel leads with which capability is unavailable and why, then preserves typed work, existing files and local reading paths. Use butter for action-needed, danger for actual failure; no animated listening state.
- **State and truth:** Distinguish quota exhausted, missing credentials, unsupported deployment, network failure and temporary provider issue. The selected realtime and dictation roles remain unavailable until verified working; no silent model substitution or fixture transport in user sessions.
- **Access, focus and fit:** Retry, settings and permitted alternatives are readable and keyboard reachable. Keep entered text/transcript intact. Compact views show the reason before action choices; do not push a plan upgrade when the true issue is provider configuration.

### PB-029 — Preferences, voice/device choice and shortcut recording

**Surface:** Settings → Appearance / Voice / Devices / Shortcuts.

- **Composition:** Native grouped settings use rounded section labels and quiet colored sample chips, with immediate labeled previews only where safe. Appearance offers system/light/dark and accessible motion reduction; device selectors show actual detected names.
- **State and truth:** Voice choices are enabled only when supported; unavailable devices stay understandable. Shortcut recorder conflicts, setting-save errors and permission-required changes appear inline without discarding previous valid settings.
- **Access, focus and fit:** All controls expose labels/values and work with Full Keyboard Access. Preview cannot silently open a mic or speak. At large text/narrow widths labels move above controls; no fixed-height settings rows.

### PB-030 — Local export, account export and deletion

**Surface:** Settings → Data / export progress / deletion sheet.

- **Composition:** Two clearly separated sections describe local conversation/file/memory export and server-held account/usage export. Deletion preview names exact scope and consequences; neutral body, danger action, no cheerful mascot or celebratory finish.
- **State and truth:** Local and account export completion are separate verified facts; partial/unavailable export explains what is missing. Deletion shows requested versus confirmed result. Do not promise cross-device conversation sync or remote erasure of third-party content.
- **Access, focus and fit:** Destructive confirmation is keyboard/VoiceOver readable and never the default focused action. Export destinations are selectable. Long consequences wrap above a persistent safe action; retain a support route if deletion fails.

### PB-031 — Privacy controls, retention and sensitive-content boundaries

**Surface:** Settings → Privacy / scope strip / redaction preview.

- **Composition:** Use a plain-language retention summary with per-data-type controls, capture scope defaults, sensitive-content exclusions and redaction preview. A lilac privacy bookmark is decorative; real status is text and native toggles.
- **State and truth:** Show when content stays local versus explicitly leaves for an authorized operation. Screenshots are not silently synced. Blocked sensitive capture and revoked access have immediate persistent indicators; do not expose secrets in hints or previews.
- **Access, focus and fit:** Privacy actions have full descriptions, keyboard labels and no hidden defaults. At small sizes the summary stays readable before advanced disclosures. Stop sharing remains visible regardless of whether this settings pane is open.

### PB-032 — VoiceOver, keyboard, contrast and reduced motion

**Surface:** All surfaces / Settings → Accessibility preferences.

- **Composition:** Every screen keeps semantic reading order, visible ring, sufficient contrast and complete text equivalent. Show text-scale and motion preferences with a static reference sample that does not force the user to watch animation.
- **State and truth:** States cannot depend on face, fill, waveform, audio or timed tooltip. Pending approval and task cancellation remain operable with VoiceOver. Reduced motion removes travel/squash, not truthful status or focus feedback.
- **Access, focus and fit:** Test 100–200% app text, both themes, Increase Contrast, Reduce Transparency and Full Keyboard Access. Reflow based on content fit; do not claim a static HTML board proves native assistive-technology compliance.

### PB-033 — Multi-display, notchless, Spaces and scaling behavior

**Surface:** Perch / Home / Settings → Display placement.

- **Composition:** Placement settings name actual displays and preview safe top-edge position without drawing a fake hardware notch. Home remains an ordinary native resizable window; user can choose menu-bar-only access if desired.
- **State and truth:** Recompute visibleFrame, safe areas and coordinate scale per monitor. On unplug, move to a valid display without stealing focus. Do not force Space switching for a task, notification or walkthrough target.
- **Access, focus and fit:** Notchless and non-Retina behavior are first-class. When the perch cannot safely fit, open through menu-bar/Home instead. Large type expands or routes content to Home, never reduces vital labels beneath legibility.

### PB-034 — Audio devices, Bluetooth, interruption and mic recovery

**Surface:** Voice capsule / Settings → Devices / recovery notice.

- **Composition:** Persistent device label accompanies the voice capsule; device picker is a native list. A recovery notice identifies actual selected/unavailable input and retains transcript. The visual waveform stops when input is not live.
- **State and truth:** Bluetooth/device change, mic revoked, interrupted output, disconnected device and capture failure have explicit reasons using the appropriate voice/dictation axis. Never silently capture from a newly selected mic without the product-defined consent behavior.
- **Access, focus and fit:** Stop voice/capture remains reachable. VoiceOver does not receive continuous audio level announcements. Compact layout keeps device name available in a labeled disclosure, not a microscopic caption or transient tooltip.

### PB-035 — Offline, sleep/wake and app-crash recovery

**Surface:** Home → Recovery / task inspector / Connections.

- **Composition:** On return, show an orderly recovery tray listing affected task attempts, last confirmed action and available reconciliation. Local conversations and files remain readable; a neutral offline notice does not hide them.
- **State and truth:** Active attempts become `interrupted` after a crash until reconciled. No blind replay of sends, payments or other external effects. Wake may trigger one routine catch-up per policy; not a burst of missed celebrations or queued backlogs.
- **Access, focus and fit:** Recovery review is keyboard navigable and preserves task identity. No automatic foreground window on wake. Small view prioritizes unresolved side effects and safe choices before artwork or historical logs.

### PB-036 — Secure updates, signing and release rollback

**Surface:** Settings → Updates / release detail.

- **Composition:** Use a factual native release panel: installed version, available signed update, release notes, verified integrity result and clear install/restart choice. Reference art may show a small Pebbi carrying a note, but no claim that a binary exists.
- **State and truth:** Signature/notarization or feed failure blocks install with actionable information. Rollback is a documented controlled recovery path, not an arbitrary unsigned download. Version and channel come from actual release metadata.
- **Access, focus and fit:** Update choice is not preempted by a modal blocking all local work unless genuinely necessary. Release notes are selectable and accessible; narrow view stacks metadata. No fabricated green “secure” seal.

### PB-037 — Diagnostics, support and redacted telemetry

**Surface:** Settings → Diagnostics and support.

- **Composition:** A readable diagnostics summary shows relevant environment/capability status, opt-in telemetry posture and a Preview diagnostic bundle action. Redacted detail is inspectable before export; support links use conventional text.
- **State and truth:** Bundle generation and sending are separate actions. Missing provider connection and actual test failure are explicit. Do not include tokens, raw private transcripts, screenshot contents or developer resource names in samples/log previews.
- **Access, focus and fit:** Copy diagnostic ID and export work from keyboard. Monospace logs can scroll within a labeled region, while privacy explanation and safe actions stay in the ordinary flow. No auto-submit of support data.

### PB-038 — Resource budgets, latency and idle efficiency

**Surface:** Settings → Diagnostics / Home loading and idle.

- **Composition:** Idle Home has a still Pebbi, not a breathing loop. Resource diagnostics show measured values and collection interval only when available. Loading uses a relevant state label and a small native indicator, never fake seconds or progress.
- **State and truth:** Slow operation notices identify which task or connection is delayed; they do not assert performance targets were met. Hidden surfaces stop decorative rendering. Quit leaves no product daemon alive.
- **Access, focus and fit:** Performance details are optional disclosures and readable to VoiceOver without rapid updates. At narrow width use labeled rows. Native profiling across hardware is release evidence; the static board does not establish CPU/memory/latency budgets.

### PB-039 — Support, privacy, account and download web surfaces

**Surface:** Public Support / Privacy / Account / Download pages.

- **Composition:** Use the original outlined wordmark, cream/plum material pair, large rounded headings and a restrained ceramic corner illustration. Each page has a conventional main content column and footer, not a generic feature-tile landing page.
- **State and truth:** Download shows real signed artifact/version only when available; otherwise says unavailable. Account redirects through authorized identity/billing flows; privacy states actual handling; support explains contact paths without fake chat availability or testimonials.
- **Access, focus and fit:** Pages can be server-rendered Fastify surfaces later; no new React/web-app requirement. At 320 CSS pixels all legal/form content reflows; keyboard skip link, semantic headings, underlined prose links and strong focus are required. Brand-board HTML is not these pages.

### PB-040 — Complete end-to-end acceptance and honest release gating

**Surface:** Settings → Diagnostics / release evidence document.

- **Composition:** Build verification is primarily a release evidence document, not a gamified customer dashboard. If exposed in diagnostics, use explicit capability rows with Passed, Failed, Blocked or Not tested and links to redacted evidence.
- **State and truth:** Never mark blocked realtime/dictation, missing credentials, untested architecture, absent signing or unwitnessed native accessibility as passed. Reference illustrations and fixtures are labeled design/test only and cannot satisfy live acceptance.
- **Access, focus and fit:** Status includes text, icon, environment and verification context; no percentages that hide critical blockers. At compact sizes expose one evidence item per row with complete reason. The full PB roster is checked, not a hand-picked subset.


## Coverage and implementation handoff

This document has one dedicated section for every PB-001 through PB-040, including public pages and honest release gating. Shared axis tables cover all exact task, voice, dictation, connection and routine state values. The [verification record](verification.json) records the machine check of requirement IDs and tokens; it is documentation validation, not a claim of app acceptance.

Later native design review must capture real light/dark screenshots at wide, compact, notchless and large-text sizes; observe focus, VoiceOver, motion and truthful live state. If implementation cannot support a specified provider, permission or OS action, render the honest unavailable/recovery view and record the external blocker. Do not reinterpret this complete specification as an MVP or silently remove a PB requirement.
