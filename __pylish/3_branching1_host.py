import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

import pyblish.api


class MyPlugin(pyblish.api.ContextPlugin):
    hosts = ["maya"]

    def process(self, context):
        from maya import cmds

        cmds.headsUpMessage("Hello from Pyblish")


pyblish.api.register_plugin(MyPlugin)

import pyblish.util

pyblish.util.publish()
# Hello from Pyblish