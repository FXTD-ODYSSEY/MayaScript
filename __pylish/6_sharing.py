import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import os
import datetime
import pyblish.api


class CollectUserDir(pyblish.api.ContextPlugin):
    order = 0

    def process(self, context):
        context.data["userDir"] = os.path.expanduser("~")


class WriteTime(pyblish.api.ContextPlugin):
    order = 1

    def process(self, context):
        user_dir = context.data["userDir"]
        destination_path = os.path.join(user_dir, "time.txt")

        print("Writing time to %s" % destination_path)
        with open(destination_path, "w") as f:
            f.write("The time is %s" % datetime.datetime.today().ctime())


pyblish.api.register_plugin(CollectUserDir)
pyblish.api.register_plugin(WriteTime)

import pyblish.util

pyblish.util.publish()
# Writing time to C:\Users\marcus\Documents\time.txt