# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-22 15:25:32'

""" 
选择曲线控制器和模型生成毛囊
"""

import maya.api.OpenMaya as om
import pymel.core as pm

def getCloesestUV(mesh,transform):
    """ 使用 pymel 的 getUVAtPoint 有些点无法获取到正确uv"""
    # Note 获取模型
    sel_list = om.MSelectionList()
    sel_list.add(str(mesh))
    path = sel_list.getDagPath(0)
    mesh = om.MFnMesh(path)

    loc = pm.spaceLocator()
    pm.pointConstraint(transform,loc)
    # Note 获取 中心点 的位置
    pos = om.MPoint(*loc.t.get())

    pm.delete(loc)

    # Note 获取最近的点
    cloesest_pos,_ = mesh.getClosestPoint(pos,space=om.MSpace.kObject)
    
    return mesh.getUVAtPoint(cloesest_pos)

def createFollicle(oMesh, uPos=0.0, vPos=0.0):
    """创建并连接毛囊"""
    
    # Note https://chrislesage.com/character-rigging/manually-create-maya-follicle-in-python/
    pName = '_'.join((oMesh.name(),'follicle','#'))
    oFoll = pm.createNode('follicle',name=pName)

    oMesh.outMesh.connect(oFoll.inputMesh)
    oMesh.worldMatrix[0].connect(oFoll.inputWorldMatrix)

    oFoll.outRotate.connect(oFoll.getParent().rotate)
    oFoll.outTranslate.connect(oFoll.getParent().translate)
    oFoll.parameterU.set(uPos)
    oFoll.parameterV.set(vPos)
    oFoll.getParent().t.lock()
    oFoll.getParent().r.lock()

    return oFoll

if __name__ == "__main__":
    base_mesh = pm.ls(sl=1,fl=1,dag=1,ni=1,type="mesh")[0]
    follicle_list = []
    crv_list = pm.ls(sl=1,fl=1,dag=1,ni=1,type="nurbsCurve")
        
    for crv in crv_list:
        u,v,_ = getCloesestUV(base_mesh,crv.getParent())
        fol = createFollicle(base_mesh,u,v)
        # NOTE 记录原始位置
        follicle_list.append(fol)
        grp = "%s_fol"%crv
        if not pm.objExists(grp):
            grp = pm.group(crv,n=grp)
        pm.pointConstraint(fol.getParent(),grp,mo=1)

    follicle_grp = pm.group(follicle_list,n="follicle_grp")

