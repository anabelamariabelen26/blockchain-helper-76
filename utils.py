import time
import functools
import requests
from typing import Callable, Any

def retry_network_operation(retries: int = 3, delay: float = 1.0, backoff: float = 2.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, ConnectionError) as e:
                    last_exception = e
                    if attempt == retries - 1:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
            if last_exception:
                raise last_exception
        return wrapper
    return decorator

@retry_network_operation(retries=3, delay=1.0)
def fetch_blockchain_data(url: str, params: dict = None) -> dict:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
