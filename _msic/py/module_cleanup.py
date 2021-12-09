# -*- coding: utf-8 -*-
"""
auto reload module base on the file directory
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
import sys
import pkgutil
from types import ModuleType

def module_cleanup(module):
    if isinstance(module,str):
        module = sys.modules.get(module)
        if not module:
            return
    assert isinstance(module,ModuleType), "not support type %s" % type(module)
    for _, mod, _ in pkgutil.walk_packages(module.__path__,module.__name__+"."):
        print("remove %s" % mod)
        sys.modules.pop(mod,None)


if __name__ == "__main__":
    MODULE = r"F:\light_git\MAvatar"
    sys.path.insert(0, MODULE) if MODULE not in sys.path else None
    module_cleanup("pose_editor")
    import pose_editor

    pose_editor.launch()

