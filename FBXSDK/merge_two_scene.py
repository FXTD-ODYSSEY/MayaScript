# -*- coding: utf-8 -*-
"""
http://docs.autodesk.com/FBX/2014/ENU/FBX-SDK-Documentation/index.html?url=files/GUID-C08BAE05-B074-441C-9DBE-CE1811C0E6E2.htm,topicNumber=d30e8326
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-05-13 09:01:04'
MeshVertex

import fbx
import FbxCommon

def merge_two_scene(fbx_1,fbx_2,output_file=None):
    
    output_file = output_file if output_file else fbx_2

    # NOTE 删除第一张 UV 
    manager, scene_1 = FbxCommon.InitializeSdkObjects()
    scene_2 = fbx.FbxScene.Create(manager, "")
    result_1 = FbxCommon.LoadScene(manager, scene_1, fbx_1)
    result_2 = FbxCommon.LoadScene(manager, scene_2, fbx_2)
    if not result_1 or not result_2:
        return
    
    root_1 = scene_1.GetRootNode()
    root_2 = scene_2.GetRootNode()
    for node in root_1:
        root_2.AddChild(node)
    
    root_1.DisconnectAllSrcObject()

    for i in range(scene_1.GetSrcObjectCount()):
        obj = scene_1.GetSrcObject(i)
        if obj == root_1 or obj == scene_1.GetGlobalSettings():
            continue
        obj.ConnectDstObject(scene_2)
    
    scene_1.DisconnectAllSrcObject()
    
    FbxCommon.SaveScene(manager, scene_2, output_file)
    
    
if __name__ == "__main__":
    fbx_1 = ""
    fbx_2 = ""
    merge_two_scene(fbx_1,fbx_2)
    
    



# /**
#  * Entry point for the merging two scenes sample program.
#  */
# int main(int argc, char** argv) {
#     // Create an SDK manager.
#     FbxManager* lSdkManager = FbxManager::Create();

#     // Create a new scene so it can be populated by the imported file.
#     FbxScene* lCurrentScene = FbxScene::Create(lSdkManager,"My Scene");

#     // Load the scene.
#     LoadScene(lSdkManager, lCurrentScene, "file1.fbx");

#     // Modify the scene. In this example, only one node name is changed.
#     lCurrentScene->GetRootNode()->GetChild(0)->SetName("Test Name");

#     // Create a reference scene to store the contents of the currently loaded scene.
#     FbxScene *lMyRefScene = FbxScene::Create(lSdkManager, "My Reference Scene");

#     // Move the node tree of the currently loaded scene into the reference scene.
#     int lNumChildren = lCurrentScene->GetRootNode()->GetChildCount();
#     for(int i = 0; i < lNumChildren; i++) {

#         // Obtain a child node from the currently loaded scene.
#         FbxNode* lChildNode = lCurrentScene->GetRootNode()->GetChild(i);

#         // Attach the child node to the reference scene's root node.
#         lMyRefScene->GetRootNode()->AddChild(lChildNode);
#     }

#     // Remove the children from the root node.
#     lCurrentScene->GetRootNode()->DisconnectAllSrcObject();

#     // Move other objects to the reference scene.
#     int lNumSceneObjects = lCurrentScene->GetSrcObjectCount();
#     for(int i = 0; i < lNumSceneObjects; i++) {
#         FbxObject* lObj = lCurrentScene->GetSrcObject(i);
#         if(lObj == lCurrentScene->GetRootNode() || *lObj == lCurrentScene->GetGlobalSettings()){
#             // Don't move the root node or the scene's global settings; these
#             // objects are created for every scene.
#             continue;
#         }
#         // Attach the object to the reference scene.
#         lObj->ConnectDstObject(lMyRefScene);
#     }

#     // Disconnect all scene objects.
#     lCurrentScene->DisconnectAllSrcObject();

#     // Import the second file into lCurrentScene.
#     LoadScene(lSdkManager, lCurrentScene, "file1.fbx");

#     // Get the names after the second file is loaded.
#     FbxString lNameBeforeUpdate = lCurrentScene->GetRootNode()->GetChild(0)->GetName();
#     FbxString lReferenceName = lMyRefScene->GetRootNode()->GetChild(0)->GetName();

#     // Update the root's child 0 name.
#     lCurrentScene->GetRootNode()->GetChild(0)->SetName(lReferenceName);
#     FbxString lNameAfterUpdate = lCurrentScene->GetRootNode()->GetChild(0)->GetName();

#     // Destroy the reference scene.
#     lMyRefScene->Destroy();
#     lMyRefScene = NULL;

#     // Verification step
#     printf("Verification (0 for success): %d\n", lNameAfterUpdate.Compare("Test Name"));

#     // Destroy the sdk manager.
#     lSdkManager->Destroy();
#     exit(0);
# }