# Day 15 — Inference Log Triage
**Phase:** Pythonic idioms + stdlib · **Time:** ~25 min

You just canary-deployed `churn-v4` next to `churn-v3`, and the on-call channel says error rates are up. The serving container writes one JSON object per request to a JSON Lines file (`requests.jsonl` in this folder). You want a quick triage function that tells you, per model, how many requests succeeded vs failed, and which error messages show up most.

## Task
Implement `summarize_requests(path, *, top_n=3)` in `solution.py`. It returns a `dict`:

```python
{"total": int, "by_model": {model: {"ok": int, "error": int}}, "top_errors": [(message, count), ...]}
```

- `path` is a `pathlib.Path`. Read it as text; each non-blank line is one JSON object. Skip blank (or whitespace-only) lines.
- Every record must have a `"model"` (str) and a `"status"` (int). A status **below 400** counts as `"ok"`, **400 or above** counts as `"error"`.
- `total` is the number of records (blank lines don't count).
- `by_model` maps each model name to a plain `dict` with **both** keys `"ok"` and `"error"`, even when one is `0`.
- `top_errors` counts the `"error"` field of failed records (status ≥ 400) that have one. Return the `top_n` most common as `(message, count)` tuples, highest count first; on a tie, the message seen first in the file comes first.
- Raise `ValueError` if a line isn't valid JSON, or a record is missing `"model"` or `"status"`. The message must include the **1-based line number**, e.g. `"line 4: ..."`.
- An empty file returns `{"total": 0, "by_model": {}, "top_errors": []}`.

### Sample
Using the `requests.jsonl` in this folder (8 records plus one blank line):

```python
summarize_requests(Path("requests.jsonl"))
# -> {
#   "total": 8,
#   "by_model": {
#     "churn-v3": {"ok": 2, "error": 1},
#     "churn-v4": {"ok": 1, "error": 3},
#     "fraud-v7": {"ok": 0, "error": 1},
#   },
#   "top_errors": [
#     ("CUDA out of memory", 2),
#     ("missing feature: tenure_months", 1),
#     ("model not loaded", 1),
#   ],
# }
```

(The `churn-v3` 404 has no `"error"` field, so it counts toward `by_model` but not `top_errors`.)

## Check your work
```bash
pytest -q
```

## JS → Python
`collections.Counter` is the built-in version of the `counts[key] = (counts[key] || 0) + 1` pattern you've written a hundred times in JS, and `.most_common(n)` does the sort-and-slice for you. `json.loads(line)` is `JSON.parse(line)`, and it raises `json.JSONDecodeError` (a subclass of `ValueError`) instead of `SyntaxError`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
