import pytest

from solution import parse_checkpoint, plan_cleanup

SAMPLE = [
    "ckpt-e003-l0.5100.pt",
    "ckpt-e001-l0.9100.pt",
    "notes.txt",
    "ckpt-e005-l0.5800.pt",
    "ckpt-e002-l0.6200.pt",
    "ckpt-e004-l0.5300.pt",
]


def test_parse_checkpoint_sample_and_whitespace():
    assert parse_checkpoint("ckpt-e012-l0.4312.pt") == (12, 0.4312)
    epoch, loss = parse_checkpoint("  ckpt-e7-l1.25.pt\n")
    assert (epoch, loss) == (7, 1.25)
    assert isinstance(epoch, int) and isinstance(loss, float)


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "   ",
        "notes.txt",
        "model-e001-l0.5.pt",
        "ckpt-e001-l0.5.bin",
        "ckpt-e001.pt",
        "ckpt-eXX-l0.5.pt",
        "ckpt-e001-labc.pt",
    ],
)
def test_parse_checkpoint_rejects_bad_names(bad):
    with pytest.raises(ValueError):
        parse_checkpoint(bad)


def test_plan_cleanup_sample():
    keep, delete = plan_cleanup(SAMPLE, keep_best=2, keep_last=1)
    assert keep == ["ckpt-e003-l0.5100.pt", "ckpt-e004-l0.5300.pt", "ckpt-e005-l0.5800.pt"]
    assert delete == ["ckpt-e001-l0.9100.pt", "ckpt-e002-l0.6200.pt"]


def test_overlap_is_kept_once_and_defaults():
    # Loss keeps improving, so the best checkpoint is also the latest one.
    names = [f"ckpt-e{e:03d}-l{1.0 - e / 10:.4f}.pt" for e in range(1, 6)]
    keep, delete = plan_cleanup(names)  # keep_best=2, keep_last=1
    assert keep == ["ckpt-e004-l0.6000.pt", "ckpt-e005-l0.5000.pt"]
    assert delete == ["ckpt-e001-l0.9000.pt", "ckpt-e002-l0.8000.pt", "ckpt-e003-l0.7000.pt"]


def test_zero_keep_last_and_tie_breaks_to_earlier_epoch():
    names = [
        " ckpt-e04-l0.40.pt ",
        "ckpt-e02-l0.40.pt",
        "ckpt-e03-l0.55.pt",
        "ckpt-e01-l0.80.pt",
    ]
    keep, delete = plan_cleanup(names, keep_best=1, keep_last=0)
    assert keep == ["ckpt-e02-l0.40.pt"]
    assert delete == ["ckpt-e01-l0.80.pt", "ckpt-e03-l0.55.pt", "ckpt-e04-l0.40.pt"]

    keep, delete = plan_cleanup(names, keep_best=0, keep_last=0)
    assert keep == []
    assert len(delete) == 4


def test_empty_and_negative():
    assert plan_cleanup([]) == ([], [])
    assert plan_cleanup(["notes.txt", "README.md"]) == ([], [])
    with pytest.raises(ValueError):
        plan_cleanup(SAMPLE, keep_best=-1)
    with pytest.raises(ValueError):
        plan_cleanup(SAMPLE, keep_last=-1)
