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

from fbx import *
from DisplayCommon import *

def DisplayMaterial(pGeometry):
    lMaterialCount = 0
    lNode = None
    if pGeometry:
        lNode = pGeometry.GetNode()
        if lNode:
            lMaterialCount = lNode.GetMaterialCount()

    for l in range(pGeometry.GetLayerCount()):
        leMat = pGeometry.GetLayer(l).GetMaterials()
        if leMat:
            if leMat.GetReferenceMode() == FbxLayerElement.eIndex:
                #Materials are in an undefined external table
                continue

            if lMaterialCount > 0:
                theColor = FbxColor()
                
                header = "    Materials on layer %d: " % l 
                DisplayString(header)

                for lCount in range(lMaterialCount):
                    DisplayInt("        Material ", lCount)

                    lMaterial = lNode.GetMaterial(lCount)

                    DisplayString("            Name: \"", lMaterial.GetName(), "\"") 

                    #Get the implementation to see if it's a hardware shader.
                    lImplementation = GetImplementation(lMaterial, "ImplementationHLSL")
                    lImplemenationType = "HLSL"
                    if not lImplementation:
                        lImplementation = GetImplementation(lMaterial, "ImplementationCGFX")
                        lImplemenationType = "CGFX"
                    if lImplementation:
                        #Now we have a hardware shader, let's read it
                        print("            Hardware Shader Type: %s\n" % lImplemenationType.Buffer())
                        lRootTable = lImplementation.GetRootTable()
                        lFileName = lRootTable.DescAbsoluteURL.Get()
                        lTechniqueName = lRootTable.DescTAG.Get() 


                        lTable = lImplementation.GetRootTable()
                        lEntryNum = lTable.GetEntryCount()

                        for i in range(lEntryNum):
                            lEntry = lTable.GetEntry(i)
                            lEntry.GetEntryType(True) 

                            lTest = lEntry.GetSource()
                            print("            Entry: %s\n" % lTest.Buffer())

                            if cmp( FbxPropertyEntryView.sEntryType, lEntrySrcType ) == 0:
                                lFbxProp = lMaterial.FindPropertyHierarchical(lEntry.GetSource()) 
                                if not lFbxProp.IsValid():
                                    lFbxProp = lMaterial.RootProperty.FindHierarchical(lEntry.GetSource())
                            elif cmp( FbxConstantEntryView.sEntryType, lEntrySrcType ) == 0:
                                lFbxProp = lImplementation.GetConstants().FindHierarchical(lEntry.GetSource())
                            
                            if lFbxProp.IsValid():
                                if lFbxProp.GetSrcObjectCount( FbxCriteria.ObjectType(FbxTexture.ClassId) ) > 0:
                                    #do what you want with the texture
                                    for j in range(lFbxProp.GetSrcObjectCount(FbxCriteria.ObjectType(FbxTexture.ClassId))):
                                        lTex = lFbxProp.GetSrcObject(FbxCriteria.ObjectType(FbxTexture.ClassId),j)
                                        print("                Texture: %s\n" % lTex.GetFileName())
                                else:
                                    lFbxType = lFbxProp.GetPropertyDataType()
                                    if (lFbxType == eFbxBool):
                                        lFbxProp = FbxPropertyBool1(lFbxProp)
                                        DisplayBool("                Bool: ", lFbxProp.Get())
                                    elif (lFbxType == eFbxInt):
                                        lFbxProp = FbxPropertyInteger1(lFbxProp)
                                        DisplayInt("                Int: ", lFbxProp.Get())
                                    elif (lFbxType == eFbxEnum):
                                        lFbxProp = FbxPropertyEnum(lFbxProp)
                                        DisplayInt("                Enum: ", lFbxProp.Get())
                                    elif (lFbxType == eFbxFloat):
                                        lFbxProp = FbxPropertyFloat1(lFbxProp)
                                        DisplayDouble("                Float: ", lFbxProp.Get())
                                    elif ( lFbxType == eFbxDouble):
                                        lFbxProp = FbxPropertyDouble1(lFbxProp)
                                        DisplayDouble("                Double: ", lFbxProp.Get())
                                    elif ( lFbxType == eFbxString ):
                                        lFbxProp = FbxPropertyString(lFbxProp)
                                        DisplayString("                String: ", lFbxProp.Get())
                                    elif ( lFbxType == eFbxDouble2):
                                        lFbxProp = FbxPropertyDouble2(lFbxProp)
                                        res, lDouble2= lFbxProp.Get()
                                        lVect = []
                                        lVect[0] = lDouble2[0]
                                        lVect[1] = lDouble2[1]
                                        Display2DVector("                2D vector: ", lVect)
                                    elif ( lFbxType == eFbxDouble3):
                                        lFbxProp = FbxPropertyDouble3(lFbxProp)
                                        res, lDouble3 = lFbxProp.Get()
                                        lVect = []
                                        lVect[0] = lDouble3[0]
                                        lVect[1] = lDouble3[1]
                                        lVect[2] = lDouble3[2]
                                        Display3DVector("                3D vector: ", lVect)
                                    elif ( lFbxType == eFbxDouble4):
                                        lFbxProp = FbxPropertyDouble4(lFbxProp)
                                        res, lDouble4 = lFbxProp.Get()
                                        lVect = []
                                        lVect[0] = lDouble4[0]
                                        lVect[1] = lDouble4[1]
                                        lVect[2] = lDouble4[2]
                                        lVect[3] = lDouble4[3]
                                        Display4DVector("                4D vector: ", lVect)
                                    elif ( lFbxType == eFbxDouble4x4):
                                        lFbxProp = FbxPropertyXMatrix(lFbxProp)
                                        res, lDouble44 = lFbxProp.Get(EFbxType.eFbxDouble44)
                                        for j in range(4):
                                            lVect = []
                                            lVect[0] = lDouble44[j][0]
                                            lVect[1] = lDouble44[j][1]
                                            lVect[2] = lDouble44[j][2]
                                            lVect[3] = lDouble44[j][3]
                                            Display4DVector("                4x4D vector: ", lVect)

                    elif (lMaterial.GetClassId().Is(FbxSurfacePhong.ClassId)):
                        # We found a Phong material.  Display its properties.

                        # Display the Ambient Color
                        lFbxDouble3 = lMaterial.Ambient
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Ambient: ", theColor)

                        # Display the Diffuse Color
                        lFbxDouble3 = lMaterial.Diffuse
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Diffuse: ", theColor)

                        # Display the Specular Color (unique to Phong materials)
                        lFbxDouble3 = lMaterial.Specular
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Specular: ", theColor)

                        # Display the Emissive Color
                        lFbxDouble3 = lMaterial.Emissive
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Emissive: ", theColor)

                        # Opacity is Transparency factor now
                        lFbxDouble1 = lMaterial.TransparencyFactor
                        DisplayDouble("            Opacity: ", 1.0-lFbxDouble1.Get())

                        # Display the Shininess
                        lFbxDouble1 = lMaterial.Shininess
                        DisplayDouble("            Shininess: ", lFbxDouble1.Get())

                        # Display the Reflectivity
                        lFbxDouble3 = lMaterial.Reflection
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Reflectivity: ", theColor)
                    elif lMaterial.GetClassId().Is(FbxSurfaceLambert.ClassId):
                        # We found a Lambert material. Display its properties.
                        # Display the Ambient Color
                        lFbxDouble3 = lMaterial.Ambient
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Ambient: ", theColor)

                        # Display the Diffuse Color
                        lFbxDouble3 = lMaterial.Diffuse
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Diffuse: ", theColor)

                        # Display the Emissive
                        lFbxDouble3 = lMaterial.Emissive
                        theColor.Set(lFbxDouble3.Get()[0], lFbxDouble3.Get()[1], lFbxDouble3.Get()[2])
                        DisplayColor("            Emissive: ", theColor)

                        # Display the Opacity
                        lFbxDouble1 = lMaterial.TransparencyFactor
                        DisplayDouble("            Opacity: ", 1.0-lFbxDouble1.Get())
                    else:
                        DisplayString("Unknown type of Material")

                    lString = lMaterial.ShadingModel
                    DisplayString("            Shading Model: ", lString.Get().Buffer())
                    DisplayString("")
