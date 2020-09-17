# -*- coding: utf-8 -*-
"""
遍历动画 FBX ，导入动画 并且将目标角色 bake 出 fbx
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-08 15:34:24'


import os
import posixpath
from maya import cmds
from maya import mel


path = r"G:\_minigame\Assets\RPG Character Animation Pack\Animations"
file_path = cmds.file(q=1,sn=1)

def SetFbxParameter():
    if not cmds.pluginInfo('fbxmaya', q=True, loaded=True):
        cmds.loadPlugin('fbxmaya')
    mel.eval('FBXResetExport')
    mel.eval('FBXExportFileVersion -v FBX201200')
    mel.eval('FBXExportUpAxis y')
    mel.eval('FBXExportShapes  -v false')
    mel.eval('FBXExportScaleFactor 1.0')
    mel.eval('FBXExportInAscii -v true')
    mel.eval('FBXExportConstraints -v false')
    mel.eval('FBXExportLights -v false')
    mel.eval('FBXExportSkins -v false')
    mel.eval('FBXExportSmoothingGroups -v true')
    mel.eval('FBXExportSmoothMesh -v false')
    mel.eval('FBXExportEmbeddedTextures -v false')
    mel.eval('FBXExportCameras -v false')
    mel.eval('FBXExportBakeResampleAnimation -v false')
    mel.eval('FBXExportSkeletonDefinitions -v true')Browse_BTN
    
for root, dirs, files in os.walk(path, topdown=False):
    folder = os.path.basename(root)
    
    folder_path = posixpath.join(os.path.dirname(file_path),folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
    for fbx in files:
        
        if not fbx.lower().endswith(".fbx"):
            continue
        
        SetFbxParameter()
        
        fbx_path = posixpath.join(root,fbx)
        fbx_path = fbx_path.replace('\\','/')
        mel.eval('FBXImport -f "%s"' % fbx_path)
        
        # NOTE 获取导入的 Locator 层级，逐个约束到对应的骨骼上
        for loc in cmds.ls('Motion',dag=1,ni=1,type="locator"):
            loc = cmds.listRelatives(loc,p=1)[0]
            jnt = '%s_jnt' % (loc[2:] if loc.startswith('B_') else loc)
            if cmds.objExists(jnt):
                cmds.parentConstraint(loc,jnt,mo=0)
        
        cmds.select('root')
        
        timeStart = cmds.playbackOptions(q=1,min=1)
        timeEnd = cmds.playbackOptions(q=1,max=1)
        cmds.bakeResults(cmds.ls('root',dag=1,type="joint"),
        t = (timeStart,timeEnd),
        sampleBy = 1, 
        disableImplicitControl = 1, 
        preserveOutsideKeys = 1, 
        minimizeRotation = 1, 
        simulation=True )
        output_path = posixpath.join(folder_path,fbx)
        
        mel.eval('FBXExport -f "%s" -s' % output_path)
        
        cmds.file(file_path,o=1,f=1)
        break
    break

        