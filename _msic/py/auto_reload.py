# -*- coding: utf-8 -*-
"""
auto reload the module by the given name
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
import imp
from types import ModuleType

GUARD_COUNT = 50


def auto_reload(module):

    assert isinstance(module, ModuleType), "not support type %s" % type(module)
    module_name = module.__name__

    path = module.__file__
    if os.path.isfile(path):
        path = os.path.dirname(path)

    path = os.path.abspath(path)

    packages = set()
    for root, _, files in os.walk(path):
        if "__init__.py" not in files:
            continue
        for f in files:
            if not f.endswith(".py"):
                continue
            inter = root.replace(path, "").replace("\\", ".")
            package = module_name + inter
            if f != "__init__.py":
                package += ".%s" % os.path.splitext(f)[0]
            packages.add(package)

    guard = 0
    packages = sorted(packages, key=lambda e: e.count("."), reverse=True)
    while packages:
        guard += 1
        indices = set()
        for i, package in enumerate(packages):
            module = sys.modules.get(package)
            try:
                if module is None:
                    __import__(package)
                else:
                    imp.reload(module)
                indices.add(i)
            except AttributeError as e:
                if guard > GUARD_COUNT:
                    print("=> auto_reload guard overflow")
                    raise
            except ImportError:
                indices.add(i)
            except Exception:
                raise

        for i in sorted(indices, reverse=True):
            packages.pop(i)


if __name__ == "__main__":
    import sys

    MODULE = os.path.join(__file__, "..", "..", "tests")
    MODULE = os.path.abspath(MODULE)
    MODULE not in sys.path and sys.path.insert(0, MODULE)
    import module_test

    auto_reload(module_test)
    from module_test.controller import dev

    dev.carry_call()
