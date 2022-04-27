
from typing import get_type_hints

class Extender(object):
    def test(self):
        pass

def test():
    # type: () -> str
    return "asd"

hints = get_type_hints(test)
print(hints)

