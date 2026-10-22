# Timer rules component

## Responsibility and interface

**Name:** `TimerController` (Python).

**Job:** Own the focus/break state machine and remaining-time calculation, accepting timer actions and publishing state to QML without owning drawing or animation.

Accepted actions:
- `start()` — start a ready phase.
- `pause()` — pause a running phase.
- `resume()` — continue a paused phase.
- `reset()` — abandon the current period and restore a ready, full-length focus period.
- `update(elapsed_seconds)` — internal timing input, not a QML user action; advance the timer using eligible elapsed time.

Values published to QML, with change notifications:
- `phase`: `focus` or `break`.
- `status`: `ready`, `running` or `paused`.
- `remainingSeconds`: nonnegative integer seconds for the countdown.
- `phaseDurationSeconds`: the configured duration of the current phase.
- `focusDurationSeconds` and `breakDurationSeconds`: the configured durations.

QML owns formatting, drawing and animation. Python retains precise fractional remaining time internally and publishes `remainingSeconds = max(0, ceil(remaining_time))`, so the display never becomes negative or shows zero before a period ends.

## Durations and initial state

| Setting | Ordinary use | Short test configuration |
|---|---:|---:|
| Focus duration | 25 minutes (1,500 seconds) | 10 seconds |
| Break duration | 5 minutes (300 seconds) | 4 seconds |

Initial state: **phase `focus`, status `ready`, remaining time 1,500 seconds** (10 seconds with the test configuration).

## Transition rules

In this table, `P` means either phase, `R` is its precise remaining time, and `D(P)` is its configured full duration. Before handling a user action while running, account for elapsed time up to that action; if the period has ended, apply the zero transition first.

| Current phase/status | Event | Resulting phase/status | Remaining-time effect |
|---|---|---|---|
| `P / ready` | Start | `P / running` | Keep `R`; begin counting down from it. |
| `P / running` or `P / paused` | Start | Unchanged | Ignore; do not restart, resume or create another countdown. |
| `P / running` | Pause | `P / paused` | Save the remaining time at the instant of the action; stop counting down. |
| `P / ready` or `P / paused` | Pause | Unchanged | Ignore; preserve `R`. |
| `P / paused` | Resume | `P / running` | Keep saved `R`; establish a new timing baseline so paused time is excluded. |
| `P / ready` or `P / running` | Resume | Unchanged | Ignore; preserve the countdown rules already in effect. |
| Either phase / any status | Reset | `focus / ready` | Set remaining time to the full focus duration. During a break, discard that break and return to focus; do not start automatically. |
| `P / running` | Update before zero | `P / running` | Subtract eligible elapsed time, clamping at zero. |
| `focus / running` | Focus reaches zero | `break / ready` | End focus and load the full break duration. Wait for Start. |
| `break / running` | Break reaches zero | `focus / ready` | End break and load the full focus duration. Wait for Start. |
| `P / ready` or `P / paused` | Update / passage of time | Unchanged | Preserve `R`; no countdown. |

Neither phase starts automatically. Any elapsed time beyond a period's end is discarded rather than deducted from the next, ready phase. A zero-completion event only applies to the currently running phase; stale or inapplicable events are ignored. All inapplicable user actions are likewise ignored, not reported as errors.

## Small example without a real clock

Use the test configuration and synthetic elapsed times:

1. Initially: `focus / ready`, **10 seconds** remaining.
2. Start: `focus / running`, **10 seconds** remaining.
3. Advance by 3 seconds, then Pause: `focus / paused`, **7 seconds** remaining.
4. Advance by 5 seconds while paused: still `focus / paused`, **7 seconds** remaining.
5. Resume: `focus / running`, **7 seconds** remaining.
6. Advance by 2 seconds: `focus / running`, **5 seconds** remaining.
7. Advance by 5 more seconds: focus ends; state becomes `break / ready`, **4 seconds** remaining, waiting for Start.

## Computer-sleep policy

**Exclude computer sleep from an active period.** On waking, retain the remaining time from just before sleep and continue counting only awake, running time. Paused time is also excluded. The clock implementation must support this policy rather than treating time spent asleep as elapsed countdown time.

## Qt bridge proposal

**Name:** `TimerBridge` (Python `QObject`).

**Job:** Adapt `TimerController` to QML by forwarding button actions, supplying eligible elapsed time and publishing a coherent, read-only view of the core state.

### Ownership and timing

The bridge accepts an existing `TimerController` or creates one with the configured focus and break durations. The core remains the sole owner of timer rules, precise remaining time and phase transitions; the bridge reads its state and never maintains a second countdown.

The bridge owns a parented `QTimer`, the last clock reading (the monotonic baseline) and a configurable refresh interval, initially **100 ms**. The interval controls refresh frequency, not the amount deducted: each refresh uses measured elapsed time. The `QTimer` may remain active in ready and paused states because the core ignores elapsed time in those states.

Inject a clock callable returning monotonic seconds. In production, its readings must exclude computer sleep, or a clock adapter must remove suspended time using platform sleep/wake information. An arbitrary monotonic clock is not sufficient if it includes sleep. The `QTimer` itself is only a wake-up source, not a clock. Initialize the baseline from the supplied clock when the bridge is created.

### QML surface

Expose these read-only Qt properties, each sourced from the corresponding core value:

| QML property | Source on `TimerController` |
|---|---|
| `phase` | Current `phase`: `focus` or `break`. |
| `status` | Current `status`: `ready`, `running` or `paused`. |
| `remainingSeconds` | Core's published integer remaining time, `max(0, ceil(remaining_time))`. |
| `phaseDurationSeconds` | Configured duration of the core's current phase. |
| `focusDurationSeconds` | Configured focus duration. |
| `breakDurationSeconds` | Configured break duration. |

Expose four no-argument QML slots: `start()`, `pause()`, `resume()` and `reset()`. These delegate to the corresponding core actions; `update(elapsed_seconds)` is internal and is not exposed as a button action.

### Operation order

Handle refreshes and actions serially on the bridge's Qt thread.

For each periodic refresh:

1. Read the clock once and calculate eligible elapsed time since the baseline.
2. Move the baseline to that reading **before** calling the core.
3. Call `controller.update(elapsed_seconds)`. The core counts time only while running and performs any zero transition, discarding excess elapsed time.
4. Read and publish the complete resulting state.

For each user action:

1. Read the clock once, calculate eligible elapsed time and move the baseline to that reading.
2. Call `controller.update(elapsed_seconds)` **before** applying Start, Pause, Resume or Reset, even if the action would otherwise be inapplicable.
3. Apply the requested core action against the state resulting from that update. If the interval completed a phase, the action therefore applies to the next, ready phase. For example, Start can start that phase; Pause is ignored there.
4. Read and publish the complete resulting state.

Updating the baseline for every operation ensures that ready or paused time cannot be charged to a later running interval. Do not publish an intermediate state between the elapsed-time update and the action.

### Change notification and startup

Use a shared `stateChanged` signal as the Qt NOTIFY signal for all six properties. After each operation, collect all six core values into one snapshot, compare it with the previously published snapshot, and replace the whole snapshot before emitting the signal. Property getters read that snapshot, so QML always sees mutually consistent values. This snapshot is a presentation cache, not another timer model. If none of the published values changed, no notification is needed, even if the core's fractional remaining time changed.

For a newly created core, initialize the snapshot to `focus / ready` with the full focus duration: 1,500 seconds normally or 10 seconds in the test configuration. Starting the refresh `QTimer` does not start the countdown; the core waits for Start. If a core is supplied, publish its existing state rather than resetting it.

### Clock-driven test example

A test can inject a callable that returns a mutable fake clock reading, advance that reading explicitly and invoke the refresh handler or a button slot without sleeping or waiting for a real `QTimer` timeout.

With the 10-second focus configuration and an initial fake reading of 0: Start at 0; Pause at 3 must first account for three seconds and publish `focus / paused` with 7 seconds remaining. Resume at 8 must leave 7 seconds remaining, excluding the five paused seconds. A refresh at 10 must publish `focus / running` with 5 seconds remaining. This checks elapsed-time accounting at actions as well as the fresh baseline on resume.
