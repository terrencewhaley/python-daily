# Day 13 — Shadow Deploy Diff
**Phase:** Python fundamentals through a JS lens · **Time:** ~20 min

You're rolling out v8 of the `fraud-detector` model in **shadow mode**: every transaction still gets the live v7 prediction, but v8 scores it too and its answer is only logged. Before you flip traffic to v8, you want to know how often the two models agree, which kinds of disagreements happen (does v8 suddenly flag lots of `legit` as `fraud`?), and which requests got no prediction because one of the models errored.

## Task
Implement two functions in `solution.py`:

**`compare_predictions(ids, live, shadow)`** → `dict`
- `ids`, `live` and `shadow` are parallel lists: position `i` is request `ids[i]`, with the live model's label `live[i]` and the shadow model's label `shadow[i]`. Labels are strings; `None` means that model failed on that request.
- Raise `ValueError` if the three lists don't all have the same length, or if an id appears more than once.
- Return a dict with exactly these keys:
  - `"compared"`: number of requests where **both** labels are present.
  - `"agree"`: how many of those have equal labels.
  - `"agreement"`: `agree / compared` rounded to 4 decimals, or `None` if nothing was compared.
  - `"disagreements"`: list of ids where the labels differ, in input order.
  - `"flips"`: dict mapping `(live_label, shadow_label)` tuples to how many times that disagreement happened. Keys appear in the order each flip was **first seen**.
  - `"skipped"`: list of ids where either label is `None`, in input order.
- Don't modify the input lists.

**`format_report(result)`** → `list[str]`
- Takes the dict from `compare_predictions` and returns lines:
  - First: `"agreement: {agree}/{compared} ({pct}%)"` with the percentage to 1 decimal, e.g. `"agreement: 4/6 (66.7%)"`. If nothing was compared: `"agreement: n/a (0 compared)"`.
  - Then one line per flip, in the dict's order: `"flip {live} -> {shadow}: {count}"`.
  - Last, only if anything was skipped: `"skipped {n}: {ids}"` with the ids joined by `", "`.

### Sample
```python
ids    = ["tx-101", "tx-102", "tx-103", "tx-104", "tx-105", "tx-106", "tx-107"]
live   = ["legit",  "fraud",  "legit",  "legit",  None,     "review", "legit"]
shadow = ["legit",  "fraud",  "fraud",  "legit",  "legit",  "fraud",  "fraud"]

result = compare_predictions(ids, live, shadow)
# {'compared': 6, 'agree': 3, 'agreement': 0.5,
#  'disagreements': ['tx-103', 'tx-106', 'tx-107'],
#  'flips': {('legit', 'fraud'): 2, ('review', 'fraud'): 1},
#  'skipped': ['tx-105']}

format_report(result)
# ['agreement: 3/6 (50.0%)',
#  'flip legit -> fraud: 2',
#  'flip review -> fraud: 1',
#  'skipped 1: tx-105']
```

## Check your work
```bash
pytest -q
```

## JS → Python
`zip(ids, live, shadow)` walks three lists in lockstep and hands you a tuple you can unpack in the `for` line, which replaces JS's `ids.forEach((id, i) => { const a = live[i]; ... })`. And unlike JS objects, Python dicts can use a tuple like `("legit", "fraud")` as a key directly, no `` `${a}->${b}` `` string-key trick needed; they also remember insertion order, like a JS `Map`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
