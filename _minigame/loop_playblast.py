# -*- coding: utf-8 -*-
"""
遍历导出的 FBX ，输出拍屏
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


path = r"G:\_minigame\RPG Character"
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
    mel.eval('FBXExportSkeletonDefinitions -v true')
    
for root, dirs, files in os.walk(path, topdown=False):
        
    for fbx in files:
        
        if not fbx.lower().endswith(".fbx"):
            continue
        
        SetFbxParameter()
        
        fbx_path = posixpath.join(root,fbx)
        fbx_path = fbx_path.replace('\\','/')
        mel.eval('FBXImport -f "%s"' % fbx_path)
        
        output_path = os.path.splitext(fbx_path)[0]
        cmds.playblast(filename=output_path,
                           format="qt",
                           sequenceTime=0,
                           clearCache=1,
                           viewer=0,
                           showOrnaments=0,
                           framePadding=4,
                           percent=100,
                           compression="H.264",
                           quality=100,
                           forceOverwrite=1,
                        #    widthHeight=[w, h]
                           )
        
        cmds.file(file_path,o=1,f=1)
        # break
    # break
        