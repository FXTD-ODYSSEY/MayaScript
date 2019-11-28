# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-24 13:41:31'

import pymel.core as pm

def tglAttr():
    # NOTE 获取当前使用的工具
    ctx = pm.currentCtx()
    sel_list = pm.ls(sl=1)

    if ctx == "moveSuperContext":
        attr_list = ['tx','ty','tz']
    elif ctx == "RotateSuperContext":
        attr_list = ['rx','ry','rz']
    elif ctx == "scaleSuperContext":
        attr_list = ['sx','sy','sz']
    else:
        return
    
    for sel in sel_list:
        for attr in attr_list:
            if not hasattr(sel,attr):
                continue
            attr = pm.Attribute("%s.%s"%(sel,attr))
            attr.setKeyable(not attr.isKeyable())
            attr.setLocked(not attr.isLocked())
            
if __name__ == "__main__":
    tglAttr()