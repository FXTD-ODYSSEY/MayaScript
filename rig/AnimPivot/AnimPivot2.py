# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-27 10:54:44'

"""
创建可以K帧的旋转轴心设置
解决动态偏移的问题 - 导致无法回到原点_(:з」∠)_
参考： https://forums.autodesk.com/t5/maya-programming/attributechange-scriptjob-and-its-lying-ways-help/td-p/6217887

~后来发现不需要动态更新 scirptjob 就可以了~
我错了，还是需要实时更新
"""

import pymel.core as pm
from functools import partial
import maya.api.OpenMaya as om
from textwrap import dedent
import uuid

def pivotEvent(sel,loc,msg, m_plug, otherMplug, clientData):

    # msg  kIncomingDirection = 2048
    # msg  kAttributeSet = 8
    # 2048 + 8 = 2056
    if msg == 2056:
        if not pm.objExists(sel) or not pm.objExists(loc):
            return
        node,attr = m_plug.name().split(".")
        if str(loc) == node and "translate" in attr and pm.objExists(loc):
            pm.xform(sel, piv=pm.xform(loc,q=1,ws=1,t=1), ws=1)

def deleteCallback(idx):
    om.MMessage.removeCallback(idx)

def addAttrCallback(sel,loc):

    UUID = str(uuid.uuid4()).replace("-","_")
    node = 'pivotFollow_%s' % UUID

    # Get sphere's MObject
    sel_list = om.MSelectionList()
    sel_list.add(str(loc))
    _node = sel_list.getDependNode(0)

    # Connect callback to event
    idx = om.MNodeMessage.addAttributeChangedCallback(_node, partial(pivotEvent,sel,loc))
    deleteEvent = lambda:om.MMessage.removeCallback(idx)
    pm.scriptJob( ro=1,nd= [str(loc),deleteEvent], protected=True)
    pm.scriptJob( ro=1,e= ["SceneOpened",deleteEvent], protected=True)
    
    
    script = dedent("""
    import pymel.core as pm
    from functools import partial

    def pivotEvent(sel,loc,msg, m_plug, otherMplug, clientData):
        if msg == 2056:
            if not pm.objExists(sel) or not pm.objExists(loc):
                return
            node,attr = m_plug.name().split(".")
            if str(loc) == node and "translate" in attr and pm.objExists(loc):
                pm.xform(sel, piv=pm.xform(loc,q=1,ws=1,t=1), ws=1)

    if pm.objExists("{sel}") and pm.objExists("{loc}"):
        sel_list = om.MSelectionList()
        sel_list.add("{loc}")
        _node = sel_list.getDependNode(0)
        idx = om.MNodeMessage.addAttributeChangedCallback(_node, partial(pivotEvent,"{sel}","{loc}"))
        deleteEvent = lambda: om.MMessage.removeCallback(idx)
        pm.scriptJob( ro=1,nd= ["{loc}",deleteEvent], protected=True)
        pm.scriptJob( ro=1,e= ["SceneOpened",deleteEvent], protected=True)
        
    elif pm.objExists("{node}"):
        pm.delete("{node}")
    """.format(sel=sel,loc=loc,node=node))
    pm.scriptNode( st=1, bs=script, n=node, stp='python')


# def deleteEvent(idx,node):
#     if pm.scriptJob(q=1,ex=idx):
#         pm.scriptJob(k=idx,f=1)
#     if pm.objExists(node):
#         pm.delete(node)

# def updatePivot(sel,loc):
#     pos = pm.xform(loc,q=1,ws=1,t=1)
#     pm.xform(sel, piv=pos, ws=1)

# def createScriptJob(sel,loc):
#     UUID = str(uuid.uuid4()).replace("-","_")
#     node = 'pivotFollow_%s' % UUID
    
#     # idx = pm.scriptJob( attributeChange=['%s.t'%loc,partial(pivotEvent,sel,loc)] )
#     pivotEvent = partial(updatePivot,sel,loc)
#     idx = pm.scriptJob( attributeChange=['%s.t'%loc,pivotEvent] )

#     _deleteEvent = partial(deleteEvent,idx,node)
#     pm.scriptJob( ro=1,nd= [str(loc),_deleteEvent], protected=True)
#     pm.scriptJob( ro=1,e= ["SceneOpened",_deleteEvent], protected=True)

#     script = dedent("""
#     import pymel.core as pm
#     from functools import partial

#     def deleteEvent(idx,node):
#         if pm.scriptJob(q=1,ex=idx):
#             pm.scriptJob(k=idx,f=1)
#         if pm.objExists(node):
#             pm.delete(node)

#     def updatePivot():
#         pos = pm.xform("{1}",q=1,ws=1,t=1)
#         pm.xform("{0}", piv=pos, ws=1)

#     if pm.objExists("{0}") and pm.objExists("{1}"):
#         print "load"
        
#         idx = pm.scriptJob( attributeChange=['{1}.t',updatePivot] )
#         _deleteEvent = partial(deleteEvent,idx,"{2}")
#         pm.scriptJob( ro=1,nd= ["{1}",_deleteEvent], protected=True)
#         pm.scriptJob( ro=1,e= ["SceneOpened",_deleteEvent], protected=True)
        
#     elif pm.objExists("{2}"):
#         pm.delete("{2}")
#     """.format(sel,loc,node))
#     pm.scriptNode( st=1, bs=script, n=node, stp='python')

    

def generateAnimPivotLocator(script=False):
        
    sel_list = pm.ls(sl=1)
    loc_list = []
    warning_list = []

    try:
        for sel in sel_list:
            loc_name = "%s_PIV" % sel
            if pm.objExists(loc_name):
                warn_str = u"%s 已经创建 locator" % sel
                pm.warning(warn_str)
                warning_list.append(warn_str)
                continue

            loc = pm.spaceLocator(n=loc_name)
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
            # pm.setAttr(loc.sx,l=1,k=0,cb=0)  
            # pm.setAttr(loc.sy,l=1,k=0,cb=0)  
            # pm.setAttr(loc.sz,l=1,k=0,cb=0)  
            
            if not script:
                loc.t.connect(sel.rotatePivot)
            else:
                # createScriptJob(sel,loc)
                addAttrCallback(sel,loc)

            loc_list.append(loc)


    except:
        import traceback
        pm.delete(loc)
        pm.delete(loc_list)
        pm.confirmDialog(title=u'错误', message=u'%s' % traceback.format_exc())
        return [],[]

    return loc_list,warning_list

def main(enhance):
    # NOTE 获取当前视窗的 modelEditor 开启 locator 显示
    for mp in pm.getPanel(type="modelPanel"):
        if pm.modelEditor(mp, q=1, av=1):
            pm.modelEditor(mp,e=1,locators=1)
            break
    
    loc_list,warning_list = generateAnimPivotLocator(script=enhance)
    
    pm.select(loc_list)

    if warning_list:
        warn_str = "\n".join(warning_list)
        pm.confirmDialog(title=u'警告', message=u'以下控制器创建失败：\n\n%s' % warn_str)

def singleClickCommand():
    main(False)

def doubleClickCommand():
    main(True)

if __name__ == "__main__":
    singleClickCommand()

