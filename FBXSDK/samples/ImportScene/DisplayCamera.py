"""

 Copyright (C) 2001 - 2010 Autodesk, Inc. and/or its licensors.
 All Rights Reserved.

 The coded instructions, statements, computer programs, and/or related material 
 (collectively the "Data") in these files contain unpublished information 
 proprietary to Autodesk, Inc. and/or its licensors, which is protected by 
 Canada and United States of America federal copyright law and by international 
 treaties. 
 
 The Data may not be disclosed or distributed to third parties, in whole or in
 part, without the prior written consent of Autodesk, Inc. ("Autodesk").

 THE DATA IS PROVIDED "AS IS" AND WITHOUT WARRANTY.
 ALL WARRANTIES ARE EXPRESSLY EXCLUDED AND DISCLAIMED. AUTODESK MAKES NO
 WARRANTY OF ANY KIND WITH RESPECT TO THE DATA, EXPRESS, IMPLIED OR ARISING
 BY CUSTOM OR TRADE USAGE, AND DISCLAIMS ANY IMPLIED WARRANTIES OF TITLE, 
 NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE OR USE. 
 WITHOUT LIMITING THE FOREGOING, AUTODESK DOES NOT WARRANT THAT THE OPERATION
 OF THE DATA WILL BE UNINTERRUPTED OR ERROR FREE. 
 
 IN NO EVENT SHALL AUTODESK, ITS AFFILIATES, PARENT COMPANIES, LICENSORS
 OR SUPPLIERS ("AUTODESK GROUP") BE LIABLE FOR ANY LOSSES, DAMAGES OR EXPENSES
 OF ANY KIND (INCLUDING WITHOUT LIMITATION PUNITIVE OR MULTIPLE DAMAGES OR OTHER
 SPECIAL, DIRECT, INDIRECT, EXEMPLARY, INCIDENTAL, LOSS OF PROFITS, REVENUE
 OR DATA, COST OF COVER OR CONSEQUENTIAL LOSSES OR DAMAGES OF ANY KIND),
 HOWEVER CAUSED, AND REGARDLESS OF THE THEORY OF LIABILITY, WHETHER DERIVED
 FROM CONTRACT, TORT (INCLUDING, BUT NOT LIMITED TO, NEGLIGENCE), OR OTHERWISE,
 ARISING OUT OF OR RELATING TO THE DATA OR ITS USE OR ANY OTHER PERFORMANCE,
 WHETHER OR NOT AUTODESK HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH LOSS
 OR DAMAGE. 
 
"""

from DisplayCommon import *
from fbx import FbxCamera
from fbx import FbxString
from fbx import FbxColor

def DisplayCamera(pNode):
    lCamera = pNode.GetNodeAttribute()
    lName = pNode.GetName()
    lTargetNode = pNode.GetTarget()
    lTargetUpNode = pNode.GetTargetUp()
    
    DisplayString("Camera Name: ", lName)
    if not lCamera:
        DisplayString("NOT FOUND")
        return
    
    DisplayCameraPositionAndOrientation(lCamera, lTargetNode, lTargetUpNode)

    lProjectionTypes = [ "Perspective", "Orthogonal" ]

    DisplayString("    Projection Type: ", lProjectionTypes[lCamera.ProjectionType.Get()])

    DisplayViewingAreaControls(lCamera)

    # If camera projection type is set to FbxCamera.eOrthogonal, the 
    # aperture and film controls are not relevant.
    if lCamera.ProjectionType.Get() != FbxCamera.eOrthogonal:
        DisplayApertureAndFilmControls(lCamera)

    DisplayBackgroundProperties(lCamera)
    DisplayCameraViewOptions(lCamera)
    DisplayRenderOptions(lCamera)
    DisplayDefaultAnimationValues(lCamera)


def DisplayCameraPositionAndOrientation(pCamera, pTargetNode, pTargetUpNode):
    DisplayString("    Camera Position and Orientation")
    Display3DVector("        Position: ", pCamera.Position.Get())

    if pTargetNode:
        DisplayString("        Camera Interest: ",pTargetNode.GetName())
    else:
        Display3DVector("        Default Camera Interest Position: ", pCamera.InterestPosition.Get())

    if pTargetUpNode:
        DisplayString("        Camera Up Target: ", pTargetUpNode.GetName())
    else:
        Display3DVector("        Up Vector: ", pCamera.UpVector.Get())

    DisplayDouble("        Roll: ", pCamera.Roll.Get())


def DisplayViewingAreaControls(pCamera):
    DisplayString("    Viewing Area Controls")

    lCameraFormat = [ "Custom", "D1 NTSC", "NTSC", "PAL", "D1 PAL", \
        "HD", "640x480", "320x200", "320x240", "128x128", "Full Screen"  ]

    DisplayString("        Format: ", lCameraFormat[pCamera.GetFormat()])

    lAspectRatioModes = [ "Window Size", "Fixed Ratio", "Fixed Resolution", "Fixed Width", "Fixed Height" ]

    DisplayString("        Aspect Ratio Mode: ", lAspectRatioModes[pCamera.GetAspectRatioMode()])

    # If the ratio mode is eWINDOW_SIZE, both width and height values aren't relevant.
    if pCamera.GetAspectRatioMode() != FbxCamera.eWindowSize:
        DisplayDouble("        Aspect Width: ", pCamera.AspectWidth.Get())
        DisplayDouble("        Aspect Height: ", pCamera.AspectHeight.Get())

    DisplayDouble("        Pixel Ratio: ", pCamera.PixelAspectRatio.Get())
    DisplayDouble("        Near Plane: ", pCamera.NearPlane.Get())
    DisplayDouble("        Far Plane: ", pCamera.FarPlane.Get())
    DisplayBool("        Mouse Lock: ", pCamera.LockMode.Get())


def DisplayApertureAndFilmControls(pCamera):
    DisplayString("    Aperture and Film Controls")

    lCameraApertureFormats = [ "Custom", "16mm Theatrical", "Super 16mm", "35mm Academy", \
                               "35mm TV Projection", "35mm Full Aperture", "35mm 1.85 Projection", \
                              "35mm Anamorphic", "70mm Projection", "VistaVision", "Dynavision", "Imax" ]

    DisplayString("        Aperture Format: ", lCameraApertureFormats[pCamera.GetApertureFormat()])

    lCameraApertureModes = [ "Horizontal and Vertical", "Horizontal", "Vertical", "Focal Length" ]

    DisplayString("        Aperture Mode: ", lCameraApertureModes[pCamera.GetApertureMode()])

    DisplayDouble("        Aperture Width: ", pCamera.GetApertureWidth(), " inches")
    DisplayDouble("        Aperture Height: ", pCamera.GetApertureHeight(), " inches")
    DisplayDouble("        Squeeze Ratio: ", pCamera.GetSqueezeRatio())
    DisplayDouble("        Focal Length: ", pCamera.FocalLength.Get(), "mm")
    DisplayDouble("        Field of View: ", pCamera.FieldOfView.Get(), " degrees")


def DisplayBackgroundProperties(pCamera):
    DisplayString("    Background Properties")

    if pCamera.GetBackgroundFileName():
        DisplayString("        Background File Name: \"", pCamera.GetBackgroundFileName(), "\"")
    else:
        DisplayString("        Background File Name: \"", "\"")

    lBackgroundDisplayModes = [ "Disabled", "Always", "When Media" ]

    DisplayString("        Background Display Mode: ", lBackgroundDisplayModes[pCamera.ViewFrustumBackPlaneMode.Get()])

    DisplayBool("        Foreground Matte Threshold Enable: ", pCamera.ShowFrontplate.Get())

    # This option is only relevant if background drawing mode is set to eFOREGROUND or eBACKGROUND_AND_FOREGROUND.
    if pCamera.ForegroundOpacity.Get():
        DisplayDouble("        Foreground Matte Threshold: ", pCamera.BackgroundAlphaTreshold.Get())

    lBackgroundPlacementOptions = FbxString()
    if pCamera.GetBackPlateFitImage():
        lBackgroundPlacementOptions += " Fit,"
    if pCamera.GetBackPlateCenter():
        lBackgroundPlacementOptions += " Center,"
    if pCamera.GetBackPlateKeepRatio():
        lBackgroundPlacementOptions += " Keep Ratio,"
    if pCamera.GetBackPlateCrop():
        lBackgroundPlacementOptions += " Crop,"
    if not lBackgroundPlacementOptions.IsEmpty():
        lString =  lBackgroundPlacementOptions.Left(lBackgroundPlacementOptions.GetLen() - 1)
        DisplayString("        Background Placement Options: ",lString.Buffer())

    DisplayDouble("        Background Distance: ", pCamera.BackPlaneDistance.Get())

    lCameraBackgroundDistanceModes = [ "Relative to Interest", "Absolute from Camera" ]

    DisplayString("        Background Distance Mode: ", lCameraBackgroundDistanceModes[pCamera.BackPlaneDistanceMode.Get()])


def DisplayCameraViewOptions(pCamera):
    DisplayString("    Camera View Options")

    DisplayBool("        View Camera Interest: ", pCamera.ViewCameraToLookAt.Get())
    DisplayBool("        View Near Far Planes: ", pCamera.ViewFrustumNearFarPlane.Get())
    DisplayBool("        Show Grid: ", pCamera.ShowGrid.Get())
    DisplayBool("        Show Axis: ", pCamera.ShowAzimut.Get())
    DisplayBool("        Show Name: ", pCamera.ShowName.Get())
    DisplayBool("        Show Info on Moving: ", pCamera.ShowInfoOnMoving.Get())
    DisplayBool("        Show Time Code: ", pCamera.ShowTimeCode.Get())
    DisplayBool("        Display Safe Area: ", pCamera.DisplaySafeArea.Get())

    lSafeAreaStyles = [ "Round", "Square" ]

    DisplayString("        Safe Area Style: ", lSafeAreaStyles[pCamera.SafeAreaDisplayStyle.Get()])
    DisplayBool("        Show Audio: ", pCamera.ShowAudio.Get())

    c = pCamera.BackgroundColor.Get()
    color = FbxColor(c[0], c[1], c[2])
    DisplayColor("        Background Color: ", color)

    c = pCamera.AudioColor.Get()
    color = FbxColor(c[0], c[1], c[2])
    DisplayColor("        Audio Color: ", color)

    DisplayBool("        Use Frame Color: ", pCamera.UseFrameColor.Get())

    c = pCamera.FrameColor.Get()
    color = FbxColor(c[0], c[1], c[2])
    DisplayColor("        Frame Color: ", color)


def DisplayRenderOptions(pCamera):
    DisplayString("    Render Options")

    lCameraRenderOptionsUsageTimes = [ "Interactive", "At Render" ]

    DisplayString("        Render Options Usage Time: ", lCameraRenderOptionsUsageTimes[pCamera.UseRealTimeDOFAndAA.Get()])
    DisplayBool("        Use Antialiasing: ", pCamera.UseAntialiasing.Get())
    DisplayDouble("        Antialiasing Intensity: ", pCamera.AntialiasingIntensity.Get())

    lCameraAntialiasingMethods = [ "Oversampling Antialiasing", "Hardware Antialiasing" ]

    DisplayString("        Antialiasing Method: ", lCameraAntialiasingMethods[pCamera.AntialiasingMethod.Get()])

    # This option is only relevant if antialiasing method is set to eAAOversampling.
    if pCamera.AntialiasingMethod.Get() == FbxCamera.eAAOversampling:
        DisplayInt("        Number of Samples: ", pCamera.FrameSamplingCount.Get())

    lCameraSamplingTypes = [ "Uniform", "Stochastic" ]

    DisplayString("        Sampling Type: ", lCameraSamplingTypes[pCamera.FrameSamplingType.Get()])
    DisplayBool("        Use Accumulation Buffer: ", pCamera.UseAccumulationBuffer.Get())
    DisplayBool("        Use Depth of Field: ", pCamera.UseDepthOfField.Get())

    lCameraFocusDistanceSources = [ "Camera Interest", "Specific Distance" ]

    DisplayString("        Focus Distance Source: ", lCameraFocusDistanceSources[pCamera.FocusSource.Get()])

    # This parameter is only relevant if focus distance source is set to eFocusSpecificDistance.
    if pCamera.FocusSource.Get() == FbxCamera.eFocusSpecificDistance:
        DisplayDouble("        Specific Distance: ", pCamera.FocusDistance.Get())

    DisplayDouble("        Focus Angle: ", pCamera.FocusAngle.Get(), " degrees")


def DisplayDefaultAnimationValues(pCamera):
    DisplayString("    Default Animation Values")

    DisplayDouble("        Default Field of View: ", pCamera.FieldOfView.Get())
    DisplayDouble("        Default Field of View X: ", pCamera.FieldOfViewX.Get())
    DisplayDouble("        Default Field of View Y: ", pCamera.FieldOfViewY.Get())
    DisplayDouble("        Default Optical Center X: ", pCamera.OpticalCenterX.Get())
    DisplayDouble("        Default Optical Center Y: ", pCamera.OpticalCenterY.Get())
    DisplayDouble("        Default Roll: ", pCamera.Roll.Get())
