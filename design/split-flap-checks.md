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
