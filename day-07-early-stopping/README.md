# Day 7 — Early Stopping
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

Your sentiment-model training job runs for a fixed 50 epochs, even when validation loss stopped improving at epoch 12, and once a bad learning rate made the loss explode halfway through without anyone noticing. You want two small checks the training loop can call after each epoch: one that flags sudden loss spikes, and one that decides when to stop early.

## Task
Both functions take `losses`, a list where item 0 is **epoch 1**. An item may be `None` (that epoch's eval didn't run). A loss of `0.0` is a real value, not a missing one.

**`loss_spikes(losses, ratio=1.5)`** → `list[int]`
- Compare each epoch with the one right before it. It's a spike if `loss > previous * ratio` (strictly greater).
- If either loss in a pair is `None`, skip that pair.
- Return the spiking epoch numbers (1-based), in order. Fewer than two epochs → `[]`.

**`early_stop(losses, patience=3, min_delta=0.0)`** → `tuple[int | None, int | None]` as `(stop_epoch, best_epoch)`
- Walk the epochs in order, skipping `None` entirely (it neither improves nor counts against patience).
- The first real loss becomes the best. After that, a loss is an **improvement** only if `loss < best - min_delta`: it becomes the new best and the "no improvement" count resets to 0. Otherwise the count goes up by 1.
- When the count reaches `patience`, stop: `stop_epoch` is that epoch's number.
- If it never stops, `stop_epoch` is `None`. `best_epoch` is the epoch of the best loss seen up to the stop (or the end), or `None` if there were no real losses.
- Raise `ValueError` if `patience` is less than 1.

### Sample
```python
loss_spikes([0.9, 0.7, 1.4, 0.8, 0.85, 2.0])
# [3, 6]          (1.4 > 0.7 * 1.5, and 2.0 > 0.85 * 1.5)

val = [0.9, 0.7, 0.72, 0.69, 0.71, 0.70, 0.73]
early_stop(val, patience=3)
# (7, 4)          best was 0.69 at epoch 4, then 3 epochs without beating it

early_stop(val, patience=3, min_delta=0.02)
# (5, 2)          0.69 doesn't beat 0.70 by more than 0.02, so epoch 2 stays best

early_stop([0.5, 0.4, 0.3])
# (None, 3)       still improving, keep training
```

## Check your work
```bash
pytest -q
```

## JS → Python
`zip(losses, losses[1:])` pairs each item with its neighbour, like `losses.slice(1).map((cur, i) => [losses[i], cur])` in JS, and `enumerate(..., start=1)` gives you 1-based numbering without an index variable. Watch truthiness: like JS, `0.0` is falsy in Python, so test for missing values with `x is None`, not `if not x`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
