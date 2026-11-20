import copy


def parse_value(text: str) -> bool | int | float | None | str:
    ...


def apply_overrides(config: dict, overrides: list[str]) -> dict:
    ...
