from collections.abc import Collection


def parse_image(ref: str) -> tuple[str, str, str]:
    ...


def audit_images(
    refs: list[str], allowed_registries: Collection[str] = ("ghcr.io",)
) -> list[str]:
    ...
