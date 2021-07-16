# coding:utf-8

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2019-12-03 22:02:34'

"""
选择骨骼生成方块控制器
"""

import pymel.core as pm
import pymel.core.datatypes as dt
import math


def generateCubeFromVector(start_pt, end_pt, distant=3, angle=45):
    x_vec = start_pt - end_pt

    y_vec = start_pt.cross(end_pt)
    if angle:
        # NOTE 角度转弧度
        angle = angle*math.pi/180
        y_vec = y_vec.rotateBy(x_vec, angle)
    y_vec.normalize()

    z_vec = x_vec.cross(y_vec)
    z_vec.normalize()

    # NOTE 计算8个顶点坐标位置
    start_corner_1 = start_pt+y_vec*distant
    start_corner_2 = start_pt-y_vec*distant
    start_corner_3 = start_pt+z_vec*distant
    start_corner_4 = start_pt-z_vec*distant

    end_corner_1 = end_pt+y_vec*distant
    end_corner_2 = end_pt-y_vec*distant
    end_corner_3 = end_pt+z_vec*distant
    end_corner_4 = end_pt-z_vec*distant

    # NOTE 生成方块曲线
    return pm.curve(d=1,p=[
        start_corner_1,
        start_corner_3,
        start_corner_2,
        start_corner_4,
        start_corner_1,
        end_corner_1,
        end_corner_3,
        end_corner_2,
        end_corner_4,
        end_corner_1,
        end_corner_4,
        start_corner_4,
        start_corner_2,
        end_corner_2,
        end_corner_3,
        start_corner_3,
    ])


def generateJointCube(distant=3):
    last_crv = None
    for i,start_jnt in enumerate(pm.ls(sl=1, v=1, ni=1, dag=1, type="joint"),1):
        start_matrix = start_jnt.worldMatrix[0].get()
        start_pt = start_jnt.getTranslation(space="world")
        for end_jnt in start_jnt.listRelatives(c=1, type="joint"):
            end_pt = end_jnt.getTranslation(space="world")
            crv = generateCubeFromVector(start_pt, end_pt, distant=distant)

            crv.rename("%s_ctrl" % start_jnt)
            x,y,z = start_pt
            pm.move(x,y,z,crv.scalePivot,crv.rotatePivot)
            grp = pm.group(crv)
            grp.rename(crv.name() + "_GRP")
            pm.xform(grp,m=start_matrix.inverse())
            pm.makeIdentity(grp,a=1,t=1,r=1,s=1,n=0,pn=1)
            pm.xform(grp,m=start_matrix)
            # if last_crv:
            #     grp.setParent(last_crv)
            last_crv = crv
            
            pm.setAttr(crv.sx,l=1,k=0,cb=0)
            pm.setAttr(crv.sy,l=1,k=0,cb=0)
            pm.setAttr(crv.sz,l=1,k=0,cb=0)
            pm.parentConstraint(crv,start_jnt,mo=1)

# def renameCurve():
#     for i,crv in enumerate(pm.ls(sl=1,dag=1,ni=1,type="nurbsCurve"),1):
#         crv = crv.getParent()
#         name = "cloth_%s_M" % i
#         crv.rename(name)
#         grp = crv.getParent()
#         grp.rename("%s_GRP" % name)


if __name__ == "__main__":
    generateJointCube(10)

    