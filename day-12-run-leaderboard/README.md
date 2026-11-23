# Day 12 — Run Leaderboard
**Phase:** Python fundamentals through a JS lens · **Time:** ~20 min

Every morning you paste the results of last night's churn-model experiments into the team's Slack channel, and lining up run names, accuracies and durations by hand is tedious and error-prone. You want a function that turns the raw run records into a tidy, aligned top-N leaderboard you can drop into a code block.

## Task
Implement two functions in `solution.py`:

**`format_duration(seconds)`** → `str`
- Under 60 s: `"45s"`. Under an hour: `"3m 07s"`. Otherwise: `"1h 02m 05s"` (hours are not capped, so `90061` → `"25h 01m 01s"`).
- Minutes and seconds after the first unit are always two digits.
- Raise `ValueError` for negative input.

**`leaderboard(runs, top=3)`** → `list[str]`
- Each run is a dict with `"run"` (name), `"val_acc"` (a float from 0 to 1, or `None`/missing if the run crashed) and `"seconds"`.
- Skip runs whose `val_acc` is `None` or missing.
- Rank by `val_acc`, highest first. On a tie, the run that appears earlier in `runs` ranks higher. Keep only the first `top`.
- Each line is: rank, `". "`, the name left-aligned and padded to the longest name **among the shown rows**, two spaces, the accuracy as a percentage with 2 decimals right-aligned in 7 characters, two spaces, then the formatted duration.
- Return `[]` if no run qualifies. Don't modify `runs`.

### Sample
```python
runs = [
    {"run": "lr-3e-4",        "val_acc": 0.9134, "seconds": 3725},
    {"run": "baseline",       "val_acc": 0.8872, "seconds": 2410},
    {"run": "lr-1e-3-warmup", "val_acc": 0.9201, "seconds": 4012},
    {"run": "crashed-oom",    "val_acc": None,   "seconds": 95},
    {"run": "dropout-0.3",    "val_acc": 0.9134, "seconds": 59},
]

format_duration(187)   # '3m 07s'

leaderboard(runs)
# ['1. lr-1e-3-warmup   92.01%  1h 06m 52s',
#  '2. lr-3e-4          91.34%  1h 02m 05s',
#  '3. dropout-0.3      91.34%  59s']
```

## Check your work
```bash
pytest -q
```

## JS → Python
f-string format specs replace a pile of JS helpers: `f"{s:02d}"` is `String(s).padStart(2, "0")`, `f"{name:<14}"` is `name.padEnd(14)`, and `f"{acc:.2%}"` is `(acc * 100).toFixed(2) + "%"`. `divmod(a, b)` gives you `Math.floor(a / b)` and `a % b` as one tuple you can unpack.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
