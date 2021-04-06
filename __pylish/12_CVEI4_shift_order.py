import sys
MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0,MODULE) if MODULE not in sys.path else None


import pyblish.api

class PreCollector(pyblish.api.ContextPlugin):
  order = pyblish.api.CollectorOrder - 0.1

  def process(self, context):
    context.create_instance("SpecialInstance")


class Collector(pyblish.api.ContextPlugin):
  order = pyblish.api.CollectorOrder

  def process(self, context):
    special_instance = context["SpecialInstance"]
    special_instance.data["specialData"] = 42
    
"""
-0.5 to 0.499.. = Collection
0.5 to 1.499.. = Validation
1.5 to 2.499.. = Extraction
2.5 to 3.499.. = Integration
"""