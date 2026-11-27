import csv
from datetime import datetime, timedelta
from pathlib import Path


def stale_pipelines(
    path: Path,
    *,
    now: datetime,
    max_age: timedelta = timedelta(hours=24),
) -> list[tuple[str, float]]:
    ...
