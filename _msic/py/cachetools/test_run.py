"""Provide function cache function."""

# Import third-party modules
import attr
import os
import time
import cachetools
# from functools import partial
# from functools32 import lru_cache
# from cache_decorator import Cache

DIR = os.path.dirname(os.path.abspath(__file__))
def optional_cache(func):
    """Decorate a function to optionally use caching on its return values.

    A function decorated by this will accept two additional keyword args:
        - "_use_optional_cache", which is set to `True` by default.
        - "_clear_optional_cache", which is set to `False` by default.

    If `_use_optional_cache` is `True`, the function will behave as if it is
    decorated by `cachetools.cached` with a `cachetools.TTLCache`.
    Otherwise, the function will not use any cached data, and will derive its
    return values manually. These return values will not be added to the cache.

    If `_clear_optional_cache` is `True`, calling the function WILL ONLY CLEAR
    THE CACHE. The decorated function will not even be called at all; the cache
    will be cleared and the function will return `None`.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.

    """
    cache = cachetools.Cache(maxsize=2048)

    @cachetools.cached(cache=cache)
    def cached_func(*args, **kwargs):
        """Run the function with its arguments and cache the result.

        Args:
            *args: Variable length list of arguments.
            **kwargs: Variable length list of keyword args.

        Returns:
            Whatever the function returns.

        """
        return func(*args, **kwargs)

    def decorator(*args, **kwargs):
        """Get the function's return value, possibly caching the results.

        Args:
            *args: Variable length list of arguments.
            **kwargs: Variable length list of keyword args.

        Returns:
            Whatever the function returns.

        """
        clear_cache = kwargs.pop("_clear_optional_cache", False)
        if clear_cache:
            cache.clear()
            return None
        use_cache = kwargs.pop("_use_optional_cache", True)
        if use_cache:
            return cached_func(*args, **kwargs)
        return func(*args, **kwargs)

    return decorator


# @attr.s(hash=False)
class Test(object):
    def __init__(self, *args, **kwargs):

        self._data = {i: i for i in range(10)}

    @property
    @cachetools.Cache(maxsize=1024)
    def data(self):
        return self._data
    
    # @Cache(cache_path=os.path.join(DIR,"test.json"))
    def get_data(self):
        print("run get data")
        res = {i:i + 1 for i in self.data}
        print("res",res)
        return res
    
    def set_data(self,data):
        self._data = data

    # def __hash__(self):
    #     return id(self)

test = Test()
print(test.data)
print(test.data)
test.set_data({i: i for i in range(20)})
time.sleep(1)
print(test.data)


# @optional_cache
# def factorial(n):
#     print(f"计算 {n} 的阶乘")
#     return 1 if n <= 1 else n * factorial(n - 1)

# factorial(5)
# factorial(3)


# a = {
#     (1,):1,
#     ():1,
# }
# print(a)

