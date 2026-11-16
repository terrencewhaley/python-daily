import pytest

from solution import early_stop, loss_spikes

VAL = [0.9, 0.7, 0.72, 0.69, 0.71, 0.70, 0.73]


def test_spikes_sample_and_custom_ratio():
    losses = [0.9, 0.7, 1.4, 0.8, 0.85, 2.0]
    assert loss_spikes(losses) == [3, 6]
    assert loss_spikes(losses, ratio=2.0) == [6]
    assert loss_spikes([1.0, 1.5]) == []  # equal to prev * ratio is not a spike


def test_spikes_short_none_and_zero():
    assert loss_spikes([]) == []
    assert loss_spikes([0.4]) == []
    assert loss_spikes([0.2, None, 5.0, 0.3, 0.9]) == [5]  # pairs touching None skipped
    assert loss_spikes([0.0, 0.1]) == [2]  # 0.0 is a real loss, not missing


def test_early_stop_sample():
    assert early_stop(VAL, patience=3) == (7, 4)
    assert early_stop(VAL, patience=2) == (6, 4)
    assert early_stop(VAL, patience=4) == (None, 4)


def test_early_stop_min_delta():
    assert early_stop(VAL, patience=3, min_delta=0.02) == (5, 2)


def test_early_stop_none_zero_and_empty():
    losses = [0.5, None, 0.0, None, None, 0.1, 0.2, 0.3]
    assert early_stop(losses, patience=3) == (8, 3)
    assert early_stop([0.5, 0.4, 0.3]) == (None, 3)
    assert early_stop([]) == (None, None)
    assert early_stop([None, None]) == (None, None)


def test_early_stop_bad_patience():
    with pytest.raises(ValueError):
        early_stop(VAL, patience=0)
