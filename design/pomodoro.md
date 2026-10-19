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
