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

from FbxCommon import *
from fbx import FbxNode

def DisplayPivotsAndLimits(pNode):
    # Pivots
    print("    Pivot Information")

    lPivotState = pNode.GetPivotState(FbxNode.eSourcePivot)
    if lPivotState == FbxNode.ePivotActive:
        print("        Pivot State: Active")
    else:
        print("        Pivot State: Reference")

    lTmpVector = pNode.GetPreRotation(FbxNode.eSourcePivot)
    print("        Pre-Rotation: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    lTmpVector = pNode.GetPostRotation(FbxNode.eSourcePivot)
    print("        Post-Rotation: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    lTmpVector = pNode.GetRotationPivot(FbxNode.eSourcePivot)
    print("        Rotation Pivot: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    lTmpVector = pNode.GetRotationOffset(FbxNode.eSourcePivot)
    print("        Rotation Offset: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    lTmpVector = pNode.GetScalingPivot(FbxNode.eSourcePivot)
    print("        Scaling Pivot: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    lTmpVector = pNode.GetScalingOffset(FbxNode.eSourcePivot)
    print("        Scaling Offset: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    print("    Limits Information")

    lIsActive = pNode.TranslationActive
    lMinXActive = pNode.TranslationMinX
    lMinYActive = pNode.TranslationMinY
    lMinZActive = pNode.TranslationMinZ
    lMaxXActive = pNode.TranslationMaxX
    lMaxYActive = pNode.TranslationMaxY
    lMaxZActive = pNode.TranslationMaxZ
    lMinValues = pNode.TranslationMin
    lMaxValues = pNode.TranslationMax

    if lIsActive:
        print("        Translation limits: Active")
    else:
        print("        Translation limits: Inactive")
    print("            X")
    if lMinXActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f" % lMinValues.Get()[0])
    if lMaxXActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[0])
    
    print("            Y")
    if lMinYActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f" % lMinValues.Get()[1])
    if lMaxYActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[1])
    
    print("            Z")
    if lMinZActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f"% lMinValues.Get()[2])
    if lMaxZActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[2])

    lIsActive = pNode.RotationActive
    lMinXActive = pNode.RotationMinX
    lMinYActive = pNode.RotationMinY
    lMinZActive = pNode.RotationMinZ
    lMaxXActive = pNode.RotationMaxX
    lMaxYActive = pNode.RotationMaxY
    lMaxZActive = pNode.RotationMaxZ
    lMinValues = pNode.RotationMin
    lMaxValues = pNode.RotationMax

    if lIsActive:
        print("        Rotation limits: Active")
    else:
        print("        Rotation limits: Inactive")    
    print("            X")
    if lMinXActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f" % lMinValues.Get()[0])
    if lMaxXActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[0])
    
    print("            Y")
    if lMinYActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f" % lMinValues.Get()[1])
    if lMaxYActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[1])
    
    print("            Z")
    if lMinZActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f"% lMinValues.Get()[2])
    if lMaxZActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[2])

    lIsActive = pNode.ScalingActive
    lMinXActive = pNode.ScalingMinX
    lMinYActive = pNode.ScalingMinY
    lMinZActive = pNode.ScalingMinZ
    lMaxXActive = pNode.ScalingMaxX
    lMaxYActive = pNode.ScalingMaxY
    lMaxZActive = pNode.ScalingMaxZ
    lMinValues = pNode.ScalingMin
    lMaxValues = pNode.ScalingMax

    if lIsActive:
        print("        Scaling limits: Active")
    else:
        print("        Scaling limits: Inactive")    
    print("            X")
    if lMinXActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f" % lMinValues.Get()[0])
    if lMaxXActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[0])
    
    print("            Y")
    if lMinYActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f" % lMinValues.Get()[1])
    if lMaxYActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[1])
    
    print("            Z")
    if lMinZActive:
        print("                Min Limit: Active")
    else:
        print("                Min Limit: Inactive")
    print("                Min Limit Value: %f"% lMinValues.Get()[2])
    if lMaxZActive:
        print("                Max Limit: Active")
    else:
        print("                Max Limit: Inactive")
    print("                Max Limit Value: %f" % lMaxValues.Get()[2])
