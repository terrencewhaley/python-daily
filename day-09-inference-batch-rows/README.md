# Day 9 — Inference Batch Rows
**Phase:** Python fundamentals through a JS lens · **Time:** ~20 min

Every night an upstream team drops a CSV of customer feature rows for your churn model's batch-inference job. Last week one row had a stray comma, the whole job crashed at 3 a.m., and nobody got predictions. You want the job to keep the good rows, report the bad ones with their line numbers, and hand the model a column-oriented view of the data.

## Task
Implement two functions in `solution.py`:

**`parse_batch(lines)`** → `tuple[list[str], list[dict], list[str]]` as `(header, records, errors)`
- `lines` is the file's lines (like `text.splitlines()`). Line numbers are **1-based positions in `lines`**, counting every line.
- Skip blank (whitespace-only) lines everywhere — but they still count toward line numbers.
- The first non-blank line is the header: split on `,` and strip each name. If a name appears twice, raise `ValueError`.
- Every later non-blank line is a row: split on `,` and strip each value. An empty value becomes `None`.
- If a row has a different number of values than the header, don't keep it; add the error `"line N: expected X fields, got Y"` instead.
- Otherwise the record is a dict mapping each header name to its value (values stay strings).
- No non-blank lines at all → `([], [], [])`.

**`to_columns(header, records)`** → `dict[str, list]`
- Return one key per header name (in header order) whose value is the list of that column's values across all records, in record order.
- No records → every column maps to `[]`.

### Sample
```python
lines = [
    "customer_id, tenure_months, plan, monthly_spend",
    "c-101, 14, pro, 49.0",
    "c-102, 3, , 12.5",
    "",
    "c-103, 27, team, 120.0, extra",
    "c-104, 1, free, 0",
]

header, records, errors = parse_batch(lines)
# header  -> ["customer_id", "tenure_months", "plan", "monthly_spend"]
# records -> [
#   {"customer_id": "c-101", "tenure_months": "14", "plan": "pro", "monthly_spend": "49.0"},
#   {"customer_id": "c-102", "tenure_months": "3", "plan": None, "monthly_spend": "12.5"},
#   {"customer_id": "c-104", "tenure_months": "1", "plan": "free", "monthly_spend": "0"},
# ]
# errors  -> ["line 5: expected 4 fields, got 5"]

to_columns(header, records)
# {"customer_id": ["c-101", "c-102", "c-104"],
#  "tenure_months": ["14", "3", "1"],
#  "plan": ["pro", None, "free"],
#  "monthly_spend": ["49.0", "12.5", "0"]}
```

## Check your work
```bash
pytest -q
```

## JS → Python
`enumerate(lines, start=1)` gives you `(line_number, line)` pairs, like `lines.forEach((line, i) => ...)` but already 1-based. And `dict(zip(header, values))` builds a record in one go, the Python version of `Object.fromEntries(header.map((h, i) => [h, values[i]]))`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
