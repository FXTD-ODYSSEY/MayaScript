# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-20 11:40:23'

""" 
将骨骼转换为 NurbsSphere 球 （parent Shape）
"""

import pymel.core as pm

if __name__ == "__main__":
    for jnt in pm.ls(sl=1,dag=1,type="joint"):
        radius = jnt.radius.get()
        sphere = pm.sphere(r=radius/10,ax=(0,1,0),n="%s_sphere"%jnt,ch=0)[0]
        pm.delete(pm.parentConstraint(jnt,sphere,mo=0))
        shape = sphere.getShape()
        pm.parent(shape,jnt,r=1,s=1)
        pm.sets( "initialShadingGroup",e=1,forceElement=shape)
        pm.delete(sphere)