# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-23 23:08:58'

"""
https://vimeo.com/85522402
"""

import math,random
from maya.api import OpenMaya as om
from maya.api import OpenMayaRender as omr
from maya import OpenMaya
from maya import OpenMayaRender
from maya import cmds


def placeObjects(filename, duplicates=100):

    meshList = om.MGlobal.getActiveSelectionList()
    
    parentPath = meshList.getDagPath(0)
    meshPath,meshObject = meshList.getComponent(1)

    parentFn = om.MFnMesh(parentPath)
    meshFn = om.MFnMesh(meshPath)
    meshIter = om.MItMeshPolygon(parentPath)

    count = 0
    while count < duplicates:

        u,v = [random.uniform(0.01,1),random.uniform(0.01,1)]

        # NOTE 获取随机 UV 的颜色 | OpenMaya2.0 不支持
        rgb = getRGBatUV(filename,[u,v])
        if rgb <= [0.4,0.4,0.4]:
            continue
        
        meshIter.reset()
        while not meshIter.isDone():
            faceId = meshIter.index()
            try:
                outPoint = meshIter.getPointAtUV([u,v],om.MSpace.kWorld)
            except RuntimeError:
                meshIter.next(1)
                continue

            faceNormal = meshIter.getNormal()
            name = meshPath.fullPathName()
            dupName = "%s_dup%s" % (name,count+1)
            dup = cmds.duplicate(name,n=dupName)

            # NOTE Maya cmds 计算角度
            t = [outPoint.x,outPoint.y,outPoint.z]
            ro = cmds.angleBetween( euler=True, v1=(0.0, 1.0, 0.0), v2=t )
            cmds.xform(dup,ws=1,t=t)
            cmds.xform(dup,ws=1,ro=ro)

            # NOTE 旧方案的计算方法
            # selectionList = om.MSelectionList()
            # selectionList.add(dupName)
            # dupMeshPath = selectionList.getDagPath(0)
            # transform = om.MFnTransform(dupMeshPath)

            # dupObjVector = om.MVector(0,1,0)
            # rotAxisOrig = dupObjVector ^ faceNormal
            # rotAxis = rotAxisOrig.normal()
            # angleOrig = dupObjVector * faceNormal
            # angle = math.acos(angleOrig)
            # quat = om.MQuaternion(angle,rotAxis)

            # transform.setTranslation(om.MVector(outPoint),om.MSpace.kWorld)
            # transform.setRotation(quat,om.MSpace.kWorld)

            count += 1
            break

def getRGBatUV(filename,uv=[0,0]):
    # NOTE file 节点名称
    texutreFileName = filename
    uCoord = uv[0]
    vCoord = uv[1]

    # NOTE 获取输入的 UV
    uUtil = OpenMaya.MScriptUtil(uCoord)
    vUtil = OpenMaya.MScriptUtil(vCoord)
    uPtr = uUtil.asFloatPtr()
    vPtr = vUtil.asFloatPtr()
    uCoord = OpenMaya.MDoubleArray(uPtr,1)
    vCoord = OpenMaya.MDoubleArray(vPtr,1)

    # NOTE file 节点的 MObject
    textureList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getSelectionListByName(texutreFileName,textureList)
    textureObject = OpenMaya.MObject()
    textureList.getDependNode(0,textureObject)

    # NOTE 获取纹理颜色采样
    resultColor = OpenMaya.MVectorArray()
    resultAlpha = OpenMaya.MDoubleArray()
    OpenMayaRender.MRenderUtil.eval2dTexture(textureObject,uCoord,vCoord,resultColor,resultAlpha)

    return [resultColor[0].x,resultColor[0].y,resultColor[0].z]
    
placeObjects("file1")

