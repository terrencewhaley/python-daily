import json
from collections import Counter, defaultdict
from pathlib import Path


def summarize_requests(path: Path, *, top_n: int = 3) -> dict:
    ...
