# Hints (smallest nudge first)

1. Open the file with `with path.open(newline="") as f:` and loop over `csv.DictReader(f)`. Keep a dict of `job -> latest success datetime`, but make sure every job you see gets an entry (start it at `None`) so never-succeeded jobs aren't lost. Wrap only `datetime.fromisoformat(row["finished_at"])` in `try/except ValueError: continue`.

2. Age in hours is `(now - last).total_seconds() / 3600`. Collect the stale `(job, round(hours, 1))` tuples (using `float("inf")` when last is `None`), then `sorted(results, key=lambda r: (-r[1], r[0]))`: negating the number sorts it largest first while the name stays A→Z. (`-inf` sorts fine.)
