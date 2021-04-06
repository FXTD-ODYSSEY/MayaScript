import pyblish.api


class MyPlugin1(pyblish.api.ContextPlugin):
    def process(self, context):
        print("hello from plugin1")
