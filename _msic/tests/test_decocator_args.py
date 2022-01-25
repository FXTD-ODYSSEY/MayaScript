
import os
class ValidatePathDecorator(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(args,kwargs)
        path = kwargs.pop("path")
        if not isinstance(path, str) or not os.path.exists(path):
            return {}
        return self.func(*args, **kwargs)

@ValidatePathDecorator
def test_call(path=""):
    print(path)
    
test_call("1123")

