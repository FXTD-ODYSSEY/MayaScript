import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None


import pyblish.api

disk = {}
items = ["JOHN.person", "door.prop"]


class CollectInstances(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder  # <-- This is new

    def process(self, context):
        for item in items:
            name, suffix = item.split(".")
            context.create_instance(name, family=suffix)


class ValidateNamingConvention(pyblish.api.InstancePlugin):

    order = pyblish.api.ValidatorOrder

    def process(self, instance):
        name = instance.data["name"]
        assert name == name.title(), "Sorry, %s should have been %s" % (
            name,
            name.title(),
        )


class ExtractInstances(pyblish.api.InstancePlugin):

    order = pyblish.api.ExtractorOrder

    def process(self, instance):
        disk[instance.data["name"]] = instance


pyblish.api.register_plugin(CollectInstances)
pyblish.api.register_plugin(ValidateNamingConvention)
pyblish.api.register_plugin(ExtractInstances)

# import pyblish.util

# print(pyblish.api.CollectorOrder)
# print(pyblish.api.ValidatorOrder)
# print(pyblish.api.ExtractorOrder)
# print(pyblish.api.IntegratorOrder)
# pyblish.util.publish()
# Sorry, JOHN should have been John
# Sorry, door should have been Door