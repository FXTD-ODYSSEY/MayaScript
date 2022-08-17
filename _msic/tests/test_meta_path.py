# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/58275573/13452951
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-07-23 10:29:10'


import sys
import types

class CustomFinder(object):
    def __init__(self):
        self.submodule_search_locations = []
        self.has_location = False
        self.origin = None
    
    def create_module(self, spec):
        return self.load_module(spec.name)
    
    # def exec_module(self, module):
    #     """Execute the given module in its own namespace
    #     This method is required to be present by importlib.abc.Loader,
    #     but since we know our module object is already fully-formed,
    #     this method merely no-ops.
    #     """
    #     print('exec_module',module)

    def find_spec(self, fullname,*args):
        self.name = fullname
        self.loader = self
        return self.find_module()
    
    # NOTES(timmyliang): compat with Python2
    def find_module(self,*args):
        return self
        
    def load_module(self, fullname):
        module = sys.modules.get(fullname)
        if module:
            return module
        
        new_module = types.ModuleType(fullname)
        sys.modules[fullname] = new_module
        new_module.__name__ = fullname
        new_module.__loader__ = self
        return new_module

if __name__ == "__main__":
    sys.meta_path.append(CustomFinder())
    
    import myapp
    print(myapp)  
