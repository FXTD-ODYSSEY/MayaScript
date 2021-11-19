# -*- coding: utf-8 -*-
"""
https://sonictk.github.io/maya_node_callback_example/
"""

from __future__ import absolute_import, division, print_function

import sys
from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-07 22:10:58"

PLUGIN_NAME = "callbackNode"
__file__ = globals().get("__file__")
__file__ = __file__ or cmds.pluginInfo(PLUGIN_NAME, q=1, p=1)


class CallbackNodeAttrMixin(object):

    group = OpenMaya.MObject()
    enable = OpenMaya.MObject()
    script = OpenMaya.MObject()
    inputs = OpenMaya.MObject()
    outputs = OpenMaya.MObject()

    @classmethod
    def initializer(cls):

        eAttr = OpenMaya.MFnEnumAttribute()
        msgAttr = OpenMaya.MFnMessageAttribute()
        cAttr = OpenMaya.MFnCompoundAttribute()
        tAttr = OpenMaya.MFnTypedAttribute()

        cls.enable = eAttr.create("enable", "e", 0)
        eAttr.addField("off", 0)
        eAttr.addField("on", 1)
        eAttr.setKeyable(1)
        eAttr.setWritable(1)

        cls.script = tAttr.create("script", "s", OpenMaya.MFnData.kString)
        tAttr.setWritable(1)

        cls.inputs = msgAttr.create("inputs", "i")
        msgAttr.setArray(1)
        msgAttr.setKeyable(1)
        msgAttr.setWritable(1)
        msgAttr.setStorable(1)

        cls.outputs = msgAttr.create("outputs", "o")
        msgAttr.setArray(1)
        msgAttr.setKeyable(1)
        msgAttr.setWritable(1)
        msgAttr.setStorable(1)

        cls.group = cAttr.create("callbackGroup", "cg")
        cAttr.addChild(cls.enable)
        cAttr.addChild(cls.script)
        cAttr.addChild(cls.inputs)
        cAttr.addChild(cls.outputs)
        cAttr.setArray(1)
        cls.addAttribute(cls.group)


# Node definition
class CallbackNode(OpenMayaMPx.MPxNode, CallbackNodeAttrMixin):
    name = PLUGIN_NAME
    node_id = OpenMaya.MTypeId(0x00991)

    # def compute(self, plug, dataBlock):
    #     print(plug,plug.name())
    #     if plug == self.output:
    #         # - Get a handle to the input attribute that we will need for the
    #         # - computation. If the value is being supplied via a connection
    #         # - in the dependency graph, then this call will cause all upstream
    #         # - connections to be evaluated so that the correct value is supplied.
    #         inputData = dataBlock.inputValue(self.input)

    #         # - Read the input value from the handle.
    #         result = inputData.asFloat()

    #         # - Get a handle on the aOutput attribute
    #         outputHandle = dataBlock.outputValue(self.output)

    #         # - Set the new output value to the handle.
    #         outputHandle.setFloat(result * 2)
    #         dataBlock.setClean(plug)
    #     return OpenMaya.kUnknownParameter

    def __init__(self):
        super(CallbackNode, self).__init__()
        print("__init__")

    def postConstructor(self):
        print("postConstructor")

    def setDependentsDirty(self, plug, plug_array):
        # TODO 测试
        print("setDependentsDirty", plug, plug_array)
        return super(CallbackNode, self).setDependentsDirty(plug, plug_array)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(cls())


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(
            CallbackNode.name,
            CallbackNode.node_id,
            CallbackNode.creator,
            CallbackNode.initializer,
        )
    except:
        sys.stderr.write("Failed to register node: %s" % CallbackNode.name)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(CallbackNode.node_id)
    except:
        sys.stderr.write("Failed to deregister node: %s" % CallbackNode.name)
        raise


if __name__ == "__main__":
    cmds.delete(cmds.ls(type=PLUGIN_NAME))
    # cmds.delete(cmds.ls(type="floatConstant"))
    cmds.flushUndo()
    if cmds.pluginInfo(PLUGIN_NAME, q=1, loaded=1):
        cmds.unloadPlugin(PLUGIN_NAME)
    cmds.loadPlugin(__file__)

    v_node = cmds.createNode(PLUGIN_NAME)

