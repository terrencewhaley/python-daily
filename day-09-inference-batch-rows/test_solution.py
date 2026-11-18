import pytest

from solution import parse_batch, to_columns

SAMPLE = [
    "customer_id, tenure_months, plan, monthly_spend",
    "c-101, 14, pro, 49.0",
    "c-102, 3, , 12.5",
    "",
    "c-103, 27, team, 120.0, extra",
    "c-104, 1, free, 0",
]

HEADER = ["customer_id", "tenure_months", "plan", "monthly_spend"]
RECORDS = [
    {"customer_id": "c-101", "tenure_months": "14", "plan": "pro", "monthly_spend": "49.0"},
    {"customer_id": "c-102", "tenure_months": "3", "plan": None, "monthly_spend": "12.5"},
    {"customer_id": "c-104", "tenure_months": "1", "plan": "free", "monthly_spend": "0"},
]


def test_parse_sample():
    header, records, errors = parse_batch(SAMPLE)
    assert header == HEADER
    assert records == RECORDS
    assert errors == ["line 5: expected 4 fields, got 5"]


def test_empty_and_blank_only_input():
    assert parse_batch([]) == ([], [], [])
    assert parse_batch(["", "   ", "\t"]) == ([], [], [])


def test_line_numbers_count_leading_blanks_and_short_rows():
    lines = ["", "  ", "id,score", "a,0.9", "b", "", "c,0.1,x,y", "d,"]
    header, records, errors = parse_batch(lines)
    assert header == ["id", "score"]
    assert records == [{"id": "a", "score": "0.9"}, {"id": "d", "score": None}]
    assert errors == [
        "line 5: expected 2 fields, got 1",
        "line 7: expected 2 fields, got 4",
    ]


def test_header_only():
    assert parse_batch(["id, score "]) == (["id", "score"], [], [])


def test_duplicate_header_raises():
    with pytest.raises(ValueError):
        parse_batch(["id, score, id", "a, 1, b"])


def test_to_columns():
    assert to_columns(HEADER, RECORDS) == {
        "customer_id": ["c-101", "c-102", "c-104"],
        "tenure_months": ["14", "3", "1"],
        "plan": ["pro", None, "free"],
        "monthly_spend": ["49.0", "12.5", "0"],
    }
    cols = to_columns(["id", "score"], [])
    assert cols == {"id": [], "score": []}
    assert list(cols) == ["id", "score"]
