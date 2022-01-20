# -*- coding: utf-8 -*-
"""Auto reload module base on the file directory."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import sys
from types import ModuleType


def module_cleanup(module_name):
    """Cleanup module_name in sys.modules cache.

    Args:
        module_name (str or ModuleType): Module Name

    Raises:
        TypeError: invalid module_name
    """
    if isinstance(module_name, ModuleType):
        module_name = module_name.__name__

    if not isinstance(module_name, str):
        raise TypeError("not support type %s" % type(module_name))
    elif module_name in sys.builtin_module_names:
        return
    
    pred = "%s." % module_name
    packages = [mod for mod in sys.modules if mod.startswith(pred)]
    packages += [module_name]
    for package in packages:
        module = sys.modules.get(package)
        if module is not None:
            del sys.modules[package]  # noqa:WPS420

if __name__ == "__main__":
    MODULE = r"F:\light_git\MAvatar"
    sys.path.insert(0, MODULE) if MODULE not in sys.path else None
    module_cleanup("pose_editor")
    # Import third-party modules
    import pose_editor

    pose_editor.launch()

