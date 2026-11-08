import time


def retry_call(
    fn,
    *,
    max_attempts: int = 4,
    base_delay: float = 1.0,
    max_delay: float = 8.0,
    retry_on: tuple = (ConnectionError, TimeoutError),
    sleep=time.sleep,
):
    ...
