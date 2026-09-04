import time
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries: int = 3, delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator