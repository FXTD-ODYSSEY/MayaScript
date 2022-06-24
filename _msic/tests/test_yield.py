"""
1. test decorator
2. test argument
"""
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
        
# iterate_sequence([1,2,3,4,5])

# ----------------------------------------------------------------

def iterate_sequence(sequence,is_iterator=False):
    for item in sequence:
        print(is_iterator)
        if is_iterator:
            yield
        print(item)

itr = iterate_sequence([1,2,3,4,5])
print(itr.send(1))
# for i in iterate_sequence([1,2,3,4,5]):
#     print(i)

