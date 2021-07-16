# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-09 14:35:16'

"""

"""


import pymel.core as pm

if __name__ == "__main__":
    for jnt in pm.ls(sl=1,dag=1,type="joint"):
        circle = pm.circle(ch=0,n="%s_ctrl"%jnt)[0]
        grp = pm.group(circle,n="%s_grp"%circle)
        pm.delete(pm.parentConstraint(jnt,grp,mo=0))
        # NOTE  冻结变换
        pm.makeIdentity(grp,a=1,t=1,r=1,s=1,n=0,pn=1)
