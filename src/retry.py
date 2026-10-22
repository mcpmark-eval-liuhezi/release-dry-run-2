"""Small retry helper with exponential backoff for the telemetry client.

Implements the hardening requested in issue #1: retries use exponential
backoff between attempts and give up after a hard cap of 5 attempts.
"""

import time


def retry_with_backoff(operation, base_delay=0.5, factor=2.0):
    """Run `operation`, retrying on failure with exponential backoff.

    Args:
        operation: A zero-argument callable to attempt.
        base_delay: Delay (in seconds) before the first retry.
        factor: Multiplier applied to the delay after each retry.

    Returns:
        The value returned by `operation` once it succeeds.

    Raises:
        Exception: The last exception raised by `operation` after the
            attempt cap is reached.
    """
    max_attempts = 5
    delay = base_delay

    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception:
            if attempt == max_attempts:
                raise
            time.sleep(delay)
            delay *= factor
