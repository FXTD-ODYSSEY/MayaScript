import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

import pyblish.api
# NOTE 共享数据
context = pyblish.api.Context()
context.data["key"] = "value"

# NOTE 用 mixCase 区分 python 命名
# wrong
context.data["my_key"] = True

# right
context.data["myKey"] = True
