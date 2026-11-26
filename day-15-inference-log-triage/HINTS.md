# Hints (smallest nudge first)

1. `for lineno, line in enumerate(path.read_text().splitlines(), start=1):` gives you the line number for free. Wrap just the `json.loads(line)` call in `try/except json.JSONDecodeError` and re-raise as `ValueError(f"line {lineno}: ...")`. Check for the required keys with `"model" not in record`.

2. Keep two counters: `by_model = defaultdict(Counter)` so `by_model[record["model"]]["ok"] += 1` just works for new models, and `errors = Counter()` for messages. At the end, build plain dicts with `{m: {"ok": c["ok"], "error": c["error"]} for m, c in by_model.items()}` (a missing `Counter` key reads as `0`), and use `errors.most_common(top_n)` for the list.
