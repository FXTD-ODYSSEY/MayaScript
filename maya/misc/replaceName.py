import re
from functools import partial
import pymel.core as pm

# NOTE 替换命名脚本
replace_func = lambda k,m:k+m.group('char') if m.group('char') == "_" else k+"_"+m.group('char')
for sel in pm.ls("Lf*"):
    new_name = re.sub(r"^Lf(?P<char>\S)",partial(replace_func,"L"),str(sel))
    sel.rename(new_name)

for sel in pm.ls("Rt*"):
    new_name = re.sub(r"^Rt(?P<char>\S)",partial(replace_func,"R"),str(sel))
    sel.rename(new_name)

