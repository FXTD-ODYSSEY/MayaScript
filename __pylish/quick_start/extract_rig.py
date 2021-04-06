import os
import shutil
from datetime import datetime

import pyblish.api
from maya import cmds


class ExtractRig(pyblish.api.InstancePlugin):
    """Serialise valid rig"""

    order = pyblish.api.ExtractorOrder
    families = ["rig"]
    hosts = ["maya"]

    def process(self, instance):
        context = instance.context
        dirname = os.path.dirname(context.data["currentFile"])
        name, family = instance.data["name"], instance.data["family"]
        date = datetime.now().strftime("%Y%m%dT%H%M%SZ")

        # Find a temporary directory with support for publishing multiple times.
        tempdir = os.path.join(dirname, "temp", date, family, name)
        tempfile = os.path.join(tempdir, name + ".ma")

        self.log.info("Exporting %s to %s" % (instance, tempfile))

        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        cmds.select(instance, noExpand=True)  # `instance` a list
        cmds.file(
            tempfile,
            type="mayaAscii",
            exportSelected=True,
            constructionHistory=False,
            force=True,
        )

        # Store reference for integration
        instance.set_data("tempdir", tempdir)
