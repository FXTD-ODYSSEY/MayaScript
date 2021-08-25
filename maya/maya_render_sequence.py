# -*- coding: utf-8 -*-
"""
HW2 渲染大图的时候会跳过更新渲染 导致一直渲染一张图
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-25 15:58:12'

import os
import traceback
import pymel.core as pm

def progress(seq, status="", title=""):
    pm.progressWindow(status=status, title=title, progress=0.0, isInterruptable=True)
    total = len(seq)
    for i, item in enumerate(seq):
        try:
            if pm.progressWindow(query=True, isCancelled=True):
                break
            pm.progressWindow(e=True, progress=float(i) / total * 100)
            yield item  # with body executes here
        except:
            traceback.print_exc()
            pm.progressWindow(ep=1)
    pm.progressWindow(ep=1)
    
defaultRenderGlobals = pm.PyNode("defaultRenderGlobals")
startFrame = int(defaultRenderGlobals.startFrame.get())
endFrame = int(defaultRenderGlobals.endFrame.get())
startFrame = 50
endFrame = 65
cam = "Rig_Luffy01_Combine:camera_cgShape"
output_path = r"G:\file_test\2021-08-25\output"

for i in progress(range(startFrame,endFrame+1)):
    pm.currentTime(i)
    editor = pm.renderWindowEditor(q=True, editorName=True)
    pm.renderWindowEditor(editor, e=True, currentCamera=cam)
    pm.mel.renderWindowRender("redoPreviousRender", "renderView")
    # Note 使用 ColorManagement 从渲染窗口输出图片
    output_image = os.path.join(output_path,"output_%s.png" % i)
    pm.renderWindowEditor(editor, e=True, com=1, wi=output_image)