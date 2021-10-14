# -*- coding: utf-8 -*-
"""
获取骨骼对应 Mesh 的 UV 值用来生成 follicle


"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-10-11 14:35:55'

import pymel.core as pm
import pymel.core.datatypes as dt
from maya import OpenMaya

SCRIPT_UTIL = OpenMaya.MScriptUtil()



def get_closet_uv(mesh,pt):
    """get_closet_uv 
    通过给定的

    :param mesh: 模型
    :type mesh: nt.Transform | nt.Mesh
    :param pt: 任意物体
    :type pt: nt.Transform
    :return: u,v
    :rtype: uv 坐标值
    """
    mesh = mesh.getShape() if hasattr(mesh,"getShape") else mesh
    mesh = mesh.__apimfn__()
    # NOTES(timmyliang) 获取骨骼的坐标点位置
    pt = OpenMaya.MPoint(*pm.xform(pt,q=1,ws=1,t=1))
    
    # NOTES(timmyliang) 获取骨骼到模型的 UV 点数值
    uvPoint = SCRIPT_UTIL.asFloat2Ptr()
    mesh.getUVAtPoint(pt,uvPoint,OpenMaya.MSpace.kWorld)
    u = SCRIPT_UTIL.getFloat2ArrayItem(uvPoint,0,0)
    v = SCRIPT_UTIL.getFloat2ArrayItem(uvPoint,0,1)
    
    return u,v

def create_follicle(mesh,u,v):
    """create_follicle [summary]
    参考 https://lesterbanks.com/2015/08/python-scripting-a-follicle-constraint-tool-in-maya/

    :param mesh: 模型
    :type mesh: nt.Transform | nt.Mesh
    :param u: uv 的 u 坐标值
    :type u: float
    :param v: uv 的 v 坐标值
    :type v: float
    :return: 对应 uv 位置的毛囊节点
    :rtype: nt.Follicle
    """    
    mesh = mesh.getShape() if hasattr(mesh,"getShape") else mesh
    follicle = pm.createNode("follicle")
    transform = follicle.getParent()
    follicle.outRotate.connect(transform.r)
    follicle.outTranslate.connect(transform.t)
    follicle.simulationMethod.set(0)
    follicle.parameterU.set(u)
    follicle.parameterV.set(v)
    mesh.outMesh.connect(follicle.inputMesh)
    mesh.worldMatrix.connect(follicle.inputWorldMatrix)
    return transform


def main():
    # NOTES(timmyliang) 输入模型
    face_mesh = pm.PyNode('head_lod0_grp|head_lod0_mesh')

    # NOTES(timmyliang) 获取当前选中的骨骼
    end_jnts = [
        jnt for jnt in pm.ls(sl=1, dag=1, type="joint") if not jnt.getChildren(type="joint")
    ]

    follicle_list = []
    for jnt in end_jnts:
        u,v = get_closet_uv(face_mesh,jnt)
        follicle = create_follicle(face_mesh.getShape(),u,v)
        follicle_list.append(follicle)


if __name__ == "__main__":
    main()






