# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-22 15:29:33'

""" 
parentConstraint 切换到 pointConstraint
"""

import pymel.core as pm

con_list = pm.ls(sl=1,dag=1,type="parentConstraint")

for con in con_list:
    src = con.target[0].targetParentMatrix.connections()[0]
    grp = con.constraintParentInverseMatrix.connections()[0]
    pm.delete(con)
    pm.pointConstraint(src,grp,mo=1)

