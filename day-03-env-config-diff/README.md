# Day 3 — Env Config Diff
**Phase:** Python fundamentals through a JS lens · **Time:** ~20 min

You're about to promote the `fraud-detector` serving deployment from staging to prod. Last time, prod broke because someone forgot to copy `MODEL_VERSION` over. Before every promotion you now want a quick diff of the two environments' variables, with secrets masked so the diff can be pasted into Slack safely.

## Task
Implement two functions in `solution.py`:

**`diff_env(old, new, ignore=())`** → `dict`
- `old` and `new` are `dict[str, str]` of env vars. `ignore` is a collection of keys to leave out of the diff entirely.
- Return a dict with exactly three keys:
  - `"added"`: keys only in `new`, sorted alphabetically (a `list`).
  - `"removed"`: keys only in `old`, sorted alphabetically (a `list`).
  - `"changed"`: a `dict` mapping each key present in both but with a different value to the tuple `(old_value, new_value)`.
- Neither input dict may be modified.

**`format_diff(old, new, ignore=())`** → `list[str]`
- Build on `diff_env` and return human-readable lines in this order: all added, then removed, then changed (each group alphabetical by key):
  - added: `+ KEY=new_value`
  - removed: `- KEY`
  - changed: `~ KEY: old_value -> new_value`
- **Mask secrets:** if a key ends with `_TOKEN`, `_SECRET` or `_PASSWORD`, show its value(s) as `***`.
- If there are no differences, return `["no changes"]`.

### Sample
```python
staging = {
    "MODEL_NAME": "fraud-detector",
    "MODEL_VERSION": "v8",
    "LOG_LEVEL": "DEBUG",
    "REGISTRY_TOKEN": "stg-abc123",
    "BATCH_SIZE": "32",
}
prod = {
    "MODEL_NAME": "fraud-detector",
    "LOG_LEVEL": "INFO",
    "REGISTRY_TOKEN": "prd-zzz999",
    "BATCH_SIZE": "32",
    "WORKERS": "4",
}

diff_env(staging, prod)
# {'added': ['WORKERS'],
#  'removed': ['MODEL_VERSION'],
#  'changed': {'LOG_LEVEL': ('DEBUG', 'INFO'),
#              'REGISTRY_TOKEN': ('stg-abc123', 'prd-zzz999')}}

format_diff(staging, prod)
# ['+ WORKERS=4',
#  '- MODEL_VERSION',
#  '~ LOG_LEVEL: DEBUG -> INFO',
#  '~ REGISTRY_TOKEN: *** -> ***']

format_diff(staging, prod, ignore={"LOG_LEVEL", "REGISTRY_TOKEN"})
# ['+ WORKERS=4', '- MODEL_VERSION']
```

## Check your work
```bash
pytest -q
```

## JS → Python
Python's `dict.keys()` behaves like a real set, so `new.keys() - old.keys()` gives you the added keys in one expression (in JS you'd write `Object.keys(b).filter(k => !(k in a))`). `&` is intersection, `|` is union. And `str.endswith` takes a tuple, so you can check several suffixes at once.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
