# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-22 15:25:32'

""" 
选择骨骼生成和模型生成毛囊
"""

import maya.api.OpenMaya as om
import pymel.core as pm

def getCloesestUV(mesh,jnt):
    """ 使用 pymel 的 getUVAtPoint 有些点无法获取到正确uv"""
    # Note 获取模型
    sel_list = om.MSelectionList()
    sel_list.add(str(mesh))
    path = sel_list.getDagPath(0)
    mesh = om.MFnMesh(path)

    # Note 获取 骨骼 的位置
    jnt_pos = om.MPoint(*pm.xform(jnt,q=1,ws=1,t=1))

    # Note 获取最近的点
    cloesest_pos,_ = mesh.getClosestPoint(jnt_pos,space=om.MSpace.kObject)
    
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
    base_mesh = pm.ls(sl=1,fl=1,dag=1,type="mesh")[0]
    follicle_list = []
    jnt_list = pm.ls(sl=1,fl=1,dag=1,type="joint")
        
    for jnt in jnt_list:
        u,v,_ = getCloesestUV(base_mesh,jnt)
        fol = createFollicle(base_mesh,u,v)
        # NOTE 记录原始位置
        follicle_list.append(fol)
        grp = "%s_fol"%jnt
        if not pm.objExists(grp):
            grp = pm.group(jnt,n=grp)
        pm.pointConstraint(fol.getParent(),grp,mo=1)

    follicle_grp = pm.group(follicle_list,n="follicle_grp")
