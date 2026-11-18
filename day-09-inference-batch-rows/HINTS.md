# Hints (smallest nudge first)

1. Loop with `for n, line in enumerate(lines, start=1)` so you always know the line number, and `continue` on blank lines (`not line.strip()` is truthy for them). Keep `header` as `None` until you've seen the first non-blank line; that tells you whether the current line is the header or a row.

2. Values: `[v.strip() or None for v in line.split(",")]` (an empty string is falsy, so `or None` swaps it). Compare `len(values)` with `len(header)` and append an f-string error on mismatch; otherwise `records.append(dict(zip(header, values)))`. Duplicate header check: compare `len(set(header))` with `len(header)`. For `to_columns`, a dict comprehension with a list comprehension inside: `{name: [...] for name in header}`.
