import pytest

from solution import audit_images, parse_image


@pytest.mark.parametrize(
    "ref, expected",
    [
        ("ghcr.io/acme/fraud-detector:v7", ("ghcr.io", "acme/fraud-detector", "v7")),
        ("redis:7.2", ("docker.io", "redis", "7.2")),
        ("localhost:5000/models/churn:dev", ("localhost:5000", "models/churn", "dev")),
        ("acme/feature-store", ("docker.io", "acme/feature-store", "latest")),
        ("  nginx  ", ("docker.io", "nginx", "latest")),
        ("123.dkr.ecr.us-east-1.amazonaws.com/ml/batch-scorer:2026.11.12",
         ("123.dkr.ecr.us-east-1.amazonaws.com", "ml/batch-scorer", "2026.11.12")),
        ("localhost/scratch", ("localhost", "scratch", "latest")),
    ],
)
def test_parse_image(ref, expected):
    assert parse_image(ref) == expected


@pytest.mark.parametrize("ref", ["", "   ", "acme/feature-store:", "ghcr.io/acme/x:"])
def test_parse_image_rejects_bad_refs(ref):
    with pytest.raises(ValueError):
        parse_image(ref)


def test_audit_sample():
    refs = [
        "ghcr.io/acme/fraud-detector:v7",
        "redis:7.2",
        "   ",
        "ghcr.io/acme/feature-store",
        "localhost:5000/models/churn:dev",
    ]
    assert audit_images(refs) == [
        "#2 redis:7.2: registry 'docker.io' not allowed",
        "#4 ghcr.io/acme/feature-store: unpinned tag 'latest'",
        "#5 localhost:5000/models/churn:dev: registry 'localhost:5000' not allowed",
    ]


def test_audit_clean_and_empty():
    assert audit_images([]) == []
    assert audit_images(["ghcr.io/acme/a:v1", "", "ghcr.io/acme/b:1.0.3"]) == []


def test_audit_both_problems_in_order_and_custom_allowlist():
    refs = ["nginx", " python:3.12-slim "]
    assert audit_images(refs) == [
        "#1 nginx: registry 'docker.io' not allowed",
        "#1 nginx: unpinned tag 'latest'",
        "#2 python:3.12-slim: registry 'docker.io' not allowed",
    ]
    assert audit_images(refs, allowed_registries={"docker.io", "ghcr.io"}) == [
        "#1 nginx: unpinned tag 'latest'",
    ]


def test_audit_invalid_reference_gets_one_line():
    refs = ["ghcr.io/acme/x:", "ghcr.io/acme/ok:v2", "ghcr.io/acme/y:latest"]
    assert audit_images(refs) == [
        "#1 ghcr.io/acme/x:: invalid reference",
        "#3 ghcr.io/acme/y:latest: unpinned tag 'latest'",
    ]
