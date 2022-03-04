
import os
# import attr
import importlib
import pkgutil
from pymel import core as pm
from xml import dom

mod = dom.registerDOMImplementation

print(dir(pkgutil.find_loader(mod.__module__)))
pkg = pkgutil.find_loader(mod.__module__)
print(pkg.get_filename())
