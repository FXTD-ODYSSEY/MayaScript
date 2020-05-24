#simply create two polygon spheres. Move the second away from the first, select the first and run the code below.  
import maya.cmds as cmds  

cmds.delete(cmds.ls(type='collisionDeformer'))  
cmds.flushUndo()  
cmds.unloadPlugin('collisionDeformer.py')  
cmds.loadPlugin('collisionDeformer.py')  
cmds.deformer(type='collisionDeformer')  
cmds.connectAttr('pSphere2.worldMesh', 'collisionDeformer1.colliderTarget')  
cmds.connectAttr('pSphere2.matrix', 'collisionDeformer1.colliderMatrix')  
cmds.connectAttr('pSphere2.boundingBox.boundingBoxSize.boundingBoxSizeX', 'collisionDeformer1.colliderBoundingBox.colliderBoundingBoxX')  
cmds.connectAttr('pSphere2.boundingBox.boundingBoxSize.boundingBoxSizeY', 'collisionDeformer1.colliderBoundingBox.colliderBoundingBoxY')  
cmds.connectAttr('pSphere2.boundingBox.boundingBoxSize.boundingBoxSizeZ', 'collisionDeformer1.colliderBoundingBox.colliderBoundingBoxZ')  