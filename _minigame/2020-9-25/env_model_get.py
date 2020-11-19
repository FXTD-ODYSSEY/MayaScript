# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-25 11:48:28'


import os
import pymel.core as pm
output_path = r"D:\_minigame\_Env\01\Splendid"
base_name = os.path.basename(output_path)

def main():
    
    sel_list = pm.ls(sl=1)
    if not sel_list:
        return
    sel = sel_list[0]
    
    pm.undoInfo(ock=1)

    pm.parent(sel,w=1)
    # NOTE 居中轴心
    pm.xform(sel,cp=1)
    
    pm.mel.BakeCustomPivot()
    
    sel.t.set(0,0,0)
    sel.r.set(0,0,0)
    x,_,z = pm.xform(sel,q=1,rp=1)
    bbox = pm.exactWorldBoundingBox(sel)
    pm.xform(sel,piv=[x,bbox[1],z])
    
    pm.mel.BakeCustomPivot()
    pm.xform(sel,ws=1,t=[0,0,0])
    index = 1
    path = os.path.join(output_path,"%s_%s.ma" % (base_name,str(index).zfill(2)))
    while os.path.exists(path):
        index += 1
        path = os.path.join(output_path,"%s_%s.ma" % (base_name,str(index).zfill(2)))

    path = path.replace('\\','/')
    print(path)
    # commnad = 'FBXExport -f "%s.fbx" -s ' % path.replace('\\','/')
    # NOTE 导出 ma 文件
    pm.mel.file(path,f=1,options="v=0;",typ="mayaAscii",pr=1,es=1)
    pm.undoInfo(cck=1)
    
    pm.undo()


if __name__ == "__main__":
    main()