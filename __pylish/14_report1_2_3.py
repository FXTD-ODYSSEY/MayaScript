import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import pyblish.api

class CollectCaptainAmerica(pyblish.api.ContextPlugin):
  order = pyblish.api.CollectorOrder

  def process(self, context):
    context.create_instance("Captain America", isHero=False)

class ValidateCaptainAmerica(pyblish.api.InstancePlugin):
  order = pyblish.api.ValidatorOrder

  def process(self, instance):
    self.log.info("Entering validator..")
    self.log.info("About to validate instance: %s" % instance)

    if not instance.data.get("isHero"):
        self.log.warning("Something is not right.. aborting")
        raise Exception("%s must be a hero" % instance)

pyblish.api.register_plugin(CollectCaptainAmerica)
pyblish.api.register_plugin(ValidateCaptainAmerica)

import pyblish.util
context = pyblish.util.publish()

header = "{:<10}{:<40} -> {}".format("Success", "Plug-in", "Instance")
result = "{success:<10}{plugin.__name__:<40} -> {instance}"
error = "{:<10}+-- EXCEPTION: {:<70}"
record = "{:<10}+-- {level}: {message:<70}"

results = list()
for r in context.data["results"]:
  # Format summary
  results.append(result.format(**r))
  print(r)
  
  # Format log records
  for lr in r["records"]:
    results.append(record.format("", level=lr.levelname, message=lr.msg))

  # Format exception (if any)
  if r["error"]:
    results.append(error.format("", r["error"]))

report = """
{header}
{line}
{results}
"""
print(report.format(header=header,
                    results="\n".join(results),
                    line="-" * 70))