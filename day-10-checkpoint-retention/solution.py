def parse_checkpoint(name: str) -> tuple[int, float]:
    ...


def plan_cleanup(
    names: list[str], keep_best: int = 2, keep_last: int = 1
) -> tuple[list[str], list[str]]:
    ...
