def parse_epochs(lines: list[str]) -> list[dict]:
    ...


def best_epoch(
    lines: list[str], metric: str = "val_loss", higher_is_better: bool = False
) -> int | None:
    ...
