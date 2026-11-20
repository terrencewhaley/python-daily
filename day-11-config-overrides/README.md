# Day 11 — Config Overrides
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

Your churn-model training script loads a nested `config` dict, and teammates keep editing the YAML file just to try a different learning rate, then forgetting to change it back. You want Hydra-style command-line overrides instead: `python train.py optimizer.lr=0.001 epochs=50`. Each override is a dotted key path and a value given as text, and the value needs to come out as the right Python type.

## Task
**`parse_value(text)`** → `bool | int | float | None | str`
- Strip surrounding whitespace first.
- `true` / `false` (any case) → `True` / `False`.
- `null` / `none` (any case) → `None`.
- Anything `int()` accepts → `int`; otherwise anything `float()` accepts → `float` (so `"1e-3"` → `0.001`).
- Wrapped in matching quotes (`"..."` or `'...'`) → the text inside, as a `str`, untouched (so `'"042"'` → `"042"`, not `42`).
- Everything else → the stripped `str`.

**`apply_overrides(config, overrides)`** → `dict`
- Each override is `"<dotted.key>=<value>"`. Split on the **first** `=`; strip the key; parse the value with `parse_value`.
- Walk the dotted path into nested dicts, creating any that are missing, and set the last key.
- Overrides apply in order, so a later one wins.
- **Don't mutate** `config` (or any dict inside it). Return a new dict.
- Raise `ValueError` for: no `=`, an empty key, an empty path segment (`a..b`, `.a`, `a.`), or a path that runs *through* a non-dict value (e.g. `optimizer.lr.x=1` when `lr` is `0.01`).

### Sample
```python
parse_value(" 50 ")      # -> 50
parse_value("TRUE")      # -> True
parse_value("'0.5'")     # -> "0.5"

config = {
    "model": {"name": "churn-xgb", "max_depth": 6},
    "optimizer": {"lr": 0.01},
    "epochs": 20,
}
apply_overrides(config, [
    "optimizer.lr=0.001",
    "epochs=50",
    "model.max_depth = 8",
    "data.shuffle=true",
    'run_name="042"',
])
# -> {
#     "model": {"name": "churn-xgb", "max_depth": 8},
#     "optimizer": {"lr": 0.001},
#     "epochs": 50,
#     "data": {"shuffle": True},
#     "run_name": "042",
# }
# ...and config itself is unchanged.
```

## Check your work
```bash
pytest -q
```

## JS → Python
`key, _, raw = item.partition("=")` splits on the first `=` only (JS's `split("=")` would also break `url=a=b`), and `d.setdefault(k, {})` is `d[k] ??= {}` in one call that also returns the value. For a deep copy, `copy.deepcopy(config)` plays the role of `structuredClone(config)`; `dict(config)` is only a shallow `{...config}`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
