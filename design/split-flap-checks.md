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
