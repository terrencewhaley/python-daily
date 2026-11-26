from pathlib import Path

import pytest

from solution import summarize_requests

HERE = Path(__file__).parent


def write_lines(tmp_path, *lines):
    p = tmp_path / "requests.jsonl"
    p.write_text("\n".join(lines) + "\n")
    return p


def test_sample_file():
    assert summarize_requests(HERE / "requests.jsonl") == {
        "total": 8,
        "by_model": {
            "churn-v3": {"ok": 2, "error": 1},
            "churn-v4": {"ok": 1, "error": 3},
            "fraud-v7": {"ok": 0, "error": 1},
        },
        "top_errors": [
            ("CUDA out of memory", 2),
            ("missing feature: tenure_months", 1),
            ("model not loaded", 1),
        ],
    }


def test_top_n_and_tie_order():
    result = summarize_requests(HERE / "requests.jsonl", top_n=2)
    assert result["top_errors"] == [
        ("CUDA out of memory", 2),
        ("missing feature: tenure_months", 1),
    ]


def test_empty_and_blank_only_files(tmp_path):
    empty = {"total": 0, "by_model": {}, "top_errors": []}
    p = tmp_path / "empty.jsonl"
    p.write_text("")
    assert summarize_requests(p) == empty
    assert summarize_requests(write_lines(tmp_path, "", "   ", "")) == empty


def test_status_boundary_and_both_keys(tmp_path):
    p = write_lines(
        tmp_path,
        '{"model": "a", "status": 399}',
        '{"model": "a", "status": 399}',
        '{"model": "b", "status": 400, "error": "bad request"}',
    )
    result = summarize_requests(p)
    assert result["by_model"] == {"a": {"ok": 2, "error": 0}, "b": {"ok": 0, "error": 1}}
    assert type(result["by_model"]["a"]) is dict
    assert result["top_errors"] == [("bad request", 1)]


def test_error_field_on_success_is_ignored(tmp_path):
    p = write_lines(tmp_path, '{"model": "a", "status": 200, "error": "warmup retry"}')
    assert summarize_requests(p)["top_errors"] == []


@pytest.mark.parametrize(
    "bad_line",
    [
        '{"model": "a", "status": 200',  # truncated JSON
        '{"status": 200}',  # no model
        '{"model": "a"}',  # no status
    ],
)
def test_bad_record_reports_line_number(tmp_path, bad_line):
    p = write_lines(tmp_path, '{"model": "a", "status": 200}', "", bad_line)
    with pytest.raises(ValueError, match=r"line 3\b"):
        summarize_requests(p)
