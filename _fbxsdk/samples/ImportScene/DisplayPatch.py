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
from DisplayMaterial import DisplayMaterial
from DisplayTexture  import DisplayTexture
from DisplayLink     import DisplayLink
from DisplayShape    import DisplayShape

def DisplayPatch(pNode):
    lPatch = pNode.GetNodeAttribute()

    DisplayString("Patch Name: ", pNode.GetName())

    lSurfaceModes = [ "Raw", "Low No Normals", "Low", "High No Normals", "High" ]

    DisplayString("    Surface Mode: ", lSurfaceModes[lPatch.GetSurfaceMode()])

    lControlPointsCount = lPatch.GetControlPointsCount()
    lControlPoints = lPatch.GetControlPoints()

    for i in range(lControlPointsCount):
        DisplayInt("    Control Point ", i)
        Display3DVector("        Coordinates: ", lControlPoints[i])
        DisplayDouble("        Weight: ", lControlPoints[i][3])

    lPatchTypes = [ "Bezier", "Bezier Quadric", "Cardinal", "B-Spline", "Linear" ]

    DisplayString("    Patch U Type: ", lPatchTypes[lPatch.GetPatchUType()])
    DisplayInt("    U Count: ", lPatch.GetUCount())
    DisplayString("    Patch V Type: ", lPatchTypes[lPatch.GetPatchVType()])
    DisplayInt("    V Count: ", lPatch.GetVCount())
    DisplayInt("    U Step: ", lPatch.GetUStep())
    DisplayInt("    V Step: ", lPatch.GetVStep())
    DisplayBool("    U Closed: ", lPatch.GetUClosed())
    DisplayBool("    V Closed: ", lPatch.GetVClosed())
    DisplayBool("    U Capped Top: ", lPatch.GetUCappedTop())
    DisplayBool("    U Capped Bottom: ", lPatch.GetUCappedBottom())
    DisplayBool("    V Capped Top: ", lPatch.GetVCappedTop())
    DisplayBool("    V Capped Bottom: ", lPatch.GetVCappedBottom())

    DisplayString("")

    DisplayTexture(lPatch)
    DisplayMaterial(lPatch)
    DisplayLink(lPatch)
    DisplayShape(lPatch)
