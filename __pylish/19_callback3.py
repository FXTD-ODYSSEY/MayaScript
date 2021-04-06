import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import pyblish.api
from maya import cmds


def on_instance_toggled(instance, new_value, old_value):
    node = instance.data["nodeName"]
    cmds.setAttr(node + ".publish", new_value)
