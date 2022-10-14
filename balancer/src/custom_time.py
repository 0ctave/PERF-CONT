from functools import wraps
import time

def timeit(verbose=True):
    """
    The function `timeit` returns a function `timeit_decorator` which returns a function
    `timeit_wrapper` which returns the time taken to execute the function `func`
    
    Args:
      verbose: If True, prints the time taken by the function. Defaults to True
    
    Returns:
      A wrapper to time a function
    """
    def timeit_decorator(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            if verbose : print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
            return total_time
        return timeit_wrapper
    return timeit_decorator
