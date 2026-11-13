# Day 6 — Hyperparameter Sweep Plan
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

You're about to launch a hyperparameter sweep for the churn model on a shared GPU cluster. The sweep is described as a small grid (each hyperparameter → the values to try), and last week someone fat-fingered a grid that expanded to 400 runs and ate the team's GPU quota. Before anything is submitted you want to expand the grid into individual run configs, give each run a name, and refuse to plan anything over budget.

## Task
Implement two functions in `solution.py`:

**`expand_grid(grid)`** → `list[dict]`
- `grid` maps each hyperparameter name to the values to try (a `list` or `tuple`).
- A value that is **not** a list or tuple (e.g. `"optimizer": "adam"`) is a fixed setting: treat it as a one-item list.
- Return one dict per combination (the cartesian product). Keys keep the grid's order, and the **last** key varies fastest (like nested `for` loops in key order).
- If any hyperparameter has an empty list of values → `[]`.
- An empty grid `{}` → `[{}]` (exactly one run, with no overrides).
- Don't modify `grid`.

**`plan_sweep(grid, prefix="sweep", max_runs=50)`** → `list[str]`
- Expand the grid, then return one line per run: the run name followed by each `key=value`, separated by single spaces.
- Run names are `{prefix}-{n}` with `n` counting from **1**, zero-padded to 3 digits (`sweep-001`).
- Values are shown with plain `str()` (`0.001`, `True`, `adam`).
- A run with no params is just its name (no trailing space).
- Raise `ValueError` if the number of runs would exceed `max_runs` (exactly `max_runs` is fine). Don't return a partial plan.

### Sample
```python
grid = {"lr": [0.01, 0.001], "batch_size": [32, 64], "optimizer": "adam"}

expand_grid(grid)
# [
#   {"lr": 0.01,  "batch_size": 32, "optimizer": "adam"},
#   {"lr": 0.01,  "batch_size": 64, "optimizer": "adam"},
#   {"lr": 0.001, "batch_size": 32, "optimizer": "adam"},
#   {"lr": 0.001, "batch_size": 64, "optimizer": "adam"},
# ]

plan_sweep(grid, prefix="churn")
# [
#   "churn-001 lr=0.01 batch_size=32 optimizer=adam",
#   "churn-002 lr=0.01 batch_size=64 optimizer=adam",
#   "churn-003 lr=0.001 batch_size=32 optimizer=adam",
#   "churn-004 lr=0.001 batch_size=64 optimizer=adam",
# ]

plan_sweep({"lr": [0.1, 0.01, 0.001], "seed": [1, 2]}, max_runs=5)
# ValueError (6 runs > 5)
```

## Check your work
```bash
pytest -q
```

## JS → Python
`dict(zip(keys, values))` is Python's `Object.fromEntries(keys.map((k, i) => [k, values[i]]))` in one call, and `f"{n:03d}"` replaces JS's `String(n).padStart(3, "0")`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
