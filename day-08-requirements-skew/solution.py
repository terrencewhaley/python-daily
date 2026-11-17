from typing import Any


def parse_requirements(text: str) -> dict[str, str | None]:
    ...


def compare_requirements(train_text: str, serve_text: str) -> dict[str, list[Any]]:
    ...
