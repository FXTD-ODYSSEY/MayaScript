"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""

def TriangulateSplitAllMeshes(pScene, pManager):
    lNode = pScene.GetRootNode()
    lConverter = FbxGeometryConverter(pManager)
    
    if lNode:
        for i in range(lNode.GetChildCount()):
            lChildNode = lNode.GetChild(i)
            if lChildNode.GetNodeAttribute() != None:
                lAttributeType = (lChildNode.GetNodeAttribute().GetAttributeType())
            
                if lAttributeType == FbxNodeAttribute.eMesh:
                    lMesh = lChildNode.GetNodeAttribute()
                
                    print("\nMESH NAME :: %s" % lMesh.GetName())
                    print("MESH POLYGONS :: %i" % lMesh.GetPolygonCount())
                    print("MESH EDGES :: %i" % lMesh.GetMeshEdgeCount())     
                    print("TRIANGULATING MESH")
                    lTriangulatedMesh = lConverter.Triangulate(lMesh, False)
                    print("\nTRIANGULATING MESH COMPLETED")
                    print("TRIANGULATED MESH POLYGONS :: %i" % lTriangulatedMesh.GetPolygonCount())
                    print("TRIANGULATED MESH EDGES :: %i" % lTriangulatedMesh.GetMeshEdgeCount())                
                
                    lChildNode.RemoveNodeAttribute(lMesh)
                    lChildNode.AddNodeAttribute(lTriangulatedMesh)
                
                    # Mesh is triangulated, we can now split it per material
                    lResult = lConverter.SplitMeshPerMaterial(lTriangulatedMesh, False) 
                    #lChildNode.RemoveNodeAttribute(lTriangulatedMesh)       
                
def ListAllMeshesCount(pScene):
    print("NUMBER OF GEOMETRIES :: %i" % pScene.GetGeometryCount())
                
if __name__ == "__main__":
    try:
        from FbxCommon import *
    except ImportError:
        print("Error: module FbxCommon module failed to import.\n")
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
    lSdkManager, lScene = InitializeSdkObjects()

    # The example can take a FBX file as an argument.
    if len(sys.argv) > 1:
        print("\n\nFile: %s\n" % sys.argv[1])
        lResult = LoadScene(lSdkManager, lScene, sys.argv[1])
    else :
        lResult = False

        print("\n\nUsage: SplitMeshPerMaterial <FBX file name>\n")

    if not lResult:
        print("\n\nAn error occurred while loading the scene...")
    else :
        print("BEFORE SPLITTING MESHES")
        ListAllMeshesCount(lScene)
        TriangulateSplitAllMeshes(lScene, lSdkManager)
        
        print("\nAFTER SPLITTING MESHES")            
        ListAllMeshesCount(lScene)
        
        SaveScene(lSdkManager, lScene, "multiplematerials_output.fbx")
        
    # Destroy all objects created by the FBX SDK.
    lSdkManager.Destroy()
   
    sys.exit(0)
