# Hints (smallest nudge first)

1. `for req_id, a, b in zip(ids, live, shadow):` gives you one request at a time, already unpacked. Check the lengths *before* the loop, because `zip` silently stops at the shortest list. For duplicates, compare `len(set(ids))` with `len(ids)`.

2. Inside the loop: if `a is None or b is None`, append to `skipped` and `continue`. Otherwise bump `compared`; if `a == b` bump `agree`, else append the id and do `flips[(a, b)] = flips.get((a, b), 0) + 1`. In the report, `f"{agree / compared:.1%}"` won't quite match the format, so compute `agree / compared * 100` and use `:.1f`; loop with `for (a, b), n in result["flips"].items():` and finish with `", ".join(result["skipped"])`.
