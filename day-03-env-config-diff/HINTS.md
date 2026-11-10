# Hints (smallest nudge first)

1. Think in sets of keys. `old.keys()` and `new.keys()` support `-` (difference) and `&` (intersection) directly, and `set(ignore)` lets you subtract the ignored keys from each. `sorted(...)` turns a set into a sorted list.
2. For `"changed"`, a dict comprehension over the shared keys works well: `{k: (old[k], new[k]) for k in sorted(shared) if old[k] != new[k]}`. In `format_diff`, write a tiny helper like `show(key, value)` that returns `"***"` when `key.endswith(("_TOKEN", "_SECRET", "_PASSWORD"))`, and build each line with an f-string.
