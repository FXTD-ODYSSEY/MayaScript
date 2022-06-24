import sys
MODULE = r"C:\_thm\rez_local_cache\ext\attrs\20.3.0\python"
MODULE not in sys.path and sys.path.insert(0,MODULE)

import attr
from Qt import QtCore

@attr.s(init=False)
class TestObject(QtCore.QObject):
    example = attr.ib()
    test_data = attr.ib()
    tested = QtCore.Signal()
    
    def __attrs_post_init__(self):
        super(TestObject, self).__init__()
    
test = TestObject(1,2)
print(test)


