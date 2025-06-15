import time
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)

def rate_limit(calls: int, period: int):
    """
    Decorator to implement rate limiting.
    
    Args:
        calls: Number of calls allowed in the period
        period: Time period in seconds
    """
    def decorator(func: Callable) -> Callable:
        last_reset = datetime.now()
        calls_made = 0
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal last_reset, calls_made
            now = datetime.now()
            
            if now - last_reset > timedelta(seconds=period):
                last_reset = now
                calls_made = 0
                
            if calls_made >= calls:
                sleep_time = period - (now - last_reset).total_seconds()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                last_reset = datetime.now()
                calls_made = 0
                
            calls_made += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log the execution time of a function.
    
    Args:
        func: The function to decorate
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(
            f"Function {func.__name__} took {end_time - start_time:.2f} seconds to execute"
        )
        return result
    return wrapper 