"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""

import sys

SAMPLE_FILENAME_MC = "ExportScene03_MC.fbx"
SAMPLE_FILENAME_PC2 = "ExportScene03_PC2.fbx"

gExportVertexCacheMCFormat = True
gCacheType = 0
    
def CreateScene(pSdkManager, pScene, pSampleFileName):
    lCube = CreateCubeWithTexture(pSdkManager, "Cube")
    lPyramid = CreatePyramidWithMaterials(pSdkManager, "Pyramid")    
    lTriangle = CreateTriangle(pSdkManager, "Triangle")
    
    MapShapeOnPyramid(pSdkManager, lPyramid)
    MapVertexCacheOnTriangle(pSdkManager, lTriangle, pSampleFileName)
    
    SetCubeDefaultPosition(lCube)
    SetPyramidDefaultPosition(lPyramid)
    SetTriangleDefaultPosition(lTriangle)
    
    # Build the node tree.
    lRootNode = pScene.GetRootNode()
    lRootNode.AddChild(lCube)
    lRootNode.AddChild(lPyramid)
    lRootNode.AddChild(lTriangle)
    
    # Create the Animation Stack
    lAnimStack = FbxAnimStack.Create(pScene, "Show all faces")

    # The animation nodes can only exist on AnimLayers therefore it is mandatory to
    # add at least one AnimLayer to the AnimStack. And for the purpose of this example,
    # one layer is all we need.
    lAnimLayer = FbxAnimLayer.Create(pScene, "Base Layer")
    lAnimStack.AddMember(lAnimLayer)
    
    Animate(lCube, lAnimLayer)
    Animate(lPyramid, lAnimLayer)
    
    lGlobalSettings = pScene.GetGlobalSettings()
    if gCacheType == 0:
        AnimateVertexCacheOnTriangleDoubleVertex(lTriangle, FbxTime.GetFrameRate(lGlobalSettings.GetTimeMode()))
    else:
        AnimateVertexCacheOnTriangleInt32(lTriangle, FbxTime.GetFrameRate(lGlobalSettings.GetTimeMode()))
        
    return True

# Create a cube with a texture. 
def CreateCubeWithTexture(pSdkManager, pName):
    lMesh = FbxMesh.Create(pSdkManager,pName)

    lControlPoint0 = FbxVector4(-50, 0, 50)
    lControlPoint1 = FbxVector4(50, 0, 50)
    lControlPoint2 = FbxVector4(50, 100, 50)
    lControlPoint3 = FbxVector4(-50, 100, 50)
    lControlPoint4 = FbxVector4(-50, 0, -50)
    lControlPoint5 = FbxVector4(50, 0, -50)
    lControlPoint6 = FbxVector4(50, 100, -50)
    lControlPoint7 = FbxVector4(-50, 100, -50)
    
    lNormalXPos = FbxVector4(1, 0, 0)
    lNormalXNeg = FbxVector4(-1, 0, 0)
    lNormalYPos = FbxVector4(0, 1, 0)
    lNormalYNeg = FbxVector4(0, -1, 0)
    lNormalZPos = FbxVector4(0, 0, 1)
    lNormalZNeg = FbxVector4(0, 0, -1)
    
    lMesh.InitControlPoints(24)
    lMesh.SetControlPointAt(lControlPoint0, 0)
    lMesh.SetControlPointAt(lControlPoint1, 1)
    lMesh.SetControlPointAt(lControlPoint2, 2)
    lMesh.SetControlPointAt(lControlPoint3, 3)
    lMesh.SetControlPointAt(lControlPoint1, 4)
    lMesh.SetControlPointAt(lControlPoint5, 5)
    lMesh.SetControlPointAt(lControlPoint6, 6)
    lMesh.SetControlPointAt(lControlPoint2, 7)
    lMesh.SetControlPointAt(lControlPoint5, 8)
    lMesh.SetControlPointAt(lControlPoint4, 9)
    lMesh.SetControlPointAt(lControlPoint7, 10)
    lMesh.SetControlPointAt(lControlPoint6, 11)
    lMesh.SetControlPointAt(lControlPoint4, 12)
    lMesh.SetControlPointAt(lControlPoint0, 13)
    lMesh.SetControlPointAt(lControlPoint3, 14)
    lMesh.SetControlPointAt(lControlPoint7, 15)
    lMesh.SetControlPointAt(lControlPoint3, 16)
    lMesh.SetControlPointAt(lControlPoint2, 17)
    lMesh.SetControlPointAt(lControlPoint6, 18)
    lMesh.SetControlPointAt(lControlPoint7, 19)
    lMesh.SetControlPointAt(lControlPoint1, 20)
    lMesh.SetControlPointAt(lControlPoint0, 21)
    lMesh.SetControlPointAt(lControlPoint4, 22)
    lMesh.SetControlPointAt(lControlPoint5, 23)
    
    # Set the normals on Layer 0.
    lLayer = lMesh.GetLayer(0)
    if lLayer == None:
        lMesh.CreateLayer()
        lLayer = lMesh.GetLayer(0)

    # We want to have one normal for each vertex (or control point),
    # so we set the mapping mode to eByControlPoint.
    lLayerElementNormal= FbxLayerElementNormal.Create(lMesh, "")
    lLayerElementNormal.SetMappingMode(FbxLayerElement.eByControlPoint)
    
    # Here are two different ways to set the normal values.
    firstWayNormalCalculations = True
    if firstWayNormalCalculations:
        # The first method is to set the actual normal value
        # for every control point.
        lLayerElementNormal.SetReferenceMode(FbxLayerElement.eDirect)

        lLayerElementNormal.GetDirectArray().Add(lNormalZPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalZPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalZPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalZPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalXPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalXPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalXPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalXPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalZNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalZNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalZNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalZNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalXNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalXNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalXNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalXNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalYPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalYPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalYPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalYPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalYNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalYNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalYNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalYNeg)
    else:
        # The second method is to the possible values of the normals
        # in the direct array, and set the index of that value
        # in the index array for every control point.
        lLayerElementNormal.SetReferenceMode(FbxLayerElement.eIndexToDirect)

        # Add the 6 different normals to the direct array
        lLayerElementNormal.GetDirectArray().Add(lNormalZPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalXPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalZNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalXNeg)
        lLayerElementNormal.GetDirectArray().Add(lNormalYPos)
        lLayerElementNormal.GetDirectArray().Add(lNormalYNeg)

        # Now for each control point, we need to specify which normal to use
        lLayerElementNormal.GetIndexArray().Add(0) # index of lNormalZPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(0) # index of lNormalZPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(0) # index of lNormalZPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(0) # index of lNormalZPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(1) # index of lNormalXPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(1) # index of lNormalXPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(1) # index of lNormalXPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(1) # index of lNormalXPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(2) # index of lNormalZNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(2) # index of lNormalZNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(2) # index of lNormalZNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(2) # index of lNormalZNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(3) # index of lNormalXNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(3) # index of lNormalXNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(3) # index of lNormalXNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(3) # index of lNormalXNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(4) # index of lNormalYPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(4) # index of lNormalYPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(4) # index of lNormalYPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(4) # index of lNormalYPos in the direct array.
        lLayerElementNormal.GetIndexArray().Add(5) # index of lNormalYNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(5) # index of lNormalYNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(5) # index of lNormalYNeg in the direct array.
        lLayerElementNormal.GetIndexArray().Add(5) # index of lNormalYNeg in the direct array.

    lLayer.SetNormals(lLayerElementNormal)
    
    # Array of polygon vertices.
    lPolygonVertices = ( 0, 1, 2, 3,
        4, 5, 6, 7,
        8, 9, 10, 11,
        12, 13, 14, 15,
        16, 17, 18, 19,
        20, 21, 22, 23 )

    # Set texture mapping for diffuse channel.
    lTextureDiffuseLayer=FbxLayerElementTexture.Create(lMesh, "Diffuse Texture")
    lTextureDiffuseLayer.SetMappingMode(FbxLayerElement.eByPolygon)
    lTextureDiffuseLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetTextures(FbxLayerElement.eTextureDiffuse, lTextureDiffuseLayer)

    # Set texture mapping for ambient channel.
    lTextureAmbientLayer=FbxLayerElementTexture.Create(lMesh, "Ambient Textures")
    lTextureAmbientLayer.SetMappingMode(FbxLayerElement.eByPolygon)
    lTextureAmbientLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetTextures(FbxLayerElement.eTextureAmbient, lTextureAmbientLayer)

    # Set texture mapping for emissive channel.
    lTextureEmissiveLayer=FbxLayerElementTexture.Create(lMesh, "Emissive Textures")
    lTextureEmissiveLayer.SetMappingMode(FbxLayerElement.eByPolygon)
    lTextureEmissiveLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetTextures(FbxLayerElement.eTextureEmissive, lTextureEmissiveLayer)

    # Create UV for Diffuse channel
    lUVDiffuseLayer = FbxLayerElementUV.Create(lMesh, "DiffuseUV")
    lUVDiffuseLayer.SetMappingMode(FbxLayerElement.eByPolygonVertex)
    lUVDiffuseLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetUVs(lUVDiffuseLayer, FbxLayerElement.eTextureDiffuse)

    lVectors0 = FbxVector2(0, 0)
    lVectors1 = FbxVector2(1, 0)
    lVectors2 = FbxVector2(1, 1)
    lVectors3 = FbxVector2(0, 1)

    lUVDiffuseLayer.GetDirectArray().Add(lVectors0)
    lUVDiffuseLayer.GetDirectArray().Add(lVectors1)
    lUVDiffuseLayer.GetDirectArray().Add(lVectors2)
    lUVDiffuseLayer.GetDirectArray().Add(lVectors3)

    # Create UV for Ambient channel
    lUVAmbientLayer=FbxLayerElementUV.Create(lMesh, "AmbientUV")

    lUVAmbientLayer.SetMappingMode(FbxLayerElement.eByPolygonVertex)
    lUVAmbientLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetUVs(lUVAmbientLayer, FbxLayerElement.eTextureAmbient)

    lVectors0.Set(0, 0)
    lVectors1.Set(1, 0)
    lVectors2.Set(0, 0.418586879968643)
    lVectors3.Set(1, 0.418586879968643)

    lUVAmbientLayer.GetDirectArray().Add(lVectors0)
    lUVAmbientLayer.GetDirectArray().Add(lVectors1)
    lUVAmbientLayer.GetDirectArray().Add(lVectors2)
    lUVAmbientLayer.GetDirectArray().Add(lVectors3)

    # Create UV for Emissive channel
    lUVEmissiveLayer=FbxLayerElementUV.Create(lMesh, "EmissiveUV")

    lUVEmissiveLayer.SetMappingMode(FbxLayerElement.eByPolygonVertex)
    lUVEmissiveLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetUVs(lUVEmissiveLayer, FbxLayerElement.eTextureEmissive)

    lVectors0.Set(0.2343, 0)
    lVectors1.Set(1, 0.555)
    lVectors2.Set(0.333, 0.999)
    lVectors3.Set(0.555, 0.666)

    lUVEmissiveLayer.GetDirectArray().Add(lVectors0)
    lUVEmissiveLayer.GetDirectArray().Add(lVectors1)
    lUVEmissiveLayer.GetDirectArray().Add(lVectors2)
    lUVEmissiveLayer.GetDirectArray().Add(lVectors3)

    #Now we have set the UVs as eINDEX_TO_DIRECT reference and in eBY_POLYGON_VERTEX  mapping mode
    #we must update the size of the index array.
    lUVDiffuseLayer.GetIndexArray().SetCount(24)
    lUVEmissiveLayer.GetIndexArray().SetCount(24)
    lUVAmbientLayer.GetIndexArray().SetCount(24)

    #in the same way we with Textures, but we are in eBY_POLYGON and as we are doing a cube,
    #we should have 6 polygons (1 for each faces of the cube)
    lTextureDiffuseLayer.GetIndexArray().SetCount(6)
    lTextureAmbientLayer.GetIndexArray().SetCount(6)
    lTextureEmissiveLayer.GetIndexArray().SetCount(6)

    # Create polygons. Assign texture and texture UV indices.
    for i in range(6):
        #we won't use the default way of assigning textures, as we have
        #textures on more than just the default (diffuse) channel.
        lMesh.BeginPolygon(-1, -1, False)

        #Here we set the the index array for each channel
        lTextureDiffuseLayer.GetIndexArray().SetAt(i,0)
        lTextureAmbientLayer.GetIndexArray().SetAt(i,0)
        lTextureEmissiveLayer.GetIndexArray().SetAt(i,0)

        for j in range(4):
            #this function points 
            lMesh.AddPolygon(lPolygonVertices[i*4 + j]) # Control point index. 
            
            #Now we have to update the index array of the UVs for diffuse, ambient and emissive
            lUVDiffuseLayer.GetIndexArray().SetAt(i*4+j, j)
            lUVAmbientLayer.GetIndexArray().SetAt(i*4+j, j)
            lUVEmissiveLayer.GetIndexArray().SetAt(i*4+j, j)

        lMesh.EndPolygon()

    CreateTexture(pSdkManager, lMesh)
    
    lNode = FbxNode.Create(pSdkManager,pName)
    lNode.SetNodeAttribute(lMesh)
    lNode.SetShadingMode(FbxNode.eTextureShading)
    return lNode

# Create a pyramid with materials. 
def CreatePyramidWithMaterials(pSdkManager, pName):
    lMesh = FbxMesh.Create(pSdkManager, pName)

    lControlPoint0 = FbxVector4(-50, 0, 50)
    lControlPoint1 = FbxVector4(50, 0, 50)
    lControlPoint2 = FbxVector4(50, 0, -50)
    lControlPoint3 = FbxVector4(-50, 0, -50)
    lControlPoint4 = FbxVector4(0, 100, 0)

    lNormalP0 = FbxVector4(0, 1, 0)
    lNormalP1 = FbxVector4(0, 0.447, 0.894)
    lNormalP2 = FbxVector4(0.894, 0.447, 0)
    lNormalP3 = FbxVector4(0, 0.447, -0.894)
    lNormalP4 = FbxVector4(-0.894, 0.447, 0)

    # Create control points.
    lMesh.InitControlPoints(16)     
    lMesh.SetControlPointAt(lControlPoint0, 0)
    lMesh.SetControlPointAt(lControlPoint1, 1)
    lMesh.SetControlPointAt(lControlPoint2, 2)
    lMesh.SetControlPointAt(lControlPoint3, 3)
    lMesh.SetControlPointAt(lControlPoint0, 4)
    lMesh.SetControlPointAt(lControlPoint1, 5)
    lMesh.SetControlPointAt(lControlPoint4, 6)
    lMesh.SetControlPointAt(lControlPoint1, 7)
    lMesh.SetControlPointAt(lControlPoint2, 8)
    lMesh.SetControlPointAt(lControlPoint4, 9)
    lMesh.SetControlPointAt(lControlPoint2, 10)
    lMesh.SetControlPointAt(lControlPoint3, 11)
    lMesh.SetControlPointAt(lControlPoint4, 12)
    lMesh.SetControlPointAt(lControlPoint3, 13)
    lMesh.SetControlPointAt(lControlPoint0, 14)
    lMesh.SetControlPointAt(lControlPoint4, 15)

    # specify normals per control point.
    lLayer = lMesh.GetLayer(0)
    if lLayer == None:
        lMesh.CreateLayer()
        lLayer = lMesh.GetLayer(0)

    lNormalLayer= FbxLayerElementNormal.Create(lMesh, "")
    lNormalLayer.SetMappingMode(FbxLayerElement.eByControlPoint)
    lNormalLayer.SetReferenceMode(FbxLayerElement.eDirect)

    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP1)
    lNormalLayer.GetDirectArray().Add(lNormalP1)
    lNormalLayer.GetDirectArray().Add(lNormalP1)
    lNormalLayer.GetDirectArray().Add(lNormalP2)
    lNormalLayer.GetDirectArray().Add(lNormalP2)
    lNormalLayer.GetDirectArray().Add(lNormalP2)
    lNormalLayer.GetDirectArray().Add(lNormalP3)
    lNormalLayer.GetDirectArray().Add(lNormalP3)
    lNormalLayer.GetDirectArray().Add(lNormalP3)
    lNormalLayer.GetDirectArray().Add(lNormalP4)
    lNormalLayer.GetDirectArray().Add(lNormalP4)
    lNormalLayer.GetDirectArray().Add(lNormalP4)

    lLayer.SetNormals(lNormalLayer)

    # Array of polygon vertices.
    lPolygonVertices = (0, 3, 2, 1,
        4, 5, 6,
        7, 8, 9,
        10, 11, 12,
        13, 14, 15)

    # Set material mapping.
    lMaterialLayer=FbxLayerElementMaterial.Create(lMesh, "")
    lMaterialLayer.SetMappingMode(FbxLayerElement.eByPolygon)
    lMaterialLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
    lLayer.SetMaterials(lMaterialLayer)

    # Create polygons. Assign material indices.

    # Pyramid base.
    lMesh.BeginPolygon(0) # Material index.

    for j in range(4):
        lMesh.AddPolygon(lPolygonVertices[j]) # Control point index.

    lMesh.EndPolygon ()

    # Pyramid sides.
    for i in range(5):
        lMesh.BeginPolygon(i) # Material index.

        for j in range(3):
            lMesh.AddPolygon(lPolygonVertices[4 + 3*(i - 1) + j]) # Control point index.

        lMesh.EndPolygon()

    lNode = FbxNode.Create(pSdkManager,pName)
    lNode.SetNodeAttribute(lMesh)
    
    CreateMaterials(pSdkManager, lMesh)

    return lNode

def CreateTriangle(pSdkManager, pName):
    lMesh = FbxMesh.Create(pSdkManager, pName)

    # The three vertices
    lControlPoint0 = FbxVector4(-50, 0, 50)
    lControlPoint1 = FbxVector4(50, 0, 50)
    lControlPoint2 = FbxVector4(0, 50, -50)

    # Create control points.
    lMesh.InitControlPoints(3)
    lMesh.SetControlPointAt(lControlPoint0, 0)
    lMesh.SetControlPointAt(lControlPoint1, 1)
    lMesh.SetControlPointAt(lControlPoint2, 2)

    # Create the triangle's polygon
    lMesh.BeginPolygon()
    lMesh.AddPolygon(0) # Control point 0
    lMesh.AddPolygon(1) # Control point 1
    lMesh.AddPolygon(2) # Control point 2
    lMesh.EndPolygon()

    lNode = FbxNode.Create(pSdkManager,pName)
    lNode.SetNodeAttribute(lMesh)

    return lNode

# Create texture for cube.
def CreateTexture(pSdkManager, pMesh):
    # A texture need to be connected to a property on the material,
    # so let's use the material (if it exists) or create a new one
    lMaterial = None

    # get the node of mesh, add material for it.
    lNode = pMesh.GetNode()
    if lNode:
        lMaterial = lNode.GetSrcObject(FbxCriteria.ObjectType(FbxSurfacePhong.ClassId), 0)
        if not lMaterial:
            lMaterialName = "toto"
            lShadingName  = "Phong"
            lBlack = FbxDouble3(0.0, 0.0, 0.0)
            lRed = FbxDouble3(1.0, 0.0, 0.0)
            lDiffuseColor = FbxDouble3(0.75, 0.75, 0.0)
            lMaterial = FbxSurfacePhong.Create(pSdkManager, lMaterialName)

            # Generate primary and secondary colors.
            lMaterial.Emissive.Set(lBlack)
            lMaterial.Ambient.Set(lRed)
            lMaterial.AmbientFactor.Set(1.)
            # Add texture for diffuse channel
            lMaterial.Diffuse.Set(lDiffuseColor)
            lMaterial.DiffuseFactor.Set(1.)
            lMaterial.TransparencyFactor.Set(0.4)
            lMaterial.ShadingModel.Set(lShadingName)
            lMaterial.Shininess.Set(0.5)
            lMaterial.Specular.Set(lBlack)
            lMaterial.SpecularFactor.Set(0.3)

            lNode.AddMaterial(lMaterial)

    lTexture = FbxFileTexture.Create(pSdkManager,"Diffuse Texture")

    # Set texture properties.
    lTexture.SetFileName("scene03.jpg") # Resource file is in current directory.
    lTexture.SetTextureUse(FbxTexture.eStandard)
    lTexture.SetMappingType(FbxTexture.eUV)
    lTexture.SetMaterialUse(FbxFileTexture.eModelMaterial)
    lTexture.SetSwapUV(False)
    lTexture.SetTranslation(0.0, 0.0)
    lTexture.SetScale(1.0, 1.0)
    lTexture.SetRotation(0.0, 0.0)

    # don't forget to connect the texture to the corresponding property of the material
    if lMaterial:
        lMaterial.Diffuse.ConnectSrcObject(lTexture)

    lTexture = FbxFileTexture.Create(pSdkManager,"Ambient Texture")

    # Set texture properties.
    lTexture.SetFileName("gradient.jpg") # Resource file is in current directory.
    lTexture.SetTextureUse(FbxTexture.eStandard)
    lTexture.SetMappingType(FbxTexture.eUV)
    lTexture.SetMaterialUse(FbxFileTexture.eModelMaterial)
    lTexture.SetSwapUV(False)
    lTexture.SetTranslation(0.0, 0.0)
    lTexture.SetScale(1.0, 1.0)
    lTexture.SetRotation(0.0, 0.0)

    # don't forget to connect the texture to the corresponding property of the material
    if lMaterial:
        lMaterial.Ambient.ConnectSrcObject(lTexture)

    lTexture = FbxFileTexture.Create(pSdkManager,"Emissive Texture")

    # Set texture properties.
    lTexture.SetFileName("spotty.jpg") # Resource file is in current directory.
    lTexture.SetTextureUse(FbxTexture.eStandard)
    lTexture.SetMappingType(FbxTexture.eUV)
    lTexture.SetMaterialUse(FbxFileTexture.eModelMaterial)
    lTexture.SetSwapUV(False)
    lTexture.SetTranslation(0.0, 0.0)
    lTexture.SetScale(1.0, 1.0)
    lTexture.SetRotation(0.0, 0.0)

    # don't forget to connect the texture to the corresponding property of the material
    if lMaterial:
        lMaterial.Emissive.ConnectSrcObject(lTexture)


# Create materials for pyramid.
def CreateMaterials(pSdkManager, pMesh):
    colors = (FbxDouble3(0.0, 0.0, 0.0), FbxDouble3(0.0, 1.0, 1.0), FbxDouble3(0.0, 1.0, 0.0), FbxDouble3(1.0, 1.0, 1.0), FbxDouble3(1.0, 0.0, 0.0))
    
    for i in range(5):
        lMaterialName = "material"
        lShadingName = "Phong"
        lMaterialName += str(i)
        lBlack = FbxDouble3(0.0, 0.0, 0.0)
        lRed = FbxDouble3(1.0, 0.0, 0.0)
        lMaterial = FbxSurfacePhong.Create(pSdkManager, lMaterialName)

        # Generate primary and secondary colors.
        lMaterial.Emissive.Set(lBlack)
        lMaterial.Ambient.Set(lRed)
            
        lMaterial.Diffuse.Set(colors[i])
        lMaterial.TransparencyFactor.Set(0.0)
        lMaterial.ShadingModel.Set(lShadingName)
        lMaterial.Shininess.Set(0.5)

        #get the node of mesh, add material for it.
        lNode = pMesh.GetNode()
        if lNode:
            lNode.AddMaterial(lMaterial)

# Map pyramid control points onto an upside down shape.
def MapShapeOnPyramid(pScene, pPyramid):
    lShape = FbxShape.Create(pScene,"")

    lControlPoint0 = FbxVector4(-50, 100, 50)
    lControlPoint1 = FbxVector4(50, 100, 50)
    lControlPoint2 = FbxVector4(50, 100, -50)
    lControlPoint3 = FbxVector4(-50, 100, -50)
    lControlPoint4 = FbxVector4(0, 0, 0)

    lNormalP0 = FbxVector4(0, 1, 0)
    lNormalP1 = FbxVector4(0, -0.447, 0.894)
    lNormalP2 = FbxVector4(0.894, -0.447, 0)
    lNormalP3 = FbxVector4(0, -0.447, -0.894)
    lNormalP4 = FbxVector4(-0.894, -0.447, 0)

    # Create control points.
    lShape.InitControlPoints(16)
    lShape.SetControlPointAt(lControlPoint0, 0)
    lShape.SetControlPointAt(lControlPoint1, 1)
    lShape.SetControlPointAt(lControlPoint2, 2)
    lShape.SetControlPointAt(lControlPoint3, 3)
    lShape.SetControlPointAt(lControlPoint0, 4)
    lShape.SetControlPointAt(lControlPoint1, 5)
    lShape.SetControlPointAt(lControlPoint4, 6)
    lShape.SetControlPointAt(lControlPoint1, 7)
    lShape.SetControlPointAt( lControlPoint2, 8)
    lShape.SetControlPointAt(lControlPoint4, 9)
    lShape.SetControlPointAt(lControlPoint2, 10)
    lShape.SetControlPointAt(lControlPoint3, 11)
    lShape.SetControlPointAt(lControlPoint4, 12)
    lShape.SetControlPointAt(lControlPoint3, 13)
    lShape.SetControlPointAt(lControlPoint0, 14)
    lShape.SetControlPointAt(lControlPoint4, 15)

    # specify normals per control point.
    lLayer = lShape.GetLayer(0)
    if not lLayer:
        lShape.CreateLayer()
        lLayer = lShape.GetLayer(0)

    lNormalLayer = FbxLayerElementNormal.Create(lShape, "")
    lNormalLayer.SetMappingMode(FbxLayerElement.eByControlPoint)
    lNormalLayer.SetReferenceMode(FbxLayerElement.eDirect)

    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP0)
    lNormalLayer.GetDirectArray().Add(lNormalP1)
    lNormalLayer.GetDirectArray().Add(lNormalP1)
    lNormalLayer.GetDirectArray().Add(lNormalP1)
    lNormalLayer.GetDirectArray().Add(lNormalP2)
    lNormalLayer.GetDirectArray().Add(lNormalP2)
    lNormalLayer.GetDirectArray().Add(lNormalP2)
    lNormalLayer.GetDirectArray().Add(lNormalP3)
    lNormalLayer.GetDirectArray().Add(lNormalP3)
    lNormalLayer.GetDirectArray().Add(lNormalP3)
    lNormalLayer.GetDirectArray().Add(lNormalP4)
    lNormalLayer.GetDirectArray().Add(lNormalP4)
    lNormalLayer.GetDirectArray().Add(lNormalP4)

    lLayer.SetNormals(lNormalLayer)

    lBlendShape = FbxBlendShape.Create(pScene, "")
    lBlendShapeChannel = FbxBlendShapeChannel.Create(pScene, "")
    pPyramid.GetMesh().AddDeformer(lBlendShape)
    lBlendShape.AddBlendShapeChannel(lBlendShapeChannel)
    lBlendShapeChannel.AddTargetShape(lShape)

def MapVertexCacheOnTriangle(pSdkManager, pTriangle, pSampleFileName):
    # By convention, all cache files are created in a _fpc folder located at the same
    # place as the .Fbx file. 
    lFBXAbsolutePath = FbxPathUtils.Resolve(pSampleFileName)

    # Create a cache directory with the same name as the Fbx file
    lFPCAbsoluteDirectory  = FbxPathUtils.GetFolderName(lFBXAbsolutePath.Buffer())
    lFPCAbsoluteDirectory += "/"
    lFPCAbsoluteDirectory += FbxPathUtils.GetFileName(pSampleFileName, False)
    lFPCAbsoluteDirectory += "_fpc"

    # Make this path the shortest possible
    lFPCAbsoluteDirectory = FbxPathUtils.Clean(lFPCAbsoluteDirectory.Buffer())

    # Now get the point cache absolute and relative file name
    lAbsolutePCFileName = lFPCAbsoluteDirectory + FbxString("/") + pTriangle.GetName()
    if gExportVertexCacheMCFormat:
        lAbsolutePCFileName += ".xml"
    else:
        lAbsolutePCFileName += ".pc2"

    lRelativePCFileName = FbxPathUtils.GetRelativeFilePath((FbxPathUtils.GetFolderName(lFBXAbsolutePath.Buffer()) + "/").Buffer(), lAbsolutePCFileName.Buffer())

    # Make sure the direcotry exist.
    if not FbxPathUtils.Create(lAbsolutePCFileName.Buffer()):
        # Cannot create this directory. So do not create the point cache
        return

    #
    # Create the cache file
    #
    lCache = FbxCache.Create(pSdkManager, pTriangle.GetName())

    lCache.SetCacheFileName(lRelativePCFileName.Buffer(), lAbsolutePCFileName.Buffer())
    if gExportVertexCacheMCFormat:
        lCache.SetCacheFileFormat(FbxCache.eMayaCache)
    else:
        lCache.SetCacheFileFormat(FbxCache.eMaxPointCacheV2)

    #
    # Create the vertex deformer
    #
    lDeformer = FbxVertexCacheDeformer.Create(pSdkManager, pTriangle.GetName())

    lDeformer.SetCache(lCache)
    lDeformer.Channel.Set(pTriangle.GetName())
    lDeformer.Active.Set(True)

    # Apply the deformer on the mesh
    pTriangle.GetGeometry().AddDeformer(lDeformer)

# Cube is translated to the left.
def SetCubeDefaultPosition(pCube):
    pCube.LclTranslation.Set(FbxDouble3(-75.0, -50.0, 0.0))
    pCube.LclRotation.Set(FbxDouble3(0.0, 0.0, 0.0))
    pCube.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

# Pyramid is translated to the right.
def SetPyramidDefaultPosition(pPyramid):
    pPyramid.LclTranslation.Set(FbxDouble3(75.0, -50.0, 0.0))
    pPyramid.LclRotation.Set(FbxDouble3(0.0, 0.0, 0.0))
    pPyramid.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

def SetTriangleDefaultPosition(pTriangle):
    pTriangle.LclTranslation.Set(FbxDouble3(200.0, -50.0, 0.0))
    pTriangle.LclRotation.Set(FbxDouble3(0.0, 0.0, 0.0))
    pTriangle.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

# Displays 6 different angles.
def Animate(pNode, pAnimLayer):
    lTime = FbxTime()
    
    lCurve = pNode.LclRotation.GetCurve(pAnimLayer, "Y", True)
    if lCurve:
        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeyModifyBegin()
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(0.5)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(1.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 180.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(1.5)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 270.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 360.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()

    lCurve = pNode.LclRotation.GetCurve(pAnimLayer, "X", True)
    if lCurve:
        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]

        lCurve.KeyModifyBegin()
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.5)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(3.5)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, -90.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(4.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()

    # The upside down shape is at index 0 because it is the only one.
    # The cube has no shape so the function returns NULL is this case.
    lGeometry = pNode.GetNodeAttribute()
    lCurve = lGeometry.GetShapeChannel(0, 0, pAnimLayer, True)
    if lCurve:
        lTime.SetSecondDouble(0.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]

        lCurve.KeyModifyBegin()
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(2.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 100.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)

        lTime.SetSecondDouble(4.0)
        lKeyIndex = lCurve.KeyAdd(lTime)[0]
        lCurve.KeySetValue(lKeyIndex, 0.0)
        lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()

def AnimateVertexCacheOnTriangleDoubleVertex(pTriangle, pFrameRate):
    # Move the vertices from their original position to the center.
    lDeformer = pTriangle.GetGeometry().GetDeformer(0, FbxDeformer.eVertexCache)
    lCache = lDeformer.GetCache()

    # Write samples for 4 seconds
    lTimeIncrement = FbxTime()
    lCurrentTime = FbxTime()
    lStopTime = FbxTime()
    lTimeIncrement.SetTime(0, 0, 0, 1) # 1 frame @ current frame rate
    lStopTime.SetTime(0, 0, 4)         # 4 seconds

    lFrameCount = lStopTime.Get()/lTimeIncrement.Get()

    # Open the file for writing
    if gExportVertexCacheMCFormat:
        lRet = lCache.OpenFileForWrite(FbxCache.eMCOneFile, pFrameRate, pTriangle.GetName(), FbxCache.eMCX)
    else:
        lRet = lCache.OpenFileForWrite(0.0, pFrameRate, lFrameCount, 3)

    lChannelIndex = lCache.GetChannelIndex(pTriangle.GetName())
    lCurrentFrame = 0

    while lCurrentTime <= lStopTime:
        lVertices = []
        lScaleFactor = 1.0 - lCurrentTime.GetSecondDouble()/lStopTime.GetSecondDouble()

        lVertices.append(-50.0 * lScaleFactor)  # X
        lVertices.append(0.0)                   # Y
        lVertices.append(50.0  * lScaleFactor)  # Z

        lVertices.append(50.0  * lScaleFactor)  # X
        lVertices.append(0.0)                   # Y
        lVertices.append(50.0  * lScaleFactor)  # Z

        lVertices.append(0.0   * lScaleFactor)  # X
        lVertices.append(50.0  * lScaleFactor)  # Y
        lVertices.append( -50.0 * lScaleFactor)  # Z

        if gExportVertexCacheMCFormat:
            lCache.Write(lChannelIndex, lCurrentTime, lVertices, 3)
        else:
            lCache.Write(lCurrentFrame, lVertices)

        lCurrentTime += lTimeIncrement
        lCurrentFrame += 1
        
    lCache.CloseFile()

def AnimateVertexCacheOnTriangleInt32(pTriangle, pFrameRate):
    #
    # Move the vertices from their original position to the center.
    #
    lDeformer = pTriangle.GetGeometry().GetDeformer(0, FbxDeformer.eVertexCache)
    lCache = lDeformer.GetCache()
    lRet = False

    # Write samples for 4 seconds
    lTimeIncrement = FbxTime()
    lCurrentTime = FbxTime()
    lStopTime = FbxTime()
    lTimeIncrement.SetTime(0, 0, 0, 1) # 1 frame @ current frame rate
    lStopTime.SetTime(0, 0, 4)         # 4 seconds

    lFrameCount = lStopTime.Get()/lTimeIncrement.Get()

    # Open the file for writing int32 array
    if gExportVertexCacheMCFormat:
        lRet = lCache.OpenFileForWrite(FbxCache.eMCOneFile, pFrameRate, pTriangle.GetName(), FbxCache.eMCX, FbxCache.kInt32Array)

    lChannelIndex = lCache.GetChannelIndex(pTriangle.GetName())
    lCurrentFrame = 0

    while lCurrentTime <= lStopTime:
        v = [0, 0]

        v[0] = -10 + lCurrentFrame
        v[1] = v[0]+1

        if gExportVertexCacheMCFormat:
            lCache.Write(lChannelIndex, lCurrentTime, v, 2)

        lCurrentTime += lTimeIncrement
        lCurrentFrame +=  1

    lCache.CloseFile()

    # Open the file for reading int32 array
    if gExportVertexCacheMCFormat:
        lRet = lCache.OpenFileForRead()

    lCurrentTime2 = FbxTime()
    lCurrentFrame = 0

    print("Testing awCache int32 array read and write\n")
    passTest = True
    # printf("Should print out -10 .. 110\n")
    while lCurrentTime2 <= lStopTime:
        v = [0, 0]
        if gExportVertexCacheMCFormat:
            lCache.Read(lChannelIndex, lCurrentTime2, v, 2)
        if v[0] != -10 + lCurrentFrame or v[0]+1 != v[1]:
            print("awCache int32 array read/write mismatch\n")
            passTest = False
            break

        lCurrentTime2 += lTimeIncrement
        lCurrentFrame += 1
    
    lCache.CloseFile()
    printf("awCache int32 array read and write test passed\n")

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
    
    # The example can take an output file name as an argument.
    lSampleFileName = ""
    if len(sys.argv) > 1:
        lSampleFileName = sys.argv[1]
    # A default output file name is given otherwise.
    elif gExportVertexCacheMCFormat:
        lSampleFileName = SAMPLE_FILENAME_MC
    else:
        lSampleFileName = SAMPLE_FILENAME_PC2

    # Create the scene.
    lResult = CreateScene(lSdkManager, lScene, lSampleFileName)

    if lResult == False:
        print("\n\nAn error occurred while creating the scene...\n")
        lSdkManager.Destroy()
        sys.exit(1)

    # Save the scene.
    lResult = FbxCommon.SaveScene(lSdkManager, lScene, lSampleFileName)

    if lResult == False:
        print("\n\nAn error occurred while saving the scene...\n")
        lSdkManager.Destroy()
        sys.exit(1)

    # Destroy all objects created by the FBX SDK.
    lSdkManager.Destroy()
   
    sys.exit(0)
