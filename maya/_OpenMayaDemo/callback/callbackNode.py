# -*- coding: utf-8 -*-
"""
https://sonictk.github.io/maya_node_callback_example/
Callback Node for dynamic update value without connections

__MAYA_CALLBACK_FUNC__ | default is `__callback__`
customize the callback function name 
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-07 22:10:58"

import os
import ast
import imp
from collections import defaultdict
from functools import partial
from string import Template

from maya import cmds
from maya import OpenMaya
from pymel.api import plugins
from pymel import core as pm

import six


PLUGIN_NAME = "callbackNode"
__file__ = globals().get("__file__")
__file__ = __file__ or cmds.pluginInfo(PLUGIN_NAME, q=1, p=1)
DIR = os.path.dirname(os.path.abspath(__file__))
nestdict = lambda: defaultdict(nestdict)


def ignore_undo_deco(func):
    def wrapper(*args, **kwargs):
        cmds.undoInfo(swf=0)
        res = func(*args, **kwargs)
        cmds.undoInfo(swf=1)
        return res

    return wrapper


class CallbackNodeAttrMixin(object):

    group = OpenMaya.MObject()
    enable = OpenMaya.MObject()
    script = OpenMaya.MObject()
    inputs = OpenMaya.MObject()
    outputs = OpenMaya.MObject()

    @classmethod
    def initialize(cls):

        eAttr = OpenMaya.MFnEnumAttribute()
        msgAttr = OpenMaya.MFnMessageAttribute()
        cAttr = OpenMaya.MFnCompoundAttribute()
        tAttr = OpenMaya.MFnTypedAttribute()

        cls.enable = eAttr.create("enable", "e", 1)
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

        cls.group = cAttr.create("group", "g")
        cAttr.addChild(cls.enable)
        cAttr.addChild(cls.script)
        cAttr.addChild(cls.inputs)
        cAttr.addChild(cls.outputs)
        cAttr.setArray(1)

        cls.addAttribute(cls.group)


class CallbackNodelogicMixin(object):
    @staticmethod
    def is_valid_python(code):
        """
        https://stackoverflow.com/a/11854793
        """
        try:
            ast.parse(code)
        except SyntaxError:
            return False
        return True

    def on_script_updated(self, msg, plug, other_plug=None, data=None):

        is_setattr = msg & OpenMaya.MNodeMessage.kAttributeSet
        if plug.attribute() != self.script and msg and not is_setattr:
            return

        grp = plug.parent()
        index = grp.logicalIndex()
        script = plug.asString()
        if not script:
            return

        module_name = "__CallbackCache[%s]__" % index

        envs = os.environ.copy()
        envs.update({"__file__": __file__, "__dir__": DIR})
        path = Template(script).substitute(envs)
        path = os.path.abspath(path)
        module = None
        if os.path.isfile(path):
            module = imp.load_source(module_name, path)
        elif self.is_valid_python(script):
            module = imp.new_module(module_name)
            six.exec_(script, module.__dict__)

        if module:
            self.cache[index] = module
        else:
            OpenMaya.MGlobal.displayWarning("`%s` not valid" % plug.name())

    def eval_sync_grp(self, grp, call_type):
        index = grp.logicalIndex()
        is_enable = grp.child(self.enable).asBool()
        module = self.cache.get(index)
        scirpt_plug_name = grp.child(self.script).name()
        callback = getattr(module, self.call_name, None)
        plug_data = self.plug_cache.get(index)
        try:
            assert is_enable
            assert module, "`%s` not valid" % scirpt_plug_name
            assert callable(callback), "`%s` -> `%s` method not exists" % (
                scirpt_plug_name,
                self.call_name,
            )
            inputs = plug_data["inputs"]
            assert inputs, "`%s` is empty" % grp.child(self.inputs).name()
            outputs = plug_data["outputs"]
            assert outputs, "`%s` is empty" % grp.child(self.outputs).name()

        except AssertionError as e:
            msg = str(e)
            msg and OpenMaya.MGlobal.displayWarning(msg)
            return

        data = {}
        data["inputs"] = [i for _, i in sorted(plug_data["inputs"].items())]
        data["outputs"] = [o for _, o in sorted(plug_data["outputs"].items())]
        data["type"] = call_type
        # NOTE ignore undo run callback
        cmds.evalDeferred(partial(ignore_undo_deco(callback), data))


class CallbackNode(CallbackNodeAttrMixin, CallbackNodelogicMixin, plugins.DependNode):
    call_name = os.getenv("__MAYA_CALLBACK_FUNC__") or "__callback__"
    _name = PLUGIN_NAME
    # _typeId = OpenMaya.MTypeId(0x00991)

    def postConstructor(self):
        self.cache = {}
        self.plug_cache = nestdict()
        self.is_connection_made = False
        self.is_connection_broke = False

        obj = self.thisMObject()
        OpenMaya.MNodeMessage.addAttributeChangedCallback(obj, self.on_script_updated)

    def setDependentsDirty(self, plug, plug_array):
        data = {}
        call_type = "eval"
        filter_attrs = [self.enable]
        if self.is_connection_made:
            call_type = "make_connection"
            self.is_connection_made = False
        else:
            filter_attrs.append(self.outputs)

        if self.is_connection_broke:
            call_type = "broke_connection"
            self.is_connection_broke = False

        # NOTE refresh message attribute
        cmds.evalDeferred(partial(cmds.dgdirty, plug.name(), c=1))

        attribute = plug.attribute()
        if attribute in filter_attrs:
            return
        elif attribute == self.script:
            return self.on_script_updated(0, plug)

        assert plug.isElement(), "unknown plug updated"
        grp = plug.array().parent()
        if grp == self.group:
            self.eval_sync_grp(grp, call_type)

    def connectionMade(self, plug, otherPlug, src):
        self.is_connection_made = True
        attribute = plug.attribute()
        is_inputs = attribute == self.inputs
        is_outputs = attribute == self.outputs
        if is_inputs or is_outputs:
            grp = plug.array().parent()
            grp_index = grp.logicalIndex()
            category = "inputs" if is_inputs else "outputs"
            index = plug.logicalIndex()
            self.plug_cache[grp_index][category][index] = otherPlug.name()

        # print("connectionMade", plug.name(), otherPlug.name(), src)
        return super(CallbackNode, self).connectionMade(plug, otherPlug, src)

    def connectionBroken(self, plug, otherPlug, src):
        self.is_connection_broke = True
        attribute = plug.attribute()
        is_inputs = attribute == self.inputs
        is_outputs = attribute == self.outputs
        if is_inputs or is_outputs:
            grp = plug.array().parent()
            grp_index = grp.logicalIndex()
            category = "inputs" if is_inputs else "outputs"
            index = plug.logicalIndex()
            self.plug_cache[grp_index][category].pop(index, None)

        # print("connectionBroken", plug.name(), otherPlug.name(), src)
        return super(CallbackNode, self).connectionBroken(plug, otherPlug, src)


def initializePlugin(mobject):
    CallbackNode.register(mobject)


def uninitializePlugin(mobject):
    CallbackNode.deregister(mobject)


if __name__ == "__main__":
    from textwrap import dedent

    cmds.delete(cmds.ls(type=PLUGIN_NAME))
    cmds.delete(cmds.ls(type="floatConstant"))
    cmds.flushUndo()
    if cmds.pluginInfo(PLUGIN_NAME, q=1, loaded=1):
        cmds.unloadPlugin(PLUGIN_NAME)
    cmds.loadPlugin(__file__)

    node = cmds.createNode(PLUGIN_NAME)
    float_constant = cmds.createNode("floatConstant")
    cmds.connectAttr(float_constant + ".outFloat", node + ".g[0].i[0]", f=1)
    float_constant = cmds.createNode("floatConstant")
    cmds.connectAttr(float_constant + ".inFloat", node + ".g[0].o[0]", f=1)
    code = dedent(
        """
        import pymel.core as pm
        def __callback__(data):
            inputs = data["inputs"]
            outputs = data["outputs"]
            src = pm.PyNode(inputs[0])
            dst = pm.PyNode(outputs[0])
            val = src.get()
            dst.set(val)
        """
    )
    node = "callbackNode1"
    cmds.setAttr(node + ".g[0].s", code, typ="string")
