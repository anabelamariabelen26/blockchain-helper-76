import time
import functools
import requests
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, ConnectionError) as e:
                    last_exception = e
                    time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def fetch_blockchain_data(endpoint: str) -> dict:
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()