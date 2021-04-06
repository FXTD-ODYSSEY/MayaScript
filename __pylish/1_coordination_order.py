import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

import pyblish.api

class FirstPlugin(pyblish.api.ContextPlugin):
  order = 0

  def process(self, context):
    print("hello")

class SecondPlugin(pyblish.api.ContextPlugin):
  order = 1

  def process(self, context):
    print("world")

pyblish.api.register_plugin(FirstPlugin)
pyblish.api.register_plugin(SecondPlugin)

import pyblish.util
pyblish.util.publish()
# hello
# world