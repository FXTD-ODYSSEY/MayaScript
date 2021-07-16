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

def DisplayNurb(pNode):
    lNurb = pNode.GetNodeAttribute ()

    DisplayString("Nurb Name: ", pNode.GetName())

    lSurfaceModes = [ "Raw", "Low No Normals", "Low", "High No Normals", "High" ]

    DisplayString("    Surface Mode: ", lSurfaceModes[lNurb.GetSurfaceMode()])

    lControlPointsCount = lNurb.GetControlPointsCount()
    lControlPoints = lNurb.GetControlPoints()

    for i in range(lControlPointsCount):
        DisplayInt("    Control Point ", i)
        Display3DVector("        Coordinates: ", lControlPoints[i])
        DisplayDouble("        Weight: ", lControlPoints[i][3])

    lNurbTypes = [ "Periodic", "Closed", "Open" ]

    DisplayString("    Nurb U Type: ", lNurbTypes[lNurb.GetNurbsUType()])
    DisplayInt("    U Count: ", lNurb.GetUCount())
    DisplayString("    Nurb V Type: ", lNurbTypes[lNurb.GetNurbsVType()])
    DisplayInt("    V Count: ", lNurb.GetVCount())
    DisplayInt("    U Order: ", lNurb.GetUOrder())
    DisplayInt("    V Order: ", lNurb.GetVOrder())
    DisplayInt("    U Step: ", lNurb.GetUStep())
    DisplayInt("    V Step: ", lNurb.GetVStep())

    lUKnotCount = lNurb.GetUKnotCount()
    lVKnotCount = lNurb.GetVKnotCount()
    lUMultiplicityCount = lNurb.GetUCount()
    lVMultiplicityCount = lNurb.GetVCount()
    lUKnotVector = lNurb.GetUKnotVector()
    lVKnotVector = lNurb.GetVKnotVector()
    lUMultiplicityVector = lNurb.GetUMultiplicityVector()
    lVMultiplicityVector = lNurb.GetVMultiplicityVector()

    lString = "    U Knot Vector: "

    for i in range(lUKnotCount):
        lString += str(lUKnotVector[i])

        if i < lUKnotCount - 1:
            lString += ", "

    lString += "\n"
    print(lString)

    lString = "    V Knot Vector: "

    for i in range(lVKnotCount):
        lString += str(lVKnotVector[i])

        if i < lVKnotCount - 1:
            lString += ", "

    lString += "\n"
    print(lString)

    lString = "    U Multiplicity Vector: "

    for i in range(lUMultiplicityCount):
        lString += str(lUMultiplicityVector[i])

        if i < lUMultiplicityCount - 1:
            lString += ", "

    lString += "\n"
    print(lString)

    lString = "    V Multiplicity Vector: "

    for i in range(lVMultiplicityCount):
        lString += str(lVMultiplicityVector[i])

        if i < lVMultiplicityCount - 1:
            lString += ", "

    lString += "\n"
    print(lString)

    DisplayString("")

    DisplayTexture(lNurb)
    DisplayMaterial(lNurb)
    DisplayLink(lNurb)
    DisplayShape(lNurb)
