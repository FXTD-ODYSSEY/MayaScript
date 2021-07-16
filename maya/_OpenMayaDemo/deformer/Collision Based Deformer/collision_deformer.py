# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-23 23:52:40'

"""
http://www.polygon.me/2017/06/collision-based-deformer.html
"""

import maya.OpenMaya as OpenMaya  
import maya.OpenMayaAnim as OpenMayaAnim  
import maya.OpenMayaMPx as OpenMayaMPx  

class collisionDeformer(OpenMayaMPx.MPxDeformerNode):  
    kPluginNodeId = OpenMaya.MTypeId(0x00000012)  
    kPluginNodeTypeName = "collisionDeformer"  
    
    def __init__(self):  
        OpenMayaMPx.MPxDeformerNode.__init__( self )  
        self.accelParams = OpenMaya.MMeshIsectAccelParams() #speeds up intersect calculation  
        self.intersector = OpenMaya.MMeshIntersector() #contains methods for efficiently finding the closest point to a mesh, required for collider  

    def deform( self, block, geoItr, matrix, index ):  
            
        #get ENVELOPE  
        envelope = OpenMayaMPx.cvar.MPxGeometryFilter_envelope  
        envelopeHandle = block.inputValue(envelope)  
        envelopeVal = envelopeHandle.asFloat()  
            
        if envelopeVal!=0:  
    
            #get COLLIDER MESH (as worldMesh)  
            colliderHandle = block.inputValue(self.collider)  
            inColliderMesh = colliderHandle.asMesh()  
                
            if not inColliderMesh.isNull():  
                    
                    #get collider fn mesh  
                    inColliderFn = OpenMaya.MFnMesh(inColliderMesh)  
                    
                    #get DEFORMED MESH  
                    inMesh = self.get_input_geom(block, index)  
                    
                    #get COLLIDER WORLD MATRIX to convert the bounding box to world space  
                    colliderMatrixHandle = block.inputValue(self.colliderMatrix)  
                    colliderMatrixVal = colliderMatrixHandle.asMatrix()  
                    
                    #get BOUNDING BOX MIN VALUES  
                    colliderBoundingBoxMinHandle = block.inputValue(self.colliderBoundingBoxMin)  
                    colliderBoundingBoxMinVal = colliderBoundingBoxMinHandle.asFloat3()  
                    
                    #get BOUNDING BOX MAX VALUES  
                    colliderBoundingBoxMaxHandle = block.inputValue(self.colliderBoundingBoxMax)  
                    colliderBoundingBoxMaxVal = colliderBoundingBoxMaxHandle.asFloat3()  
                    
                    #build new bounding box based on given values  
                    bbox = OpenMaya.MBoundingBox()  
                    bbox.expand(OpenMaya.MPoint(colliderBoundingBoxMinVal[0], colliderBoundingBoxMinVal[1], colliderBoundingBoxMinVal[2]))  
                    bbox.expand(OpenMaya.MPoint(colliderBoundingBoxMaxVal[0], colliderBoundingBoxMaxVal[1], colliderBoundingBoxMaxVal[2]))  
                    
                    #set up point on mesh and intersector for returning closest point and accelParams if required  
                    pointOnMesh = OpenMaya.MPointOnMesh()   
                    self.intersector.create(inColliderMesh, colliderMatrixVal)  
                    
                    #set up constants for allIntersections  
                    faceIds = None  
                    triIds = None  
                    idsSorted = False  
                    space = OpenMaya.MSpace.kWorld  
                    maxParam = 100000  
                    testBothDirs = False  
                    accelParams = None  
                    sortHits = False  
                    hitRayParams = None  
                    hitFaces = None  
                    hitTriangles = None  
                    hitBary1 = None  
                    hitBary2 = None  
                    tolerance = 0.0001  
                    floatVec = OpenMaya.MFloatVector(0, 1, 0) #set up arbitrary vector n.b this is fine for what we want here but anything more complex may require vector obtained from vertex  
                    
                    #deal with main mesh  
                    inMeshFn = OpenMaya.MFnMesh(inMesh)  
                    inPointArray = OpenMaya.MPointArray()  
                    inMeshFn.getPoints(inPointArray, OpenMaya.MSpace.kWorld)  
                    
                    #create array to store final points and set to correct length  
                    length = inPointArray.length()  
                    finalPositionArray = OpenMaya.MPointArray()  
                    finalPositionArray.setLength(length)  

                    #loop through all points. could also be done with geoItr  
                    for num in range(length):  
                        point = inPointArray[num]  
                        
                        #if point is within collider bounding box then consider it  
                        if bbox.contains(point):  
                            ##-- allIntersections variables --##  
                            floatPoint = OpenMaya.MFloatPoint(point)  
                            hitPoints = OpenMaya.MFloatPointArray()  

                            inColliderFn.allIntersections( floatPoint, floatVec, faceIds, triIds, idsSorted, space, maxParam, testBothDirs, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTriangles, hitBary1, hitBary2, tolerance )  
                    
                            if hitPoints.length()%2 == 1:       
                                #work out closest point  
                                closestPoint = OpenMaya.MPoint()  
                                inColliderFn.getClosestPoint(point, closestPoint, OpenMaya.MSpace.kWorld, None)  
                                    
                                #calculate delta and add to array  
                                delta = point - closestPoint  
                                finalPositionArray.set(point - delta, num)  
                                    
                            else:  
                                finalPositionArray.set(point, num)  
                                    
                        #if point is not in bounding box simply add the position to the final array  
                        else:  
                            finalPositionArray.set(point, num)  
                                    
                    inMeshFn.setPoints(finalPositionArray, OpenMaya.MSpace.kWorld)  
                                        
    def get_input_geom(self, block, index):  
        input_attr = OpenMayaMPx.cvar.MPxGeometryFilter_input  
        input_geom_attr = OpenMayaMPx.cvar.MPxGeometryFilter_inputGeom  
        input_handle = block.outputArrayValue(input_attr)  
        input_handle.jumpToElement(index)  
        input_geom_obj = input_handle.outputValue().child(input_geom_attr).asMesh()  
        return input_geom_obj  
                
            
def creator():  
    return OpenMayaMPx.asMPxPtr(collisionDeformer())  

    
def initialize():  
    gAttr = OpenMaya.MFnGenericAttribute()  
    mAttr = OpenMaya.MFnMatrixAttribute()  
    nAttr = OpenMaya.MFnNumericAttribute()  
    
    collisionDeformer.collider = gAttr.create( "colliderTarget", "col")  
    gAttr.addDataAccept( OpenMaya.MFnData.kMesh )  
            
    collisionDeformer.colliderBoundingBoxMin = nAttr.createPoint( "colliderBoundingBoxMin", "cbbmin")  
    
    collisionDeformer.colliderBoundingBoxMax = nAttr.createPoint( "colliderBoundingBoxMax", "cbbmax")  
    
    collisionDeformer.colliderMatrix = mAttr.create("colliderMatrix", "collMatr", OpenMaya.MFnNumericData.kFloat )  
    mAttr.setHidden(True)  
    
    collisionDeformer.multiplier = nAttr.create("multiplier", "mult", OpenMaya.MFnNumericData.kFloat, 1)  
    
    collisionDeformer.addAttribute( collisionDeformer.collider )  
    collisionDeformer.addAttribute( collisionDeformer.colliderMatrix )  
    collisionDeformer.addAttribute( collisionDeformer.colliderBoundingBoxMin )  
    collisionDeformer.addAttribute( collisionDeformer.colliderBoundingBoxMax )  
    collisionDeformer.addAttribute( collisionDeformer.multiplier )  
    
    outMesh = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom  
    
    collisionDeformer.attributeAffects( collisionDeformer.collider, outMesh )  
    collisionDeformer.attributeAffects( collisionDeformer.colliderBoundingBoxMin, outMesh )  
    collisionDeformer.attributeAffects( collisionDeformer.colliderBoundingBoxMax, outMesh )  
    collisionDeformer.attributeAffects( collisionDeformer.colliderMatrix, outMesh )  
    collisionDeformer.attributeAffects( collisionDeformer.multiplier, outMesh )  

    
def initializePlugin(obj):  
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Grover', '1.0', 'Any')  
    try:  
        plugin.registerNode('collisionDeformer', collisionDeformer.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)  
    except:  
        raise RuntimeError, 'Failed to register node'  

            
def uninitializePlugin(obj):  
    plugin = OpenMayaMPx.MFnPlugin(obj)  
    try:  
        plugin.deregisterNode(collisionDeformer.kPluginNodeId)  
    except:  
        raise RuntimeError, 'Failed to deregister node'  
            

