import maya.cmds as mc
import maya.OpenMaya as om
from math import fmod


def rayIntersect(mesh, point, direction):

    #posted on cgtalk.com

    om.MGlobal.clearSelectionList()

    om.MGlobal.selectByName(mesh)
    sList = om.MSelectionList()
    #Assign current selection to the selection list object
    om.MGlobal.getActiveSelectionList(sList)

    item = om.MDagPath()
    sList.getDagPath(0, item)
    item.extendToShape()

    fnMesh = om.MFnMesh(item)

    raySource = om.MFloatPoint(point[0], point[1], point[2], 1.0)
    rayDir = om.MFloatVector(direction[0], direction[1], direction[2])
    faceIds = None
    triIds = None
    idsSorted = False
    testBothDirections = False
    worldSpace = om.MSpace.kWorld
    maxParam = 999999
    accelParams = None
    sortHits = True
    hitPoints = om.MFloatPointArray()
    #hitRayParams = om.MScriptUtil().asFloatPtr()
    hitRayParams = om.MFloatArray()
    hitFaces = om.MIntArray()
    hitTris = None
    hitBarys1 = None
    hitBarys2 = None
    tolerance = 0.0001
    hit = fnMesh.allIntersections(raySource, rayDir, faceIds, triIds, idsSorted, worldSpace, maxParam, testBothDirections, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTris, hitBarys1, hitBarys2, tolerance)

    result = int(fmod(len(hitFaces), 2))

    #clear selection as may cause problem if the function is called multiple times in succession
    om.MGlobal.clearSelectionList()
    return result