import pytest

from solution import batch_labels, split_dataset

FILES = [f"scan_{i:02d}.png" for i in range(10)]


def test_split_sample():
    original = list(FILES)
    train, val, test = split_dataset(FILES)
    assert train == FILES[:8]
    assert val == ["scan_08.png"]
    assert test == ["scan_09.png"]
    assert FILES == original  # input untouched


def test_split_custom_fractions_and_leftovers():
    items = [f"row_{i}" for i in range(7)]
    train, val, test = split_dataset(items, train=0.5, val=0.25)
    # int(3.5) = 3, int(1.75) = 1, leftover 3 goes to test
    assert train == ["row_0", "row_1", "row_2"]
    assert val == ["row_3"]
    assert test == ["row_4", "row_5", "row_6"]
    assert split_dataset([], train=0.7, val=0.2) == ([], [], [])
    assert split_dataset(items, train=1.0, val=0.0) == (items, [], [])


@pytest.mark.parametrize("train, val", [(0.95, 0.1), (-0.1, 0.5), (0.8, -0.2)])
def test_split_bad_fractions(train, val):
    with pytest.raises(ValueError):
        split_dataset(FILES, train=train, val=val)


def test_batch_labels_sample():
    assert batch_labels(FILES[:8], 3) == [
        "batch 1/3: scan_00.png..scan_02.png (3)",
        "batch 2/3: scan_03.png..scan_05.png (3)",
        "batch 3/3: scan_06.png..scan_07.png (2)",
    ]


def test_batch_labels_single_item_batches_and_exact_fit():
    assert batch_labels(FILES[:4], 3) == [
        "batch 1/2: scan_00.png..scan_02.png (3)",
        "batch 2/2: scan_03.png (1)",
    ]
    assert batch_labels(FILES[:2], 1) == [
        "batch 1/2: scan_00.png (1)",
        "batch 2/2: scan_01.png (1)",
    ]
    assert batch_labels(FILES, 10) == ["batch 1/1: scan_00.png..scan_09.png (10)"]
    assert batch_labels(FILES[:3], 50) == ["batch 1/1: scan_00.png..scan_02.png (3)"]


def test_batch_labels_empty_and_bad_size():
    assert batch_labels([], 4) == []
    with pytest.raises(ValueError):
        batch_labels(FILES, 0)
    with pytest.raises(ValueError):
        batch_labels(FILES, -2)
