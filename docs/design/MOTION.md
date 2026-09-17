# Pebbi — motion and character performance

Motion explains cause and continuity. The brand remains expressive without moving. Styling: [DESIGN.md](../../DESIGN.md). Exact state axes: [Components](COMPONENTS.md). Behavior scope: [CONTRACT](../CONTRACT.md).

## Non-negotiable behavior

Input wins over animation. Pointer-down response is immediate; commit occurs on release inside the control. Start every interrupted transition at its currently presented value, not a stale target; carry velocity for direct manipulation. Never block a Stop, Deny, Cancel, keyboard action or new task event while a spring settles. Native animations must run on display-aligned facilities; do not install timer-driven idle animation loops.

Keep spatial origins consistent: a perch expands from its top-edge anchor and returns there, an inspector enters/exits from the same side, a sheet remains tied to its parent. A menu appears at its trigger, not a global screen coordinate. Avoid repositioning across a display as spectacle; fade out and back at the validated new anchor if the display geometry changes.

## Motion recipes

These values are design starting points in seconds/milliseconds, not a reason to delay the underlying state or invent a timeout. Springs use response and damping ratio, not a fixed completion duration. Test on actual macOS hardware and stop motion when its surface is off-screen.

| Event | Normal recipe | Reduced-motion equivalent | Trigger/guard |
|---|---|---|---|
| Button press | Immediate state tint; at most one-point ledge compression, 80–100 ms settle | Tint only, immediate | User pointer/key input, not hover loops |
| Perch expand/collapse | Response 0.30 s, damping 1.0; grow from safe top-edge anchor | Immediate layout or 100 ms opacity crossfade | Explicit open/close; retain focused child or return to opener |
| Inspector reveal | Response 0.32 s, damping 1.0; at most 16-point translation | 100 ms crossfade without travel | Explicit inspect; no automatic focus jump from background completion |
| Native sheet | Platform transition, source-anchored; no added bounce | Honor OS Reduce Motion | Present after intent; denial/cancel available immediately |
| User reposition | Track pointer one-to-one; release response 0.40 s, damping 1.0 | Direct manipulation remains; no post-release travel embellishment | Clamp to visible frame; preserve grab offset |
| Pebbi selection | Four-degree maximum lean plus 3% crown compression; one settle, response 0.28 s, damping 0.9 | Static selected pose with check/border | Explicit selection, never state polling |
| Task completion | Single 4-point lift and smiling settle, at most 350 ms; completion check arrives with event | Check + static smile, optional 100 ms fade | Only verified `succeeded`; suppress when Focus/call rules apply |
| Approval arrival | Butter slip appears over 120 ms; no object bounce | Immediate slip | Real `waitingForApproval`; no celebration encouraging acceptance |
| Voice amplitude | Bounded mouth openness and small line waveform based on real audio, not synthetic busy sine wave | Static mic/speaker icon + exact state; optional simple non-moving level meter | `listening`/`speaking`, live signal only |
| Thinking | One glance upward on transition; optional native busy glyph in UI, not a looping mascot orbit | Static glance-up pose and Thinking text | Real `thinking`; task running is independent |
| Failure or interruption | Static pose and immediate text; at most 100 ms icon crossfade | Immediate text/icon | Preserve outputs and user focus |
| Walkthrough advance | Target outline crossfades over 120 ms; pointer travels only on explicit next step, never obscures content | Static next outline and text, no pointer flight | Validate target geometry immediately before drawing |
| Theme change | Use platform appearance update; optional 120 ms color crossfade | Immediate opaque color change | No whole-screen luminance flash; respect accessibility preferences |
| File output arrival | New row appears without re-sorting focused item; optional 100 ms fade | Immediate row | Verified output; no dropping/throwing metaphor |

No viewport parallax, spinning camera, breathing background, automatic carousel, random eye tracking, confetti, repeatedly pulsing microphone halo or persistent particle system. A friendly still pose is the idle state. Do not animate every streaming token.

## Mascot state hierarchy

The mascot is redundant feedback, not the authoritative status control. At most one expression animation runs. Accessible text always reports the exact affected subsystem.

Priority for the compact face when multiple axes are active:

1. Fresh approval, active takeover or a serious actionable failure: attentive/concerned static pose; show the specific label and separate stop affordance.
2. Dictation capture or active screen sharing: show privacy indicator regardless of face; never hide it behind speaking animation.
3. Voice `listening`/`speaking`: listening/speaking pose, without altering task badges.
4. Task `running` or voice `thinking`: focused/glance-up pose.
5. Verified completion: single smile settle, unless suppressed or superseded.
6. Idle: still friendly face.

This is presentation arbitration, not a new product state machine. A task can be `running` while voice is `interrupted`; the task row remains Running and the voice capsule remains Speech interrupted. A failed connection does not turn every Pebbi into a failed task. The [expression sheet](assets/mascot-expression-sheet.svg) includes canonical example captions, not an exhaustive combined-state atlas.

## Audio, haptics and notification restraint

Sound is optional and off where notification/call/Focus policies require suppression. Do not emit a chime for every tool step. If a completion sound is enabled, fire it with the actual verified completion event, not after a delayed animation. Do not require sound to know the mic is live. Haptics are optional on supported hardware only; do not imply a universal Mac haptic capability. Status announcements and unread records remain available when all sensory flourish is disabled.

## User preferences and accessibility

Honor OS Reduce Motion independently from Reduce Transparency and Increase Contrast; also expose a Pebbi motion setting that can reduce further, never override the OS reduction. Reduced motion removes translation, spring overshoot, squash, parallax and amplitude-driven character motion. Keep readable text, icon changes, focus and user-controlled direct manipulation. A brief opacity change is optional, not required.

On sleep, hidden windows, inactive Spaces, app pause and Quit, stop decorative work. Quit must end app-owned activity, not leave a mascot animation or daemon alive. Background completion never brings a window to front. Resume by rendering the current confirmed state, not replaying all missed gestures or celebrations.

## Implementation acceptance evidence

Record native normal/reduced-motion transitions, keyboard interruption during each animation, frame pacing on supported hardware, VoiceOver output and energy impact during idle. Test a pending approval arriving during speech; Cancel task during perch collapse; monitor disconnect during dragging; device loss while mouth animation is active; and a late success event after cancellation has started. The UI must reflect reconciled canonical state rather than completing an obsolete animation. These are future native acceptance checks, not evidence supplied by the static HTML board.
