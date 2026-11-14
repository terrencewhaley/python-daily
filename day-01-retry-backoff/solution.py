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
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except retry_on:
            if attempt == max_attempts:
                raise
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            sleep(delay)
