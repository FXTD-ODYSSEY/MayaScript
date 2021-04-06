import pyblish.api
from maya import cmds


class CollectRig(pyblish.api.ContextPlugin):
    """Discover and collect available rigs into the context"""

    order = pyblish.api.CollectorOrder

    def process(self, context):
        for node in cmds.ls(sets=True):
            if not node.endswith("_RIG"):
                continue

            name = node.rsplit("_", 1)[0]
            instance = context.create_instance(name, family="rig")

            # Collect associated nodes
            members = cmds.sets(node, query=True)
            cmds.select([node] + members, noExpand=True)
            instance[:] = cmds.file(
                constructionHistory=True, exportSelected=True, preview=True, force=True
            )
