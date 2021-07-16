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
from fbx import FbxMarker
from fbx import FbxColor


def DisplayMarker(pNode):
    lMarker = pNode.GetNodeAttribute()

    DisplayString("Marker Name: ", pNode.GetName())

    # Type
    lString = "    Marker Type: "
    if lMarker.GetType() == FbxMarker.eStandard:
        lString += "Standard"
    elif lMarker.GetType() == FbxMarker.eOptical:
         lString += "Optical"
    elif lMarker.GetType() == FbxMarker.eEffectorIK:
         lString += "IK Effector"
    elif lMarker.GetType() == FbxMarker.eEffectorFK:
         lString += "FK Effector"
    DisplayString(lString)

    # Look
    lString = "    Marker Look: "
    if lMarker.Look.Get() == FbxMarker.eCube:
        lString += "Cube"
    elif lMarker.Look.Get() == FbxMarker.eHardCross:
        lString += "Hard Cross"
    elif lMarker.Look.Get() == FbxMarker.eLightCross:
        lString += "Light Cross"
    elif lMarker.Look.Get() == FbxMarker.eSphere:
        lString += "Sphere"
    DisplayString(lString)

    # Size
    #lString = "    Size: "
    #lString += str(lMarker.Size.Get())
    DisplayDouble("    Size: ", lMarker.Size.Get())

    # Color
    c = lMarker.Color.Get()
    color = FbxColor(c[0], c[1], c[2])
    DisplayColor("    Color: ", color)

    # IKPivot
    Display3DVector("    IKPivot: ", lMarker.IKPivot.Get())
