from __future__ import print_function
import gc
import ctypes

def patchable_builtin(klass):
    refs = gc.get_referents(klass.__dict__)
    assert len(refs) == 1
    return refs[0]

dikt = patchable_builtin(str)

dikt["__getattr__"] = lambda self,attr:print(attr)



