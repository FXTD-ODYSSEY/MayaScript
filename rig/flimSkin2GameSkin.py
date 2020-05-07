# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 21:16:58'

"""

"""

from maya import cmds
from maya import mel
import pymel.core as pm
from maya import OpenMayaUI

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import wrapInstance

class RigWinow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(RigWinow,self).__init__(parent)
        # NOTE 初始化 mel 脚本
        mel.eval('source channelBoxCommand')

        self.setWindowTitle(u"导出引擎工具")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        rig_btn = QtWidgets.QPushButton(u'绑定导出',self)
        rig_btn.clicked.connect(self.genereateRig)

        anim_btn = QtWidgets.QPushButton(u'动画导出',self)
        anim_btn.clicked.connect(self.genereateAnim)

        layout.addWidget(rig_btn)
        layout.addWidget(anim_btn)

    def getJntList(self,mesh_list):
        jnt_list = set()
        for mesh in mesh_list:
            skin_list = mesh.listHistory(type="skinCluster")
            skin = next(iter(skin_list),None)
            if skin is None: continue
            jnt_list.update(skin.listHistory(type="joint"))
        return jnt_list

    def genereateAnim(self):
        # NOTE 导入所有的 reference
        [ref.importContents(True) for ref in pm.listReferences()]
            
        mesh_list = pm.ls(ni=1,v=1,type="mesh")
        # NOTE 删除非变形器历史
        pm.bakePartialHistory( mesh_list,prePostDeformers=True )
        jnt_list = self.getJntList(mesh_list)

        pm.select(cl=1)
        root = pm.joint(n="root")

        anim_jnt_list = []
        for jnt in jnt_list:
            pm.select(cl=1)
            anim_jnt = pm.joint(n="%s_bind"%jnt)
            con = pm.parentConstraint(jnt,anim_jnt,mo=0)
            anim_jnt.setParent(root)
            anim_jnt_list.append(anim_jnt)

        # NOTE bake 关键帧
        start_time = pm.playbackOptions(q=1,min=1)
        end_time = pm.playbackOptions(q=1,max=1)
        pm.bakeResults(
            anim_jnt_list,
            simulation=1, 
            t=(start_time,end_time)
        )

        # NOTE 删除 root 骨骼下的所有约束
        pm.delete(pm.ls(root,dag=1,ni=1,type="constraint"))

        pm.select(root)

    def genereateRig(self,select=True):
        # NOTE 导入所有的 reference
        [ref.importContents(True) for ref in pm.listReferences()]
        
        # NOTE 获取场景中所有可见的模型
        mesh_list = pm.ls(ni=1,v=1,type="mesh")
        # NOTE 删除非变形器历史
        pm.bakePartialHistory( mesh_list,prePostDeformers=True )
        jnt_list = self.getJntList(mesh_list)

        pm.select(cl=1)
        root = pm.joint(n="root")

        # NOTE 删除所有 IK 控制器 & Blendshape
        pm.delete(pm.ls(type="ikEffector"))
        pm.delete(pm.ls(type="blendShape"))

        for jnt,pos in {jnt:pm.xform(jnt,q=1,ws=1,t=1) for jnt in jnt_list}.iteritems():
            jnt.tx.setLocked(0)
            jnt.ty.setLocked(0)
            jnt.tz.setLocked(0)
            jnt.rx.setLocked(0)
            jnt.ry.setLocked(0)
            jnt.rz.setLocked(0)
            jnt.sx.setLocked(0)
            jnt.sy.setLocked(0)
            jnt.sz.setLocked(0)

            jnt.tx.showInChannelBox(1)
            jnt.ty.showInChannelBox(1)
            jnt.tz.showInChannelBox(1)
            jnt.rx.showInChannelBox(1)
            jnt.ry.showInChannelBox(1)
            jnt.rz.showInChannelBox(1)
            jnt.sx.showInChannelBox(1)
            jnt.sy.showInChannelBox(1)
            jnt.sz.showInChannelBox(1)

            mel.eval('CBdeleteConnection %s' % jnt.tx)
            mel.eval('CBdeleteConnection %s' % jnt.ty)
            mel.eval('CBdeleteConnection %s' % jnt.tz)
            mel.eval('CBdeleteConnection %s' % jnt.rx)
            mel.eval('CBdeleteConnection %s' % jnt.ry)
            mel.eval('CBdeleteConnection %s' % jnt.rz)
            mel.eval('CBdeleteConnection %s' % jnt.sx)
            mel.eval('CBdeleteConnection %s' % jnt.sy)
            mel.eval('CBdeleteConnection %s' % jnt.sz)

            jnt.setParent(root)
            jnt.rename("%s_bind" % jnt)
            parent = jnt.getParent()
            if parent.name() == root:
                jnt.tx.set(pos[0])
                jnt.ty.set(pos[1])
                jnt.tz.set(pos[2])
            else:
                jnt.s.set(parent.s.get())
                parent.s.set(1,1,1)
                jnt.setParent(root)
                pm.delete(parent)


        [pm.delete(node) for jnt in jnt_list for node in jnt.getChildren()]
                
        pm.select(root,mesh_list) if select else None
        
        return root

    def mayaShow(self,name="RigWinow"):
        # NOTE 如果变量存在 就检查窗口多开
        if pm.workspaceControl(name,q=1,ex=1):
            pm.deleteUI(name)
        window = pm.workspaceControl(name,label=self.windowTitle())
        pm.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        ptr = self.mayaToQT(window)
        ptr.setLayout(QtWidgets.QVBoxLayout())
        ptr.layout().setContentsMargins(0,0,0,0)
        ptr.layout().addWidget(self)
        return ptr
    
    def mayaToQT( self,name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )


if __name__ == "__main__":
    try:
        MF_RigWin = RigWinow()
        MF_RigWin.mayaShow()
    except :
        import traceback
        traceback.print_exc()