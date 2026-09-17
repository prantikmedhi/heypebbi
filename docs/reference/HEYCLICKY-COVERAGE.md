# HeyClicky reference coverage — Pebbi original implementation

Research checked **2026-09-17**. This is a coverage/evidence audit, not an endorsement, a license opinion, an implementation claim or instructions from the reference product. Pebbi behavior is governed by the [canonical contract](../CONTRACT.md), [product definition](../product/PRODUCT.md), [requirements](../product/REQUIREMENTS.md) and [app flows](../product/APP-FLOWS.md).

## Evidence and method

The live homepage and changelog were retrieved directly over HTTPS with HTTP 200 and their HTML-visible text inspected. The first third-party extraction service failed with 403; direct retrieval succeeded. This audit therefore uses the live origin text, not the failed extract or search snippets. Trust/privacy pages and the public repository README/LICENSE were also retrieved directly. Repository main resolved to commit `a80fa80721a8aebe51a170a7780705024ebc6e46`, dated `2026-04-27T19:24:56Z`, in the inspected GitHub commit response.

| Ref | Source inspected | What it establishes |
| --- | --- | --- |
| C | [Live changelog](https://www.heyclicky.com/changelog) | Vendor statements about advertised capabilities, fixes, removals and version/date chronology |
| H | [Live homepage and FAQ](https://www.heyclicky.com/) | Current landing-page positioning, user-facing scope, pricing claims and FAQ wording |
| T | [Trust page](https://www.heyclicky.com/trust) | Vendor's stated data/processing boundaries; not independent technical verification |
| P | [Privacy policy](https://www.heyclicky.com/privacy-policy) | Vendor's published provider/storage/retention disclosures; not Pebbi policy |
| R | [Public repository README](https://raw.githubusercontent.com/farzaa/clicky/main/README.md) | Public snapshot's documented architecture and explicit notice that newer work is private |
| L | [Public repository LICENSE](https://raw.githubusercontent.com/farzaa/clicky/main/LICENSE) | MIT text, copyright notice and conditions in the inspected repository |
| G | [Repository main commit metadata](https://api.github.com/repos/farzaa/clicky/commits/main) | Commit identity/date observed for the public main branch |

**Latest advertised releases observed:** `v1.0.50`, September 14, 2026; preceding major expansion `v1.0.49`, September 12, 2026. Earlier still-relevant behavior is marked with its advertised release rather than silently attributed to the latest release. [C](https://www.heyclicky.com/changelog)

**Personally tested reference-app behavior:** none. No reference-app binary was installed, no sign-in/payment/desktop control was performed, no vendor performance/usage metric was reproduced and no private production implementation was inspected. “Inspected” below means source text inspected. The public README is documentation evidence, not a code audit. Pebbi has documentation and original brand references only at this point; every mapped implementation remains to be built and verified.

## Public snapshot and MIT boundary

The README's April 27 update explicitly separates the existing open-source code from newer private work. Its documented pipeline is a native Swift menu-bar app, speech transcription, model reasoning, synthesized speech, screen capture/pointing and a Cloudflare Worker proxy. That older description is not evidence that the public snapshot contains persistent assistants, full Home, current routines, MCP, current computer-use behavior or the current production models. [R](https://raw.githubusercontent.com/farzaa/clicky/main/README.md)

The inspected license is **MIT License**, copyright **(c) 2026 Farza**. It permits use, copying, modification, distribution and other listed uses subject to including the copyright and permission notice in copies/substantial portions, and disclaims warranty/liability. If later implementation reuses code, record exactly what was reused and retain required notices. This documentation task copies no application code. The repository license is not evidence of rights to copy distinctive brand assets, character designs, private production code or proprietary marketing artwork. Do not assume current website assets share the repository license. [L](https://raw.githubusercontent.com/farzaa/clicky/main/LICENSE)

Pebbi instead follows the locked native Swift runtime, selected Azure roles and authenticated backend in the [contract](../CONTRACT.md). No Claude/Codex/Hermes CLI dependency, old Worker proxy or reference mascot is inherited merely because it appears in older documentation.

## Latest advertised feature mapping

Every row is **vendor-advertised, not firsthand tested**. “Original Pebbi direction” is normative only through the linked PB requirements, not a claim that Pebbi already works. Version references all refer to [C](https://www.heyclicky.com/changelog).

| Ref feature | Advertised release/evidence | Pebbi PB IDs | Original Pebbi direction and verification target |
| --- | --- | --- | --- |
| Personalization interview, appearance choice and three suggested assistants | 1.0.49, getting started | PB-003, PB-004, PB-011 | Optional four-topic interview, default Pebbi plus up to two confirmed jobs, original ceramic-like appearance; manual path without models |
| Conversational assistant creation and introductory explanation | 1.0.49, getting started | PB-004, PB-011 | Editable native profile proposal before Save; no automatic task launch from creation |
| Separate setup usage allowance | 1.0.49, getting started | PB-004, PB-027, PB-028 | Operator-configured, visibly separate allowance if provided; manual setup remains usable; no invented free quota |
| Persistent assistants with name, memory, conversation and folder | 1.0.49, assistants/Home | PB-011, PB-012, PB-013, PB-021 | Durable Pebbi identity, isolated local context/workspace and inspectable memory; no server content sync |
| Integrated Home with conversations and files; expand out of notch | 1.0.49, assistants/Home | PB-005, PB-012, PB-014, PB-033 | Native Home plus perch/menu bar; explicit notchless and multi-display paths |
| Dock and global shortcut entry | 1.0.49, assistants/Home | PB-001, PB-005, PB-006 | Consistent local view across Dock/menu/perch/Home with validated shortcut defaults |
| Face/color customization and listening/thinking/speaking reactions | 1.0.49, assistants/Home | PB-011, PB-029, PB-032 | Original Pebbi face/material language, exact canonical state mapping and reduced-motion/text alternatives |
| Pins, search, archive and working/needs-you/unread status | 1.0.49, assistants/Home | PB-011, PB-012, PB-015, PB-026 | Stable ordering, independent flags, global attention without hidden active approvals |
| Earlier legacy work can be shown/moved with confirmation | 1.0.49, assistants/Home | PB-012, PB-030, PB-035 | Preserve Pebbi's own history/migrations; no HeyClicky importer or legacy toggle without an actual Pebbi legacy format |
| Voice shortcut in a selected chat; type or follow up while working | 1.0.49, voice/conversations | PB-006, PB-007, PB-016 | Origin-aware routing and race-free turn assignment; typed path without mandatory microphone |
| Ask from other apps and route to named assistant/new job | 1.0.49, voice/conversations | PB-006, PB-007, PB-011, PB-016 | Explicit-name/context routing, ambiguity asks before execution; creation still reviewed |
| Contextual status/result/retry follow-ups with named spoken updates | 1.0.49, voice/conversations | PB-007, PB-015, PB-016, PB-017 | Concrete target/task association; no blind retry of uncertain external effects |
| Live task steps, stop, retry, concurrent assistants and busy queues | 1.0.49, voice/conversations | PB-015, PB-016, PB-017 | Journaled canonical attempts, one active per Pebbi, verified terminal results and scoped resource leases |
| Long chats paginate, preserve scroll and jump to latest | 1.0.49, voice/conversations | PB-012, PB-038 | Stable anchors and local drafts; background tokens never drag reading position |
| More recent history and onboarding retained as context | 1.0.49, voice/conversations | PB-004, PB-013, PB-031 | Explicitly approved facts plus inspectable compaction; do not copy a vendor message-count window as architecture |
| File drag/drop, attach, paste and attachment-only messages | 1.0.49, files/apps/settings | PB-010, PB-014, PB-021 | Validated imports and source ownership; failed drop keeps composer usable |
| Inline documents/PDF/images, larger preview, open in app/Finder | 1.0.49, files/apps/settings | PB-014, PB-021 | Native preview/Quick Look with exact artifact provenance and safe external opening |
| Each chat remembers document; live Markdown and animated images | 1.0.49, files/apps/settings | PB-012, PB-014, PB-032 | Per-chat preview state; safe rendering and animation respecting reduced motion |
| Custom MCP URL or local command, browser/API-key auth, tool discovery | 1.0.49, files/apps/settings | PB-022, PB-023, PB-031 | HTTPS remote or separately parsed local executable, first-launch consent, Keychain secrets and untrusted metadata review |
| Connecting/ready/re-auth status and immediate voice capability refresh | 1.0.49, files/apps/settings | PB-022, PB-023, PB-029 | Exact connection enums; existing conversations see real capabilities after change |
| In-Home account/apps/voice/shortcut settings, preview and update actions | 1.0.49, files/apps/settings | PB-002, PB-022, PB-029, PB-036 | Native categories and real account state; explicit preview; separate download/install/relaunch |
| Skills removed pending redesign | 1.0.49, files/apps/settings | PB-011, PB-023 | No community Skills marketplace requirement; jobs/memory/tools are native product concepts, not copied marketplace behavior |
| Personalized source-backed suggestions, read-only research, approval before task | 1.0.49, suggestions | PB-020, PB-022, PB-024, PB-031 | Opt-in sources, disclosed lookback, evidence manifest and no writes during research |
| Approve, skip, adjust conversationally and cancel adjustment | 1.0.49, suggestions | PB-007, PB-017, PB-024 | Versioned proposal, cancel restores original and cancels its speech; approval creates one task |
| Morning invitation delayed for calls/sharing/Focus and dismissed once seen | 1.0.49, suggestions | PB-024, PB-026, PB-034 | Local opted-in invitation, coalescing and manual Quiet; no promise to detect all calls |
| Research recent full documents from connected apps/public web; rejection feedback | 1.0.49, suggestions | PB-014, PB-020, PB-024, PB-031 | Default disclosed 72-hour scope, complete-read coverage, optional feedback with bounded retention |
| Repeated tasks run while Mac app open; pause/resume/run now/delete | 1.0.49, routines | PB-011, PB-025 | Local scheduling, explicit timezone/next due and profile/global routine controls |
| Silent routine results with unread; one sleep catch-up | 1.0.49, routines | PB-025, PB-026, PB-035 | Durable unread result, no chime/speech, at most one coalesced catch-up |
| Wait offline/busy, retry failure, preserve pause; archive assistant pauses routines | 1.0.49, routines | PB-016, PB-025, PB-035 | Bounded retries with failure streak; waiting not counted as failure; restore never auto-resumes |
| Ask before computer input, persistent option and voice decisions | 1.0.49, computer use | PB-007, PB-017, PB-018 | `allowOnce`/bounded `allowForScope`/`deny`; no standing high-risk grant; manual protected UI |
| User chooses current tab or separate Chromium browser window/profile | 1.0.49, computer use | PB-018, PB-019, PB-022 | Opt-in Chrome/Brave extension + authenticated helper; selected scope, no ordinary-profile debug port |
| Permission fixes, retries, clear drawings/speech on skipped tour | 1.0.49, improved/fixed | PB-003, PB-004, PB-009 | Per-permission actual state, no duplicate prompts; tutorial cancellation cleans its own presentation |
| Updated start/finish/help cues and cancelling adjustment speech | 1.0.49, improved/fixed | PB-007, PB-024, PB-026, PB-034 | Distinct nonessential cues with quiet policy; stopped speech cannot return late |
| Team checkout promotion codes | 1.0.49, improved/fixed | PB-027, PB-039 | Hosted Stripe capabilities only when operator configured; no team/admin product scope inferred from vendor checkout |
| Lower Home idle CPU and assistant-switching overhead | 1.0.49, improved/fixed | PB-038, PB-040 | Pin own budgets and measure own hardware; vendor CPU percentages are not Pebbi results |
| Bluetooth cue pre-roll and first-reply sound fix | 1.0.49, improved/fixed | PB-034, PB-038 | Actual audio route/cold-start tests and no synthetic pass |
| Dictation works with Home visible but only targets its composer when focused | 1.0.49, improved/fixed | PB-006, PB-010, PB-033 | Capture/revalidate origin, never choose a background Home by visibility |
| External-display menu/shortcut/Escape fixes and screen-picker recovery | 1.0.49, improved/fixed | PB-003, PB-006, PB-033 | Test notchless external monitors, actual OS permission recheck and input routing |
| Floating-card hit targets and non-reordering assistant list | 1.0.49, improved/fixed | PB-005, PB-011, PB-032, PB-033 | Native accessible controls and stable ordering during state updates |
| Long-history launch, relaunch live work and restored suggestions fixes | 1.0.49, improved/fixed | PB-012, PB-013, PB-024, PB-035, PB-038 | Durable journals/recovery, no replayed writes and opt-in restored suggestion scheduling |
| Long conversations no longer permanently reject new turns | 1.0.50, assistants/routines | PB-012, PB-013, PB-035 | Compaction/version consistency, critical context review and continued usable conversation |
| Missing saved conversation starts fresh rather than repeated failure | 1.0.50, assistants/routines | PB-011, PB-012, PB-035 | Disclosed recovery preserving Pebbi memory and known task links; never pretend old text recovered |
| Startup/finished-task follow-up race fixed | 1.0.50, assistants/routines | PB-015, PB-016 | Atomic association at safe boundary or new attempt after terminal state; durable queue ack |
| Routine pauses after three consecutive failed runs | 1.0.50, assistants/routines | PB-025, PB-027, PB-028 | Three failed occurrences after bounded safe retries, approved usage ceilings and explicit Resume; no endless credit loop |
| Draft and attachment persistence per chat while app remains open | 1.0.50, Home/suggestions | PB-005, PB-012, PB-014, PB-035 | Pebbi goes further: local drafts persist across relaunch and never migrate to another chat |
| Mark unread/read without opening, including current chat | 1.0.50, Home/suggestions | PB-012, PB-026 | Manual unread remains meaningful until explicit read/reopen action |
| Escape suppresses immediate hover reopen; links make room | 1.0.50, Home/suggestions | PB-005, PB-006, PB-033 | Hover latch until pointer leaves; no swallowed Escape or obstructed external destination |
| Home menu styling and removed implementation-file/folder profile shortcuts | 1.0.50, Home/suggestions | PB-005, PB-011, PB-021, PB-032 | Original tactile native menus; profile prioritizes jobs/memory/routines/results, workspace remains accessible through Files |
| Suggestion source details travel into task | 1.0.50, Home/suggestions | PB-016, PB-020, PB-024 | Queued task retains source manifest/snapshots and revalidates before use |
| Upgrade card no longer obscured; plan/portal link errors recover | 1.0.50, billing | PB-005, PB-027, PB-028 | Perch yields to native billing card, browser-open failure returns truthful unchanged-plan state |

## Earlier advertised functions that remain in scope

These source entries fill behavior not repeated in the latest release notes. Superseded/removed behavior is identified separately below. Evidence remains vendor-advertised, not personally tested.

| Advertised function | Source | Pebbi PB IDs | Original direction / boundary |
| --- | --- | --- | --- |
| Voice and typed screen-aware explanation, teaching and pointing | [H](https://www.heyclicky.com/), [C](https://www.heyclicky.com/changelog) 1.0, 1.0.21, 1.0.26 | PB-007, PB-008, PB-009 | Explicit capture scope; typed accessible equivalent; verified targets |
| User drawing/circling to identify spatial focus | [C](https://www.heyclicky.com/changelog) 1.0.25, 1.0.33 | PB-008, PB-009 | Original annotations scoped to chosen capture; text alternative |
| Longer walkthroughs and continuation retaining goal/completed steps | [C](https://www.heyclicky.com/changelog) 1.0.48 | PB-009, PB-013, PB-035 | Resumable progress; no silent fifteen-step completion cap |
| Whole PDF/file/web-page reading rather than visible pixels only | [C](https://www.heyclicky.com/changelog) 1.0.47 | PB-008, PB-014, PB-019, PB-020 | Coverage manifest; explicit partial extraction and browser/file authorization |
| Dictation hold/hands-free, editable shortcuts, language choice, word dictionary | [C](https://www.heyclicky.com/changelog) 1.0.37, 1.0.48 | PB-006, PB-010, PB-029 | Review-first; explicit dictionary editing without background typing surveillance; test supported languages rather than inherit counts |
| Screen-aware drafting into an app | [C](https://www.heyclicky.com/changelog) 1.0.37 | PB-008, PB-010, PB-013, PB-017 | Clearly labeled generated draft, separate from faithful dictation; capture consent and insertion review |
| Long dictation backup and interruption preservation | [C](https://www.heyclicky.com/changelog) 1.0.47 | PB-010, PB-031, PB-034, PB-035 | Recoverable transcript under user retention policy; no silent discard on device change |
| Keyboard-layout-aware insertion and clipboard race fixes | [C](https://www.heyclicky.com/changelog) 1.0.48 | PB-006, PB-010, PB-032 | Actual field verification; explicit clipboard fallback and conditional restoration |
| Terminal dictation does not execute input | [C](https://www.heyclicky.com/changelog) 1.0.48 | PB-010, PB-017, PB-021 | Collapse line breaks, review exact text and never submit Return |
| Native computer-use driver advertised as background pointer-safe | [C](https://www.heyclicky.com/changelog) 1.0.48 | PB-017, PB-018, PB-033 | Own AX driver first; explicitly approved real foreground fallback instead of universal guarantee |
| Mic fallback, Bluetooth profile handling, external audio interface fixes | [C](https://www.heyclicky.com/changelog) 1.0.48 | PB-029, PB-034, PB-038 | Explicit/preauthorized fallback, actual formats/hardware tests and stopped-session nonrestart |
| Muted speaker reply placed on clipboard | [C](https://www.heyclicky.com/changelog) 1.0.48 | PB-007, PB-010, PB-034 | Deliberate difference: preserve readable reply and offer Copy, never overwrite clipboard automatically |
| Google Workspace, Notion, Slack/Linear and native app tasks | [C](https://www.heyclicky.com/changelog) 1.0.10, 1.0.11, 1.0.15 | PB-018, PB-021, PB-022 | Explicit catalog with configured adapter tests and scope/grant boundaries |
| Google Calendar and Spotify playback | [C](https://www.heyclicky.com/changelog) 1.0.21, 1.0.22 | PB-007, PB-017, PB-022 | Document read/control/write tool classes, selected account and authorization |
| Account deletion, Keychain credentials and support logs | [C](https://www.heyclicky.com/changelog) 1.0.23, 1.0.32, 1.0.47 | PB-002, PB-030, PB-031, PB-037 | Separate local/server export/deletion, redacted previewable diagnostics and authoritative completion |
| Plans, recurring billing, usage limits and cancellation | [H](https://www.heyclicky.com/) | PB-027, PB-028, PB-039 | Nest/Studio/Constellation, configured Stripe values, server reservation ledger; no copied prices |
| Installation, updates, release notes, minimum macOS and support links | [H](https://www.heyclicky.com/), [C](https://www.heyclicky.com/changelog) 1.0.34–36, 1.0.48 | PB-001, PB-036, PB-037, PB-039 | Signed/notarized universal target with actual hardware proof and verified public release/support routes |
| Local lifecycle/privacy boundaries and cloud processing | [T](https://www.heyclicky.com/trust), [P](https://www.heyclicky.com/privacy-policy) | PB-001, PB-031, PB-035, PB-037 | Explicit actual Pebbi data flow; no unverified privacy/compliance guarantees inherited |

## Deliberate differences and evidence conflicts

1. **Current production is not the public snapshot.** The latest vendor functions postdate the public README's private-development notice. MIT permission does not supply missing implementation. Pebbi scope includes persistent assistants, memory, files, conversations, MCP, suggestions/routines, native computer use and dedicated browser window; it is not reduced to the old voice/cursor example. [R](https://raw.githubusercontent.com/farzaa/clicky/main/README.md) [C](https://www.heyclicky.com/changelog)
2. **Homepage messaging is not a precise entitlement contract.** The homepage contains a free-download claim alongside paid plans and allowance tables. Its FAQ's broad talk availability and app-compatibility claims are not sufficient to establish actual limits or integration safety. Pebbi shows server-authoritative configured entitlements, real unavailable roles and explicit supported adapters. [H](https://www.heyclicky.com/)
3. **Trust/processing descriptions differ in specificity.** Trust describes cloud processing and limited providers; privacy names a broader set. Latest suggestions describe authorized connected-app research. These statements must not be collapsed into an independent guarantee of zero background data access or identical provider routing. Pebbi's own disclosures must match its actual read-only opt-in research and cloud request path. [T](https://www.heyclicky.com/trust) [P](https://www.heyclicky.com/privacy-policy) [C](https://www.heyclicky.com/changelog)
4. **Safety tightens persistent grants.** Vendor notes advertise persistent computer/extra-usage approval and historically more eager writes. Pebbi uses bounded grants, fresh high-risk previews, manual protected UI and explicit CGEvent takeover. Tool allowlisting is not a sandbox, and cancellation is not rollback. [C](https://www.heyclicky.com/changelog)
5. **Removed products stay removed from parity assumptions.** Historical proactive activity tracking was withdrawn; Skills is described as removed in 1.0.49; Notes was removed earlier. Pebbi includes opt-in read-only suggestions, not hidden activity tracking, and no required community Skills/standalone Notes product. Its own Files/memory fulfill distinct scoped needs. [C](https://www.heyclicky.com/changelog)
6. **Original brand, not a character swap.** Do not reproduce source character families, face designs, gel-menu artwork, copy, cursor persona or homepage composition. Pebbi uses pocket-world tactility, its own assets and native accessible hierarchy from [DESIGN.md](../../DESIGN.md).
7. **No inherited performance or language claims.** Source CPU/latency/language counts are vendor claims. Pebbi's own measured budgets, language support and Bluetooth/native-app compatibility require acceptance evidence on stated environments. [C](https://www.heyclicky.com/changelog)
8. **No developer-runtime dependency.** Historical references to bundled Codex/managed policies or a Cloudflare Worker do not override Pebbi's Swift runtime/authenticated backend/locked model roles. Provider availability follows actual deployment tests, not brand-name/model mentions in a changelog. [R](https://raw.githubusercontent.com/farzaa/clicky/main/README.md) [C](https://www.heyclicky.com/changelog)
9. **No unrequested team/cloud product.** Vendor team-checkout promotion codes and legacy migration do not imply team administration, content sync, remote routine execution or import of proprietary history in Pebbi. Hosted billing can expose configured provider-supported promotions without adding those scopes. [C](https://www.heyclicky.com/changelog)

## Pebbi coverage closure

| Requirement range | Coverage interpretation |
| --- | --- |
| PB-001–PB-006 | Native lifecycle, account, permissions, onboarding, surfaces and shortcuts expanded beyond reference UX assumptions |
| PB-007–PB-014 | Conversation, screen guidance, dictation, persistent assistants/history/memory and complete document handling |
| PB-015–PB-023 | Durable verified work, concurrency/approval, native/browser control, research/files and built-in/custom connections |
| PB-024–PB-031 | Source-backed suggestions, bounded local routines, attention, metering, preferences and data ownership/privacy |
| PB-032–PB-040 | Pebbi's explicit accessibility, hardware, recovery, secure release, diagnostics, efficiency, public surfaces and full evidence gates |

Accessibility and full release gating are Pebbi requirements even where the source pages do not document them. Absence of a vendor statement is not evidence the vendor lacks a feature; it simply cannot support a source claim. Likewise a mapped feature is not a passed Pebbi test.

## Verification handoff

- [Requirements](../product/REQUIREMENTS.md) and [App flows](../product/APP-FLOWS.md) enumerate every PB-001–PB-040 individually.
- [Screens](../design/SCREENS.md) must give each PB a real design treatment; [Acceptance](../quality/ACCEPTANCE.md) and [coverage.json](../quality/coverage.json) must give each PB executable/manual evidence.
- Explicit regression targets from 1.0.50: long-context continuation; missing-conversation recovery; start/finish follow-up race; three-failure routine pause; per-chat drafts; manual unread; Escape hover latch; proposal source propagation; unobscured billing/link-error handling.
- Explicit regression targets from 1.0.49: persistence/queues, safe routine wake, permission recovery, source-backed read-only suggestions, custom MCP auth/discovery, native/browser scope, external-monitor focus and Bluetooth first audio.
- Current live audio deployment blockers are recorded in the contract. No reference claim, fixture or catalog listing resolves them. Actual tenant/billing/signing/hardware inputs remain external acceptance prerequisites.
