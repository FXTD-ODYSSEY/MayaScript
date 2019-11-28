# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 10:19:31'

"""
遍历物体生成偏移组
"""


import pymel.core as pm

def grpObject(objType="nurbsCurve"):
        
    sel_list = pm.ls(sl=1,dag=1,ni=1,type=objType)

    grp_list = []
    for sel in sel_list:
        # if hasattr(sel,"getTransform"):
        #     sel = sel.getTransform()
        grp = pm.group(sel,n="%s_ofst"%sel)
        grp_list.append(grp)
    
    return grp_list

if __name__ == "__main__":
    grp_list = grpObject()

for grp in grp_list:
    pm.parentConstraint("locator1",grp,mo=1)