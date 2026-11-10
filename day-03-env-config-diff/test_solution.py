import copy

from solution import diff_env, format_diff

STAGING = {
    "MODEL_NAME": "fraud-detector",
    "MODEL_VERSION": "v8",
    "LOG_LEVEL": "DEBUG",
    "REGISTRY_TOKEN": "stg-abc123",
    "BATCH_SIZE": "32",
}
PROD = {
    "MODEL_NAME": "fraud-detector",
    "LOG_LEVEL": "INFO",
    "REGISTRY_TOKEN": "prd-zzz999",
    "BATCH_SIZE": "32",
    "WORKERS": "4",
}


def test_diff_env_sample():
    assert diff_env(STAGING, PROD) == {
        "added": ["WORKERS"],
        "removed": ["MODEL_VERSION"],
        "changed": {
            "LOG_LEVEL": ("DEBUG", "INFO"),
            "REGISTRY_TOKEN": ("stg-abc123", "prd-zzz999"),
        },
    }


def test_format_diff_sample_masks_secrets():
    assert format_diff(STAGING, PROD) == [
        "+ WORKERS=4",
        "- MODEL_VERSION",
        "~ LOG_LEVEL: DEBUG -> INFO",
        "~ REGISTRY_TOKEN: *** -> ***",
    ]


def test_ignore_skips_keys_everywhere():
    assert format_diff(STAGING, PROD, ignore={"LOG_LEVEL", "REGISTRY_TOKEN"}) == [
        "+ WORKERS=4",
        "- MODEL_VERSION",
    ]
    d = diff_env(STAGING, PROD, ignore=["WORKERS", "MODEL_VERSION"])
    assert d["added"] == [] and d["removed"] == []


def test_groups_are_sorted_and_added_secrets_masked():
    old = {"Z_OLD": "1", "A_OLD": "1"}
    new = {"DB_PASSWORD": "hunter2", "API_SECRET": "s", "B_NEW": "x"}
    assert format_diff(old, new) == [
        "+ API_SECRET=***",
        "+ B_NEW=x",
        "+ DB_PASSWORD=***",
        "- A_OLD",
        "- Z_OLD",
    ]


def test_no_changes_and_empty_inputs():
    assert format_diff({}, {}) == ["no changes"]
    assert format_diff(STAGING, dict(STAGING)) == ["no changes"]
    assert diff_env({}, {}) == {"added": [], "removed": [], "changed": {}}


def test_inputs_not_modified():
    old, new = copy.deepcopy(STAGING), copy.deepcopy(PROD)
    d = diff_env(old, new, ignore={"LOG_LEVEL"})
    lines = format_diff(old, new, ignore={"LOG_LEVEL"})
    assert "LOG_LEVEL" not in d["changed"]
    assert lines[-1] == "~ REGISTRY_TOKEN: *** -> ***"
    assert old == STAGING and new == PROD
