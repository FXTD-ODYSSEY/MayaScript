import os
import json
import inspect
from types import ModuleType

target_dir = r"F:\repo\MayaScript\maya\_mGear\_dir"
prefix = "mgear."

def dump_dir_module(module):
    
    if isinstance(module, str):
        module = __import__(module)
        
    for name, mod in inspect.getmembers(module):
        if not isinstance(mod, ModuleType):
            continue
        module_name = mod.__name__
        if not module_name.startswith(prefix):
            continue
        module_name = module_name.replace(prefix, "")
        path = os.path.join(target_dir, module_name + ".py")
        with open(path, "w") as f:
            json.dump(dir(mod), f, ensure_ascii=False)

if __name__ == "__main__":
    dump_dir_module("mgear.core")