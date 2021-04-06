import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

import pyblish.api

items = ["john", "door"]


class CollectInstances(pyblish.api.ContextPlugin):
    order = 0

    def process(self, context):
        for item in items:
            context.create_instance(item)


# NOTE Using InstancePlugin
class PrintInstances(pyblish.api.InstancePlugin):
    order = 1

    def process(self, instance):
        print("Instance is: %s" % instance)


pyblish.api.register_plugin(CollectInstances)
pyblish.api.register_plugin(PrintInstances)

import pyblish.util

pyblish.util.publish()
# The instance is "john"
# The instance is "door"