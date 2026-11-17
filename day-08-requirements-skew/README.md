# Day 8 — Requirements Skew
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

Your churn model trains in one Docker image and serves from another, each built from its own `requirements.txt`. Last week predictions drifted because training used `pandas==2.2.2` while serving quietly ran `2.1.0`, and nobody noticed for days. You want a check in CI that parses both files and reports training/serving skew before the serving image ships.

## Task
**`parse_requirements(text)`** → `dict[str, str | None]`
- `text` is the full contents of a requirements file. Go line by line.
- Ignore blank lines, comment lines (starting with `#`), and option lines starting with `-` (like `-r base.txt` or `--index-url ...`). Drop inline comments: everything from `#` onward.
- The package **name** is everything before the first of these characters: `= < > ! ~ [`. Strip whitespace, lowercase it, and replace `_` with `-` (so `Scikit_Learn` → `scikit-learn`). Extras like `uvicorn[standard]==0.30.1` are named `uvicorn`.
- The **version** is the text after `==` (stripped) if the line pins with `==`; otherwise `None` (`torch>=2.3` and plain `torch` are both unpinned).
- If the same package name appears twice, raise `ValueError`.

**`compare_requirements(train_text, serve_text)`** → `dict` with exactly these keys:
- `"missing_in_serving"`: sorted names in training but not in serving. (Serving-only packages like `uvicorn` are fine.)
- `"version_mismatch"`: sorted list of `(name, train_version, serve_version)` tuples for packages that are pinned in **both** files to different versions.
- `"unpinned"`: sorted names that are unpinned in **either** file (each name once).

### Sample
```python
train = """
# training image
numpy==1.26.4
pandas == 2.2.2   # parquet support
scikit-learn==1.5.0
xgboost==2.0.3
torch>=2.3
-r base.txt
"""
serve = """
NumPy==1.26.4
pandas==2.1.0
Scikit_Learn==1.5.0
uvicorn[standard]==0.30.1
torch
"""

parse_requirements(train)
# {"numpy": "1.26.4", "pandas": "2.2.2", "scikit-learn": "1.5.0",
#  "xgboost": "2.0.3", "torch": None}

compare_requirements(train, serve)
# {"missing_in_serving": ["xgboost"],
#  "version_mismatch": [("pandas", "2.2.2", "2.1.0")],
#  "unpinned": ["torch"]}
```

## Check your work
```bash
pytest -q
```

## JS → Python
Python `set`s do in one operator what JS needs `filter` + `includes` for: `a - b` (difference), `a & b` (intersection), `a | b` (union). And `dict.keys()` already behaves like a set, so `train.keys() - serve.keys()` just works. `str.partition("#")` splits once and always gives back three parts, like `const [before] = s.split("#")` in JS but without the edge cases.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
