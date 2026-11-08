import pytest

from solution import retry_call


def make_flaky(failures):
    it = iter(failures)

    def upload():
        exc = next(it, None)
        if exc:
            raise exc
        return "uploaded fraud-detector:v7"

    return upload


def test_succeeds_after_transient_errors():
    delays = []
    fn = make_flaky([ConnectionError("reset"), TimeoutError("slow")])
    assert retry_call(fn, sleep=delays.append) == "uploaded fraud-detector:v7"
    assert delays == [1.0, 2.0]


def test_first_try_success_never_sleeps():
    delays = []
    assert retry_call(make_flaky([]), sleep=delays.append) == "uploaded fraud-detector:v7"
    assert delays == []


def test_gives_up_after_max_attempts():
    delays = []
    with pytest.raises(ConnectionError):
        retry_call(make_flaky([ConnectionError()] * 10), sleep=delays.append)
    assert delays == [1.0, 2.0, 4.0]


def test_non_retryable_error_raises_immediately():
    delays = []
    with pytest.raises(ValueError):
        retry_call(make_flaky([ValueError("bad manifest")]), sleep=delays.append)
    assert delays == []


def test_delay_is_capped():
    delays = []
    retry_call(make_flaky([ConnectionError()] * 5), max_attempts=6, sleep=delays.append)
    assert delays == [1.0, 2.0, 4.0, 8.0, 8.0]
