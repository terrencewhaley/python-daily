# Hints (smallest nudge first)

1. A `for attempt in range(1, max_attempts + 1):` loop with `try: return fn()` inside does most of the work. A successful `return` exits the loop.
2. In `except retry_on:`, if this was the last attempt, a bare `raise` re-raises the current error. Otherwise sleep for `min(base_delay * 2 ** (attempt - 1), max_delay)`. Exceptions not in `retry_on` aren't caught, so they propagate automatically.
