# coding:utf 8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-20 10:02:57'

""" 
通过pointOnCurveInfo获取曲线上的点
"""
import pymel.core as pm

if __name__ == "__main__":
    
        
    cv_list = []

    for sel in pm.ls(sl=1,fl=1):
        if type(sel) == pm.general.NurbsCurveCV:
            cv_list.append(sel)
        elif hasattr(sel,"getShape"):
            crv = sel.getShape()
            if type(crv) == pm.nodetypes.NurbsCurve:
                cv_list.extend(crv.cv)

    for cv in cv_list:
        idx = cv.index()
        crv = cv.node()   
        info = pm.createNode("pointOnCurveInfo")
        info.parameter.set((idx-1)%len(crv.cv))
        crv.worldSpace[0].connect(info.inputCurve)

        loc = pm.spaceLocator()
        info.position.connect(loc.t)


