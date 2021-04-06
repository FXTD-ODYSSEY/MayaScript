import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import pyblish.util
import pyblish.api


class MyCollector(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder

    def process(self, context):
        pyblish.api.emit("myEvent", data="myData")


def on_my_event(data):
    print(data)

pyblish.api.register_plugin(MyCollector)
pyblish.api.register_callback("myEvent", on_my_event)
pyblish.util.publish()
# 打印 myData
