import pytest

from solution import format_duration, leaderboard

RUNS = [
    {"run": "lr-3e-4", "val_acc": 0.9134, "seconds": 3725},
    {"run": "baseline", "val_acc": 0.8872, "seconds": 2410},
    {"run": "lr-1e-3-warmup", "val_acc": 0.9201, "seconds": 4012},
    {"run": "crashed-oom", "val_acc": None, "seconds": 95},
    {"run": "dropout-0.3", "val_acc": 0.9134, "seconds": 59},
]


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (0, "0s"),
        (59, "59s"),
        (60, "1m 00s"),
        (187, "3m 07s"),
        (3600, "1h 00m 00s"),
        (3725, "1h 02m 05s"),
        (90061, "25h 01m 01s"),
    ],
)
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected


def test_format_duration_rejects_negative():
    with pytest.raises(ValueError):
        format_duration(-5)


def test_sample_leaderboard():
    assert leaderboard(RUNS) == [
        "1. lr-1e-3-warmup   92.01%  1h 06m 52s",
        "2. lr-3e-4          91.34%  1h 02m 05s",
        "3. dropout-0.3      91.34%  59s",
    ]


def test_top_and_width_follow_shown_rows():
    # Only the shown rows decide the name column width.
    assert leaderboard(RUNS, top=1) == ["1. lr-1e-3-warmup   92.01%  1h 06m 52s"]
    small = [
        {"run": "a", "val_acc": 1.0, "seconds": 5},
        {"run": "bb", "val_acc": 0.5, "seconds": 61},
    ]
    assert leaderboard(small) == [
        "1. a   100.00%  5s",
        "2. bb   50.00%  1m 01s",
    ]


def test_skips_missing_metric_and_handles_empty():
    assert leaderboard([]) == []
    assert leaderboard([{"run": "x", "val_acc": None, "seconds": 3}]) == []
    no_key = [{"run": "y", "seconds": 3}, {"run": "z", "val_acc": 0.5, "seconds": 3}]
    assert leaderboard(no_key) == ["1. z   50.00%  3s"]


def test_does_not_modify_input():
    runs = [dict(r) for r in RUNS]
    assert len(leaderboard(runs, top=5)) == 4
    assert runs == RUNS
