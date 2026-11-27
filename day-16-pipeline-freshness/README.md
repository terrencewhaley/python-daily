# Day 16 — Pipeline Freshness
**Phase:** Pythonic idioms + stdlib · **Time:** ~25 min

Your feature store is fed by a handful of scheduled batch jobs, and the orchestrator exports every run to a CSV (`pipeline_runs.csv` in this folder). If a job hasn't *succeeded* recently, the models downstream are training on stale features, even when the job is "running" or retrying. You want a freshness check that lists the jobs breaking their SLA, worst first, so it can page on-call.

## Task
Implement `stale_pipelines(path, *, now, max_age=timedelta(hours=24))` in `solution.py`. It returns a `list` of `(job, hours_since_success)` tuples.

- `path` is a `pathlib.Path` to a CSV with the header `job,status,started_at,finished_at`. Timestamps are ISO 8601 with a UTC offset, e.g. `2026-11-27T02:30:00+00:00`. `now` is a timezone-aware `datetime`.
- A job's **last success** is the latest `finished_at` among its rows with `status == "success"`. Rows aren't in time order.
- Ignore rows that aren't `"success"` when finding the last success, and skip any `"success"` row whose `finished_at` is blank or isn't a valid timestamp (don't crash).
- A job is **stale** if `now - last_success` is **strictly greater** than `max_age`. Exactly `max_age` old is still fresh.
- A job that appears in the file but has **no valid success at all** is stale, with `hours_since_success = float("inf")`.
- `hours_since_success` is the age in hours as a `float`, rounded to 1 decimal place.
- Sort by `hours_since_success`, **largest first**; on a tie, by job name A→Z.
- A CSV with only the header returns `[]`.

### Sample
```python
now = datetime(2026, 11, 27, 12, 0, tzinfo=timezone.utc)
stale_pipelines(Path("pipeline_runs.csv"), now=now)
# -> [("drift-report", inf), ("embeddings-refresh", 51.0), ("label-sync", 26.0)]
```

(`feature-backfill` succeeded 9.5 h ago. `model-eval`'s newest row has a bad timestamp, so its last valid success is exactly 24 h ago, which is still fresh. `drift-report` has never succeeded.)

## Check your work
```bash
pytest -q
```

## JS → Python
`csv.DictReader(f)` gives you each row as a dict keyed by the header, much like `papaparse` with `header: true`, and `datetime.fromisoformat(s)` is your `new Date(s)`, except it raises `ValueError` on junk instead of handing you an `Invalid Date`. `sorted(items, key=...)` replaces JS's `(a, b) => ...` comparator: you return *what to sort by* (a tuple works for tie-breakers) rather than comparing two items.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
