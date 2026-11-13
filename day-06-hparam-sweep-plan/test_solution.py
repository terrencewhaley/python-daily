import copy

import pytest

from solution import expand_grid, plan_sweep

SAMPLE = {"lr": [0.01, 0.001], "batch_size": [32, 64], "optimizer": "adam"}


def test_expand_sample_order_and_fixed_values():
    original = copy.deepcopy(SAMPLE)
    assert expand_grid(SAMPLE) == [
        {"lr": 0.01, "batch_size": 32, "optimizer": "adam"},
        {"lr": 0.01, "batch_size": 64, "optimizer": "adam"},
        {"lr": 0.001, "batch_size": 32, "optimizer": "adam"},
        {"lr": 0.001, "batch_size": 64, "optimizer": "adam"},
    ]
    assert list(expand_grid(SAMPLE)[0]) == ["lr", "batch_size", "optimizer"]
    assert SAMPLE == original  # grid not modified


def test_expand_tuples_and_scalar_types():
    grid = {"dropout": (0.1, 0.3), "warmup": True, "epochs": 10}
    assert expand_grid(grid) == [
        {"dropout": 0.1, "warmup": True, "epochs": 10},
        {"dropout": 0.3, "warmup": True, "epochs": 10},
    ]


def test_expand_empty_cases():
    assert expand_grid({}) == [{}]
    assert expand_grid({"lr": [0.1, 0.01], "seed": []}) == []


def test_plan_sample():
    assert plan_sweep(SAMPLE, prefix="churn") == [
        "churn-001 lr=0.01 batch_size=32 optimizer=adam",
        "churn-002 lr=0.01 batch_size=64 optimizer=adam",
        "churn-003 lr=0.001 batch_size=32 optimizer=adam",
        "churn-004 lr=0.001 batch_size=64 optimizer=adam",
    ]


def test_plan_defaults_padding_and_no_params():
    lines = plan_sweep({"seed": list(range(12))})
    assert lines[0] == "sweep-001 seed=0"
    assert lines[-1] == "sweep-012 seed=11"
    assert plan_sweep({}) == ["sweep-001"]
    assert plan_sweep({"lr": []}) == []


def test_plan_budget():
    grid = {"lr": [0.1, 0.01, 0.001], "seed": [1, 2]}
    with pytest.raises(ValueError):
        plan_sweep(grid, max_runs=5)
    assert len(plan_sweep(grid, max_runs=6)) == 6
