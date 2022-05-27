import module
import module2


from typing import Union
from typing import cast
from typing import TYPE_CHECKING


class Test(object):
    def make(self):
        print("make")

test = Test()
module_list = [module,module2]
if TYPE_CHECKING:
    test = cast(module | module2 | Test, 0)
    

test.d