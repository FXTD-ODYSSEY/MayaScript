import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None
import os
import random
import datetime

import pygal
import pyblish.api

class FlipCoin(pyblish.api.ContextPlugin):
  def process(self, context):
    if random.random() > 0.5:
        raise Exception("Failed")

class ArchiveValidation(pyblish.api.ContextPlugin):
  # Run after all validators have finished
  order = pyblish.api.ValidatorOrder + 0.1

  def process(self, context):
    formatted_results = self.format_results(context)

    # Compute output directory
    date = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(os.path.expanduser("~"), "logs")
    output_path = os.path.join(output_dir, date + ".txt")

    # Write to disk
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    with open(output_path, "w") as f:
      # E.g. c:\users\marcus\Documents\logs\20150612-110000.txt
      f.write(formatted_results)

    # Print rather than log, as this plug-in
    # won't be included in the results.
    print("Outputted to: %s" % output_dir)
    context.data["archiveDir"] = output_dir

  def format_results(self, context):
    header = "{:<10}{:<40} -> {}".format("Success", "Plug-in", "Instance")
    result = "{success:<10}{plugin.__name__:<40} -> {instance}"
    error = "{:<10}+-- EXCEPTION: {:<70}"
    record = "{:<10}+-- {level}: {message:<70}"

    results = list()
    for r in context.data["results"]:
      # Format summary
      results.append(result.format(**r))

      # Format log records
      for lr in r["records"]:
        results.append(record.format("", level=lr.levelname, message=lr.message))

      # Format exception (if any)
      if r["error"]:
        results.append(error.format("", r["error"]))

    report = """
{header}
{line}
{results}
    """

    return report.format(
      header=header,
      results="\n".join(results),
      line="-" * 70)

class PlotArchive(pyblish.api.ContextPlugin):
    # Run after archival
    order = pyblish.api.ValidatorOrder + 0.2

    def process(self, context):
        input_path = context.data["archiveDir"]
        output_path = os.path.join(input_path, "graph.svg")

        results = list()
        for fname in os.listdir(input_path)[-10:]:
            abspath = os.path.join(input_path, fname)
            with open(abspath) as f:
                lines = f.readlines()[2:]  # Top two are headers
                results.append([fname, any(line.startswith("0") for line in lines)])

        chart = pygal.StackedLine(fill=True,
                                  interpolate='cubic',
                                  style=pygal.style.LightSolarizedStyle)

        chart.title = 'Successful publishes over time'
        chart.x_labels = [str(results.index(r)) for r in results]
        chart.add("Publish", [r[1] for r in results])
        chart.render_to_file(output_path)


pyblish.api.register_plugin(FlipCoin)
pyblish.api.register_plugin(ArchiveValidation)
pyblish.api.register_plugin(PlotArchive)

import pyblish.util
pyblish.util.publish()
# Outputted to: C:\Users\marcus\logs