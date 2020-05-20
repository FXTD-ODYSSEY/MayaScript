# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-20 16:32:26'

"""

"""

import maya.cmds as cm
import math
from functools import partial


# Helper Functions
def f(vector):
    return [float("{:.15f}".format(c)) for c in vector]

def clamp(value, min, max):
    return min if value < min else max if value > max else value


def clamp_v(vector, min, max):
    return [clamp(component, min, max) for component in vector]


def abs_v(vector):
    return [abs(component) for component in vector]


def normalize(vector):
    magnitude = math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]) + (vector[2] * vector[2]))
    if magnitude == 0:
        return vector
    else:
        return [vector[0] / magnitude, vector[1] / magnitude, vector[2] / magnitude]


def sub(vec_a, vec_b):
    return [vec_a[0] - vec_b[0], vec_a[1] - vec_b[1], vec_a[2] - vec_b[2]]


def scale(vector, scalar):
    return [vector[0] * scalar, vector[1] * scalar, vector[2] * scalar]


# System Functions

class Undo(object):
    """
    Undo Context Helper
    With Undo():
        Single Undo Chunk
    With Undo(0):
        Omit from Undo
    """
    def __init__(self, result=1):
        self.result = result

    def __enter__(self):
        if self.result == 0:
            cm.undoInfo(stateWithoutFlush=0)
        else:
            cm.undoInfo(openChunk=1)

    def __exit__(self, *exc_info):
        if self.result == 0:
            cm.undoInfo(stateWithoutFlush=1)
        else:
            cm.undoInfo(closeChunk=1)


class rpartial(partial):
    """
    Last argument passed to rpartial used for Undo / Redo print result
    """
    def __init__(self, *args):
        self.result = args[-1]

    def __repr__(self):
        return self.result


def hideViewport(func):
    def wrapper(*args, **kwargs):
        for mp in cm.getPanel(type="modelPanel"):
            if cm.modelEditor(mp, q=1, av=1):
                break
        # NOTE 获取当前显示的对象
        nurbsCurves        = cm.modelEditor(mp,q = 1,nurbsCurves        = 1)
        nurbsSurfaces      = cm.modelEditor(mp,q = 1,nurbsSurfaces      = 1)
        cv                 = cm.modelEditor(mp,q = 1,cv                 = 1)
        hulls              = cm.modelEditor(mp,q = 1,hulls              = 1)
        polymeshes         = cm.modelEditor(mp,q = 1,polymeshes         = 1)
        subdivSurfaces     = cm.modelEditor(mp,q = 1,subdivSurfaces     = 1)
        planes             = cm.modelEditor(mp,q = 1,planes             = 1)
        lights             = cm.modelEditor(mp,q = 1,lights             = 1)
        cameras            = cm.modelEditor(mp,q = 1,cameras            = 1)
        imagePlane         = cm.modelEditor(mp,q = 1,imagePlane         = 1)
        joints             = cm.modelEditor(mp,q = 1,joints             = 1)
        ikHandles          = cm.modelEditor(mp,q = 1,ikHandles          = 1)
        deformers          = cm.modelEditor(mp,q = 1,deformers          = 1)
        dynamics           = cm.modelEditor(mp,q = 1,dynamics           = 1)
        particleInstancers = cm.modelEditor(mp,q = 1,particleInstancers = 1)
        fluids             = cm.modelEditor(mp,q = 1,fluids             = 1)
        hairSystems        = cm.modelEditor(mp,q = 1,hairSystems        = 1)
        follicles          = cm.modelEditor(mp,q = 1,follicles          = 1)
        nCloths            = cm.modelEditor(mp,q = 1,nCloths            = 1)
        nParticles         = cm.modelEditor(mp,q = 1,nParticles         = 1)
        nRigids            = cm.modelEditor(mp,q = 1,nRigids            = 1)
        dynamicConstraints = cm.modelEditor(mp,q = 1,dynamicConstraints = 1)
        locators           = cm.modelEditor(mp,q = 1,locators           = 1)
        dimensions         = cm.modelEditor(mp,q = 1,dimensions         = 1)
        pivots             = cm.modelEditor(mp,q = 1,pivots             = 1)
        handles            = cm.modelEditor(mp,q = 1,handles            = 1)
        textures           = cm.modelEditor(mp,q = 1,textures           = 1)
        strokes            = cm.modelEditor(mp,q = 1,strokes            = 1)
        motionTrails       = cm.modelEditor(mp,q = 1,motionTrails       = 1)
        pluginShapes       = cm.modelEditor(mp,q = 1,pluginShapes       = 1)
        clipGhosts         = cm.modelEditor(mp,q = 1,clipGhosts         = 1)
        greasePencils      = cm.modelEditor(mp,q = 1,greasePencils      = 1)

        cm.modelEditor(mp,e=1,allObjects=0)
        res = func(*args, **kwargs)

        cm.modelEditor(mp,e = 1,nurbsCurves        = nurbsCurves)
        cm.modelEditor(mp,e = 1,nurbsSurfaces      = nurbsSurfaces)
        cm.modelEditor(mp,e = 1,cv                 = cv)
        cm.modelEditor(mp,e = 1,hulls              = hulls)
        cm.modelEditor(mp,e = 1,polymeshes         = polymeshes)
        cm.modelEditor(mp,e = 1,subdivSurfaces     = subdivSurfaces)
        cm.modelEditor(mp,e = 1,planes             = planes)
        cm.modelEditor(mp,e = 1,lights             = lights)
        cm.modelEditor(mp,e = 1,cameras            = cameras)
        cm.modelEditor(mp,e = 1,imagePlane         = imagePlane)
        cm.modelEditor(mp,e = 1,joints             = joints)
        cm.modelEditor(mp,e = 1,ikHandles          = ikHandles)
        cm.modelEditor(mp,e = 1,deformers          = deformers)
        cm.modelEditor(mp,e = 1,dynamics           = dynamics)
        cm.modelEditor(mp,e = 1,particleInstancers = particleInstancers)
        cm.modelEditor(mp,e = 1,fluids             = fluids)
        cm.modelEditor(mp,e = 1,hairSystems        = hairSystems)
        cm.modelEditor(mp,e = 1,follicles          = follicles)
        cm.modelEditor(mp,e = 1,nCloths            = nCloths)
        cm.modelEditor(mp,e = 1,nParticles         = nParticles)
        cm.modelEditor(mp,e = 1,nRigids            = nRigids)
        cm.modelEditor(mp,e = 1,dynamicConstraints = dynamicConstraints)
        cm.modelEditor(mp,e = 1,locators           = locators)
        cm.modelEditor(mp,e = 1,dimensions         = dimensions)
        cm.modelEditor(mp,e = 1,pivots             = pivots)
        cm.modelEditor(mp,e = 1,handles            = handles)
        cm.modelEditor(mp,e = 1,textures           = textures)
        cm.modelEditor(mp,e = 1,strokes            = strokes)
        cm.modelEditor(mp,e = 1,motionTrails       = motionTrails)
        cm.modelEditor(mp,e = 1,pluginShapes       = pluginShapes)
        cm.modelEditor(mp,e = 1,clipGhosts         = clipGhosts)
        cm.modelEditor(mp,e = 1,greasePencils      = greasePencils)

        return res
    return wrapper
