# Hints (smallest nudge first)

1. Normalize first: build a new dict where every value is a list (`isinstance(v, (list, tuple))` tells you which ones already are). After that, `expand_grid` is just "every combination of these lists". Try it by hand for a grid with one key, then two: what do you add to each existing combination when a new key comes along?

2. Start with `combos = [{}]` and, for each `key, values` in the grid, replace it with `[{**c, key: v} for c in combos for v in values]` (an empty `values` naturally empties everything). Or look up `itertools.product(*lists)` and rebuild each dict with `dict(zip(keys, combo))`. For `plan_sweep`, check `len(runs) > max_runs` before building any lines, then use `enumerate(runs, start=1)`, `f"{prefix}-{n:03d}"` and `" ".join(...)`.
