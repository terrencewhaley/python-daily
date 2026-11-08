# Bonus — Retry with Backoff
**Phase:** Scripts & Tooling · **Time:** ~20 min

Your training pipeline pushes each finished model to the model registry. The registry's API is flaky: it sometimes drops the connection or times out, and one blip currently fails the whole nightly job.

## Task
Implement `retry_call(fn, ...)` in `solution.py`:
- Call `fn()`. If it works, return its result.
- On an exception listed in `retry_on`, wait and try again. The wait doubles each time (`base_delay`, then `2×`, `4×`…), capped at `max_delay`.
- After `max_attempts` total tries, re-raise the last error.
- Raise any other exception (e.g. `ValueError`) immediately, with no retry.
- Wait by calling the injected `sleep` function so tests run instantly.

## Check your work
```bash
pip install pytest   # once
pytest -q
```

## JS → Python
`except (ConnectionError, TimeoutError):` catches only those types. In JavaScript you'd check `err instanceof …` inside a `catch` and re-throw everything else; Python puts the filter in the syntax. The bare `*` in the signature makes every later argument keyword-only, like destructuring an options object `{ maxAttempts = 4 }`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
