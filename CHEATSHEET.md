# Python API cheatsheet

Running list of the Python pieces from each day's problem. Newest day at the bottom.

## Day 01 — Retry with backoff

| Python | What it does | JS equivalent |
|---|---|---|
| `for i in range(1, n + 1):` | Loops `i = 1, 2, ..., n`. The end value is **exclusive**, so `range(1, 5)` gives 1, 2, 3, 4 | `for (let i = 1; i <= n; i++)` |
| `try: ... except SomeError:` | Catches only that error type. Other errors pass through untouched | `try/catch` plus an `instanceof` check |
| `except (A, B):` | Catches either type. Pass a tuple, or a variable holding one | `if (!(e instanceof A \|\| e instanceof B)) throw e` |
| `raise` (bare, inside `except`) | Re-raises the error being handled, with the original traceback | `throw err` inside `catch` |
| `return` inside a loop | Exits the function and the loop immediately | same |
| `min(a, b)` / `max(a, b)` | Smaller / larger of the values | `Math.min` / `Math.max` |
| `2 ** n` | Exponent. Binds tighter than `*` | `2 ** n` |
| `def f(a, *, b=1, c=2):` | Bare `*` makes everything after it keyword-only | destructured options object `{ b = 1, c = 2 }` |
| `sleep=time.sleep` (function as a default arg) | Pass behavior in as a parameter so tests can swap in a fake (dependency injection) | passing a mock `fetch` or fake timer |
| `pytest -q` (run inside the day's folder) | Runs that folder's tests quietly | `jest` |
