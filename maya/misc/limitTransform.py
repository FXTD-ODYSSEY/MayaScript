# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-29 09:31:24'

"""
锁定 Transform 在 -1 到 1 的范围
"""

import pymel.core as pm

def limitTranform(objType="nurbsCurve",limits=['t'],maxVal=1,minVal=-1):
    """transformLimit 锁定目标的移动范围
    
    Parameters
    ----------
    objType : str, optional
        遍历物体的类型, by default "nurbsCurve"
    limits : list, optional
        锁定的属性 支持 ['t','r','s'], by default ['t']
    maxVal : int, optional
        锁定的最大值, by default 1
    minVal : int, optional
        锁定的最小值, by default -1
    """
    sel_list = pm.ls(sl=1,dag=1,ni=1,type=objType)

    for sel in sel_list:
        if hasattr(sel,"getTransform"):
            sel = sel.getTransform()
        
        for limit in limits:
            if limit == 't' or limit == 'translate':
                pm.transformLimits(sel,tx=(minVal,maxVal),etx=(1,0))
                pm.transformLimits(sel,ty=(minVal,maxVal),ety=(1,0))
                pm.transformLimits(sel,tz=(minVal,maxVal),etz=(1,0))
                pm.transformLimits(sel,tx=(minVal,maxVal),etx=(1,1))
                pm.transformLimits(sel,ty=(minVal,maxVal),ety=(1,1))
                pm.transformLimits(sel,tz=(minVal,maxVal),etz=(1,1))
            elif limit == 'r' or limit == 'rotate':
                pm.transformLimits(sel,rx=(minVal,maxVal),erx=(1,0))
                pm.transformLimits(sel,ry=(minVal,maxVal),ery=(1,0))
                pm.transformLimits(sel,rz=(minVal,maxVal),erz=(1,0))
                pm.transformLimits(sel,rx=(minVal,maxVal),erx=(1,1))
                pm.transformLimits(sel,ry=(minVal,maxVal),ery=(1,1))
                pm.transformLimits(sel,rz=(minVal,maxVal),erz=(1,1))
            elif limit == 's' or limit == 'scale':
                pm.transformLimits(sel,sx=(minVal,maxVal),esx=(1,0))
                pm.transformLimits(sel,sy=(minVal,maxVal),esy=(1,0))
                pm.transformLimits(sel,sz=(minVal,maxVal),esz=(1,0))
                pm.transformLimits(sel,sx=(minVal,maxVal),esx=(1,1))
                pm.transformLimits(sel,sy=(minVal,maxVal),esy=(1,1))
                pm.transformLimits(sel,sz=(minVal,maxVal),esz=(1,1))


if __name__ == "__main__":
    limitTranform()