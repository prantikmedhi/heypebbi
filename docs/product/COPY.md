# Pebbi — interface copy and language contract

English source copy for native UI and required public/account pages. [Contract](../CONTRACT.md), [Requirements](REQUIREMENTS.md), [App flows](APP-FLOWS.md) and [IA](INFORMATION-ARCHITECTURE.md) govern meaning. Exact visual style belongs to [DESIGN.md](../../DESIGN.md). Strings below are proposed original Pebbi copy, not copied vendor prose and not claims of a shipped application.

## Voice and writing rules

Pebbi is friendly, lively and matter-of-fact. Color, tactile illustration and original mascot reactions carry much of the playfulness; safety/error language stays calm and precise. Use warm short sentences, sentence case and concrete verbs. Prefer “Your draft is still here” to a joke about failure. Never use guilt, simulated distress, claims of consciousness or dependency-building language. Pebbi is explicitly AI.

Use **Pebbi**, **Pebbis**, **Home**, **Conversations**, **Files**, **Suggestions**, **Routines**, **Connections**, **Settings** exactly. Use HeyPebbi for project/legal context where appropriate, not as a second assistant name. Avoid “agent” as the only explanation of a task. Say “Pebbi can work on this” when useful, but never say work happened without evidence.

- Name the active Pebbi in spoken updates: “Research Pebbi is waiting for a source.” Do not use a generic “it” when multiple tasks are active.
- Say what happened, what remains safe/available and what the user can do next. Do not hide the actionable error behind “Something went wrong.”
- Distinguish “Generated,” “Saved,” “Executed,” “Tested,” “Sent” and “Verified.” A successful API request is not a verified external outcome.
- “Stop speaking” affects speech. “Stop task” affects execution. “Close” affects presentation. Never reuse a generic Stop label when its scope is ambiguous.
- Do not promise unlimited, free, instant, fully private, always working, fully background or all deleted unless the specific verified contract supports it.
- Do not narrate every tool call. Show meaningful progress; retain inspectable detail.
- Do not quote raw provider errors, endpoints, home paths, tokens or private content in banners/notifications. Use a safe code and diagnostic reference.
- AI output may use a user's preferred tone within its task, but system approval, billing, privacy and error strings remain standardized.

## Substitutions, localization and accessibility

Braced values below are runtime placeholders, not unresolved product decisions. `{pebbiName}`, `{appName}`, `{fileName}`, `{recipient}`, `{resource}`, `{version}`, `{dateTime}`, `{timezone}`, `{usageUnit}`, `{amount}`, `{currency}`, `{count}` and `{reason}` must come from verified state. Escape untrusted strings for their presentation context and never interpret them as markup/instructions. If unavailable, use an explicit fallback such as “the selected app,” not invented identity.

Use locale-aware dates/timezones, pluralization and integer-minor-unit currency formatting from trusted values. Preserve identifiers case exactly. Display important target strings without truncating distinguishing suffixes; allow selectable full text. Long names must wrap, not hide consequences. Accessible names describe action and scope; decorative face labels do not replace status. Announce semantic changes once, not each stream token.

## Core identity copy

| Location | Copy |
| --- | --- |
| Public/product headline | A little company for the work ahead. |
| Product explanation | Pebbi is an AI companion for your Mac. Talk or type, understand what is on screen, and give a Pebbi a job you can return to. |
| First-run identity | Meet Pebbi. A small AI companion, with room for your big and small jobs. |
| First-run disclosure | Pebbi stores your work on this Mac. When you ask for AI help, approved content is sent to our service and model providers. You choose screen, file and app access. |
| Empty default chat | What would you like a hand with? |
| Empty Pebbis collection | Give a Pebbi a job of its own. Its conversations, memory and files stay together. |
| Manual setup choice | Set up without an interview |
| Missing AI setup | The interview is unavailable right now. You can still name your Pebbi and choose its job. |
| Selected domain note in internal docs only | `heypebbi.com` is the selected domain; registration and trademark clearance require verification. |

Do not put internal domain-clearance notes in a live consumer page after verification; replace only with verified operator/legal facts. Do not invent a company registration, support address or certification to fill the space.

## Canonical state labels

These are display labels for exact underlying enums, not new states.

### Task

| Enum | Short label | Expanded explanation | Main available action |
| --- | --- | --- | --- |
| `queued` | In queue | {pebbiName} will start when its turn and required resources are available. | View queue / Stop task |
| `running` | Working | {pebbiName} is working on {taskTitle}. | View progress / Stop task |
| `waitingForApproval` | Needs approval | Review this action before {pebbiName} continues. | Review action |
| `waitingForInput` | Needs your input | {question} | Answer / Stop task |
| `waitingForConnection` | Needs a connection | {connectionName} is unavailable. Your request is saved. | Reconnect / View details |
| `cancelling` | Stopping | No new actions will start. Checking what already happened. | View progress |
| `cancelled` | Stopped | The task stopped. Review any changes already made. | View result / Retry if safe |
| `succeeded` | Complete | The requested result is ready and verified as shown below. | Open result |
| `failed` | Could not finish | {safeReason} Your available work is still here. | View details / Retry if safe |
| `interrupted` | Interrupted | Pebbi closed before this attempt finished. Check its last actions before retrying. | Review recovery |

For an optional limitation in an otherwise satisfied result, describe the limitation next to the relevant artifact. If a mandatory result is missing, do not label it fully complete. A cancelled task with an unknown external outcome additionally says: **“We cannot yet confirm whether {actionDescription} happened. Do not repeat it until you check.”**

### Voice

| Enum | Label | Detail when needed |
| --- | --- | --- |
| `idle` | Ready to talk | Hold your voice shortcut, or type instead. |
| `connecting` | Connecting voice | Preparing your voice session. |
| `listening` | Listening | Microphone: {deviceName}. |
| `thinking` | Thinking | Your message is being processed. |
| `speaking` | Speaking | Stop speaking does not stop an active task. |
| `interrupted` | Speech interrupted | Your conversation is still here. |
| `unavailable` | Voice unavailable | {safeReason} You can use available typed features instead. |
| `failed` | Voice connection failed | Your available transcript is saved. Retry when you are ready. |

“Ready to talk” only renders when required capability/permission is actually ready. It cannot mask `unavailable`.

### Dictation

| Enum | Label | Detail/action |
| --- | --- | --- |
| `idle` | Ready to dictate | Start dictation |
| `capturing` | Recording dictation | Stop recording |
| `transcribing` | Finishing transcript | Waiting for final recognized text |
| `reviewing` | Review your words | Destination: {appName} — {fieldLabel} |
| `inserting` | Inserting text | Checking the selected field |
| `completed` | Text inserted | Inserted into {appName} — {fieldLabel} |
| `cancelled` | Dictation cancelled | Nothing else will be inserted. Open saved text if available. |
| `failed` | Dictation could not finish | Your recognized text is still available. |

Copy-only action receipt: **“Copied to clipboard. Not inserted or sent.”** A direct-insertion path without positive confirmation must say **“Insertion could not be confirmed. Check the field before trying again.”** It cannot show `completed` as verified insertion.

### Connections and routines

| Enum family | Enum | Label |
| --- | --- | --- |
| Connection | `disconnected` | Not connected |
| Connection | `connecting` | Connecting |
| Connection | `ready` | Connected |
| Connection | `expired` | Sign in again |
| Connection | `degraded` | Some tools unavailable |
| Connection | `failed` | Connection failed |
| Routine | `active` | Active |
| Routine | `paused` | Paused |
| Routine | `blocked` | Needs attention |
| Routine | `archived` | Archived |

Always pair ambiguous “Needs attention” with the actual cause. A routine blocked by connection is not a failed run; a connection is not ready because its configuration was saved.

## Approval and takeover copy

### Standard bounded action

**Title:** Review {pebbiName}'s next action

**Body fields, always shown:** App or connection; account; operation; exact resource/destination; data to be sent/changed; expected effect; what can and cannot be undone. Show output/message preview in full or an expandable readable view before buttons.

**Buttons:** Allow once / Allow for this scope / Don't allow

**Decision mapping:** `allowOnce` / `allowForScope` / `deny`.

**Scoped-grant explanation:** “Allow {toolClass} for {resource} until {dateTime}. You can revoke this in Settings → Grants.” Never replace this with “Always allow.” High-risk classes omit the scoped choice entirely.

**Stale preview:** “This action changed after you reviewed it. Check the new version before allowing it.”

**Ambiguous voice:** “Do you mean {proposalA} or {proposalB}? Nothing has started.”

### High-risk action

**Outbound message:** “Send this exact message to {recipient} using {accountLabel}?” Buttons: Send once / Keep draft. This remains a fresh approval even when connector reads or general tools were previously allowed.

**Publishing:** “Publish this version to {destination}? People with access there may see it.” Buttons: Publish once / Keep draft.

**Destructive operation:** “Delete {count} items from {resource}? {verifiedRecoveryDescription}” Buttons: Delete these items / Cancel. Do not promise undo unless tested and supported.

**Payment:** “This opens a payment step for {amount} {currency}. Review and complete it yourself in the secure provider page.” Buttons: Open payment page / Cancel. Pebbi does not type payment credentials or bypass authentication.

**Credential/OS consent:** “Please complete this sign-in or permission step yourself. Pebbi will wait, then check whether access is available.” Button: I've finished / Cancel task. “I've finished” triggers recheck, not presumed success.

### Code execution

**Title:** Review code before running

**Body:** “This runs with your macOS user permissions. Pebbi's workspace rules are not an OS sandbox; code may access other files or the network. Review the full script, inputs, arguments and limits before allowing this run.”

**Buttons:** Allow this run / Keep file only. A fresh `allowOnce` is required for each exact script version and execution intent. Never imply a model-generated script is trusted just because Pebbi wrote it.

### Foreground takeover

**Title:** Pebbi needs your pointer and keyboard

**Body:** “To {actionDescription}, {pebbiName} needs to bring {appName} forward and control this window. Your real pointer may move. You can stop at any time. This approval covers {boundedScope} only.”

**Buttons:** Allow this takeover / Show me how / Don't allow

**Active indicator:** “Controlling {appName} — {actionDescription}” with **Stop task**.

**User interruption:** “You took over. Pebbi paused before its next action.”

Never call CGEvent input background-safe. Semantic AX background work may say “Working in {appName} without moving your pointer” only when the active action truly has that capability.

## Capture, memory and disclosure copy

| Context | Copy |
| --- | --- |
| Screen scope picker | Choose what Pebbi can see for this request. |
| Capture disclosure | The selected content will be sent for AI analysis. Other windows are not included in this scope. |
| Capture active | Screen context: {scopeLabel} |
| Scope changed | That window or display changed. Choose the content again before Pebbi continues. |
| Blank/unreadable capture | Pebbi could not read this capture. Try a new selection or attach the source file. |
| Whole-document distinction | This image shows only what is visible. Attach the document or allow its page source to read the rest. |
| Sensitive-content boundary | This may contain sensitive information. Remove or redact it before sending. |
| Proposed memory | Remember this for {scopeLabel}? |
| Memory provenance | Suggested from {sourceLabel}. Not saved yet. |
| Forget memory | Remove this from future remembered context? The original conversation is not deleted. |
| Compaction disclosure | This conversation has a shorter working summary. Your original messages are still available where retained. |
| Private session | Private session: conversation and memory will not be kept here unless you explicitly save an output. Necessary account/usage records and minimal records needed to check unfinished external actions still apply. |
| Local/cloud distinction | History and files live on this Mac. Approved request content is processed through our service and model providers. |
| Revoked source | Access to {resource} was removed. Pebbi will not read it again unless you allow it. |

Avoid guarantees that every secret can be detected. When uncertain, ask for user redaction rather than claiming the content is safe.

## Dictation and audio copy

- Review heading: **Your words, ready to check.**
- Insert button: **Insert into {appName}**.
- Focus changed: **“The active field changed. Your text has not been inserted. Select the intended field, then try again.”**
- Secure field: **“Pebbi cannot dictate into a secure field. Enter this yourself.”**
- Terminal preview: **“Line breaks were removed so this text cannot submit a command by itself. Review it before inserting. Pebbi will not press Return.”**
- Clipboard option: **“Copy instead? This replaces your current clipboard. Copying does not insert or send the text.”**
- Partial recording: **“Recording was interrupted. These are the words recovered so far.”**
- Mic fallback: **“{deviceName} disconnected. Use {fallbackDeviceName} for this session?”** Buttons: Use this microphone / Type instead / Cancel.
- Preauthorized fallback notice: **“Microphone changed to {fallbackDeviceName}, using your saved fallback preference.”**
- Muted output: **“Your output is muted. The reply is available as text.”** Buttons: Open transcript / Audio settings.
- Unavailable transcription: **“Dictation is not connected to a working transcription deployment. Your existing text is safe. Check connection details or type instead.”**

## Suggestions and routines copy

| Context | Copy/actions |
| --- | --- |
| Suggestions opt-in | Let Pebbi look for useful next jobs in the sources you choose. Research is read-only. Nothing runs until you approve. |
| Source lookback | Looks at available work from the last {lookbackHours} hours in {sourceLabels}. |
| Proposal | {proposalTitle}; Why this may help; Sources; Pebbi; Expected result; Required access |
| Proposal controls | Approve / Adjust / Skip / View sources |
| No proposal | No useful suggestion is ready. Your sources have not been changed. |
| Missing source | Suggestions could not read {sourceLabel}. Reconnect it or continue with the remaining selected sources. |
| Approved busy task | Added to {pebbiName}'s queue with its sources. |
| Optional greeting | A few ideas are ready when you are. |
| Greeting controls | Show suggestions / Dismiss |
| Routine disclosure | Runs on this Mac while Pebbi is open. If your Mac misses several runs, Pebbi catches up once. |
| Schedule review | {scheduleDescription} in {timezone}. Next run: {dateTime}. |
| Routine pause | Pause future runs? The current task will continue unless you stop it separately. |
| Third failure | This routine paused after three failed runs in a row. Last issue: {safeReason}. Fix the issue, then resume when ready. |
| Routine blocked | Waiting for {dependencyName}. No new run has started. |
| Archived Pebbi | Archiving {pebbiName} pauses its routines. Restoring it will not resume them automatically. |
| Quiet result | New result from {pebbiName}. |

Do not copy source-vendor greetings, character-style names or playful punctuation patterns. Routine results have no spoken announcement/chime by default.

## Billing, blockers, export and deletion copy

| Context | Copy/actions |
| --- | --- |
| Plans | Nest / Studio / Constellation |
| Unconfigured price | Plan details are not available yet. Paid checkout is disabled. |
| Usage | Used: {consumed} {usageUnit}. Reserved for current work: {reserved} {usageUnit}. |
| Allowance exhaustion | This task reached your {usageUnit} allowance. Your request and available results are saved. |
| Extra usage | Continue using up to {boundedAmount} more {usageUnit} from your existing allowance? This does not charge your card. |
| Checkout return | Checking your subscription status. |
| Verified plan change | Your plan is now {planName}. |
| Checkout cancelled | Your plan has not changed. |
| Portal link failure | The subscription page could not open. Your plan has not changed. |
| Local export | Export work stored on this Mac. Includes selected conversations, memories, routine definitions and files; excludes credentials. |
| Account export | Export account and usage data held by our service. Local chats and files are a separate export. |
| Export partial failure | {completedScope} was exported. {failedScope} could not be exported. The package is not complete. |
| Account deletion confirmation | Delete your account? Review what will be removed, what remains on other Macs, and any legally required billing records. This is separate from deleting local files. |
| Local deletion success | The selected local data was removed from this Mac. |
| Server deletion pending/failure | Account deletion is not confirmed. {safeReason} Your local-data result is shown separately. |
| Sign-out disclosure | Sign out of {accountLabel}? Your local work stays on this Mac and is locked to this account unless you delete it. |

Never insert sample prices, provider endpoints, tenant IDs or keys in production strings. Configuration failures are external blockers, not permission to fabricate a live checkout/session.

## PB coverage: exact moment copy and recovery

The following copy moments are required in addition to shared state labels. Use the same PB IDs in [Acceptance](../quality/ACCEPTANCE.md).

| PB | Normal moment | Unhappy path / next action |
| --- | --- | --- |
| PB-001 | Pebbi is ready on this Mac. | This version requires macOS 14.2 or later. / View requirements |
| PB-002 | Signed in as {accountLabel}. | Your session expired. Your local work is still here. / Sign in |
| PB-003 | {permissionName} is available. | {permissionName} is not allowed. / Open System Settings / Recheck / Not now |
| PB-004 | These Pebbis are ready to make yours. | The interview is unavailable. / Set up manually |
| PB-005 | Open in Home / Return to perch | This display disconnected. Pebbi moved to {displayName}. |
| PB-006 | Shortcut saved: {shortcutLabel}. | That shortcut conflicts with {conflictLabel}. / Record another |
| PB-007 | {pebbiName} is listening. | Voice unavailable. / View connection / Use available typed features |
| PB-008 | Screen context: {scopeLabel}. | The selection changed. / Choose again |
| PB-009 | Step {stepNumber}: {instruction}. | This control moved. / Check the current screen / Continue manually |
| PB-010 | Review before inserting. | The active field changed. Nothing was inserted. / Choose destination |
| PB-011 | {pebbiName} was saved. | This Pebbi could not be saved. Your edits are still here. / Retry |
| PB-012 | Mark as unread / Jump to latest | This saved conversation cannot be found. / Start a fresh conversation |
| PB-013 | Memory saved for {scopeLabel}. | This conflicts with a saved fact. / Review both |
| PB-014 | Read {readCount} of {totalCount} available sections. | Some sections could not be read. / View coverage / Choose another file |
| PB-015 | Result ready. / Open {artifactName} | This task could not finish. Available results are below. / View details |
| PB-016 | Added to {pebbiName}'s queue. | Which Pebbi should receive this? / Choose Pebbi |
| PB-017 | Review this action before continuing. | The result of the last action is uncertain. / Review recovery |
| PB-018 | Working in {appName}. | This action needs your real pointer. / Review takeover / Show me how |
| PB-019 | Browser scope: {browserName} — {tabOrWindowLabel}. | This tab is no longer available. / Choose a tab / Open dedicated window |
| PB-020 | Sources and result are ready. | Found {verifiedCount} matching items; {requestedCount} were requested. / View gaps |
| PB-021 | Saved to {workspaceLabel}. | The destination is outside the allowed folder. / Choose folder / Cancel |
| PB-022 | Connected as {connectionAccount}. | This connection needs sign-in again. / Reconnect |
| PB-023 | Review this connection's tools. | The server could not start or validate. / Edit configuration / View redacted details |
| PB-024 | Your idea is ready to review. | Its source changed. Review the updated proposal before starting. |
| PB-025 | Next run: {dateTime} ({timezone}). | Paused after three failed runs. / View issue / Resume |
| PB-026 | New result from {pebbiName}. | Notifications are off. Results still appear in Home. / Notification settings |
| PB-027 | Your verified plan is {planName}. | Subscription status could not be confirmed. / Check again |
| PB-028 | This feature is available. | {capabilityName} is not connected. Your request is saved. / View details |
| PB-029 | Preference saved. | That device or option is unavailable. Your previous setting is unchanged. |
| PB-030 | Export verified. / Open export | Deletion is not fully confirmed. / Review each data scope |
| PB-031 | Private session is on. | This content needs redaction before sending. / Review content |
| PB-032 | Accessible name: Stop {pebbiName}'s task. | The visual guide is unavailable. Text steps remain below. |
| PB-033 | Perch display: {displayName}. | This screen layout changed. / Confirm new target |
| PB-034 | Microphone: {deviceName}. | Audio was interrupted. Your recognized words are saved. / Review / Resume |
| PB-035 | Your drafts and local work are restored. | An earlier task was interrupted. / Review before retrying |
| PB-036 | Version {version} is ready to install. | This update could not be verified. Your current version is unchanged. |
| PB-037 | Diagnostic export is ready to review. | This report was not sent. / Save locally / Retry |
| PB-038 | Waiting for an available work slot. | This is taking longer than expected. / View progress / Stop task |
| PB-039 | Download Pebbi for macOS. | No verified release is available here yet. / View requirements |
| PB-040 | Internal evidence: {caseId} — {actualResult}. | Release blocked: {verifiedBlocker}. Fixture results do not count as live verification. |

Counts, coverage totals, subscription labels and receipt copy above require actual state. If total sections are unknown, say “Read {readCount} sections; complete coverage could not be established” rather than inventing a denominator.

## Release-copy gate

Before publishing app/web copy, verify that every claim of installation, live model availability, connected app support, supported hardware, price, plan change, download, certification or successful action has actual evidence. Remove unverified testimonial/statistical claims rather than borrowing the reference product's. Public privacy/support/account copy must use verified operator details and explain actual retention. The current documentation pack must not display a production success story in place of missing credentials or signing authority.
