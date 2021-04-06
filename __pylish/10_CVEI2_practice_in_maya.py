# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-02-22 10:24:56"


import sys

MODULE = r"C:\Magician\maya\MagiMaya\scripts"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

disk = {}
server = {}


class cmds:
    @staticmethod
    def ls(type, assemblies):
        return maya.scene.keys()

    @staticmethod
    def file(path, exportSelected):
        disk[path] = maya.scene[maya.selected]

    @staticmethod
    def select(node):
        maya.selected = node


class maya:
    selected = None
    cmds = cmds
    scene = {
        "john": 0xB3513451,  # Binary
        "door": 0x516B481F,
    }


sys.modules["maya"] = maya

import pyblish.api
from maya import cmds


class CollectInstances(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder

    def process(self, context):
        for name in cmds.ls(type="transform", assemblies=True):
            context.create_instance(name)


class ExtractInstances(pyblish.api.InstancePlugin):
    order = pyblish.api.ExtractorOrder

    def process(self, instance):
        # 1. Compute temporary output path
        name = instance.data["name"]
        transient_path = "c:\temp\%s.mb" % name

        # 2. Perform serialisation
        cmds.select(name)
        cmds.file(transient_path, exportSelected=True)

        # 3. Store reference for subsequent plug-ins
        instance.data["transientDest"] = transient_path


class IntegrateInstances(pyblish.api.InstancePlugin):
    order = pyblish.api.IntegratorOrder

    def process(self, instance):
        transient_dest = instance.data["transientDest"]
        permanent_dest = "/instances/%s.mb" % instance
        server[permanent_dest] = disk[transient_dest]


pyblish.api.register_plugin(CollectInstances)
pyblish.api.register_plugin(ExtractInstances)
pyblish.api.register_plugin(IntegrateInstances)

import pyblish.util

pyblish.util.publish()
print(disk)
print(server)
# {'c:\temp\\john.mb': 3008443473L, 'c:\temp\\door.mb': 1365985311}
# {'/instances/john.mb': 3008443473L, '/instances/door.mb': 1365985311}