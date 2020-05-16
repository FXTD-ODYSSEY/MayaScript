# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 21:16:58'

"""
将本文件拖拽到 Maya 视窗即可完成安装
"""

import os
import sys
import json
import shutil
import hashlib
import tempfile
import traceback

from maya import cmds
from maya import mel
import pymel.core as pm
from maya import OpenMayaUI
try:
    from Qt import QtGui
    from Qt import QtCore
    from Qt import QtWidgets
    from Qt.QtCompat import wrapInstance,QFileDialog
except:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    from PySide2.QtWidgets import QFileDialog

from textwrap import dedent

def progressWin(seq,title='',status=''):
    cmds.progressWindow(	
        title=title ,
        status=status ,
        progress=0.0,
        isInterruptable=True )
    total = len(seq)
    for i,item in enumerate(seq):
        try:
            if cmds.progressWindow( query=True, isCancelled=True ) : break
            cmds.progressWindow( e=True, progress=float(i)/total*100)
            yield item  # with body executes here
        except:
            traceback.print_exc()
            cmds.progressWindow(ep=1)
    cmds.progressWindow(ep=1)

def SetFbxParameter():
    if not cmds.pluginInfo('fbxmaya', q=True, loaded=True):
        cmds.loadPlugin('fbxmaya')
    mel.eval('FBXResetExport')
    mel.eval('FBXExportFileVersion -v FBX201600')
    mel.eval('FBXExportUpAxis y')
    mel.eval('FBXExportShapes  -v false')
    mel.eval('FBXExportScaleFactor 1.0')
    mel.eval('FBXExportInAscii -v true')
    mel.eval('FBXExportConstraints -v false')
    mel.eval('FBXExportLights -v false')
    mel.eval('FBXExportSkins -v false')
    mel.eval('FBXExportSmoothingGroups -v true')
    mel.eval('FBXExportSmoothMesh -v false')
    mel.eval('FBXExportEmbeddedTextures -v false')
    mel.eval('FBXExportCameras -v false')
    mel.eval('FBXExportBakeResampleAnimation -v false')
    mel.eval('FBXExportSkeletonDefinitions -v true')

class FileListWidget(QtWidgets.QListWidget):
    def addItem(self,item):
        _item = item.text() if type(item) is QtWidgets.QListWidgetItem else item
        if not self.findItems(_item, QtCore.Qt.MatchContains):
            super(FileListWidget,self).addItem(item)

class AnimBatcherWin(QtWidgets.QWidget):

    old_md5_data = {}
    new_md5_data = {}

    def __init__(self):
        super(AnimBatcherWin, self).__init__()

        self.File_List = FileListWidget(self)
        self.File_List.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.File_List.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.File_List.customContextMenuRequested.connect(
            self.fileItemRightClickEvent)

        self.File_List.setAcceptDrops(True)
        self.File_List.dropEvent = self.listDropEvent
        self.File_List.dragMoveEvent = self.listDragMoveEvent
        self.File_List.dragEnterEvent = self.listDropEnterEvent
        
        self.Root_BTN = QtWidgets.QPushButton(u'获取Maya文件目录路径', self)
        self.Root_BTN.clicked.connect(self.handleSetDirectory)
        self.File_BTN = QtWidgets.QPushButton(u'获取Maya文件', self)
        self.File_BTN.clicked.connect(self.getMayaFiles)
        self.Current_BTN = QtWidgets.QPushButton(u'获取当前打开的Maya文件', self)
        self.Current_BTN.clicked.connect(self.getCurrent)

        self.Button_Layout = QtWidgets.QHBoxLayout()
        self.Button_Layout.addWidget(self.Root_BTN)
        self.Button_Layout.addWidget(self.File_BTN)
        self.Button_Layout.addWidget(self.Current_BTN)

        self.export = QtWidgets.QPushButton(u'批量导出动画文件', self)
        # self.export.clicked.connect(self.batchReplace)

        self.Main_Layout = QtWidgets.QVBoxLayout()
        self.Main_Layout.addWidget(self.File_List)
        self.Main_Layout.addLayout(self.Button_Layout)
        self.Main_Layout.addWidget(self.export)
        self.Main_Layout.setContentsMargins(0, 0, 0, 0)
        self.Main = QtWidgets.QWidget()
        self.Main.setLayout(self.Main_Layout)

        # NOTE 添加文件监视器功能
        self.watcher = QtCore.QFileSystemWatcher(self)
        self.watcher.directoryChanged.connect(self.handleDirectoryChanged)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.handleTimer)

        self.Exclude_Array = [".history", ".git", ".vscode"]

        # NOTE 添加启动的路径为搜索路径
        path = os.path.dirname(pm.sceneName()) if pm.sceneName() else os.path.dirname(__file__)
        self.handleSetDirectory(directory=path)

        # NOTE 添加 UI
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().addWidget(self.Main)

        self.loadJson()

    def saveJson(self):
        
        data = {
            "path_list":[self.File_List.item(i).toolTip() for i in range(self.File_List.count())],
        }

        json_path = os.path.join(tempfile.gettempdir(),"RF_Watcher.json")

        with open(json_path,'w') as f:
            # json.dump(data,f,ensure_ascii=False)
            json.dump(data,f)
        
    def loadJson(self):

        json_path = os.path.join(tempfile.gettempdir(),"RF_Watcher.json")

        if not os.path.exists(json_path):
            return

        try:
            with open(json_path,'r') as f:
                data = json.load(f,encoding="utf-8")
        except:
            os.remove(json_path)
            return
        
        for path in data["path_list"]:
            self.addItem(path)

    def fileItemRightClickEvent(self):
        self.menu = QtWidgets.QMenu(self)
        remove_action = QtWidgets.QAction(u'删除选择', self)
        remove_action.triggered.connect(self.fileRemoveItem)
        clear_action = QtWidgets.QAction(u'清空全部', self)
        clear_action.triggered.connect(self.itemClear)

        self.menu.addAction(remove_action)
        self.menu.addAction(clear_action)
        self.menu.popup(QtGui.QCursor.pos())
    
    def itemClear(self):
        self.File_List.clear()
        self.saveJson()

    def fileRemoveItem(self):
        # NOTE 如果没有选择 直接删除当前项
        for item in self.File_List.selectedItems():
            row = self.File_List.row(item)
            item = self.File_List.takeItem(row)
            path = item.toolTip()
            if self.old_md5_data.has_key(path):
                del self.old_md5_data[path]
        self.saveJson()

    def getMayaFiles(self):
        path_list, _ = QFileDialog().getOpenFileNames(
            self, caption=u"获取Maya文件", filter="Maya Scene (*.ma *.mb);;所有文件 (*)")

        for path in path_list:
            self.addItem(path)

    def getCurrent(self):
        path = cmds.file(q=1,sn=1)
        if os.path.exists(path):
            _, maya_file = os.path.split(path)
            item = QtWidgets.QListWidgetItem(maya_file)
            item.setToolTip(path)
            self.File_List.addItem(item)

    def addItem(self,path):
        _, file_name = os.path.split(path)
        matches = self.File_List.findItems(file_name, QtCore.Qt.MatchExactly)
        if not matches:
            item = QtWidgets.QListWidgetItem(file_name)
            item.setToolTip(path)
            self.File_List.addItem(item)
        else:
            for match in matches:
                if path == match.toolTip():
                    break
            else:
                item = QtWidgets.QListWidgetItem(path)
                item.setToolTip(path)
                self.File_List.addItem(item)
        self.saveJson()

    def listDropEvent(self,event):
        u'''
        listDropEvent 拖拽文件添加item
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现图片拖拽加载效果
        
        Arguments:
            event {QDropEvent} -- dropEvent 固定的事件参数
        
        '''
        # Note 获取拖拽文件的地址
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = str(url.toLocalFile())
                # Note 过滤已有的路径
                if path.split(".")[-1] in ["ma","mb"]:
                    self.addItem(path)
            self.saveJson()
            
        else:
            event.ignore()
 
    def listDragMoveEvent(self,event):
        u'''
        listDragMoveEvent 文件拖拽的移动事件
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现图片拖拽加载效果
        
        Arguments:
            event {QDragMoveEvent} --  dragMoveEvent 固定的事件参数
        
        '''
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    def listDropEnterEvent(self,event):
        u'''
        listDropEnterEvent 文件拖拽的进入事件
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现图片拖拽加载效果
        
        Arguments:
            event {QDragEnterEvent} --  dropEnterEvent 固定的事件参数
        
        '''
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def handleDirectoryChanged(self):
        """handleDirectoryChanged 路径下的文件发生了变化执行更新"""
        self.timer.stop()
        self._changed = True
        self.timer.start()

    def handleSetDirectory(self, directory=None):
        directory = directory if directory else QtWidgets.QFileDialog.getExistingDirectory(
            self)
        if directory:
            self.timer.stop()
            directories = self.watcher.directories()
            if directories:
                self.watcher.removePaths(directories)

            self._changed = False
            self.watcher.addPath(directory)
            self.updateList()
            self.timer.start()

    def handleTimer(self):
        if self._changed:
            self._changed = False
            self.updateList()

    def updateList(self):
        """updateList 更新列表"""
        self.new_md5_data = {}
        for directory in self.watcher.directories():
            for root, _, files in os.walk(directory):
                root = root.replace("\\", "/")
                # Note 过滤目录
                check = [x for x in root.split("/") if x in self.Exclude_Array]
                if len(check) > 0:
                    continue

                for item in progressWin(files,title=root,status=root):
                    if item.endswith(".mb") or item.endswith(".ma"):
                        file_path = os.path.join(root, item).replace("\\", "/")
                        hash_value = self.get_md5(file_path)
                        self.new_md5_data[file_path] = hash_value

                        # Note 检查文件是否存在，如果不存在则添加新的路径
                        if self.old_md5_data.has_key(file_path):
                            # Note 根据md5 检查文件是否被修改
                            if self.old_md5_data[file_path] != hash_value:
                                self.old_md5_data[file_path] = hash_value
                                target_item = self.File_List.findItems(
                                    os.path.split(file_path)[1], QtCore.Qt.MatchContains)[0]
                                target_item.setText(item)
                                target_item.setToolTip(file_path)
                        else:
                            self.old_md5_data[file_path] = hash_value
                            self.addItem(file_path)
                            self.saveJson()


        # Note 检查文件是否被删除，被删除的从列表中去掉
        if len(self.new_md5_data) != len(self.old_md5_data):
            for key in self.old_md5_data:
                if not self.new_md5_data.has_key(key):
                    item = self.File_List.findItems(
                        os.path.split(key)[1], QtCore.Qt.MatchContains)
                    self.File_List.takeItem(self.File_List.row(item[0]))
                    del self.old_md5_data[key]
                    self.saveJson()


    def get_md5(self, file_path):
        BLOCKSIZE = 65536
        hl = hashlib.md5()
        with open(file_path, 'r') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hl.update(buf)
                buf = f.read(BLOCKSIZE)
        return hl.hexdigest()

def errorLog(func):
    def wrapper(*args, **kwargs):
        res = None
        try:
            res = func(*args, **kwargs)
        except RuntimeError,e:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(QtWidgets.QApplication.activeWindow(),u"错误",e.message)
            raise e
        except Exception,e:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(QtWidgets.QApplication.activeWindow(),u"错误", "未知错误\n%s" %traceback.format_exc())
            raise e

        return res
    return wrapper

class ExportRigWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ExportRigWindow,self).__init__(parent)
        # NOTE 初始化 mel 脚本
        mel.eval('source channelBoxCommand')
        mel.eval('source moveJointsMode')

        self.setWindowTitle(u"导出引擎工具")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        rig_btn = QtWidgets.QPushButton(u'导出绑定',self)
        rig_btn.clicked.connect(self.genereateRig)

        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        batcher = AnimBatcherWin()
        batcher.export.clicked.connect(lambda *args:self.batchExportDirectory([batcher.File_List.item(i).toolTip() for i in range(batcher.File_List.count())]))
        # anim_btn = QtWidgets.QPushButton(u'导出动画',self)
        # anim_btn.clicked.connect(self.genereateAnim)

        # batch_btn = QtWidgets.QPushButton(u'导出动画目录',self)
        # batch_btn.clicked.connect(self.batchExportDirectory)

        layout.addWidget(rig_btn)
        layout.addWidget(self.line)
        layout.addWidget(batcher)
    
    @errorLog
    def preExport(self):
        Scene = pm.sceneName()
        if not Scene:
            raise RuntimeError(u"当前文件为未保存的空场景，请先保存")

        # NOTE 保存当前文件
        pm.saveFile()
        SetFbxParameter()
        
        return Scene

    @errorLog
    def getJntList(self,mesh_list):
        
        jnt_list = {jnt for mesh in mesh_list for skin in mesh.history(type="skinCluster") for jnt in skin.inputs(type="joint")}
        if not jnt_list:
            raise RuntimeError(u"当前文件找不到可输出的蒙皮骨骼")
        return jnt_list
    
    def getRelParent(self,jnt_list,root):
        """
        https://stackoverflow.com/questions/55196834/how-to-get-the-list-of-root-parents-created-in-a-scene-autodesk-maya-python

        """
        jnt_parent = {}
        for jnt in jnt_list:
            hi_tree = jnt.longName().split("|")[1:-1]
            parent = None
            while parent not in jnt_list:
                if not hi_tree: 
                    parent = root
                    break
                parent = pm.PyNode(hi_tree.pop())
            jnt_parent[jnt] = parent if parent != root else parent
        return jnt_parent
        
    def genereateAnim(self,reopen=True):
        # export_path,_ = self.getFilename()
        Scene = self.preExport()
        FBXAnim = os.path.join(Scene.dirname(),"FBXAnim") 
        os.mkdir(FBXAnim) if not os.path.exists(FBXAnim) else None
        export_path = os.path.join(FBXAnim,"%s.FBX" % Scene.namebase)
        export_path = export_path.replace('\\','/')

        # NOTE 导入所有的 reference
        ref_list = pm.listReferences()
        if len(ref_list) > 1:
            raise RuntimeError("动画文件包含多个引用文件")

        [ref.importContents(True) for ref in pm.listReferences()]
            
        mesh_list = pm.ls("MODEL",ni=1,dag=1,type="mesh")
        mesh_list = mesh_list if mesh_list else pm.ls(pm.pickWalk(d="down"),ni=1,dag=1,type="mesh")
        # # NOTE 删除非变形器历史
        # pm.bakePartialHistory( mesh_list,prePostDeformers=True )
        jnt_list = self.getJntList(mesh_list)

        pm.select(cl=1)
        root = pm.joint(n="root")

        jnt_parent = self.getRelParent(jnt_list,root)

        anim_parent = {}
        for jnt in jnt_list:
            pm.select(cl=1)
            anim_jnt = pm.joint(n="%s_bind"%jnt)
            pm.parentConstraint(jnt,anim_jnt,mo=0)
            pm.scaleConstraint(jnt,anim_jnt,mo=0)
            parent = jnt_parent[jnt]
            anim_parent[anim_jnt] = "%s_bind" % parent if parent != root else root

        jnt_transform = {}
        for anim_jnt,parent in anim_parent.items():
            anim_jnt.setParent(parent)
            # NOTE 删除骨骼缩放修正组
            transform = anim_jnt.getParent()
            if transform != parent:
                pm.ungroup(transform)

        # NOTE bake 关键帧
        start_time = pm.playbackOptions(q=1,min=1)
        end_time = pm.playbackOptions(q=1,max=1)
        pm.bakeResults(
            anim_parent.keys(),
            simulation=1, 
            t=(start_time,end_time)
        )

        # NOTE 删除 root 骨骼下的所有约束
        pm.delete(pm.ls(root,dag=1,ni=1,type="constraint"))

        pm.select(root)

        # NOTE 导出文件
        mel.eval('FBXExport -f "' + export_path + '" -s')
        os.startfile(os.path.dirname(export_path))

        # NOTE 重新打开当前文件
        if reopen:
            pm.openFile(pm.sceneName(),f=1)

    def genereateRig(self,select=True):
        
        # export_path,_ = self.getFilename()
        # if not os.path.exists(export_path):
        #     return

        Scene = self.preExport()
        export_path = os.path.join(Scene.dirname(),"%s.FBX" % Scene.namebase) 
        export_path = export_path.replace('\\','/')

        mel.eval('FBXExportSkins -v true')

        # NOTE 导入所有的 reference
        [ref.importContents(True) for ref in pm.listReferences()]
        
        # NOTE 获取场景中所有可见的模型
        mesh_list = pm.ls("MODEL",ni=1,dag=1,type="mesh")
        mesh_list = mesh_list if mesh_list else pm.ls(pm.pickWalk(d="down"),ni=1,dag=1,type="mesh")
        # # NOTE 删除非变形器历史
        # pm.bakePartialHistory( mesh_list,prePostDeformers=True )
        jnt_list = self.getJntList(mesh_list)

        pm.select(cl=1)
        root = pm.joint(n="root")

        jnt_parent = self.getRelParent(jnt_list,root)

        mel.eval('moveJointsMode 1;')
        # # NOTE 删除所有 Blendshape
        # pm.delete(pm.ls(type="ikEffector"))
        pm.delete(pm.ls(type="blendShape"))

        jnt_transform = {}
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
                jnt.t.set(pos)
            else:
                jnt_transform[jnt] = parent

        # NOTE clear jnt transform node
        for jnt,parent in jnt_transform.items():
            pm.xform(parent, piv=pm.xform(jnt,q=1,ws=1,t=1), ws=1)
            # jnt.s.set(parent.s.get())
            # parent.s.set(1,1,1)
            pm.ungroup(parent)
        
        
        # NOTE delete unrelated node
        [pm.delete(node) for jnt in jnt_list for node in jnt.getChildren()]
        
        # NOTE reparent hierarchy
        jnt_transform = {}
        for jnt,parent in jnt_parent.items():
            jnt.setParent(parent)
            transform = jnt.getParent()
            if transform != parent:
                jnt_transform[jnt] = transform

        for jnt,parent in jnt_transform.items():
            pm.xform(parent, piv=pm.xform(jnt,q=1,ws=1,t=1), ws=1)
            # NOTE 避免意外扭动
            jnt.s.set(1,1,1)
            parent.s.set(1,1,1)
            pm.ungroup(parent)

        [mesh.getParent().setParent(w=1) for mesh in mesh_list]
        pm.select(root,mesh_list)
        pm.delete(pm.ls(type="dagPose"))
        pm.dagPose(bp=1,s=1)
        # mel.eval('moveJointsMode 0;')
        
        # # NOTE 导出文件
        # mel.eval('FBXExport -f "' + export_path + '" -s')
        # os.startfile(os.path.dirname(export_path))

        # # NOTE 重新打开当前文件
        # pm.openFile(pm.sceneName(),f=1)

    def batchExportDirectory(self,dir_list):
        # if dir_list is None:
            # path = QtWidgets.QFileDialog.getExistingDirectory(self,dir=pm.sceneName().dirname())
            # dir_list = os.listdir(path)
        err_list = []
        # for file_path in progressWin(dir_list,u"批量导出动画"):
        for file_path in dir_list:
            if not file_path.endswith(".ma") and not  file_path.endswith(".mb"):
                continue
            pm.openFile(file_path,f=1)
            try:
                self.genereateAnim(False)
            except:
                print("=====================================\n")
                print(file_path + "\n")
                print("=====================================\n")
                import traceback
                traceback.print_exc()
                err_list.append(file_path)
                continue
        
        if err_list:
            QtWidgets.QMessageBox.warning(self,u"警告",u"下列文件输出失败\n%s" % u"\n".join(err_list))
        else:
            QtWidgets.QMessageBox.information(self,u"恭喜你",u"输出成功")


    def mayaShow(self,name=None):
        name = self.__class__.__name__ if name is None else name
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
    
    @staticmethod
    def mayaToQT( name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )


# NOTE 加载图片
qt_resource_data = b"\
\x00\x00\x0d\x04\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x20\x00\x00\x00\x20\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0b\x13\x00\x00\x0b\x13\
\x01\x00\x9a\x9c\x18\x00\x00\x07\xc6\x69\x54\x58\x74\x58\x4d\x4c\
\x3a\x63\x6f\x6d\x2e\x61\x64\x6f\x62\x65\x2e\x78\x6d\x70\x00\x00\
\x00\x00\x00\x3c\x3f\x78\x70\x61\x63\x6b\x65\x74\x20\x62\x65\x67\
\x69\x6e\x3d\x22\xef\xbb\xbf\x22\x20\x69\x64\x3d\x22\x57\x35\x4d\
\x30\x4d\x70\x43\x65\x68\x69\x48\x7a\x72\x65\x53\x7a\x4e\x54\x63\
\x7a\x6b\x63\x39\x64\x22\x3f\x3e\x20\x3c\x78\x3a\x78\x6d\x70\x6d\
\x65\x74\x61\x20\x78\x6d\x6c\x6e\x73\x3a\x78\x3d\x22\x61\x64\x6f\
\x62\x65\x3a\x6e\x73\x3a\x6d\x65\x74\x61\x2f\x22\x20\x78\x3a\x78\
\x6d\x70\x74\x6b\x3d\x22\x41\x64\x6f\x62\x65\x20\x58\x4d\x50\x20\
\x43\x6f\x72\x65\x20\x35\x2e\x36\x2d\x63\x31\x34\x35\x20\x37\x39\
\x2e\x31\x36\x33\x34\x39\x39\x2c\x20\x32\x30\x31\x38\x2f\x30\x38\
\x2f\x31\x33\x2d\x31\x36\x3a\x34\x30\x3a\x32\x32\x20\x20\x20\x20\
\x20\x20\x20\x20\x22\x3e\x20\x3c\x72\x64\x66\x3a\x52\x44\x46\x20\
\x78\x6d\x6c\x6e\x73\x3a\x72\x64\x66\x3d\x22\x68\x74\x74\x70\x3a\
\x2f\x2f\x77\x77\x77\x2e\x77\x33\x2e\x6f\x72\x67\x2f\x31\x39\x39\
\x39\x2f\x30\x32\x2f\x32\x32\x2d\x72\x64\x66\x2d\x73\x79\x6e\x74\
\x61\x78\x2d\x6e\x73\x23\x22\x3e\x20\x3c\x72\x64\x66\x3a\x44\x65\
\x73\x63\x72\x69\x70\x74\x69\x6f\x6e\x20\x72\x64\x66\x3a\x61\x62\
\x6f\x75\x74\x3d\x22\x22\x20\x78\x6d\x6c\x6e\x73\x3a\x78\x6d\x70\
\x3d\x22\x68\x74\x74\x70\x3a\x2f\x2f\x6e\x73\x2e\x61\x64\x6f\x62\
\x65\x2e\x63\x6f\x6d\x2f\x78\x61\x70\x2f\x31\x2e\x30\x2f\x22\x20\
\x78\x6d\x6c\x6e\x73\x3a\x64\x63\x3d\x22\x68\x74\x74\x70\x3a\x2f\
\x2f\x70\x75\x72\x6c\x2e\x6f\x72\x67\x2f\x64\x63\x2f\x65\x6c\x65\
\x6d\x65\x6e\x74\x73\x2f\x31\x2e\x31\x2f\x22\x20\x78\x6d\x6c\x6e\
\x73\x3a\x70\x68\x6f\x74\x6f\x73\x68\x6f\x70\x3d\x22\x68\x74\x74\
\x70\x3a\x2f\x2f\x6e\x73\x2e\x61\x64\x6f\x62\x65\x2e\x63\x6f\x6d\
\x2f\x70\x68\x6f\x74\x6f\x73\x68\x6f\x70\x2f\x31\x2e\x30\x2f\x22\
\x20\x78\x6d\x6c\x6e\x73\x3a\x78\x6d\x70\x4d\x4d\x3d\x22\x68\x74\
\x74\x70\x3a\x2f\x2f\x6e\x73\x2e\x61\x64\x6f\x62\x65\x2e\x63\x6f\
\x6d\x2f\x78\x61\x70\x2f\x31\x2e\x30\x2f\x6d\x6d\x2f\x22\x20\x78\
\x6d\x6c\x6e\x73\x3a\x73\x74\x45\x76\x74\x3d\x22\x68\x74\x74\x70\
\x3a\x2f\x2f\x6e\x73\x2e\x61\x64\x6f\x62\x65\x2e\x63\x6f\x6d\x2f\
\x78\x61\x70\x2f\x31\x2e\x30\x2f\x73\x54\x79\x70\x65\x2f\x52\x65\
\x73\x6f\x75\x72\x63\x65\x45\x76\x65\x6e\x74\x23\x22\x20\x78\x6d\
\x6c\x6e\x73\x3a\x74\x69\x66\x66\x3d\x22\x68\x74\x74\x70\x3a\x2f\
\x2f\x6e\x73\x2e\x61\x64\x6f\x62\x65\x2e\x63\x6f\x6d\x2f\x74\x69\
\x66\x66\x2f\x31\x2e\x30\x2f\x22\x20\x78\x6d\x6c\x6e\x73\x3a\x65\
\x78\x69\x66\x3d\x22\x68\x74\x74\x70\x3a\x2f\x2f\x6e\x73\x2e\x61\
\x64\x6f\x62\x65\x2e\x63\x6f\x6d\x2f\x65\x78\x69\x66\x2f\x31\x2e\
\x30\x2f\x22\x20\x78\x6d\x70\x3a\x43\x72\x65\x61\x74\x6f\x72\x54\
\x6f\x6f\x6c\x3d\x22\x41\x64\x6f\x62\x65\x20\x50\x68\x6f\x74\x6f\
\x73\x68\x6f\x70\x20\x43\x43\x20\x28\x57\x69\x6e\x64\x6f\x77\x73\
\x29\x22\x20\x78\x6d\x70\x3a\x43\x72\x65\x61\x74\x65\x44\x61\x74\
\x65\x3d\x22\x32\x30\x31\x37\x2d\x30\x37\x2d\x32\x30\x54\x31\x37\
\x3a\x33\x36\x3a\x31\x36\x2b\x30\x38\x3a\x30\x30\x22\x20\x78\x6d\
\x70\x3a\x4d\x6f\x64\x69\x66\x79\x44\x61\x74\x65\x3d\x22\x32\x30\
\x32\x30\x2d\x30\x35\x2d\x30\x38\x54\x31\x31\x3a\x30\x32\x3a\x35\
\x37\x2b\x30\x38\x3a\x30\x30\x22\x20\x78\x6d\x70\x3a\x4d\x65\x74\
\x61\x64\x61\x74\x61\x44\x61\x74\x65\x3d\x22\x32\x30\x32\x30\x2d\
\x30\x35\x2d\x30\x38\x54\x31\x31\x3a\x30\x32\x3a\x35\x37\x2b\x30\
\x38\x3a\x30\x30\x22\x20\x64\x63\x3a\x66\x6f\x72\x6d\x61\x74\x3d\
\x22\x69\x6d\x61\x67\x65\x2f\x70\x6e\x67\x22\x20\x70\x68\x6f\x74\
\x6f\x73\x68\x6f\x70\x3a\x43\x6f\x6c\x6f\x72\x4d\x6f\x64\x65\x3d\
\x22\x33\x22\x20\x70\x68\x6f\x74\x6f\x73\x68\x6f\x70\x3a\x49\x43\
\x43\x50\x72\x6f\x66\x69\x6c\x65\x3d\x22\x73\x52\x47\x42\x20\x49\
\x45\x43\x36\x31\x39\x36\x36\x2d\x32\x2e\x31\x22\x20\x78\x6d\x70\
\x4d\x4d\x3a\x49\x6e\x73\x74\x61\x6e\x63\x65\x49\x44\x3d\x22\x78\
\x6d\x70\x2e\x69\x69\x64\x3a\x38\x36\x64\x66\x66\x35\x32\x61\x2d\
\x63\x30\x62\x61\x2d\x32\x35\x34\x36\x2d\x38\x31\x34\x65\x2d\x33\
\x31\x35\x63\x37\x30\x64\x61\x62\x32\x61\x31\x22\x20\x78\x6d\x70\
\x4d\x4d\x3a\x44\x6f\x63\x75\x6d\x65\x6e\x74\x49\x44\x3d\x22\x61\
\x64\x6f\x62\x65\x3a\x64\x6f\x63\x69\x64\x3a\x70\x68\x6f\x74\x6f\
\x73\x68\x6f\x70\x3a\x64\x34\x32\x63\x62\x36\x38\x38\x2d\x64\x30\
\x39\x65\x2d\x31\x63\x34\x66\x2d\x39\x66\x38\x33\x2d\x64\x33\x30\
\x37\x36\x32\x63\x63\x37\x66\x36\x35\x22\x20\x78\x6d\x70\x4d\x4d\
\x3a\x4f\x72\x69\x67\x69\x6e\x61\x6c\x44\x6f\x63\x75\x6d\x65\x6e\
\x74\x49\x44\x3d\x22\x78\x6d\x70\x2e\x64\x69\x64\x3a\x35\x66\x30\
\x64\x33\x64\x39\x32\x2d\x39\x34\x34\x62\x2d\x62\x62\x34\x37\x2d\
\x62\x65\x61\x65\x2d\x38\x66\x64\x37\x32\x63\x63\x63\x39\x61\x63\
\x35\x22\x20\x74\x69\x66\x66\x3a\x4f\x72\x69\x65\x6e\x74\x61\x74\
\x69\x6f\x6e\x3d\x22\x31\x22\x20\x74\x69\x66\x66\x3a\x58\x52\x65\
\x73\x6f\x6c\x75\x74\x69\x6f\x6e\x3d\x22\x37\x32\x30\x30\x30\x30\
\x2f\x31\x30\x30\x30\x30\x22\x20\x74\x69\x66\x66\x3a\x59\x52\x65\
\x73\x6f\x6c\x75\x74\x69\x6f\x6e\x3d\x22\x37\x32\x30\x30\x30\x30\
\x2f\x31\x30\x30\x30\x30\x22\x20\x74\x69\x66\x66\x3a\x52\x65\x73\
\x6f\x6c\x75\x74\x69\x6f\x6e\x55\x6e\x69\x74\x3d\x22\x32\x22\x20\
\x65\x78\x69\x66\x3a\x43\x6f\x6c\x6f\x72\x53\x70\x61\x63\x65\x3d\
\x22\x31\x22\x20\x65\x78\x69\x66\x3a\x50\x69\x78\x65\x6c\x58\x44\
\x69\x6d\x65\x6e\x73\x69\x6f\x6e\x3d\x22\x33\x32\x22\x20\x65\x78\
\x69\x66\x3a\x50\x69\x78\x65\x6c\x59\x44\x69\x6d\x65\x6e\x73\x69\
\x6f\x6e\x3d\x22\x33\x32\x22\x3e\x20\x3c\x78\x6d\x70\x4d\x4d\x3a\
\x48\x69\x73\x74\x6f\x72\x79\x3e\x20\x3c\x72\x64\x66\x3a\x53\x65\
\x71\x3e\x20\x3c\x72\x64\x66\x3a\x6c\x69\x20\x73\x74\x45\x76\x74\
\x3a\x61\x63\x74\x69\x6f\x6e\x3d\x22\x63\x72\x65\x61\x74\x65\x64\
\x22\x20\x73\x74\x45\x76\x74\x3a\x69\x6e\x73\x74\x61\x6e\x63\x65\
\x49\x44\x3d\x22\x78\x6d\x70\x2e\x69\x69\x64\x3a\x35\x66\x30\x64\
\x33\x64\x39\x32\x2d\x39\x34\x34\x62\x2d\x62\x62\x34\x37\x2d\x62\
\x65\x61\x65\x2d\x38\x66\x64\x37\x32\x63\x63\x63\x39\x61\x63\x35\
\x22\x20\x73\x74\x45\x76\x74\x3a\x77\x68\x65\x6e\x3d\x22\x32\x30\
\x31\x37\x2d\x30\x37\x2d\x32\x30\x54\x31\x37\x3a\x33\x36\x3a\x31\
\x36\x2b\x30\x38\x3a\x30\x30\x22\x20\x73\x74\x45\x76\x74\x3a\x73\
\x6f\x66\x74\x77\x61\x72\x65\x41\x67\x65\x6e\x74\x3d\x22\x41\x64\
\x6f\x62\x65\x20\x50\x68\x6f\x74\x6f\x73\x68\x6f\x70\x20\x43\x43\
\x20\x28\x57\x69\x6e\x64\x6f\x77\x73\x29\x22\x2f\x3e\x20\x3c\x72\
\x64\x66\x3a\x6c\x69\x20\x73\x74\x45\x76\x74\x3a\x61\x63\x74\x69\
\x6f\x6e\x3d\x22\x73\x61\x76\x65\x64\x22\x20\x73\x74\x45\x76\x74\
\x3a\x69\x6e\x73\x74\x61\x6e\x63\x65\x49\x44\x3d\x22\x78\x6d\x70\
\x2e\x69\x69\x64\x3a\x64\x38\x62\x66\x32\x61\x34\x37\x2d\x62\x32\
\x32\x66\x2d\x66\x31\x34\x37\x2d\x62\x61\x65\x36\x2d\x38\x65\x31\
\x62\x31\x33\x37\x35\x39\x38\x61\x62\x22\x20\x73\x74\x45\x76\x74\
\x3a\x77\x68\x65\x6e\x3d\x22\x32\x30\x31\x37\x2d\x30\x38\x2d\x31\
\x34\x54\x31\x36\x3a\x35\x33\x3a\x34\x30\x2b\x30\x38\x3a\x30\x30\
\x22\x20\x73\x74\x45\x76\x74\x3a\x73\x6f\x66\x74\x77\x61\x72\x65\
\x41\x67\x65\x6e\x74\x3d\x22\x41\x64\x6f\x62\x65\x20\x50\x68\x6f\
\x74\x6f\x73\x68\x6f\x70\x20\x43\x43\x20\x28\x57\x69\x6e\x64\x6f\
\x77\x73\x29\x22\x20\x73\x74\x45\x76\x74\x3a\x63\x68\x61\x6e\x67\
\x65\x64\x3d\x22\x2f\x22\x2f\x3e\x20\x3c\x72\x64\x66\x3a\x6c\x69\
\x20\x73\x74\x45\x76\x74\x3a\x61\x63\x74\x69\x6f\x6e\x3d\x22\x73\
\x61\x76\x65\x64\x22\x20\x73\x74\x45\x76\x74\x3a\x69\x6e\x73\x74\
\x61\x6e\x63\x65\x49\x44\x3d\x22\x78\x6d\x70\x2e\x69\x69\x64\x3a\
\x38\x36\x64\x66\x66\x35\x32\x61\x2d\x63\x30\x62\x61\x2d\x32\x35\
\x34\x36\x2d\x38\x31\x34\x65\x2d\x33\x31\x35\x63\x37\x30\x64\x61\
\x62\x32\x61\x31\x22\x20\x73\x74\x45\x76\x74\x3a\x77\x68\x65\x6e\
\x3d\x22\x32\x30\x32\x30\x2d\x30\x35\x2d\x30\x38\x54\x31\x31\x3a\
\x30\x32\x3a\x35\x37\x2b\x30\x38\x3a\x30\x30\x22\x20\x73\x74\x45\
\x76\x74\x3a\x73\x6f\x66\x74\x77\x61\x72\x65\x41\x67\x65\x6e\x74\
\x3d\x22\x41\x64\x6f\x62\x65\x20\x50\x68\x6f\x74\x6f\x73\x68\x6f\
\x70\x20\x43\x43\x20\x32\x30\x31\x39\x20\x28\x57\x69\x6e\x64\x6f\
\x77\x73\x29\x22\x20\x73\x74\x45\x76\x74\x3a\x63\x68\x61\x6e\x67\
\x65\x64\x3d\x22\x2f\x22\x2f\x3e\x20\x3c\x2f\x72\x64\x66\x3a\x53\
\x65\x71\x3e\x20\x3c\x2f\x78\x6d\x70\x4d\x4d\x3a\x48\x69\x73\x74\
\x6f\x72\x79\x3e\x20\x3c\x2f\x72\x64\x66\x3a\x44\x65\x73\x63\x72\
\x69\x70\x74\x69\x6f\x6e\x3e\x20\x3c\x2f\x72\x64\x66\x3a\x52\x44\
\x46\x3e\x20\x3c\x2f\x78\x3a\x78\x6d\x70\x6d\x65\x74\x61\x3e\x20\
\x3c\x3f\x78\x70\x61\x63\x6b\x65\x74\x20\x65\x6e\x64\x3d\x22\x72\
\x22\x3f\x3e\x3a\x18\x3c\x1b\x00\x00\x04\xe4\x49\x44\x41\x54\x58\
\xc3\xc5\x56\x7d\x4c\x57\x55\x18\x7e\x4c\x2c\xa1\x08\x10\x09\xb4\
\x34\x23\x53\x19\xcb\x48\xd7\x1c\x2a\x60\xe9\x44\xa8\xd4\x85\xd0\
\x1f\xb5\xb2\x9c\x99\xad\x15\x69\xb3\x52\x68\x16\x08\x66\xc5\xd0\
\xd0\x20\x51\x98\x09\xe1\x04\x6c\x7c\xa4\x22\x2e\x90\x06\x82\x1f\
\x20\x28\x88\x5a\x83\xe9\xf8\xac\xe1\x0a\x22\xcb\x41\xcf\xab\xef\
\x65\x57\x06\xfc\x7e\x8c\xdf\xe6\xd9\x9e\xdd\xf7\x9c\x7b\xce\xb9\
\xcf\x79\x3f\x9e\x73\xd1\xdb\xdb\x8b\xbb\x09\xdc\x75\x02\x97\xd0\
\x8b\x5a\xfc\xbb\x89\xcf\x5e\x6b\x91\x88\xec\x57\x01\x3c\x44\x8c\
\xc6\x10\x4d\xf6\x3d\x8f\xee\x5c\x9a\x93\x88\xfb\x07\x9c\x24\x04\
\xce\xe2\x7a\x54\x19\x9a\xcb\xd8\xfd\x92\xd8\x46\x6c\x1e\x0c\x17\
\x70\xa3\xfb\x7d\x6c\x4c\xa1\xfd\x1c\xe1\x60\xec\x53\x87\xff\xb2\
\x4f\xa0\x71\x0d\x4d\x37\x62\x8c\x8c\xc9\xbe\x27\xd1\xfa\x0b\xcd\
\x30\x62\x8a\x8c\x71\xfd\x33\xf5\xb8\x59\xa5\xa4\x1c\x6f\x11\xa8\
\x40\x7b\x2c\x17\x9f\xe5\xc0\xd7\xc4\x4a\x62\xc1\x60\xe0\x87\xba\
\xd6\x62\xfd\x41\xdd\xd4\xd1\x20\x50\x83\xae\xfc\xfd\x38\xb6\x4d\
\xe7\x39\xcb\x98\xec\x5b\x82\xab\xa7\x69\xae\x27\xbc\x65\xac\x0c\
\x2d\xf3\xe8\x95\x3a\x5d\x3f\xad\x8f\xc0\x70\x42\x30\x10\x81\x2a\
\xfc\x75\x64\x17\x32\x93\x69\x86\xaa\x17\x06\x24\xc0\xbe\xdf\x39\
\x74\x5e\xd6\xb1\xd9\x7d\x04\x8a\xd1\x20\x6e\xc9\x20\x76\x0e\x15\
\x02\x22\x6e\x1f\x0a\x4a\x0a\x50\x97\x43\xdb\x93\xb0\xb7\x09\x01\
\x6b\x43\x20\x90\xb8\x1e\x42\x85\x78\x61\x29\xe1\x31\x62\x02\x8c\
\xdd\x9c\x1a\xfc\xdd\x66\x6d\x08\x18\xc3\xd6\xf9\x08\x88\xe1\x06\
\xaf\x98\x09\x58\xbb\xfe\x14\xfe\xb8\xa6\xde\xbc\x4d\x80\xed\x01\
\xc2\x9f\xf8\x98\x88\xb1\x10\x82\xcd\x3a\x67\x03\xe1\x6b\xaa\x04\
\xc9\xf2\xd5\x5a\x45\x5b\x64\x9e\x84\x2a\x1f\xd5\x4d\xb4\x8f\x9a\
\x42\x1b\x45\x7c\x45\x84\xf7\x25\x21\xdb\x3d\xc4\x38\x62\xa6\x12\
\x19\xd0\xf5\xe2\xba\xdd\xc8\x49\x50\x37\xcf\xd2\x6c\x1f\xa5\x04\
\xa4\xce\x9f\x20\xe6\x1a\xf3\xf3\x50\x99\x56\x88\x4b\xf5\xb4\x77\
\xf5\x0b\xad\x1f\xe1\x75\x2b\x89\xeb\xd1\xd3\x31\x9c\x0a\x30\x63\
\x15\xde\x0d\x10\xe2\xac\xed\x08\x86\xe0\x1b\x0d\x87\xbd\x51\x19\
\x03\xe5\x80\x21\x50\xa6\xf9\x98\xac\xb1\x8c\xe4\x82\x96\x3d\xc8\
\x93\x05\xbb\x89\xd8\xfe\xae\x67\xf2\xb5\x7f\x8a\xb8\x1a\xda\xd9\
\xea\xea\x37\x89\xa9\x67\xd0\x11\x5d\x84\xdf\x0e\xd0\x0e\x22\x26\
\x5a\x22\x20\x02\x65\x9a\x0f\x27\x75\x7d\x40\x30\x96\xae\xe6\x82\
\x46\x56\xc4\xb5\x00\x2c\x8c\xd0\x2c\x7f\xd6\x70\x1d\x17\x36\xc4\
\x20\xf1\xb8\xe6\xc0\x72\xe2\x69\xf1\x40\x39\xda\xb6\x1e\xc1\x85\
\x3c\x25\xe4\x69\x89\x80\x8c\xf7\xcd\x97\x1c\x30\xa0\x64\xfc\x58\
\x15\xe9\x54\xb6\xf6\x38\xec\x5b\x63\x68\xbe\xbc\xaf\x41\x77\xed\
\x0e\xa4\xfd\xc0\xfe\x6b\x52\x6a\xba\xe6\xce\x0d\x47\x48\x40\x12\
\xea\x41\x39\x19\x5d\x1d\x49\x97\x8b\x64\x2e\x92\x53\x5a\x22\x30\
\xdc\xfc\xa1\x8e\x94\x70\xe9\x3b\x77\x10\x30\x11\xb9\x97\x78\x6c\
\x39\xc2\xc2\xa8\xfd\x9d\xc6\x22\xd1\x0a\x5f\xcc\xdf\xae\x32\xec\
\x62\x10\x50\x2f\x85\x6a\xde\x6c\x35\xe5\x8d\xf4\x93\x88\x64\xf3\
\x25\x27\xe5\x99\x81\xe2\x6a\xf5\xcc\xa0\x4d\xae\xda\xf1\x5a\x32\
\x6b\x25\x49\x75\x73\xd1\x8a\x39\xc4\x7d\xa6\xb9\x62\x3f\xaa\xe3\
\x0b\xac\xc0\x32\x42\xc2\xfb\x12\x2c\x34\x09\x89\x0b\xf1\x94\x24\
\xa9\x6a\xc4\x93\xd9\x38\x15\x44\x4d\x48\xa1\xa2\x1d\x28\x43\x6b\
\x36\x91\x59\x8a\xe6\x8c\x44\xe4\x84\xe8\x7c\x3b\x0b\xfb\x0a\x61\
\x77\xa3\x0c\xad\x6e\x74\xb9\xdd\x79\xfc\x13\x7f\x0c\x97\x3f\x9b\
\x80\x49\xfe\x5a\x46\x72\x9a\x65\xe3\xe0\xb6\x62\x2f\x8e\x26\x16\
\xe0\x62\x1a\xdf\x3d\x6e\xd6\x83\x21\x9b\xd5\xbf\x4e\x6c\xfc\xf8\
\xb7\xf1\xc8\x10\xcd\x58\x4c\x2c\x24\x7c\x88\x19\x26\xf8\x6c\xc0\
\x17\xef\xe5\xa3\xe6\x90\xf6\x1d\x2c\x7d\xc7\x6a\x02\x54\x2e\xff\
\x42\x5c\x89\xb2\x87\x43\xb0\xfe\x0d\x49\xcc\xc7\xf6\x3b\xcf\xd8\
\xf1\x70\xf7\x4c\x43\x71\x42\x38\xa2\xd7\x49\x22\x1b\xe1\x18\x31\
\x01\xc6\x3c\xd9\x0d\x13\xfc\x23\xb1\x7d\x53\x26\xca\xa3\xe9\x72\
\x0f\x73\x22\x32\x3c\xa3\xaa\xd1\xf5\x56\x1e\xaa\x43\x27\x62\xf2\
\xec\x9f\x6e\xd7\xb9\xaf\xe6\xc4\xc8\x09\x94\xa3\x3d\x9d\xfb\x2c\
\x19\x0d\xbb\xb9\x67\x70\xbd\xea\x34\x3a\xae\x44\x20\x7e\x95\x54\
\x4a\x29\x9a\x66\x51\xdf\xcb\x38\x5e\xc9\xf7\x81\x72\x51\x1d\xc7\
\xaf\x22\xd7\x4b\x8c\x7f\xc1\x11\x13\x28\x45\x8b\x08\xd0\x0b\xa2\
\x68\x51\x48\x7c\x99\x97\x58\x0f\xd1\x5b\x84\x86\x5a\x3e\x6f\x4a\
\x3f\x10\x21\xa9\x7a\xcd\x7a\x9f\xc0\xd5\xfd\x7c\x3e\xaf\x37\xa4\
\x4d\x08\x64\x28\x81\x69\x84\x6b\x0e\xce\x15\x99\x95\x6d\x27\xb2\
\x9a\x39\xfe\xa3\x5e\x6c\xae\x9c\x9f\xc6\x67\xb0\x0d\x09\x34\xa5\
\x3b\xc3\x55\x2e\xa0\xe9\x92\x58\x21\x78\x23\x80\xd2\x7c\x43\x3e\
\x5e\x89\x3f\x7b\xdc\xf1\x70\xa3\xfe\x68\x78\x7f\x8e\x24\x07\x99\
\x6f\x53\x0f\x24\x21\x77\x45\x2a\x0a\x13\xb5\xf4\x24\xfb\x1d\x53\
\x50\x90\x2a\x04\xde\xc6\xc6\x4e\xf6\x0f\xab\x26\x38\x32\x61\x3f\
\x8c\xc5\xde\xd7\x69\x07\xda\x2c\x07\x24\x9b\x29\x40\x07\x59\xe7\
\xe1\x5a\x82\x63\x66\x60\xe6\xf4\xc3\xa8\xbd\xc8\xd2\xcc\x67\xff\
\x13\x29\x3b\x26\x67\xc0\x49\xb4\xa5\xa8\x4e\xd8\xae\x0a\xc4\xed\
\x1e\x78\x64\x6a\x0e\xaa\xb2\xbe\xc7\xcf\x09\x5e\xf0\x11\xd7\x3a\
\x3b\xc1\x65\x9e\xdc\x8e\x54\x3f\xbf\x0a\xfc\xfe\x11\x65\xf9\x3b\
\x47\x38\x2d\xd2\xd3\xdb\x4e\x07\xb4\x89\xb2\x79\xad\xc3\x96\x0f\
\x0a\x50\x9f\xc7\x4c\xcf\x62\x15\x64\xd2\x33\xb9\x7c\x66\xc7\x60\
\xcf\x4a\x3d\xf9\x62\xfd\xe7\xb3\x9d\x12\x9a\x9a\xbd\xc6\xd5\x57\
\xef\x82\x17\x4d\x08\xd2\xf1\x29\xfd\xef\x82\xc1\xf6\xfd\x1f\x5a\
\xf5\x05\xa0\x0a\x89\xf4\xf7\x00\x00\x00\x00\x49\x45\x4e\x44\xae\
\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x0f\
\x0d\x67\xfa\x47\
\x00\x46\
\x00\x69\x00\x67\x00\x68\x00\x74\x00\x45\x00\x78\x00\x70\x00\x6f\x00\x72\x00\x74\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x71\xf2\x3c\x6f\x8f\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def createModFolder(module):
    MAYA_APP_DIR = os.environ["MAYA_APP_DIR"]
    # NOTE 构建 Mod 
    mod_path = os.path.join(MAYA_APP_DIR,"filmSkin2GameSkinMod")
    os.mkdir(mod_path) if not os.path.exists(mod_path) else None
        
    scripts = os.path.join(mod_path,"scripts")
    os.mkdir(scripts) if not os.path.exists(scripts) else None
    userSetup = os.path.join(scripts,"userSetup.py")
    with open(userSetup,'w') as f:
        f.write(dedent('''
            import {module}
            {module}.qInitResources()
        '''.format(module=module)))
    
    DIR = os.path.dirname(__file__)
    shutil.copy(os.path.join(DIR,"%s.py" % module),os.path.join(scripts,"%s.py" % module))

    mod = os.path.join(MAYA_APP_DIR,"modules","filmSkin2GameSkinMod.mod")
    with open(mod,'w') as f:
        f.write(dedent('''
        + MAYAVERSION:2014 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2015 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2016 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2017 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2018 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2019 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2020 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2021 filmSkin2GameSkinMod 1.1.0 {path}
        + MAYAVERSION:2022 filmSkin2GameSkinMod 1.1.0 {path}
        '''.format(path=mod_path)))


def onMayaDroppedPythonFile(*args):
    qInitResources()
    parentTab = mel.eval('''global string $gShelfTopLevel;string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;''')
    module,ext = os.path.splitext(os.path.basename(__file__))
    pm.shelfButton( commandRepeatable = True, image1 = "FightExport.png",iol = "export" ,label = "Fight Export Window", parent = parentTab, command = dedent("""
        import {module}
        reload({module})
        from {module} import ExportRigWindow
        try:
            MF_RigWin = ExportRigWindow()
            MF_RigWin.mayaShow()
        except :
            import traceback
            traceback.print_exc()
        
    """.format(module=module)))

    
    try:
        MF_RigWin = ExportRigWindow()
        MF_RigWin.mayaShow()
    except :
        import traceback
        traceback.print_exc()

    # NOTE 构建 Mod 
    createModFolder(module)

if __name__ == "__main__":
    try:
        MF_RigWin = ExportRigWindow()
        MF_RigWin.mayaShow()
    except :
        import traceback
        traceback.print_exc()

# import sys
# MODULE = r"F:\MayaTecent\MayaScript\rig"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import flimSkin2GameSkin
# reload(flimSkin2GameSkin)
# from flimSkin2GameSkin import ExportRigWindow
# MF_RigWin = ExportRigWindow()
# MF_RigWin.mayaShow()