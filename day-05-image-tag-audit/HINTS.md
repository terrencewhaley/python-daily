# Hints (smallest nudge first)

1. In `parse_image`, deal with the registry *before* you go looking for a tag. Once you've peeled off the registry segment (if any), only the last remaining segment can hold a `:` tag, so `localhost:5000` never confuses you. `str.split("/")` gives you a list you can slice: `parts[0]`, `parts[1:]`, `parts[-1]`.

2. For the tag: `if ":" in last: name, tag = last.rsplit(":", 1)`. For the audit, loop with `for n, ref in enumerate(refs, start=1):`, `continue` on `not ref.strip()`, and wrap `parse_image` in `try/except ValueError` so a bad ref gets one "invalid reference" line and the loop moves on.
