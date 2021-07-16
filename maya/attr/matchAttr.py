# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-16 14:09:38'

"""
根据当前的操纵杆传递属性数值
"""


import pymel.core as pm

def matchAttr():
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
    
    if len(sel_list) != 2:
        pm.headsUpMessage(u"请选择两个物体")
        pm.warning(u"请选择两个物体")

    driver,driven = sel_list

    for attr in attr_list:
        if not hasattr(driver,attr) or not hasattr(driven,attr):
            continue

        driver_attr = pm.Attribute("%s.%s"%(driver,attr))  
        driven_attr = pm.Attribute("%s.%s"%(driven,attr))

        if driven_attr.isLocked() and not driven_attr.isKeyable():
            continue

        driven_attr.set(driver_attr.get())

            
if __name__ == "__main__":
    matchAttr()