import pyblish.api


class MyPlugin2(pyblish.api.ContextPlugin):
    def process(self, context):
        print("hello from plugin2")
