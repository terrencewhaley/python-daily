# Hints (smallest nudge first)

1. Handle one line at a time: first throw away the comment part (`line.partition("#")[0]`), strip it, and `continue` if what's left is empty or starts with `-`. For `compare_requirements`, think in sets of package names: which set operation means "in training but not in serving"?

2. Name: loop `for i, ch in enumerate(line)` and `break` at the first `ch in "=<>!~["`, then slice `line[:i]` (watch the case where no such character exists, like plain `torch`). Version: `before, sep, after = line.partition("==")`; an empty `sep` means unpinned. In compare, parse both files, then use `train.keys() - serve.keys()` for missing, loop over `sorted(train.keys() & serve.keys())` for mismatches, and build an "unpinned" set from each dict separately before joining them with `|`.
