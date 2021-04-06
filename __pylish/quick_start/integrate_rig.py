import os
import shutil

import pyblish.api


class IntegrateRig(pyblish.api.InstancePlugin):
    """Copy files to an appropriate location where others may reach it"""

    order = pyblish.api.IntegratorOrder
    families = ["rig"]

    def process(self, instance):
        assert instance.data("tempdir"), "Can't find rig on disk, aborting.."

        self.log.info("Computing output directory..")
        context = instance.context
        dirname = os.path.dirname(context.data("currentFile"))
        root = os.path.join(dirname, "public")

        if not os.path.exists(root):
            os.makedirs(root)

        version = "v%03d" % (len(os.listdir(root)) + 1)

        src = instance.data("tempdir")
        dst = os.path.join(root, version)

        self.log.info("Copying %s to %s.." % (src, dst))

        shutil.copytree(src, dst)
        self.log.info("Copied successfully!")
