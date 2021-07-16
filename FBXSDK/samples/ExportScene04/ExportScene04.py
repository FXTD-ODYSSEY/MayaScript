"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""

import sys
import math

SAMPLE_FILENAME = "ExportScene04.fbx"

def CreateScene(pSdkManager, pScene):
    lLightGroup = CreateLightGroup(pSdkManager, "LightGroup")
    lMarker = CreateMarker(pSdkManager, "Marker")
    lCamera1 = CreateCamera(pSdkManager, "Camera1")
    lCamera2 = CreateCamera(pSdkManager, "Camera2")

    pScene.GetGlobalSettings().SetAmbientColor(FbxColor(1.0, 0.5, 0.2))

    SetCameraPointOfInterest(lCamera1, lMarker)
    SetCameraPointOfInterest(lCamera2, lCamera1)

    SetLightGroupDefaultPosition(lLightGroup)
    SetMarkerDefaultPosition(lMarker)
    SetCamera1DefaultPosition(lCamera1)
    SetCamera2DefaultPosition(lCamera2)

    # Create the Animation Stack
    lAnimStack = FbxAnimStack.Create(pScene, "Rotating lights")

    # The animation nodes can only exist on AnimLayers therefore it is mandatory to
    # add at least one AnimLayer to the AnimStack. And for the purpose of this example,
    # one layer is all we need.
    lAnimLayer = FbxAnimLayer.Create(pScene, "Base Layer")
    lAnimStack.AddMember(lAnimLayer)

    # Build the scene graph.
    lRootNode = pScene.GetRootNode()
    lRootNode.AddChild(lLightGroup)
    lRootNode.AddChild(lMarker)
    lRootNode.AddChild(lCamera1)
    lCamera1.AddChild(lCamera2)


    # Set camera switcher as the default camera.
    pScene.GetGlobalSettings().SetDefaultCamera(FBXSDK_CAMERA_SWITCHER)

    AnimateLightGroup(lLightGroup, lAnimLayer)
    AnimateCamera(lCamera1, lAnimLayer)
    AnimateCameraSwitcher(pScene.GetRootNode().GetCameraSwitcher(), lAnimLayer)

    return True

# Create 6 lights and set global light settings.
def CreateLightGroup(pSdkManager, pName):
    lGroup = FbxNode.Create(pSdkManager,pName)

    for i in range(6):
        lLightName = pName
        lLightName += "-Light"
        lLightName += str(i)

        lNode = CreateLight(pSdkManager, lLightName)
        lGroup.AddChild(lNode)

    for i in range(6):
        lLight = lGroup.GetChild(i).GetNodeAttribute()
        lLight.FileName.Set("gobo.tif")# Resource file is in current directory.
        lLight.DrawGroundProjection.Set(True)
        lLight.DrawVolumetricLight.Set(True)
        lLight.DrawFrontFacingVolumetricLight.Set(False)

    return lGroup

# Create a spotlight. 
def CreateLight(pSdkManager, pName):
    lLight = FbxLight.Create(pSdkManager,pName)

    lLight.LightType.Set(FbxLight.eSpot)
    lLight.CastLight.Set(True)

    lNode = FbxNode.Create(pSdkManager,pName)

    lNode.SetNodeAttribute(lLight)

    return lNode

# Create a marker to use a point of interest for the camera. 
def CreateMarker(pSdkManager, pName):
    lMarker = FbxMarker.Create(pSdkManager,pName)

    lNode = FbxNode.Create(pSdkManager,pName)

    lNode.SetNodeAttribute(lMarker)

    return lNode

def CreateCamera(pSdkManager, pName):
    lCamera = FbxCamera.Create(pSdkManager, pName)

    # Modify some camera default settings.
    lCamera.SetApertureMode(FbxCamera.eVertical)
    lCamera.SetApertureWidth(0.816)
    lCamera.SetApertureHeight(0.612)
    lCamera.SetSqueezeRatio(0.5)

    lNode = FbxNode.Create(pSdkManager,pName)

    lNode.SetNodeAttribute(lCamera)

    return lNode

def SetCameraPointOfInterest(pCamera, pPointOfInterest):
    # Set the camera to always point at this node.
    pCamera.SetTarget(pPointOfInterest)

# The light group is just over the XZ plane.
def SetLightGroupDefaultPosition(pLightGroup):
    for i in range(pLightGroup.GetChildCount()):
        SetLightDefaultPosition(pLightGroup.GetChild(i), i)

    pLightGroup.LclTranslation.Set(FbxDouble3(0.0, 15.0, 0.0))
    pLightGroup.LclRotation.Set(FbxDouble3(0.0, 0.0, 0.0))
    pLightGroup.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

def SetLightDefaultPosition(pLight, pIndex):
    # Set light location depending of it's index.
    pLight.LclTranslation.Set(FbxDouble3(math.cos(pIndex) * 40.0, 0.0, math.sin(pIndex) * 40.0))
    pLight.LclRotation.Set(FbxDouble3(20.0, (90.0 - pIndex * 60.0), 0.0))
    pLight.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

    # Set light attributes depending of it's index.
    lColor = (
        FbxDouble3(1.0, 0.0, 0.0), 
        FbxDouble3(1.0, 1.0, 0.0), 
        FbxDouble3(0.0, 1.0, 0.0), 
        FbxDouble3(0.0, 1.0, 1.0), 
        FbxDouble3(0.0, 0.0, 1.0), 
        FbxDouble3(1.0, 0.0, 1.0)
    )

    light = pLight.GetLight()
    if light:
        light.Color.Set(lColor[pIndex % 6])
        light.Intensity.Set(33.0)
        light.OuterAngle.Set(90.0)
        light.Fog.Set(100.0)

def SetMarkerDefaultPosition(pMarker):
    # The marker is at the origin.
    pMarker.LclTranslation.Set(FbxDouble3(0.0, 0.0, 0.0))
    pMarker.LclRotation.Set(FbxDouble3(0.0, 0.0, 0.0))
    pMarker.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

# The code below shows how to compute the camera rotation.
# In the present case, it wouldn't be necessary since the
# camera is set to point to the marker. 
def SetCamera1DefaultPosition(pCamera):
    lCameraLocation = FbxDouble3(0.0, 100.0, -300.0)
    lDefaultPointOfInterest = FbxDouble3(1.0, 100.0, -300.0)
    lNewPointOfInterest = FbxDouble3(0, 0, 0)
    lRotation = FbxDouble3()
    lScaling = FbxDouble3(1.0, 1.0, 1.0)

    FbxVector4.AxisAlignmentInEulerAngle(FbxVector4(lCameraLocation), FbxVector4(lDefaultPointOfInterest), 
                                          FbxVector4(lNewPointOfInterest), FbxVector4(lRotation))

    pCamera.LclTranslation.Set(lCameraLocation)
    pCamera.LclRotation.Set(lRotation)
    pCamera.LclScaling.Set(lScaling)

def SetCamera2DefaultPosition(pCamera):
    pCamera.LclTranslation.Set(FbxDouble3(-150.0, 0.0, 75.0))

# The light group rises and rotates.
def AnimateLightGroup(pLightGroup, pAnimLayer):
    for i in range(pLightGroup.GetChildCount()):
        AnimateLight(pLightGroup.GetChild(i), i, pAnimLayer)

    # Create the CurveNodes (they are necessary for the GetCurve to successfully allocate the Animation curve)
    pLightGroup.LclRotation.GetCurveNode(pAnimLayer, True)
    pLightGroup.LclTranslation.GetCurveNode(pAnimLayer, True)

    # Y axis rotation.
    lTime = FbxTime()
    lCurve = pLightGroup.LclRotation.GetCurve(pAnimLayer, "Y", True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationLinear)

        lTime.SetSecondDouble(10.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 5*360.0)

        lCurve.KeyModifyEnd()

    # Y axis translation.
    lCurve = pLightGroup.LclTranslation.GetCurve(pAnimLayer, "Y", True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 15.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(5.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 200.0)

        lCurve.KeyModifyEnd()

# The lights are changing color, intensity, orientation and cone angle.
def AnimateLight(pLight, pIndex, pAnimLayer):
    light = pLight.GetLight()
    lTime = FbxTime()

    # Intensity fade in/out.
    # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
    light.Intensity.GetCurveNode(pAnimLayer, True)
    lCurve = light.Intensity.GetCurve(pAnimLayer, True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(3.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 33.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationLinear)

        lTime.SetSecondDouble(7.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 33.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(10.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)

        lCurve.KeyModifyEnd()

    # Fog fade in/out
    # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
    light.Fog.GetCurveNode(pAnimLayer, True)
    lCurve = light.Fog.GetCurve(pAnimLayer, True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(3.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 33.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationLinear)

        lTime.SetSecondDouble(7.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 33.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(10.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)

        lCurve.KeyModifyEnd()

    # X rotation swoops & cone angle woobles.
        # Create the CurveNodes (they are necessary for the GetCurve to successfully allocate the Animation curve)
        pLight.LclRotation.GetCurveNode(pAnimLayer, True)
        light.OuterAngle.GetCurveNode(pAnimLayer, True)

        lCurve = pLight.LclRotation.GetCurve(pAnimLayer, "X", True)
        lConeCurve = light.OuterAngle.GetCurve(pAnimLayer,True)

        lCurve.KeyModifyBegin()
        lConeCurve.KeyModifyBegin()

        for i in range(8):
            lTime.SetSecondDouble(i * 0.833333)
            lValue = math.cos((i + pIndex * 60.0) * 72.0)

            lKeyIndex = lCurve.KeyAdd(lTime)[0]
            lCurve.KeySetValue(lKeyIndex, (lValue - 0.4) * 30.0)
            lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
            lKeyIndex = lConeCurve.KeyAdd(lTime)[0]
            lConeCurve.KeySetValue(lKeyIndex, (2.0 - (lValue + 1.0)) * 45.0)
            lConeCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationLinear)

        # Finally, have the lights spread out and lose focus.
        lTime.SetSecondDouble(10.0)

        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, -90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lKeyIndex = lConeCurve.KeyAdd(lTime)[0]
        lConeCurve.KeySetValue(lKeyIndex, 180.0)
        lConeCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationLinear)

        lCurve.KeyModifyEnd()
        lConeCurve.KeyModifyEnd()

    # Color cycling.
        lColor = (
            FbxDouble3(1.0, 0.0, 0.0), 
            FbxDouble3(1.0, 1.0, 0.0), 
            FbxDouble3(0.0, 1.0, 0.0), 
            FbxDouble3(0.0, 1.0, 1.0), 
            FbxDouble3(0.0, 0.0, 1.0), 
            FbxDouble3(1.0, 0.0, 1.0)
        )

        lCurve = [None, None, None]
        # Create the CurveNodes (they are necessary for the GetCurve to successfully allocate the Animation curve)
        light.Color.GetCurveNode(pAnimLayer, True)
        lCurve[0] = light.Color.GetCurve(pAnimLayer,"X", True)
        lCurve[1] = light.Color.GetCurve(pAnimLayer,"Y", True)
        lCurve[2] = light.Color.GetCurve(pAnimLayer,"Z", True)

        if lCurve[0] and lCurve[1] and lCurve[2]:
            lCurve[0].KeyModifyBegin()
            lCurve[1].KeyModifyBegin()
            lCurve[2].KeyModifyBegin()

            for i in range(24):
                j = i + pIndex

                while j > 5:
                    j -= 6

                lTime.SetSecondDouble(i * 0.4166666)

                lKeyIndex = lCurve[0].KeyAdd(lTime)[0]
                lCurve[0].KeySetValue(lKeyIndex, lColor[j][0])
                lCurve[0].KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

                lKeyIndex = lCurve[1].KeyAdd(lTime)[0]
                lCurve[1].KeySetValue(lKeyIndex, lColor[j][1])
                lCurve[1].KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

                lKeyIndex = lCurve[2].KeyAdd(lTime)[0]
                lCurve[2].KeySetValue(lKeyIndex, lColor[j][2])
                lCurve[2].KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

            lCurve[0].KeyModifyEnd()
            lCurve[1].KeyModifyEnd()
            lCurve[2].KeyModifyEnd()

# The camera is rising and rolling twice.
def AnimateCamera(pCamera, pAnimLayer):
    # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
    pCamera.LclTranslation.GetCurveNode(pAnimLayer, True)

    # X translation.
    lTime = FbxTime()
    lCurve = pCamera.LclTranslation.GetCurve(pAnimLayer, "X", True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySet(lKeyIndex, lTime, 0.0, FbxAnimCurveDef.eInterpolationLinear)

        lTime.SetSecondDouble(10.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySet(lKeyIndex, lTime, 200.0)

        lCurve.KeyModifyEnd()

    # Y translation.
    lCurve = pCamera.LclTranslation.GetCurve(pAnimLayer, "Y", True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySet(lKeyIndex, lTime, 0.0, FbxAnimCurveDef.eInterpolationLinear)

        lTime.SetSecondDouble(10.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySet(lKeyIndex, lTime, 300.0)

        lCurve.KeyModifyEnd()

    # Camera roll.
    cam = pCamera.GetCamera()
    # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
    cam.Roll.GetCurveNode(pAnimLayer, True)
    lCurve = cam.Roll.GetCurve(pAnimLayer, True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble (0.0) 
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySet(lKeyIndex, lTime, 0.0, FbxAnimCurveDef.eInterpolationLinear)

        lTime.SetSecondDouble(10.0) 
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySet(lKeyIndex, lTime, 2*360.0)

        lCurve.KeyModifyEnd()

# Alternate between camera 1 and camera 2.
def AnimateCameraSwitcher(pCameraSwitcher, pAnimLayer):
    if not pCameraSwitcher:
        return

    # Camera index keys must be set with constant interpolation to 
    # make sure camera switches occur exactly at key time.

    # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
    pCameraSwitcher.CameraIndex.GetCurveNode(pAnimLayer, True)
    lCurve = pCameraSwitcher.CameraIndex.GetCurve(pAnimLayer, True)
    if lCurve:
        lCurve.KeyModifyBegin()

        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)
        lCurve.KeySetValue(lKeyIndex, 2.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationConstant)

        lTime.SetSecondDouble(2.5)
        lKeyIndex = lCurve.KeyAdd(lTime)
        lCurve.KeySetValue(lKeyIndex, 1.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationConstant)

        lTime.SetSecondDouble(5.0)
        lKeyIndex = lCurve.KeyAdd(lTime)
        lCurve.KeySetValue(lKeyIndex, 2.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationConstant)

        lTime.SetSecondDouble(7.5)
        lKeyIndex = lCurve.KeyAdd(lTime)
        lCurve.KeySetValue(lKeyIndex, 1.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationConstant)

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
