# Split-flap transition checks

Completed by the mentor on 2026-10-19 at the learner's explicit request to complete lesson 0069 and proceed. These are executed state checks, not evidence of the learner independently writing tests.

## Reproduce

From `/home/hans/repos/linux-widget`, with the project environment activated:

```bash
python -m exercises.check_flip_transitions
```

The script loads the actual `FlipCharacter.qml` in a fresh offscreen QQuickView for each case, supplies initial character `3`, changes the public character property, and records settled-value changes and captures at animation starts. It uses the existing 400 ms per hinge (800 ms total) without changing application source. Busy requests occur 100 ms apart with an explicit running-state check; no temporary slowdown or duration restoration is needed for this programmatic version.

The existing `main.qml` preview also passed the same four state cases before the saved script was changed to load the tile directly. Loading the tile directly keeps this check useful after the manual preview is replaced with live time.

| Case | Actions | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| Startup | Fresh tile with input 3; do not change it | Settled 3; no animation starts | Settled 3; captures [] | Pass |
| Idle round trip | Request 4, wait for rest, request 3 | Settled 3 → 4 → 3; captures 4 then 3 | Settled 3 → 4 → 3; captures [4, 3] | Pass |
| Busy reversal | Request 4, then 3 while running | Finish captured 4, then catch up to 3 | Settled 3 → 4 → 3; captures [4, 3]; capture remained 4 during busy request | Pass |
| Latest request wins | Request 4, then 3 and 4 during the same fold | Finish at 4 without replaying intermediate 3 | Settled 3 → 4; captures [4]; no additional start during the observation period | Pass |

## Scope

The checks allow the event loop to run, wait for convergence with a bounded timeout, and observe another second afterward for unwanted replay. They exercise real QML property handlers and animations, rather than a Python copy of the transition algorithm. They do not judge visible glyph alignment, clipping artifacts, frame rate, real pointer routing, or desktop behavior. Visible folding still needs a rendered preview. The manual cases in lesson 0069 remain a useful visual checklist.

## Full-row visual checks — 2026-10-19

Step 7 was delegated to the mentor explicitly. Source reviewed: `experiments/flip_rollover.py`, loading the real `main.qml` and `FlipCharacter.qml`. The student launcher uses a fixed initial `11:59:59 PM`, requests `12:00:00 AM` after 2000 ms and `12:00:03 AM` after 2200 ms, then quits after 6000 ms. It has no repeating real-clock timer. Calling the static singleShot method through the timer instance is valid; that instance is not a repeating timer.

### Verification method

The mentor executed the student's launcher in an offscreen Qt/software-rendering process, attaching temporary diagnostic observers before its existing app.exec call. For the plain-rollover case only, the request_latest scheduling statement was omitted in memory; the saved launcher was not changed. The busy case executed both saved request schedules. Observers recorded each tile's settled-value changes, captured target at animation starts, running state at each request and final marker. Both cases also captured a rendered still after settling.

| Case | Expected | Actual evidence | Result |
| --- | --- | --- | --- |
| Initial scene | Complete 11:59:59 PM | Eight component values initialized to 11:59:59; five changing digit positions started on the rollover request | State initialization passes; no initial rendered still captured |
| Plain rollover | Settle at 12:00:00 AM | Hour units 1→2; minutes 59→00; seconds 59→00; unchanged hour tens and colons had no animation starts. Final marker AM | Pass for state ordering and final rendering |
| Busy arrival | Complete captured 00, then seconds units catch up to 3 | Second request arrived approximately 197 ms after the first; indices 1, 3, 4, 6 and 7 were still running, and seconds units capture remained 0. Its settled history was 9→0→3, with captures [0, 3]. Final row 12:00:03 AM | Pass for verified busy arrival and catch-up |
| Scheduled exit | Quit without manual closing | Both app.exec calls returned 0, approximately six seconds after startup (5.76 s plain, 6.01 s busy on the verification clock) | Pass |
| Settled appearance | Coherent glyphs, narrow colons, centered row and AM marker | Both offscreen stills inspected; settled glyph halves align and the full row fits | Pass for these stills only |
| Resize responsiveness and motion quality | Responsive input; no visible flashes or stutter while moving | Not exercised or established by these offscreen stills; no learner observation supplied | Not assessed |

Final renders: [plain rollover](../assets/verification/flip-rollover-2026-10-19-plain.png), [busy catch-up](../assets/verification/flip-rollover-2026-10-19-busy.png).

The actual request times were observed through property-change signals because the saved request functions do not yet print their values. The source schedules the two requests independently at 2000 and 2200 ms; the observed running-state check confirms this run really exercised busy arrival. Timer delivery is approximate, and a heavily stalled event loop can change that relationship.

These checks establish state coordination and settled software-rendered appearance. They do not establish native compositor animation quality, frame rate, GPU cost or smooth resizing. Product rendering-cost measurement and a visible responsiveness observation remain the next check; no independent learner testing or observation is inferred from the mentor's execution.

## Resource baseline and visible responsiveness — 2026-10-19

The learner reported completion and explicitly delegated the notes to the mentor. Source review confirms `run_transitions = True` guards both prepared request schedules, while the six-second quit remains unconditional. Both request functions now print their published values. The saved launcher was left unchanged.

No terminal measurements or specific visual observations from the learner were available in the chat. The following numbers were therefore measured by the mentor, not attributed to the learner.

### Mentor-measured offscreen baseline

Both runs used the same launcher and Qt offscreen/software backend. A temporary review wrapper changed only the run_transitions value in memory for the idle case, checked the app.exec return value and final requested time, and otherwise executed the saved source. GNU Time measured the whole process, including Python/Qt startup and the small review wrapper. Runs were sequential, without resize work.

| Mode | Elapsed seconds | User CPU seconds | System CPU seconds | Total CPU seconds | Peak RSS, GNU Time KB | Exit |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Idle, transitions disabled in memory | 6.23 | 0.15 | 0.02 | 0.17 | 70932 | 0; final request 11:59:59 PM |
| Prepared transitions enabled | 6.05 | 0.28 | 0.03 | 0.31 | 71224 | 0; final request 12:00:03 AM |

The transition run printed both 12:00:00 AM and 12:00:03 AM. CPU time is much smaller than the roughly six-second process lifetime because waiting is not processor work. This single pair showed 0.14 seconds more process CPU time and 292 KB more peak RSS with transitions enabled; short-run noise, startup and renderer differences prevent treating those deltas as an isolated animation cost or a performance guarantee. No optimization is justified from this pair alone.

This is an offscreen/software baseline. It does not measure the learner's native window-system rendering path, GPU usage, frame rate or frame pacing. The learner's generic completion report is recorded, but there is no specific supplied resize/close-during-motion observation to quote; that visual observation remains unverified rather than being invented in these notes.

### Functional milestone review

Milestone 06 is accepted as the local normal-window split-flap prototype on 2026-10-19: reusable aligned character halves, captured two-stage folds, startup initialization, automatic changes, latest-request catch-up, a complete live time row, optional format marker and repeatable prepared-input checks are implemented. Four isolated state cases and full-row rollover/busy-arrival checks pass; settled offscreen renders were inspected. The student-authored prepared-input launcher and static-separator extension provide practical transfer evidence. Independent retention, native motion/resize assessment and longer-running resource profiling remain review items, including milestone 14; acceptance does not imply universal desktop support or measured native animation smoothness.
