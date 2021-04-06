import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import pyblish.api

disk = {}
items = ["JOHN.person", "door.prop"]
# items = ["John.person", "Door.prop"]


class CollectInstances(pyblish.api.ContextPlugin):
    order = 0

    def process(self, context):
        for item in items:
            name, suffix = item.split(".")
            context.create_instance(name, family=suffix)


class ValidateNamingConvention(pyblish.api.InstancePlugin):
    order = 1

    def process(self, instance):
        name = instance.data["name"]
        assert name == name.title(), "Sorry, %s should have been %s" % (
            name,
            name.title(),
        )


class ExtractInstances(pyblish.api.InstancePlugin):
    order = 2

    def process(self, instance):
        disk[instance.data["name"]] = instance


pyblish.api.register_plugin(CollectInstances)
pyblish.api.register_plugin(ValidateNamingConvention)
pyblish.api.register_plugin(ExtractInstances)

import pyblish.util

pyblish.util.publish()
print("JOHN" in disk)
# True