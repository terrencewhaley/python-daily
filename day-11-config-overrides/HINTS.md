# Hints (smallest nudge first)

1. For `parse_value`, order matters: check the quotes and the special words before trying numbers, and try `int(...)` before `float(...)` (each in its own `try` / `except ValueError`). `"true".lower()` makes the case check easy.

2. For `apply_overrides`, start with `result = copy.deepcopy(config)` so nothing you touch is shared with the original. For each override, `key, sep, raw = item.partition("=")` (an empty `sep` means there was no `=`), then `*parents, last = key.split(".")`. Walk with a `node` variable: for each parent, `node = node.setdefault(part, {})`, and raise if what you got back isn't a `dict` (`isinstance(node, dict)`). Empty segments show up as `""` in the split list.
