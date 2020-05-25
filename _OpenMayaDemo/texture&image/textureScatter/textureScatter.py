# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-23 23:08:58'

"""
https://vimeo.com/85522402
"""

import math,random
from maya import OpenMaya as om
from maya import OpenMayaRender as omr

def placeObjects(filename, duplicates=5):
    meshObject = om.MObject()
    parentPath= om.MDagPath()
    meshPath = om.MDagPath()
    meshList = om.MSelectionList()
    dgMod = om.MDagModifier()

    om.MGlobal.getActiveSelectionList(meshList)
    
    meshList.getDagPath(1,meshPath)
    meshList.getDagPath(0,parentPath)
    meshList.getDependNode(0,meshObject)

    parentFn = om.MFnMesh(parentPath)
    meshFn = om.MFnMesh(meshPath)

    count = 0
    while count < duplicates:

        uv = [random.uniform(0.01,1),random.uniform(0.01,1)]
        uvUtil = om.MScriptUtil()
        uvUtil.createFromList(uv,2)
        uvPoint = uvUtil.asFloat2Ptr()

        # NOTE 获取随机 UV 的颜色
        rgb = getRGBatUV(filename,uv)
        if rgb > [0.4,0.4,0.4]:
            meshIter = om.MItMeshPolygon(meshObject)
            outPoint = om.MPoint()
            space = om.MSpace.kWorld
            
            while not meshIter.isDone():
                faceId = meshIter.index()

                try:
                    # NOTE 获取模型在 UV 上的点 | 获取失败直接报错跳过
                    parentFn.getPointAtUV(faceId,outPoint,uvPoint,space)

                    # NOTE 复制第二个选择的物体
                    name = meshPath.fullPathName()
                    dupName = "%s_dup%s" % (name,count+1)
                    dgMod.commandToExecute('duplicate -n "%s" "%s"' % (dupName,name))
                    dgMod.doIt()

                    dgMod.commandToExecute("select -r %s" % dupName)

                    dupMeshPath = om.MDagPath()
                    dupList = om.MSelectionList()
                    om.MGlobal.getActiveSelectionList(dupList)
                    dupList.getDagPath(0,dupMeshPath)

                    transform = om.MFnTransform(dupMeshPath)

                    # NOTE 根据法线计算旋转角度
                    faceNormal = om.MVector()
                    dupObjVector = om.MVector(0,1,0)
                    meshIter.getNormal(faceNormal)

                    rotAxisOrig = dupObjVector ^ faceNormal
                    rotAxis = rotAxisOrig.normal()
                    angleOrig = dupObjVector * faceNormal
                    angleOrig2 = math.acos(angleOrig)
                    angleUtil = om.MScriptUtil(angleOrig2)
                    anglePtr = angleUtil.asFloatPtr()
                    angle = om.MDoubleArray(anglePtr,1)
                    quat = om.MQuaternion(angle[0],rotAxis)

                    tXYZ = om.MVector(outPoint.x,outPoint.y,outPoint.z)

                    # NOTE 设置位置和角度
                    transform.setTranslation(tXYZ,om.MSpace.kWorld)
                    transform.setRotation(quat,om.MSpace.kWorld)

                    count += 1

                except RuntimeError:
                    pass

                meshIter.next()



def getRGBatUV(filename,uv=[0,0]):
    # NOTE file 节点名称
    texutreFileName = filename
    uCoord = uv[0]
    vCoord = uv[1]

    # NOTE 获取输入的 UV
    uUtil = om.MScriptUtil(uCoord)
    vUtil = om.MScriptUtil(vCoord)
    uPtr = uUtil.asFloatPtr()
    vPtr = vUtil.asFloatPtr()
    uCoord = om.MDoubleArray(uPtr,1)
    vCoord = om.MDoubleArray(vPtr,1)

    # NOTE file 节点的 MObject
    textureList = om.MSelectionList()
    om.MGlobal.getSelectionListByName(texutreFileName,textureList)
    textureObject = om.MObject()
    textureList.getDependNode(0,textureObject)

    # NOTE 获取纹理颜色采样
    resultColor = om.MVectorArray()
    resultAlpha = om.MDoubleArray()
    omr.MRenderUtil.eval2dTexture(textureObject,uCoord,vCoord,resultColor,resultAlpha)

    return [resultColor[0].x,resultColor[0].y,resultColor[0].z]
    
placeObjects("file1",500)

