import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

import pyblish.api

items = ["john.person", "door.prop"]


class CollectInstances(pyblish.api.ContextPlugin):
    order = 0

    def process(self, context):
        for item in items:
            name, suffix = item.split(".")
            instance = context.create_instance(name)
            instance.data["families"] = [suffix]


class PrintPersons(pyblish.api.InstancePlugin):
    order = 1
    families = ["person"]

    def process(self, instance):
        print("Person is: %s" % instance)


class PrintProps(pyblish.api.InstancePlugin):
    order = 1
    families = ["prop"]

    def process(self, instance):
        print("The prop is: %s" % instance)


pyblish.api.register_plugin(CollectInstances)
pyblish.api.register_plugin(PrintPersons)
pyblish.api.register_plugin(PrintProps)

import pyblish.util

pyblish.util.publish()
# The person is "john"
# The prop is "door"