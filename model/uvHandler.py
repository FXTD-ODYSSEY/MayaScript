# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-07 19:57:02'

"""

"""

import pymel.core as pm
def switch2BaseMap():
    """
    切换 Base Map
    """
    for texWinName in pm.getPanel(sty='polyTexturePlacementPanel'):
        for i,_map in enumerate(pm.textureWindow(texWinName,q=1,textureNames=1)):
            if 'BaseMap' in _map:
                pm.textureWindow(texWinName,e=1,textureNumber=i)

def cutUV():
    """
    分离 UV 面
    """
    sel_list = [sel for sel in pm.selected() if type(sel) == pm.general.MeshFace]
    if not sel_list: return

    border_list = pm.polyListComponentConversion(sel_list,ff=1,te=1,bo=1)
    pm.polyMapCut(border_list,ch=0)
    pm.select(sel_list)

if __name__ == "__main__":
    cutUV()
# polyListComponentConversion -ff -te -bo $containedFaces
# polyEditUV -u -0.00095372 -v -0.00267041 ;