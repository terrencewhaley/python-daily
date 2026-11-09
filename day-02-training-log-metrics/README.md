# Day 2 — Training Log Metrics
**Phase:** Python fundamentals through a JS lens · **Time:** ~20 min

Your nightly training job writes a plain-text log. Mixed in with checkpoint and warning noise are one-line epoch summaries like `epoch=3 loss=0.41 val_loss=0.47 val_acc=0.84`. Before promoting a model you want to pull those metrics out and find the best epoch, without opening the log by hand.

## Task
Implement two functions in `solution.py`:

**`parse_epochs(lines)`** → `list[dict]`
- A line is a metric line if one of its whitespace-separated tokens starts with `epoch=`. Ignore every other line.
- From a metric line, keep every `key=value` token. `epoch` becomes an `int`; every other value becomes a `float`. Tokens without `=` (timestamps, `INFO`) are ignored.
- If any value on a metric line can't be converted (e.g. `loss=oops`), skip that whole line.
- Return the dicts in log order.

**`best_epoch(lines, metric="val_loss", higher_is_better=False)`** → `int | None`
- Return the `epoch` number with the best value of `metric` (lowest by default, highest when `higher_is_better=True`).
- Epochs missing that metric don't count. On a tie, the earlier epoch wins.
- Return `None` if no epoch has the metric.

### Sample
```python
log = [
    "2026-11-09 02:00:01 INFO starting run fraud-detector",
    "2026-11-09 02:04:10 INFO epoch=1 loss=0.912 val_loss=0.884 val_acc=0.71",
    "2026-11-09 02:04:11 INFO saved checkpoint ckpt-1",
    "2026-11-09 02:08:22 INFO epoch=2 loss=0.533 val_loss=0.561 val_acc=0.80",
    "2026-11-09 02:12:30 WARNING epoch=3 loss=oops val_loss=0.6",
    "2026-11-09 02:16:41 INFO epoch=4 loss=0.301 val_loss=0.598 val_acc=0.83",
]

parse_epochs(log)
# [{'epoch': 1, 'loss': 0.912, 'val_loss': 0.884, 'val_acc': 0.71},
#  {'epoch': 2, 'loss': 0.533, 'val_loss': 0.561, 'val_acc': 0.8},
#  {'epoch': 4, 'loss': 0.301, 'val_loss': 0.598, 'val_acc': 0.83}]

best_epoch(log)                                         # 2
best_epoch(log, metric="val_acc", higher_is_better=True) # 4
```

## Check your work
```bash
pytest -q
```

## JS → Python
`key, value = token.split("=", 1)` is Python's array destructuring (`const [key, value] = token.split("=")`), and `int("oops")` raises `ValueError` instead of quietly returning `NaN` like `parseInt` does, so you catch it with `try/except`. `max(items, key=...)` works like a `reduce` that keeps the winner, with no comparator boilerplate.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
