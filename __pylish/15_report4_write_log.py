import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import os
import datetime
import pyblish.api
from textwrap import dedent

class CollectCaptainAmerica(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder

    def process(self, context):
        context.create_instance("Captain America", isHero=False)


class ValidateCaptainAmerica(pyblish.api.InstancePlugin):
    order = pyblish.api.ValidatorOrder

    def process(self, instance):
        self.log.info("Entering validator..")
        self.log.info("About to validate instance: %s" % instance)

        if not instance.data["isHero"]:
            self.log.warning("Something is not right.. aborting")
            raise Exception("%s must be a hero" % instance)


class ArchiveValidation(pyblish.api.ContextPlugin):
    # Run after all validators have finished
    order = pyblish.api.ValidatorOrder + 0.1

    def process(self, context):
        formatted_results = self.format_results(context)

        # Compute output directory
        date = datetime.datetime.today().ctime()
        date = pyblish.api.format_filename(date)
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
        print("Outputted to: %s" % output_path)

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
                results.append(record.format("", level=lr.levelname, message=lr.msg))

            # Format exception (if any)
            if r["error"]:
                results.append(error.format("", r["error"]))

        report = dedent("""
            {header}
            {line}
            {results}   
        """)

        return report.format(header=header, results="\n".join(results), line="-" * 70)


pyblish.api.register_plugin(CollectCaptainAmerica)
pyblish.api.register_plugin(ValidateCaptainAmerica)
pyblish.api.register_plugin(ArchiveValidation)

import pyblish.util

pyblish.util.publish()