## One-character tile: `FlipCharacter`

**Job:** Display one character as a split-flap tile, animating from the current character to a new one across a horizontal center seam.

### Caller input

Expose `property string character` as the target character; for example, `character: "4"`.

Keep the input boundary character-based rather than numeric: the caller formats its value and supplies exactly one displayable character, as it would for a single DotDigit position. For example, convert the number `4` to `"4"` before passing it in. The tile owns the previous character and animation progress; the caller does not supply character halves or animation frames. This is a proposed boundary, not a claim about DotDigit's exact API.

### A `3 → 4` change

Here, “upper” and “lower” mean clipped halves of the same full-size, aligned glyph—not separate smaller glyphs.

| Moment | Above the horizontal seam | Below the horizontal seam |
|---|---|---|
| **Before motion** | Upper half of **old `3`** | Lower half of **old `3`** |
| **During motion** | The old `3` upper flap folds down toward the seam, revealing the **new `4` upper half** behind it. | The **old `3` lower half** remains visible until the moving flap passes the seam; the flap's reverse shows the **new `4` lower half** as it unfolds downward over the old half. |
| **After settling** | Upper half of **new `4`** | Lower half of **new `4`** |

```text
BEFORE                  DURING (past midpoint)   AFTER
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ old 3: upper    │     │ new 4: upper    │     │ new 4: upper    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤ ← horizontal seam
│ old 3: lower    │     │ new 4 flap ↘    │     │ new 4: lower    │
│                 │     │ over old 3     │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

Keep the tile dimensions and glyph alignment fixed throughout the transition; only the flap rotates about the seam.
