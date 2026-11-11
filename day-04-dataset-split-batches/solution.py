def split_dataset(
    items: list[str], train: float = 0.8, val: float = 0.1
) -> tuple[list[str], list[str], list[str]]:
    ...


def batch_labels(items: list[str], batch_size: int) -> list[str]:
    ...
