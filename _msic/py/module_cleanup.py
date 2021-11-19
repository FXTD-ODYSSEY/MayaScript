# -*- coding: utf-8 -*-
"""
auto reload module base on the file directory
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import sys


def module_cleanup(module_name):
    assert isinstance(module_name, str), "not support type %s" % type(module_name)
    maya_folder = os.path.dirname(sys.executable)

    module_dot = module_name + "."
    packages = [p for p in sys.modules if p.startswith(module_dot)]
    packages += [module_name]
    for package in packages:
        module = sys.modules.get(package)
        # NOTE 过滤掉 Maya 内置模块
        if (
            module
            and hasattr(module, "__file__")
            and not module.__file__.startswith(maya_folder)
        ):
            del sys.modules[package]


if __name__ == "__main__":
    MODULE = r"F:\light_git\MAvatar"
    sys.path.insert(0, MODULE) if MODULE not in sys.path else None
    module_cleanup("pose_editor")
    import pose_editor

    pose_editor.launch()

