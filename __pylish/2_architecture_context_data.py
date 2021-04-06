import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

import datetime
import pyblish.api


class CollectTime(pyblish.api.ContextPlugin):
    order = 0

    def process(self, context):
        time = datetime.datetime.now()
        context.data["time"] = time
        return 1


class PrintTime(pyblish.api.ContextPlugin):
    order = 1

    def process(self, context):
        time = context.data["time"]
        print(time)  
        return 2
        

pyblish.api.register_plugin(CollectTime)
pyblish.api.register_plugin(PrintTime)

import pyblish.util

context = pyblish.util.publish()
print("context",context)