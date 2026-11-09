from solution import best_epoch, parse_epochs

LOG = [
    "2026-11-09 02:00:01 INFO starting run fraud-detector",
    "2026-11-09 02:04:10 INFO epoch=1 loss=0.912 val_loss=0.884 val_acc=0.71",
    "2026-11-09 02:04:11 INFO saved checkpoint ckpt-1",
    "2026-11-09 02:08:22 INFO epoch=2 loss=0.533 val_loss=0.561 val_acc=0.80",
    "2026-11-09 02:12:30 WARNING epoch=3 loss=oops val_loss=0.6",
    "2026-11-09 02:16:41 INFO epoch=4 loss=0.301 val_loss=0.598 val_acc=0.83",
]


def test_parse_sample_skips_noise_and_bad_lines():
    assert parse_epochs(LOG) == [
        {"epoch": 1, "loss": 0.912, "val_loss": 0.884, "val_acc": 0.71},
        {"epoch": 2, "loss": 0.533, "val_loss": 0.561, "val_acc": 0.80},
        {"epoch": 4, "loss": 0.301, "val_loss": 0.598, "val_acc": 0.83},
    ]


def test_epoch_is_int_metrics_are_float():
    (row,) = parse_epochs(["epoch=7 loss=1"])
    assert type(row["epoch"]) is int
    assert type(row["loss"]) is float


def test_best_epoch_defaults_to_lowest_val_loss():
    assert best_epoch(LOG) == 2


def test_best_epoch_higher_is_better():
    assert best_epoch(LOG, metric="val_acc", higher_is_better=True) == 4


def test_tie_goes_to_earlier_epoch_and_missing_metric_skipped():
    log = [
        "epoch=1 loss=0.5",
        "epoch=2 loss=0.4 val_loss=0.30",
        "epoch=3 loss=0.3 val_loss=0.30",
    ]
    assert best_epoch(log) == 2


def test_empty_and_no_metric_return_empty_or_none():
    assert parse_epochs([]) == []
    assert best_epoch([]) is None
    assert best_epoch(LOG, metric="f1") is None
