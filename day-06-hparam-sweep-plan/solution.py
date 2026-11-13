from typing import Any


def expand_grid(grid: dict[str, Any]) -> list[dict[str, Any]]:
    ...


def plan_sweep(
    grid: dict[str, Any], prefix: str = "sweep", max_runs: int = 50
) -> list[str]:
    ...
