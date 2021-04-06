import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None


import pyblish.api

items = ["JOHN.person", "door.prop"]
# NOTE 正确的数据
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
        print(name)
        print(name.title())
        assert name == name.title(), "Sorry, %s should have been %s" % (
            name,
            name.title(),
        )


pyblish.api.register_plugin(CollectInstances)
pyblish.api.register_plugin(ValidateNamingConvention)

import pyblish.util

pyblish.util.publish()
# Sorry, JOHN should have been John
# Sorry, door should have been Door