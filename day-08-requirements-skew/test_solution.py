import pytest

from solution import compare_requirements, parse_requirements

TRAIN = """
# training image
numpy==1.26.4
pandas == 2.2.2   # parquet support
scikit-learn==1.5.0
xgboost==2.0.3
torch>=2.3
-r base.txt
"""

SERVE = """
NumPy==1.26.4
pandas==2.1.0
Scikit_Learn==1.5.0
uvicorn[standard]==0.30.1
torch
"""


def test_parse_sample():
    assert parse_requirements(TRAIN) == {
        "numpy": "1.26.4",
        "pandas": "2.2.2",
        "scikit-learn": "1.5.0",
        "xgboost": "2.0.3",
        "torch": None,
    }


def test_parse_names_extras_and_specifiers():
    text = "Scikit_Learn==1.5.0\nuvicorn[standard]==0.30.1\nrequests~=2.31\nboto3!=1.0\nnumpy<2\n"
    assert parse_requirements(text) == {
        "scikit-learn": "1.5.0",
        "uvicorn": "0.30.1",
        "requests": None,
        "boto3": None,
        "numpy": None,
    }


def test_parse_empty_and_noise_only():
    assert parse_requirements("") == {}
    assert parse_requirements("\n   \n# just a comment\n--index-url https://pypi.org/simple\n") == {}


def test_parse_duplicate_raises():
    with pytest.raises(ValueError):
        parse_requirements("pandas==2.2.2\nnumpy==1.26.4\nPandas==2.1.0\n")


def test_compare_sample():
    assert compare_requirements(TRAIN, SERVE) == {
        "missing_in_serving": ["xgboost"],
        "version_mismatch": [("pandas", "2.2.2", "2.1.0")],
        "unpinned": ["torch"],
    }


def test_compare_identical_and_sorted_unpinned():
    same = "b-lib==1.0\na-lib==2.0\n"
    assert compare_requirements(same, same) == {
        "missing_in_serving": [],
        "version_mismatch": [],
        "unpinned": [],
    }
    train = "zeta\nalpha==1.0\nmid==3.0\n"
    serve = "alpha\nzeta==2.0\nmid==3.1\n"
    assert compare_requirements(train, serve) == {
        "missing_in_serving": [],
        "version_mismatch": [("mid", "3.0", "3.1")],
        "unpinned": ["alpha", "zeta"],
    }
