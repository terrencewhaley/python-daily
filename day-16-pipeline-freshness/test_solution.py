import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

from solution import stale_pipelines

HERE = Path(__file__).parent
NOW = datetime(2026, 11, 27, 12, 0, tzinfo=timezone.utc)
HEADER = "job,status,started_at,finished_at"


def write_csv(tmp_path, *rows):
    p = tmp_path / "runs.csv"
    p.write_text("\n".join([HEADER, *rows]) + "\n")
    return p


def test_sample_file():
    result = stale_pipelines(HERE / "pipeline_runs.csv", now=NOW)
    assert [job for job, _ in result] == ["drift-report", "embeddings-refresh", "label-sync"]
    assert math.isinf(result[0][1])
    assert result[1:] == [("embeddings-refresh", 51.0), ("label-sync", 26.0)]


def test_header_only_returns_empty(tmp_path):
    assert stale_pipelines(write_csv(tmp_path), now=NOW) == []


def test_exactly_max_age_is_fresh_but_one_minute_more_is_stale(tmp_path):
    p = write_csv(
        tmp_path,
        "on-time,success,2026-11-26T11:00:00+00:00,2026-11-26T12:00:00+00:00",
        "late,success,2026-11-26T11:00:00+00:00,2026-11-26T11:59:00+00:00",
    )
    assert stale_pipelines(p, now=NOW) == [("late", 24.0)]


def test_bad_or_blank_timestamps_are_skipped_and_never_succeeded_is_inf(tmp_path):
    p = write_csv(
        tmp_path,
        "ingest,success,2026-11-27T00:00:00+00:00,yesterday-ish",
        "ingest,success,2026-11-27T00:00:00+00:00,",
        "ingest,failed,2026-11-27T00:00:00+00:00,2026-11-27T00:10:00+00:00",
    )
    result = stale_pipelines(p, now=NOW)
    assert len(result) == 1
    job, hours = result[0]
    assert job == "ingest" and math.isinf(hours)


def test_custom_max_age_rounding_and_sorting(tmp_path):
    p = write_csv(
        tmp_path,
        "zeta,success,2026-11-27T05:00:00+00:00,2026-11-27T06:00:00+00:00",
        "alpha,success,2026-11-27T05:00:00+00:00,2026-11-27T06:00:00+00:00",
        "fresh,success,2026-11-27T10:00:00+00:00,2026-11-27T11:00:00+00:00",
        "odd,success,2026-11-27T02:00:00+00:00,2026-11-27T02:40:00+00:00",
    )
    assert stale_pipelines(p, now=NOW, max_age=timedelta(hours=2)) == [
        ("odd", 9.3),
        ("alpha", 6.0),
        ("zeta", 6.0),
    ]
