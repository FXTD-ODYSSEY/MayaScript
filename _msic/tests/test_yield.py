
from functools import wraps

def deco(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        res =  func(*args, **kwargs)
        print(res)
        print(next(res))
        return res
    return decorator

@deco
def iterate_sequence(sequence):
    for item in sequence:
        yield item
        

iterate_sequence([1,2,3,4,5])

