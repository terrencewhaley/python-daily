from collections.abc import Collection


def diff_env(
    old: dict[str, str], new: dict[str, str], ignore: Collection[str] = ()
) -> dict:
    ...


def format_diff(
    old: dict[str, str], new: dict[str, str], ignore: Collection[str] = ()
) -> list[str]:
    ...
