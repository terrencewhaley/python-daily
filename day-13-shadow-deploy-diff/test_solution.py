import pytest

from solution import compare_predictions, format_report

IDS = ["tx-101", "tx-102", "tx-103", "tx-104", "tx-105", "tx-106", "tx-107"]
LIVE = ["legit", "fraud", "legit", "legit", None, "review", "legit"]
SHADOW = ["legit", "fraud", "fraud", "legit", "legit", "fraud", "fraud"]


def test_sample_result():
    result = compare_predictions(IDS, LIVE, SHADOW)
    assert result == {
        "compared": 6,
        "agree": 3,
        "agreement": 0.5,
        "disagreements": ["tx-103", "tx-106", "tx-107"],
        "flips": {("legit", "fraud"): 2, ("review", "fraud"): 1},
        "skipped": ["tx-105"],
    }
    # flips keep first-seen order
    assert list(result["flips"]) == [("legit", "fraud"), ("review", "fraud")]


def test_sample_report():
    assert format_report(compare_predictions(IDS, LIVE, SHADOW)) == [
        "agreement: 3/6 (50.0%)",
        "flip legit -> fraud: 2",
        "flip review -> fraud: 1",
        "skipped 1: tx-105",
    ]


def test_does_not_modify_inputs():
    ids, live, shadow = list(IDS), list(LIVE), list(SHADOW)
    result = compare_predictions(ids, live, shadow)
    assert result["compared"] == 6
    assert (ids, live, shadow) == (IDS, LIVE, SHADOW)


def test_rounding_and_full_agreement_report():
    ids = ["a", "b", "c"]
    result = compare_predictions(ids, ["x", "x", "y"], ["x", "x", "z"])
    assert result["agreement"] == 0.6667
    assert format_report(result) == ["agreement: 2/3 (66.7%)", "flip y -> z: 1"]

    same = compare_predictions(ids, ["x", "y", "x"], ["x", "y", "x"])
    assert same["flips"] == {} and same["disagreements"] == []
    assert format_report(same) == ["agreement: 3/3 (100.0%)"]


def test_nothing_compared():
    empty = compare_predictions([], [], [])
    assert empty == {
        "compared": 0, "agree": 0, "agreement": None,
        "disagreements": [], "flips": {}, "skipped": [],
    }
    assert format_report(empty) == ["agreement: n/a (0 compared)"]

    all_failed = compare_predictions(["r1", "r2"], [None, "fraud"], ["legit", None])
    assert all_failed["agreement"] is None
    assert format_report(all_failed) == [
        "agreement: n/a (0 compared)",
        "skipped 2: r1, r2",
    ]


@pytest.mark.parametrize(
    "ids, live, shadow",
    [
        (["a", "b"], ["x", "y"], ["x"]),          # shadow too short
        (["a"], ["x", "y"], ["x", "y"]),          # ids too short
        (["a", "a"], ["x", "y"], ["x", "y"]),     # duplicate id
    ],
)
def test_bad_input_raises(ids, live, shadow):
    with pytest.raises(ValueError):
        compare_predictions(ids, live, shadow)
