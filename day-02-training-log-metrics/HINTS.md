# Hints (smallest nudge first)

1. Do `parse_epochs` first and have `best_epoch` call it. For each line, `line.split()` gives you tokens; `any(t.startswith("epoch=") for t in tokens)` tells you whether it's a metric line.
2. Build the dict inside a `try:` block (`k, v = t.split("=", 1)`, then `int(v)` if `k == "epoch"` else `float(v)`), and `continue` in `except ValueError:`. For `best_epoch`, filter to dicts with `metric in d`, then use `min(...)`/`max(...)` with `key=lambda d: d[metric]`. Both return the first item on a tie.
