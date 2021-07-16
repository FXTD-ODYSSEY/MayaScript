# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-23 23:39:12'

""" 
选择物体或者物体顶点 在对应位置生成 locator
"""
import pymel.core as pm

if __name__ == "__main__":
    
    for sel in pm.ls(sl=1,fl=1):
        pos = pm.xform(sel,q=1,ws=1,t=1)
        loc = pm.spaceLocator()
        loc.t.set(pos)
        if type(sel) == pm.general.MeshVertex:
            # NOTE 参考 https://stackoverflow.com/questions/23532329/how-to-convert-three-dimensional-vector-to-an-euler-rotation-in-software-like-ma
            nor = pos + sel.getNormal(space="world")
            loc2 = pm.spaceLocator(p=nor)
            pm.aimConstraint(loc2, loc) 
            pm.delete(loc2)
        else:
            rot = pm.xform(sel,q=1,ws=1,ro=1)
            loc.r.set(rot)
