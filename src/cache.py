import functools
import time


def timed_lru_cache(seconds: int = 300):
    def wrapper(func):
        @functools.lru_cache()
        def cached_func(*args, **kwargs):
            now = time.time()
            if args in cached_func.cache:  # Check if key exists
                result, timestamp = cached_func.cache[args]
                if now - timestamp < seconds:
                    return result
                else:
                    del cached_func.cache[args]  # Remove expired entry
            # If key not found or expired, calculate and store
            result = func(*args, **kwargs)
            cached_func.cache[args] = (result, now)
            return result

        return cached_func

    return wrapper
