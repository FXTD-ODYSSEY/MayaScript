# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-27 10:54:44'

"""
创建可以K帧的旋转轴心设置
"""

import pymel.core as pm


def generateAnimPivotLocator():
        
    sel_list = pm.ls(sl=1)
    loc_list = []
    warning_list = []

    try:
        for sel in sel_list:
            loc_name = "%s_piv" % sel.longName()
            if sel.rotatePivot.isConnected():
                warn_str = u"%s 旋转轴心点已经连接" % sel
                pm.warning(warn_str)
                warning_list.append(warn_str)
                continue
            # if hasattr(sel,"piv_vis"):
            #     warn_str = u"%s piv_vis 属性存在冲突" % sel
            #     pm.warning(warn_str)
            #     warning_list.append(warn_str)
            #     continue

            loc = pm.spaceLocator(n="%s_PIV" % sel)
            pm.parent(loc,sel)
            # NOTE 父子约束匹配位置
            pm.delete(pm.parentConstraint(sel,loc,mo=0))
            # NOTE 冻结变换
            pm.makeIdentity(a=1,t=1,r=1,s=1,n=0,pn=1)

            loc_shape = loc.getShape()
            
            loc_shape.localScaleX.set(40)
            loc_shape.localScaleY.set(40)
            loc_shape.localScaleZ.set(40)

            # NOTE 锁定并隐藏无关的属性
            pm.setAttr(loc.rx,l=1,k=0,cb=0)  
            pm.setAttr(loc.ry,l=1,k=0,cb=0)  
            pm.setAttr(loc.rz,l=1,k=0,cb=0)  
            pm.setAttr(loc.sx,l=1,k=0,cb=0)  
            pm.setAttr(loc.sy,l=1,k=0,cb=0)  
            pm.setAttr(loc.sz,l=1,k=0,cb=0)  
            loc.t.connect(sel.rotatePivot)    
            loc_list.append(loc)

            # pm.addAttr(sel,ln="piv_vis",at="bool")
            # sel.piv_vis.setKeyable(1)
            # sel.piv_vis.set(1)
            # sel.piv_vis.connect(loc.v)
    except:
        import traceback
        pm.delete(loc)
        pm.delete(loc_list)
        traceback.print_exc()
        return [],[]

    return loc_list,warning_list

def main():

    # NOTE 获取当前视窗的 modelEditor 开启 locator 显示
    for mp in pm.getPanel(type="modelPanel"):
        if pm.modelEditor(mp, q=1, av=1):
            pm.modelEditor(mp,e=1,locators=1)
            break
    
    loc_list,warning_list = generateAnimPivotLocator()
    
    pm.select(loc_list)

    if warning_list:
        warn_str = "\n".join(warning_list)
        pm.confirmDialog(title=u'警告', message=u'以下控制器创建失败：\n\n%s' % warn_str)

if __name__ == "__main__":
    main()
