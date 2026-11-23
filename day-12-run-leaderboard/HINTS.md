# Hints (smallest nudge first)

1. `divmod(seconds, 60)` returns `(minutes, seconds)` in one go; call it twice to get hours too. For the table, f-strings take a format spec after a colon: `f"{m:02d}"` pads to two digits, `f"{x:.2%}"` turns `0.9134` into `91.34%`.

2. Filter first (`r.get("val_acc") is not None`), then `sorted(..., key=lambda r: r["val_acc"], reverse=True)` and slice `[:top]`; Python's sort is stable, so ties keep input order. Compute `width = max(len(r["run"]) for r in shown)` and use a nested spec: `f"{name:<{width}}"` left-aligns, `f"{acc:>7.2%}"` right-aligns. `enumerate(shown, start=1)` gives you the rank.
