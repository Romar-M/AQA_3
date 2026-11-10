from functools import wraps
import time


def retry(max_attempts=3, delay=1):
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool):
        raise TypeError("max_attempts must be an integer")
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if delay < 0:
        raise ValueError("delay must not be negative")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


if __name__ == "__main__":
    attempts = 0

    @retry(max_attempts=3, delay=1)
    def unstable_operation():
        """Return a result on the third attempt."""
        global attempts
        attempts += 1
        print(f"Attempt {attempts}")
        if attempts < 3:
            raise ConnectionError("Temporary connection error")
        return "Success"

    print(unstable_operation())
