import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

import pyblish.api


def on_published(context):
    has_error = any(result["error"] is not None for result in context.data["results"])
    print("Publishing %s" % ("failed" if has_error else "finished"))


pyblish.api.register_callback("published", on_published)
# https://api.pyblish.com/data/events