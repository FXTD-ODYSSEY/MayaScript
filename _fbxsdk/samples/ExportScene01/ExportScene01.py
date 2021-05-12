"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""

import sys

SAMPLE_FILENAME  = "ExportScene01.fbx"
ClusterWeight_Root = (1, 1, 1, 1, 0.75, 0.75, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25)
ClusterWeight_LimbNode1 = (0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25)
ClusterWeight_LimbNode2 = (0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 0.75, 1, 1, 1, 1)

def CreateScene(pSdkManager, pScene):
    # Create scene info
    lSceneInfo = FbxDocumentInfo.Create(pSdkManager, "SceneInfo")
    lSceneInfo.mTitle = "Example scene"
    lSceneInfo.mSubject = "Illustrates the creation and animation of a deformed cylinder."
    lSceneInfo.mAuthor = "ExportScene01.exe sample program."
    lSceneInfo.mRevision = "rev. 1.0"
    lSceneInfo.mKeywords = "deformed cylinder"
    lSceneInfo.mComment = "no particular comments required."
    pScene.SetSceneInfo(lSceneInfo)
    
    lPatchNode = CreatePatch(pSdkManager, "Patch")
    lSkeletonRoot = CreateSkeleton(pSdkManager, "Skeleton")
    
    pScene.GetRootNode().AddChild(lPatchNode)
    pScene.GetRootNode().AddChild(lSkeletonRoot)
    
    LinkPatchToSkeleton(lSdkManager, lPatchNode, lSkeletonRoot)
    StoreBindPose(lSdkManager, lScene, lPatchNode, lSkeletonRoot)
    StoreRestPose(lSdkManager, lScene, lSkeletonRoot)
    
    AnimateSkeleton(pSdkManager, pScene, lSkeletonRoot)
    
# Create a cylinder centered on the Z axis.
def CreatePatch(pSdkManager, pName):
    PatchControlPoints = (FbxVector4(15, 0, -60), FbxVector4(0, -15, -60), FbxVector4(-15, 0, -60), FbxVector4(0, 15, -60),
                                FbxVector4(15, 0, -40), FbxVector4(0, -15, -40), FbxVector4(-15, 0, -40), FbxVector4(0, 15, -40),
                                FbxVector4(15, 0, -20), FbxVector4(0, -15, -20), FbxVector4(-15, 0, -20), FbxVector4(0, 15, -20),
                                FbxVector4(15, 0, 0), FbxVector4(0, -15, 0), FbxVector4(-15, 0, 0), FbxVector4(0, 15, 0),
                                FbxVector4(15, 0, 20), FbxVector4(0, -15, 20), FbxVector4(-15, 0, 20), FbxVector4(0, 15, 20),
                                FbxVector4(15, 0, 40), FbxVector4(0, -15, 40), FbxVector4(-15, 0, 40), FbxVector4(0, 15, 40),
                                FbxVector4(15, 0, 60), FbxVector4(0, -15, 60), FbxVector4(-15, 0, 60), FbxVector4(0, 15, 60))

    lPatch = FbxPatch.Create(pSdkManager, pName)
    lPatch.InitControlPoints(4, FbxPatch.eBSpline, 7, FbxPatch.eBSpline)
    lPatch.SetStep(4, 4)
    lPatch.SetClosed(True, False)
    for i in range(28):
        lPatch.SetControlPointAt(PatchControlPoints[i], i)
    
    lPatchNode = FbxNode.Create(lSdkManager, pName)
    # Rotate the cylinder along the X axis so the axis
    # of the cylinder is the same as the bone axis (Y axis)
    lPatchNode.LclRotation.Set(FbxDouble3(-90, 0, 0))
    lPatchNode.SetNodeAttribute(lPatch)
    
    return lPatchNode
    
# Create a skeleton with 2 segments.
def CreateSkeleton(pSdkManager, pName):
    # Create skeleton root
    lRootName = pName + "Root"
    lSkeletonRootAttribute = FbxSkeleton.Create(lSdkManager, lRootName)
    lSkeletonRootAttribute.SetSkeletonType(FbxSkeleton.eRoot)
    lSkeletonRoot = FbxNode.Create(lSdkManager, lRootName)
    lSkeletonRoot.SetNodeAttribute(lSkeletonRootAttribute)    
    lSkeletonRoot.LclTranslation.Set(FbxDouble3(0.0, -40.0, 0.0))
    
    # Create skeleton first limb node.
    lLimbNodeName1 = pName + "LimbNode1"
    lSkeletonLimbNodeAttribute1 = FbxSkeleton.Create(lSdkManager, lLimbNodeName1)
    lSkeletonLimbNodeAttribute1.SetSkeletonType(FbxSkeleton.eLimbNode)
    lSkeletonLimbNodeAttribute1.Size.Set(1.0)
    lSkeletonLimbNode1 = FbxNode.Create(lSdkManager, lLimbNodeName1)
    lSkeletonLimbNode1.SetNodeAttribute(lSkeletonLimbNodeAttribute1)    
    lSkeletonLimbNode1.LclTranslation.Set(FbxDouble3(0.0, 40.0, 0.0))
    
    # Create skeleton second limb node.
    lLimbNodeName2 = pName + "LimbNode2"
    lSkeletonLimbNodeAttribute2 = FbxSkeleton.Create(lSdkManager, lLimbNodeName2)
    lSkeletonLimbNodeAttribute2.SetSkeletonType(FbxSkeleton.eLimbNode)
    lSkeletonLimbNodeAttribute2.Size.Set(1.0)
    lSkeletonLimbNode2 = FbxNode.Create(lSdkManager, lLimbNodeName2)
    lSkeletonLimbNode2.SetNodeAttribute(lSkeletonLimbNodeAttribute2)    
    lSkeletonLimbNode2.LclTranslation.Set(FbxDouble3(0.0, 40.0, 0.0))
    
    # Build skeleton node hierarchy. 
    lSkeletonRoot.AddChild(lSkeletonLimbNode1)
    lSkeletonLimbNode1.AddChild(lSkeletonLimbNode2)
    return lSkeletonRoot

# Set the influence of the skeleton segments over the cylinder.
# The link mode is FbxLink.eTotalOne which means the total
# of the weights assigned to a given control point must equal 1.
def LinkPatchToSkeleton(pSdkManager, pPatchNode, pSkeletonRoot):
    lLimbNode1 = pSkeletonRoot.GetChild(0)
    lLimbNode2 = lLimbNode1.GetChild(0)
    
    # Bottom section of cylinder is clustered to skeleton root.
    lClusterToRoot = FbxCluster.Create(pSdkManager, "")
    lClusterToRoot.SetLink(pSkeletonRoot)
    lClusterToRoot.SetLinkMode(FbxCluster.eTotalOne)
    for i in range(0, 16):
        lClusterToRoot.AddControlPointIndex(i, ClusterWeight_Root[i])
        
    # Center section of cylinder is clustered to skeleton limb node.
    lClusterToLimbNode1 = FbxCluster.Create(pSdkManager, "")
    lClusterToLimbNode1.SetLink(lLimbNode1)
    lClusterToLimbNode1.SetLinkMode(FbxCluster.eTotalOne)
    for i in range(4, 24):
        lClusterToLimbNode1.AddControlPointIndex(i, ClusterWeight_LimbNode1[i - 4])
        
    # Top section of cylinder is clustered to skeleton limb.
    lClusterToLimbNode2 = FbxCluster.Create(pSdkManager, "")
    lClusterToLimbNode2.SetLink(lLimbNode2)
    lClusterToLimbNode2.SetLinkMode(FbxCluster.eTotalOne)
    for i in range(12, 28):
        lClusterToLimbNode2.AddControlPointIndex(i, ClusterWeight_LimbNode2[i - 12])
        
    # Now we have the Patch and the skeleton correctly positioned,
    # set the Transform and TransformLink matrix accordingly.
    lXMatrix = FbxAMatrix()
    lScene = pPatchNode.GetScene()
    if lScene:
        lXMatrix = lScene.GetAnimationEvaluator().GetNodeGlobalTransform(pPatchNode)
    lClusterToRoot.SetTransformMatrix(lXMatrix)
    lClusterToLimbNode1.SetTransformMatrix(lXMatrix)
    lClusterToLimbNode2.SetTransformMatrix(lXMatrix)
    lScene = pSkeletonRoot.GetScene()
    if lScene:
        lXMatrix = lScene.GetAnimationEvaluator().GetNodeGlobalTransform(pSkeletonRoot)
    lClusterToRoot.SetTransformLinkMatrix(lXMatrix)
    lScene = lLimbNode1.GetScene()
    if lScene:
        lXMatrix = lScene.GetAnimationEvaluator().GetNodeGlobalTransform(lLimbNode1)
    lClusterToLimbNode1.SetTransformLinkMatrix(lXMatrix)
    lScene = lLimbNode2.GetScene()
    if lScene:
        lXMatrix = lScene.GetAnimationEvaluator().GetNodeGlobalTransform(lLimbNode2)
    lClusterToLimbNode2.SetTransformLinkMatrix(lXMatrix)
    
    # Add the clusters to the patch by creating a skin and adding those clusters to that skin.
    # After add that skin.
    lSkin = FbxSkin.Create(pSdkManager, "")
    lSkin.AddCluster(lClusterToRoot)
    lSkin.AddCluster(lClusterToLimbNode1)
    lSkin.AddCluster(lClusterToLimbNode2)
    pPatchNode.GetNodeAttribute().AddDeformer(lSkin)
    
# Add the specified node to the node array. Also, add recursively
# all the parent node of the specified node to the array.
def AddNodeRecursively(pNodeArray, pNode):
    if pNode:
        AddNodeRecursively(pNodeArray, pNode.GetParent())
        found = False 
        for node in pNodeArray:
            if node.GetName() == pNode.GetName():
                found = True
        if not found:
            # Node not in the list, add it
            pNodeArray += [pNode]
    
# Store the Bind Pose
def StoreBindPose(pSdkManager, pScene, pPatchNode, pSkeletonRoot):
    # In the bind pose, we must store all the link's global matrix at the time of the bind.
    # Plus, we must store all the parent(s) global matrix of a link, even if they are not
    # themselves deforming any model.

    # In this example, since there is only one model deformed, we don't need walk through the scene

    # Now list the all the link involve in the patch deformation
    lClusteredFbxNodes = []
    if pPatchNode and pPatchNode.GetNodeAttribute():
        lSkinCount = 0
        lClusterCount = 0
        lNodeAttributeType = pPatchNode.GetNodeAttribute().GetAttributeType()
        if lNodeAttributeType in (FbxNodeAttribute.eMesh, FbxNodeAttribute.eNurbs, FbxNodeAttribute.ePatch):
            lSkinCount = pPatchNode.GetNodeAttribute().GetDeformerCount(FbxDeformer.eSkin)
            for i in range(lSkinCount):
                lSkin = pPatchNode.GetNodeAttribute().GetDeformer(i, FbxDeformer.eSkin)
                lClusterCount += lSkin.GetClusterCount()
                
        # If we found some clusters we must add the node
        if lClusterCount:
            # Again, go through all the skins get each cluster link and add them
            for i in range(lSkinCount):
                lSkin = pPatchNode.GetNodeAttribute().GetDeformer(i, FbxDeformer.eSkin)
                lClusterCount = lSkin.GetClusterCount()
                for j in range(lClusterCount):
                    lClusterNode = lSkin.GetCluster(j).GetLink()
                    AddNodeRecursively(lClusteredFbxNodes, lClusterNode)
                    
            # Add the patch to the pose
            lClusteredFbxNodes += [pPatchNode]
            
    # Now create a bind pose with the link list
    if len(lClusteredFbxNodes):
        # A pose must be named. Arbitrarily use the name of the patch node.
        lPose = FbxPose.Create(pSdkManager, pPatchNode.GetName())
        lPose.SetIsBindPose(True)

        for lFbxNode in lClusteredFbxNodes:
            lBindMatrix = FbxAMatrix()
            lScene = lFbxNode.GetScene()
            if lScene:
                lBindMatrix = lScene.GetAnimationEvaluator().GetNodeGlobalTransform(lFbxNode)
            lPose.Add(lFbxNode, FbxMatrix(lBindMatrix))

        # Add the pose to the scene
        pScene.AddPose(lPose)

# Store a Rest Pose
def StoreRestPose(pSdkManager, pScene, pSkeletonRoot):
    # This example show an arbitrary rest pose assignment.
    # This rest pose will set the bone rotation to the same value 
    # as time 1 second in the first animation stack, but the 
    # position of the bone will be set elsewhere in the scene.

    # Create the rest pose
    lPose = FbxPose.Create(pSdkManager,"A Rest Pose")

    # Set the skeleton root node to the global position (10, 10, 10)
    # and global rotation of 45deg along the Z axis.
    lT = FbxVector4(10.0, 10.0, 10.0)
    lR = FbxVector4(0.0,  0.0, 45.0)
    lS = FbxVector4(1.0, 1.0, 1.0)

    lTransformMatrix = FbxMatrix()
    lTransformMatrix.SetTRS(lT, lR, lS)

    # Add the skeleton root node to the pose
    lFbxNode = pSkeletonRoot
    lPose.Add(lFbxNode, lTransformMatrix, False) # It's a global matrix

    # Set the lLimbNode1 node to the local position of (0, 40, 0)
    # and local rotation of -90deg along the Z axis. This show that
    # you can mix local and global coordinates in a rest pose.
    lT.Set(0.0, 40.0,   0.0)
    lR.Set(0.0,  0.0, -90.0)
    lTransformMatrix.SetTRS(lT, lR, lS)

    # Add the skeleton second node to the pose
    lFbxNode = lFbxNode.GetChild(0)
    lPose.Add(lFbxNode, lTransformMatrix, True) # It's a local matrix

    # Set the lLimbNode2 node to the local position of (0, 40, 0)
    # and local rotation of 45deg along the Z axis.
    lT.Set(0.0, 40.0, 0.0)
    lR.Set(0.0,  0.0, 45.0)
    lTransformMatrix.SetTRS(lT, lR, lS)

    # Add the skeleton second node to the pose
    lFbxNode = lFbxNode.GetChild(0)
    lPose.Add(lFbxNode, lTransformMatrix, True) # It's a local matrix

    # Now add the pose to the scene
    pScene.AddPose(lPose)
    
# Create two animation stacks.
def AnimateSkeleton(pSdkManager, pScene, pSkeletonRoot):
    lKeyIndex = 0
    lTime = FbxTime()

    lRoot = pSkeletonRoot
    lLimbNode1 = pSkeletonRoot.GetChild(0)

    # First animation stack.
    lAnimStackName = "Bend on 2 sides"
    lAnimStack = FbxAnimStack.Create(pScene, lAnimStackName)

    # The animation nodes can only exist on AnimLayers therefore it is mandatory to
    # add at least one AnimLayer to the AnimStack. And for the purpose of this example,
    # one layer is all we need.
    lAnimLayer = FbxAnimLayer.Create(pScene, "Base Layer")
    lAnimStack.AddMember(lAnimLayer)

    # Create the AnimCurve on the Rotation.Z channel
    lCurve = lRoot.LclRotation.GetCurve(lAnimLayer, "Z", True)
    if lCurve:
        lCurve.KeyModifyBegin()
        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(1.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 45.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, -45.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(3.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()
    
    # Same thing for the next object
    lCurve = lLimbNode1.LclRotation.GetCurve(lAnimLayer, "Z", True)
    if lCurve:
        lCurve.KeyModifyBegin()
        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(1.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, -90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(3.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()

    # Second animation stack.
    lAnimStackName = "Bend and turn around"
    lAnimStack = FbxAnimStack.Create(pScene, lAnimStackName)

    # The animation nodes can only exist on AnimLayers therefore it is mandatory to
    # add at least one AnimLayer to the AnimStack. And for the purpose of this example,
    # one layer is all we need.
    lAnimLayer = FbxAnimLayer.Create(pScene, "Base Layer")
    lAnimStack.AddMember(lAnimLayer)

    # Create the AnimCurve on the Rotation.Y channel
    lCurve = lRoot.LclRotation.GetCurve(lAnimLayer, "Y", True)
    if lCurve:
        lCurve.KeyModifyBegin()
        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 720.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()

    lCurve = lLimbNode1.LclRotation.GetCurve(lAnimLayer, "Z", True)
    if lCurve:
        lCurve.KeyModifyBegin()
        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(1.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()
        
if __name__ == "__main__":
    try:
        import FbxCommon
        from fbx import *
    except ImportError:
        print("Error: module FbxCommon and/or fbx failed to import.\n")
        print("Copy the files located in the compatible sub-folder lib/python<version> into your python interpreter site-packages folder.")
        import platform
        if platform.system() == 'Windows' or platform.system() == 'Microsoft':
            print('For example: copy ..\\..\\lib\\Python27_x64\\* C:\\Python27\\Lib\\site-packages')
        elif platform.system() == 'Linux':
            print('For example: cp ../../lib/Python27_x64/* /usr/local/lib/python2.7/site-packages')
        elif platform.system() == 'Darwin':
            print('For example: cp ../../lib/Python27_x64/* /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
        sys.exit(1)

    # Prepare the FBX SDK.
    (lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()

    # Create the scene.
    lResult = CreateScene(lSdkManager, lScene)

    if lResult == False:
        print("\n\nAn error occurred while creating the scene...\n")
        lSdkManager.Destroy()
        sys.exit(1)

    # Save the scene.
    # The example can take an output file name as an argument.
    if len(sys.argv) > 1:
        lResult = FbxCommon.SaveScene(lSdkManager, lScene, sys.argv[1])
    # A default output file name is given otherwise.
    else:
        lResult = FbxCommon.SaveScene(lSdkManager, lScene, SAMPLE_FILENAME)

    if lResult == False:
        print("\n\nAn error occurred while saving the scene...\n")
        lSdkManager.Destroy()
        sys.exit(1)

    # Destroy all objects created by the FBX SDK.
    lSdkManager.Destroy()
   
    sys.exit(0)
