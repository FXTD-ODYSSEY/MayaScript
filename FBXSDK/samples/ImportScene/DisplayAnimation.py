"""

 Copyright (C) 2001 - 2016 Autodesk, Inc. and/or its licensors.
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
from fbx import *

def DisplayAnimation(pScene):
    for i in range(pScene.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimStack.ClassId))):
        lAnimStack = pScene.GetSrcObject(FbxCriteria.ObjectType(FbxAnimStack.ClassId), i)

        lOutputString = "Animation Stack Name: "
        lOutputString += lAnimStack.GetName()
        lOutputString += "\n"
        print(lOutputString)

        DisplayAnimationStack(lAnimStack, pScene.GetRootNode(), True)
        DisplayAnimationStack(lAnimStack, pScene.GetRootNode(), False)

def DisplayAnimationStack(pAnimStack, pNode, isSwitcher):
    nbAnimLayers = pAnimStack.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimLayer.ClassId))

    lOutputString = "Animation stack contains "
    lOutputString += str(nbAnimLayers)
    lOutputString += " Animation Layer(s)"
    print(lOutputString)

    for l in range(nbAnimLayers):
        lAnimLayer = pAnimStack.GetSrcObject(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), l)

        lOutputString = "AnimLayer "
        lOutputString += str(l)
        print(lOutputString)

        DisplayAnimationLayer(lAnimLayer, pNode, isSwitcher)

def DisplayAnimationLayer(pAnimLayer, pNode, isSwitcher=False):
    lOutputString = "     Node Name: "
    lOutputString += pNode.GetName()
    lOutputString += "\n"
    print(lOutputString)

    DisplayChannels(pNode, pAnimLayer, DisplayCurveKeys, DisplayListCurveKeys, isSwitcher)
    print

    for lModelCount in range(pNode.GetChildCount()):
        DisplayAnimationLayer(pAnimLayer, pNode.GetChild(lModelCount), isSwitcher)


def DisplayChannels(pNode, pAnimLayer, DisplayCurve, DisplayListCurve, isSwitcher):
    lAnimCurve = None

    KFCURVENODE_T_X = "X"
    KFCURVENODE_T_Y = "Y"
    KFCURVENODE_T_Z = "Z"

    KFCURVENODE_R_X = "X"
    KFCURVENODE_R_Y = "Y"
    KFCURVENODE_R_Z = "Z"
    KFCURVENODE_R_W = "W"

    KFCURVENODE_S_X = "X"
    KFCURVENODE_S_Y = "Y"
    KFCURVENODE_S_Z = "Z"

    # Display general curves.
    if not isSwitcher:
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, KFCURVENODE_T_X)
        if lAnimCurve:
            print("        TX")
            DisplayCurve(lAnimCurve)
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, KFCURVENODE_T_Y)
        if lAnimCurve:
            print("        TY")
            DisplayCurve(lAnimCurve)
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, KFCURVENODE_T_Z)
        if lAnimCurve:
            print("        TZ")
            DisplayCurve(lAnimCurve)

        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, KFCURVENODE_R_X)
        if lAnimCurve:
            print("        RX")
            DisplayCurve(lAnimCurve)
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, KFCURVENODE_R_Y)
        if lAnimCurve:
            print("        RY")
            DisplayCurve(lAnimCurve)
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, KFCURVENODE_R_Z)
        if lAnimCurve:
            print("        RZ")
            DisplayCurve(lAnimCurve)

        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, KFCURVENODE_S_X)
        if lAnimCurve:
            print("        SX")
            DisplayCurve(lAnimCurve)
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, KFCURVENODE_S_Y)
        if lAnimCurve:
            print("        SY")
            DisplayCurve(lAnimCurve)
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, KFCURVENODE_S_Z)
        if lAnimCurve:
            print("        SZ")
            DisplayCurve(lAnimCurve)

    # Display curves specific to a light or marker.
    lNodeAttribute = pNode.GetNodeAttribute()

    KFCURVENODE_COLOR_RED = "X"
    KFCURVENODE_COLOR_GREEN = "Y"
    KFCURVENODE_COLOR_BLUE = "Z"
    
    if lNodeAttribute:
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, KFCURVENODE_COLOR_RED)
        if lAnimCurve:
            print("        Red")
            DisplayCurve(lAnimCurve)
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, KFCURVENODE_COLOR_GREEN)
        if lAnimCurve:
            print("        Green")
            DisplayCurve(lAnimCurve)
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, KFCURVENODE_COLOR_BLUE)
        if lAnimCurve:
            print("        Blue")
            DisplayCurve(lAnimCurve)

        # Display curves specific to a light.
        light = pNode.GetLight()
        if light:
            lAnimCurve = light.Intensity.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Intensity")
                DisplayCurve(lAnimCurve)

            lAnimCurve = light.OuterAngle.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Cone Angle")
                DisplayCurve(lAnimCurve)

            lAnimCurve = light.Fog.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Fog")
                DisplayCurve(lAnimCurve)

        # Display curves specific to a camera.
        camera = pNode.GetCamera()
        if camera:
            lAnimCurve = camera.FieldOfView.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Field of View")
                DisplayCurve(lAnimCurve)

            lAnimCurve = camera.FieldOfViewX.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Field of View X")
                DisplayCurve(lAnimCurve)

            lAnimCurve = camera.FieldOfViewY.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Field of View Y")
                DisplayCurve(lAnimCurve)

            lAnimCurve = camera.OpticalCenterX.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Optical Center X")
                DisplayCurve(lAnimCurve)

            lAnimCurve = camera.OpticalCenterY.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Optical Center Y")
                DisplayCurve(lAnimCurve)

            lAnimCurve = camera.Roll.GetCurve(pAnimLayer)
            if lAnimCurve:
                print("        Roll")
                DisplayCurve(lAnimCurve)

        # Display curves specific to a geometry.
        if lNodeAttribute.GetAttributeType() == FbxNodeAttribute.eMesh or \
            lNodeAttribute.GetAttributeType() == FbxNodeAttribute.eNurbs or \
            lNodeAttribute.GetAttributeType() == FbxNodeAttribute.ePatch:
            lGeometry = lNodeAttribute

            lBlendShapeDeformerCount = lGeometry.GetDeformerCount(FbxDeformer.eBlendShape)
            for lBlendShapeIndex in range(lBlendShapeDeformerCount):
                lBlendShape = lGeometry.GetDeformer(lBlendShapeIndex, FbxDeformer.eBlendShape)
                lBlendShapeChannelCount = lBlendShape.GetBlendShapeChannelCount()
                for lChannelIndex in range(lBlendShapeChannelCount):
                    lChannel = lBlendShape.GetBlendShapeChannel(lChannelIndex)
                    lChannelName = lChannel.GetName()
                    lAnimCurve = lGeometry.GetShapeChannel(lBlendShapeIndex, lChannelIndex, pAnimLayer, True)
                    if lAnimCurve:
                        print("        Shape %s" % lChannelName)
                        DisplayCurve(lAnimCurve)

    # Display curves specific to properties
    lProperty = pNode.GetFirstProperty()
    while lProperty.IsValid():
        if lProperty.GetFlag(FbxPropertyFlags.eUserDefined):
            lFbxFCurveNodeName  = lProperty.GetName()
            lCurveNode = lProperty.GetCurveNode(pAnimLayer)

            if not lCurveNode:
                lProperty = pNode.GetNextProperty(lProperty)
                continue

            lDataType = lProperty.GetPropertyDataType()
            if lDataType.GetType() == eFbxBool or lDataType.GetType() == eFbxDouble or lDataType.GetType() == eFbxFloat or lDataType.GetType() == eFbxInt:
                lMessage =  "        Property "
                lMessage += lProperty.GetName()
                if lProperty.GetLabel().GetLen() > 0:
                    lMessage += " (Label: "
                    lMessage += lProperty.GetLabel()
                    lMessage += ")"

                DisplayString(lMessage)

                for c in range(lCurveNode.GetCurveCount(0)):
                    lAnimCurve = lCurveNode.GetCurve(0, c)
                    if lAnimCurve:
                        DisplayCurve(lAnimCurve)
            elif lDataType.GetType() == eFbxDouble3 or lDataType.GetType() == eFbxDouble4 or lDataType.Is(FbxColor3DT) or lDataType.Is(FbxColor4DT):
                if lDataType.Is(FbxColor3DT) or lDataType.Is(FbxColor4DT):
                    lComponentName1 = KFCURVENODE_COLOR_RED
                    lComponentName2 = KFCURVENODE_COLOR_GREEN
                    lComponentName3 = KFCURVENODE_COLOR_BLUE                    
                else:
                    lComponentName1 = "X"
                    lComponentName2 = "Y"
                    lComponentName3 = "Z"
                
                lMessage =  "        Property "
                lMessage += lProperty.GetName()
                if lProperty.GetLabel().GetLen() > 0:
                    lMessage += " (Label: "
                    lMessage += lProperty.GetLabel()
                    lMessage += ")"
                DisplayString(lMessage)

                for c in range(lCurveNode.GetCurveCount(0)):
                    lAnimCurve = lCurveNode.GetCurve(0, c)
                    if lAnimCurve:
                        DisplayString("        Component ", lComponentName1)
                        DisplayCurve(lAnimCurve)

                for c in range(lCurveNode.GetCurveCount(1)):
                    lAnimCurve = lCurveNode.GetCurve(1, c)
                    if lAnimCurve:
                        DisplayString("        Component ", lComponentName2)
                        DisplayCurve(lAnimCurve)

                for c in range(lCurveNode.GetCurveCount(2)):
                    lAnimCurve = lCurveNode.GetCurve(2, c)
                    if lAnimCurve:
                        DisplayString("        Component ", lComponentName3)
                        DisplayCurve(lAnimCurve)
            elif lDataType.GetType() == eFbxEnum:
                lMessage =  "        Property "
                lMessage += lProperty.GetName()
                if lProperty.GetLabel().GetLen() > 0:
                    lMessage += " (Label: "
                    lMessage += lProperty.GetLabel()
                    lMessage += ")"
                DisplayString(lMessage)

                for c in range(lCurveNode.GetCurveCount(0)):
                    lAnimCurve = lCurveNode.GetCurve(0, c)
                    if lAnimCurve:
                        DisplayListCurve(lAnimCurve, lProperty)

        lProperty = pNode.GetNextProperty(lProperty)


def InterpolationFlagToIndex(flags):
    #if (flags&KFCURVE_INTERPOLATION_CONSTANT)==KFCURVE_INTERPOLATION_CONSTANT:
    #    return 1
    #if (flags&KFCURVE_INTERPOLATION_LINEAR)==KFCURVE_INTERPOLATION_LINEAR:
    #    return 2
    #if (flags&KFCURVE_INTERPOLATION_CUBIC)==KFCURVE_INTERPOLATION_CUBIC:
    #    return 3
    return 0

def ConstantmodeFlagToIndex(flags):
    #if (flags&KFCURVE_CONSTANT_STANDARD)==KFCURVE_CONSTANT_STANDARD:
    #    return 1
    #if (flags&KFCURVE_CONSTANT_NEXT)==KFCURVE_CONSTANT_NEXT:
    #    return 2
    return 0

def TangeantmodeFlagToIndex(flags):
    #if (flags&KFCURVE_TANGEANT_AUTO) == KFCURVE_TANGEANT_AUTO:
    #    return 1
    #if (flags&KFCURVE_TANGEANT_AUTO_BREAK)==KFCURVE_TANGEANT_AUTO_BREAK:
    #    return 2
    #if (flags&KFCURVE_TANGEANT_TCB) == KFCURVE_TANGEANT_TCB:
    #    return 3
    #if (flags&KFCURVE_TANGEANT_USER) == KFCURVE_TANGEANT_USER:
    #    return 4
    #if (flags&KFCURVE_GENERIC_BREAK) == KFCURVE_GENERIC_BREAK:
    #    return 5
    #if (flags&KFCURVE_TANGEANT_BREAK) ==KFCURVE_TANGEANT_BREAK:
    #    return 6
    return 0

def TangeantweightFlagToIndex(flags):
    #if (flags&KFCURVE_WEIGHTED_NONE) == KFCURVE_WEIGHTED_NONE:
    #    return 1
    #if (flags&KFCURVE_WEIGHTED_RIGHT) == KFCURVE_WEIGHTED_RIGHT:
    #    return 2
    #if (flags&KFCURVE_WEIGHTED_NEXT_LEFT) == KFCURVE_WEIGHTED_NEXT_LEFT:
    #    return 3
    return 0

def TangeantVelocityFlagToIndex(flags):
    #if (flags&KFCURVE_VELOCITY_NONE) == KFCURVE_VELOCITY_NONE:
    #    return 1
    #if (flags&KFCURVE_VELOCITY_RIGHT) == KFCURVE_VELOCITY_RIGHT:
    #    return 2
    #if (flags&KFCURVE_VELOCITY_NEXT_LEFT) == KFCURVE_VELOCITY_NEXT_LEFT:
    #    return 3
    return 0

def DisplayCurveKeys(pCurve):
    interpolation = [ "?", "constant", "linear", "cubic"]
    constantMode =  [ "?", "Standard", "Next" ]
    cubicMode =     [ "?", "Auto", "Auto break", "Tcb", "User", "Break", "User break" ]
    tangentWVMode = [ "?", "None", "Right", "Next left" ]

    lKeyCount = pCurve.KeyGetCount()

    for lCount in range(lKeyCount):
        lTimeString = ""
        lKeyValue = pCurve.KeyGetValue(lCount)
        lKeyTime  = pCurve.KeyGetTime(lCount)

        lOutputString = "            Key Time: "
        lOutputString += lKeyTime.GetTimeString(lTimeString)
        lOutputString += ".... Key Value: "
        lOutputString += str(lKeyValue)
        lOutputString += " [ "
        lOutputString += interpolation[ InterpolationFlagToIndex(pCurve.KeyGetInterpolation(lCount)) ]
        #if (pCurve.KeyGetInterpolation(lCount)&KFCURVE_INTERPOLATION_CONSTANT) == KFCURVE_INTERPOLATION_CONSTANT:
        #    lOutputString += " | "
        #    lOutputString += constantMode[ ConstantmodeFlagToIndex(pCurve.KeyGetConstantMode(lCount)) ]
        #elif (pCurve.KeyGetInterpolation(lCount)&KFCURVE_INTERPOLATION_CUBIC) == KFCURVE_INTERPOLATION_CUBIC:
        #    lOutputString += " | "
        #    lOutputString += cubicMode[ TangeantmodeFlagToIndex(pCurve.KeyGetTangeantMode(lCount)) ]
        #    lOutputString += " | "
        #    lOutputString += tangentWVMode[ TangeantweightFlagToIndex(pCurve.KeyGetTangeantWeightMode(lCount)) ]
        #    lOutputString += " | "
        #    lOutputString += tangentWVMode[ TangeantVelocityFlagToIndex(pCurve.KeyGetTangeantVelocityMode(lCount)) ]
            
        lOutputString += " ]"
        print(lOutputString)

def DisplayCurveDefault(pCurve):
    lOutputString = "            Default Value: "
    lOutputString += pCurve.GetValue()
    
    print(lOutputString)

def DisplayListCurveKeys(pCurve, pProperty):
    lKeyCount = pCurve.KeyGetCount()

    for lCount in range(lKeyCount):
        lKeyValue = static_cast<int>(pCurve.KeyGetValue(lCount))
        lKeyTime  = pCurve.KeyGetTime(lCount)

        lOutputString = "            Key Time: "
        lOutputString += lKeyTime.GetTimeString(lTimeString)
        lOutputString += ".... Key Value: "
        lOutputString += lKeyValue
        lOutputString += " ("
        lOutputString += pProperty.GetEnumValue(lKeyValue)
        lOutputString += ")"

        print(lOutputString)

def DisplayListCurveDefault(pCurve, pProperty):
    DisplayCurveDefault(pCurve)
