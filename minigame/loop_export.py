# -*- coding: utf-8 -*-
"""
遍历 Maya 文件导出 FBX
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
import pymel.core as pm

path = r"D:\_minigame\_LowPoly"
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


export_path = os.path.join(path,"FBX")
if not os.path.exists(export_path):
    os.makedirs(export_path)
for root, dirs, files in os.walk(path, topdown=False):
        
    for ma in files:
        f = ma.lower()
        if not f.endswith(".ma"):
            continue
        file_path = os.path.join(root,ma)
        cmds.file(file_path,o=1,f=1)
        
        SetFbxParameter()
        name = os.path.splitext(ma)[0]
        pm.mel.FBXExport(f= os.path.join(export_path,name))
        
        
        