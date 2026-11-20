import pytest

from solution import apply_overrides, parse_value


def base_config():
    return {
        "model": {"name": "churn-xgb", "max_depth": 6},
        "optimizer": {"lr": 0.01},
        "epochs": 20,
    }


def test_parse_value_numbers_bools_and_null():
    cases = [
        (" 50 ", 50, int),
        ("-3", -3, int),
        ("0.001", 0.001, float),
        ("1e-3", 0.001, float),
        ("TRUE", True, bool),
        ("false", False, bool),
    ]
    for text, expected, kind in cases:
        value = parse_value(text)
        assert value == expected and type(value) is kind, text
    assert parse_value("null") is None
    assert parse_value("None") is None


def test_parse_value_strings_and_quotes():
    assert parse_value("  churn-xgb  ") == "churn-xgb"
    assert parse_value("'0.5'") == "0.5"
    assert parse_value('"042"') == "042"
    assert parse_value('"true"') == "true"
    assert parse_value('"mixed\'') == '"mixed\''  # quotes don't match: keep as-is
    assert parse_value("") == ""


def test_apply_overrides_sample():
    result = apply_overrides(
        base_config(),
        [
            "optimizer.lr=0.001",
            "epochs=50",
            "model.max_depth = 8",
            "data.shuffle=true",
            'run_name="042"',
        ],
    )
    assert result == {
        "model": {"name": "churn-xgb", "max_depth": 8},
        "optimizer": {"lr": 0.001},
        "epochs": 50,
        "data": {"shuffle": True},
        "run_name": "042",
    }
    assert type(result["epochs"]) is int


def test_does_not_mutate_input():
    config = base_config()
    result = apply_overrides(config, ["optimizer.lr=0.5", "model.extra.depth=2"])
    assert result["optimizer"]["lr"] == 0.5
    assert result["model"]["extra"] == {"depth": 2}
    assert config == base_config()
    assert apply_overrides(config, []) == config
    assert apply_overrides(config, []) is not config


def test_later_override_wins_and_value_may_contain_equals():
    result = apply_overrides({}, ["a.b.c=1", "a.b.c=2", "tracking.uri=http://mlflow:5000/?x=1"])
    assert result == {"a": {"b": {"c": 2}}, "tracking": {"uri": "http://mlflow:5000/?x=1"}}


@pytest.mark.parametrize(
    "bad",
    ["epochs", "=5", " =5", "a..b=1", ".a=1", "a.=1", "optimizer.lr.x=1"],
)
def test_bad_overrides_raise(bad):
    with pytest.raises(ValueError):
        apply_overrides(base_config(), [bad])
