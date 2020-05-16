# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-16 20:47:39'

"""
导出 atom 动画 修复动画文件的 IFKK 切换跳动问题
"""

import os
import re
import tempfile

from maya import mel
import pymel.core as pm
import pymel.core.nodetypes as nt

def atomFixIKFK():
        
    # ref_path = r"X:/Characters/Fight/Rig/Darius_rig.mb"

    # # NOTE 获取时间滑块
    # env = pm.language.Env()
    # playBackTimes = env.getPlaybackTimes()

    # # NOTE 获取摄像机
    # for mp in pm.getPanel(type="modelPanel"):
    #     if pm.modelEditor(mp, q=1, av=1):
    #         mp = pm.uitypes.ModelPanel(mp)
    #         cam = mp.getCamera()
    #         cam_pos = pm.xform(cam,q=1,ws=1,t=1)
    #         break
    
    
    ref_list = pm.listReferences()
    if len(ref_list) != 1:
        raise RuntimeError(u"存在多个参考或没有参考")

    ref_node = ref_list[0]
    ref_path = ref_node.path


    namespace = os.path.splitext(os.path.basename(ref_path))[0]
    # NOTE 加载 Atom 插件
    if not pm.pluginInfo('atomImportExport', q=True, loaded=True):
        pm.loadPlugin('atomImportExport')
        
    # NOTE 保存当前文件
    pm.saveFile()


    # NOTE 选择所有带关键帧的控制器
    ctrl_list = {node for crv in pm.ls(type="animCurve") for node in crv.listConnections() if type(node) is nt.Transform}
    pm.select(ctrl_list)

    atom_file = os.path.join(tempfile.gettempdir(),"IKFK_Fix.atom").replace("\\","/")
    mel.eval("""
    file -force -options "precision=8;statics=1;baked=1;sdk=0;constraint=0;animLayers=1;selected=selectedOnly;whichRange=1;range=1:10;hierarchy=none;controlPoints=0;useChannelBox=1;options=keys;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 " -typ "atomExport" -es "%s";
    """ % atom_file)

    # NOTE 去除当前参考
    ref_node.remove()

    # SceneName = pm.sceneName()

    # # NOTE 新建场景
    # pm.newFile(f=1)
    
    # # NOTE 同步时间滑块
    # env.setPlaybackTimes(playBackTimes)

    # # NOTE 同步摄像机
    # for mp in pm.getPanel(type="modelPanel"):
    #     if pm.modelEditor(mp, q=1, av=1):
    #         mp = pm.uitypes.ModelPanel(mp)
    #         mp.setCamera(cam)
    #         break
    
    # # NOTE 匹配透视相机的位置
    # if cam == "perps":
    #     pm.xform(cam,t=cam_pos,ws=1)
    
    pm.createReference(ref_path,r=1,namespace=namespace)

    # pm.select([ re.sub("^\S*:","*:",str(ctrl)) for ctrl in ctrl_list])
    pm.select(ctrl_list)

    mel.eval("""
    file -import -type "atomImport" -ra true -options ";;targetTime=3;option=insert;match=hierarchy;;selected=selectedOnly;" "%s";
    """ % atom_file)

    # pm.saveFile(SceneName)

if __name__ == "__main__":
    atomFixIKFK()