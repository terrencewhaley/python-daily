def compare_predictions(
    ids: list[str],
    live: list[str | None],
    shadow: list[str | None],
) -> dict:
    ...


def format_report(result: dict) -> list[str]:
    ...
