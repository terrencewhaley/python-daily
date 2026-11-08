# python-daily

One practical, MLOps-flavored Python problem per weekday, on the road from JavaScript to MLOps.

| Days | Phase |
|---|---|
| 1–14 | Python fundamentals through a JS lens |
| 15–30 | Pythonic idioms + the standard library |
| 31–50 | Scripts and tooling |
| 51–75 | Data for ML (NumPy, pandas) |
| 76+ | MLOps building blocks |

## Each day
```
day-NN-<name>/
  README.md         the problem
  solution.py       your code goes here
  test_solution.py  run `pytest -q` in the folder
  HINTS.md          try not to peek, ask Claude Code instead
```

## Setup (once)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Daily loop
```bash
git pull
cd day-NN-<name> && pytest -q
```

Stuck? Ask Claude Code in VS Code, e.g. "I'm stuck on day 3".
