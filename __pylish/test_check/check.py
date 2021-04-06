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

import pyblish

disk = {}
server = {}

class CollectInstances(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder

    def process(self, context):
        for name in cmds.ls(type="transform", assemblies=True):
            context.create_instance(name)

class ValidateNamingConvention(pyblish.api.InstancePlugin):

    order = pyblish.api.ValidatorOrder

    def process(self, instance):
        name = instance.data["name"]
        assert name == name.title(), "Sorry, %s should have been %s" % (
            name,
            name.title(),
        )

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
pyblish.api.register_plugin(ValidateNamingConvention)
pyblish.api.register_plugin(ExtractInstances)



        