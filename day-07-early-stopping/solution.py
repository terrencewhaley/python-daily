def loss_spikes(losses: list[float | None], ratio: float = 1.5) -> list[int]:
    ...


def early_stop(
    losses: list[float | None], patience: int = 3, min_delta: float = 0.0
) -> tuple[int | None, int | None]:
    ...
