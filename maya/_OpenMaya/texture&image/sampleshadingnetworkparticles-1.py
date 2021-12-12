# coding:utf-8
from __future__ import unicode_literals, division, print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-05-23 23:43:36'

"""
https://vimeo.com/130598894
https://mayastation.typepad.com/maya-station/2011/03/how-to-sample-a-3d-texture.html
"""

# example to be used to sample a 3D texture with a particle system
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaRender as omr
import maya.OpenMayaFX as omFX


def sampleColorAtParticle(textureNode, particleShapeNode):

    # get the particle object as an MObject

    selectionList = om.MSelectionList()
    selectionList.add(particleShapeNode)
    particleObject = om.MObject()
    selectionList.getDependNode(0, particleObject)

    # create a MFnParticle to get to the data

    particleDataFn = omFX.MFnParticleSystem(particleObject)

    # get the positionPP data

    posPPArray = om.MVectorArray()

    particleDataFn.getPerParticleAttribute("position", posPPArray)

    # these are the arguments required to sample a 3d texture:
    shadingNodeName = textureNode

    numSamples = posPPArray.length()
    pointArray = om.MFloatPointArray()
    pointArray.setLength(numSamples)

    refPoints = om.MFloatPointArray()
    refPoints.setLength(numSamples)

    for i in range(posPPArray.length()):
        particlePosVector = om.MVector()
        particlePosVector = posPPArray[i]
        location = om.MFloatPoint(
            particlePosVector[0], particlePosVector[1], particlePosVector[2])

        pointArray.set(location, i)
        refPoints.set(location, i)

    # but we don't need these
    useShadowMap = False
    reuseMaps = False
    cameraMatrix = om.MFloatMatrix()
    uCoords = None
    vCoords = None
    normals = None
    tangentUs = None
    tangentVs = None
    filterSizes = None

    # and the return arguments are empty....
    resultColors = om.MFloatVectorArray()
    resultTransparencies = om.MFloatVectorArray()

    # this is the command wot samples

    omr.MRenderUtil.sampleShadingNetwork(shadingNodeName, numSamples, useShadowMap, reuseMaps, cameraMatrix, pointArray,
                                         uCoords, vCoords, normals, refPoints, tangentUs, tangentVs, filterSizes, resultColors, resultTransparencies)

    # use the sampled colours to set rgbPP
    resultPPColors = om.MVectorArray()
    resultPPColors.clear()

    for i in range(resultColors.length()):
        floatVector = om.MFloatVector(resultColors[i])
        vector = om.MVector(floatVector)
        resultPPColors.append(vector)

    particleDataFn.setPerParticleAttribute("rgbPP", resultPPColors)
# end


# do it !
# make sure that particleShape1 has an rgbPP attribute!

sampleColorAtParticle("marble1.outColor", "particleShape1")

#
