# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-5-23 20:46:22'

"""
将本文件拖拽到 Maya 视窗即可完成安装
"""

import os
import re
import sys
import json
import shutil
import inspect
import hashlib
import tempfile
import traceback
from textwrap import dedent
from functools import partial

from maya import cmds
from maya import mel
import pymel.core as pm
import pymel.core.nodetypes as nt

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


class IProgressDialog(QtWidgets.QProgressDialog):
    u'''
    ProgressDialog 进度条窗口
    
    进度条窗口
    使用参考:
        progress_dialog = ProgressDialog(u"获取插件列表", u"取消", 0, len(list))
        for i,item in enumerate(list):
            
            # for 循环逻辑代码
            
            progress_dialog.setValue(i+1)
            if progress_dialog.wasCanceled():
                break
            progress_dialog.setLabelText(u"状态改变")
    
    Arguments:
        QProgressDialog {QProgressDialog} -- Qt 进度条窗口类
    '''
    def __init__(self, status=u"进度",button_text=u"取消",minimum=0,maximum=100,parent=None,title=""):

        super(IProgressDialog, self).__init__(parent)

        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle(status if title else title)
        self.setLabelText(status)
        self.setCancelButtonText(button_text)
        self.setRange(minimum,maximum)
        self.show()
        self.delay()

    def delay(self):
        u'''
        delay 延时1ms 防止gui无响应
        延时1ms操作 确保窗口不会呈空白
        '''
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(1, loop.quit)
        loop.exec_()
    
    def setLabelText(self,text):
        u'''
        setLabelText 设置加载文本
        
        该功能继承自 QProgressDialog 的 setLabelText
        加入延时功能来响应GUI
        Arguments:
            text {str} -- 加载文本
        '''
        super(IProgressDialog, self).setLabelText(text)
        self.delay()
    
    @classmethod
    def loop(cls,seq,**kwargs):
        self = cls(**kwargs)
        self.setMaximum(len(seq))
        for i,item in enumerate(seq):

            self.setValue(i+1)
            if self.wasCanceled():break
            try:
                yield item  # with body executes here
            except:
                import traceback
                traceback.print_exc()
                self.deleteLater()
            # self.exec_()
        self.deleteLater()
  
class FileListWidget(QtWidgets.QListWidget):

    def __init__(self, parent , fileFilter=None):
        super(FileListWidget, self).__init__(parent)
        self.watcher = parent
        self.fileFilter = fileFilter
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.setAcceptDrops(True)

    def dragEnterEvent(self,event):
        u'''
        dragEnterEvent 文件拖拽的进入事件
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现文件拖拽加载效果
        
        Arguments:
            event {QDragEnterEvent} --  dropEnterEvent 固定的事件参数
        
        '''
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self,event):
        u'''
        dropEvent 拖拽文件添加item
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现文件拖拽加载效果
        
        Arguments:
            event {QDropEvent} -- dropEvent 固定的事件参数
        
        '''
        # Note 获取拖拽文件的地址
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = (url.toLocalFile())
                _,ext = os.path.splitext(path)
                # Note 过滤已有的路径
                if ext in self.fileFilter or "*" in self.fileFilter:
                    self.watcher.addItem(path)
            
            self.watcher.saveJson()
            
        else:
            event.ignore()

    def dragMoveEvent(self,event):
        u'''
        dragMoveEvent 文件拖拽的移动事件
        
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

class IFileWatcherList(QtWidgets.QWidget):

    old_md5_data = {}
    new_md5_data = {}

    def __init__(self,jsonName=None,fileFilter=None,excludeArray=None,getCurrentCallback=None):
        super(IFileWatcherList, self).__init__()
        
        file_name = inspect.currentframe().f_back.f_code.co_filename
        md5 = self.getMD5(file_name)
        self.jsonName = jsonName if jsonName else "%s_%s.json" % (self.__class__.__name__,md5)

        self.fileFilter = fileFilter if isinstance(fileFilter,list) else ["*"]
        self.File_List = FileListWidget(self,self.fileFilter)
        self.File_List.customContextMenuRequested.connect(
            self.fileItemRightClickEvent)
        
        self.Root_BTN = QtWidgets.QPushButton(u'获取文件目录路径', self)
        self.Root_BTN.clicked.connect(self.handleSetDirectory)
        self.File_BTN = QtWidgets.QPushButton(u'获取文件', self)
        self.File_BTN.clicked.connect(self.getFile)

        self.Button_Layout = QtWidgets.QHBoxLayout()
        self.Button_Layout.addWidget(self.Root_BTN)
        self.Button_Layout.addWidget(self.File_BTN)
        
        if callable(getCurrentCallback):
            self.Current_BTN = QtWidgets.QPushButton(u'获取当前打开的文件', self)
            self.Current_BTN.clicked.connect(getCurrentCallback)
            self.Button_Layout.addWidget(self.Current_BTN)

        self.Main_Layout = QtWidgets.QVBoxLayout()
        self.Main_Layout.addWidget(self.File_List)
        self.Main_Layout.addLayout(self.Button_Layout)
        self.Main_Layout.setContentsMargins(0, 0, 0, 0)
        self.Main = QtWidgets.QWidget()
        self.Main.setLayout(self.Main_Layout)

        # NOTE 添加文件监视器功能
        self.watcher = QtCore.QFileSystemWatcher(self)
        self.watcher.directoryChanged.connect(self.handleDirectoryChanged)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.handleTimer)

        self.Exclude_Array = {".history", ".git", ".vscode"} if not isinstance(excludeArray,set) else excludeArray

        # NOTE 添加 UI
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().addWidget(self.Main)

        self.loadJson()

    def fileItemRightClickEvent(self):
        self.menu = QtWidgets.QMenu(self)
        open_file_action = QtWidgets.QAction(u'打开文件路径', self)
        open_file_action.triggered.connect(self.openFileLocation)

        remove_action = QtWidgets.QAction(u'删除选择', self)
        remove_action.triggered.connect(self.fileRemoveItem)
        clear_action = QtWidgets.QAction(u'清空全部', self)
        clear_action.triggered.connect(self.itemClear)
        

        self.menu.addAction(open_file_action)
        self.menu.addSeparator()
        self.menu.addAction(remove_action)
        self.menu.addAction(clear_action)
        self.menu.popup(QtGui.QCursor.pos())

    def saveJson(self):
        
        data = {
            "path_list":[self.File_List.item(i).toolTip() for i in range(self.File_List.count())],
        }

        json_path = os.path.join(tempfile.gettempdir(),self.jsonName)

        with open(json_path,'w') as f:
            # json.dump(data,f,ensure_ascii=False)
            json.dump(data,f)
        
    def loadJson(self):

        json_path = os.path.join(tempfile.gettempdir(),self.jsonName)

        # if not os.path.exists(json_path):
        #     return

        try:
            with open(json_path,'r') as f:
                data = json.load(f,encoding="utf-8")
        except:
            if os.path.exists(json_path):
                os.remove(json_path)
        else:
            for path in data["path_list"]:
                self.addItem(path)
    
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

    def openFileLocation(self):
        item = self.File_List.currentItem()
        path = item.toolTip()
        os.startfile(os.path.dirname(path))

    def getFile(self):
        path_list, _ = QFileDialog().getOpenFileNames(
            self, caption=u"获取Maya文件", filter="Maya Scene (*.ma *.mb);;所有文件 (*)")

        for path in path_list:
            self.addItem(path)

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
                item = QtWidgets.QListWidgetItem(file_name)
                item.setToolTip(path)
                self.File_List.addItem(item)
        self.saveJson()

    def handleDirectoryChanged(self):
        """handleDirectoryChanged 路径下的文件发生了变化执行更新"""
        self.timer.stop()
        self._changed = True
        self.timer.start()

    def handleSetDirectory(self, directory=None):
        directory = directory if directory else QFileDialog.getExistingDirectory(self)
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

                for item in IProgressDialog.loop(files,title=root,status=root):
                    file_name,ext = os.path.splitext(item)
                    if ext in self.fileFilter or "*" in self.fileFilter:
                        file_path = os.path.join(root, item).replace("\\", "/")
                        hash_value = self.getMD5(file_path)
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
            delete_list = []
            for key in self.old_md5_data:
                if key not in self.new_md5_data:
                    item = self.File_List.findItems(
                        os.path.split(key)[1], QtCore.Qt.MatchContains)
                    if item:
                        self.File_List.takeItem(self.File_List.row(item[0]))
                        delete_list.append(key)

            for key in delete_list:
                del self.old_md5_data[key]
            self.saveJson()


    def getMD5(self, file_path):
        # NOTE https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
        md5_hash = hashlib.md5()
        with open(file_path,"rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

class HLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(HLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


def SetFbxParameter():
    if not pm.pluginInfo('fbxmaya', q=True, loaded=True):
        pm.loadPlugin('fbxmaya')
    pm.mel.FBXResetExport()

    # NOTE 获取支持的最高版本 FBX 
    try:
        pm.FBXExportFileVersion(v=None)
    except Exception as err:
        version = re.search(r"FBX\d+",str(err)).group()
        
    pm.mel.FBXExportFileVersion(v=version)
    pm.mel.FBXExportUpAxis('y')
    pm.mel.FBXExportShapes(v=False)
    pm.mel.FBXExportScaleFactor(1)
    pm.mel.FBXExportInAscii(v=True)
    pm.mel.FBXExportLights(v=False)
    pm.mel.FBXExportSkins(v=False)
    pm.mel.FBXExportSmoothingGroups(v=True)
    pm.mel.FBXExportSmoothMesh(v=False)
    pm.mel.FBXExportEmbeddedTextures(v=False)
    pm.mel.FBXExportCameras(v=False)
    pm.mel.FBXExportBakeResampleAnimation(v=False)
    pm.mel.FBXExportSkeletonDefinitions(v=True)

class HIKBatchRetargetWin(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(HIKBatchRetargetWin,self).__init__(parent)
        self.error_list = []
        self.json_file = os.path.join(tempfile.gettempdir(),"%s_data.json" % self.__class__.__name__)

        # NOTE 加载 HumanIK 插件
        pm.loadPlugin("mayaHIK") if not pm.pluginInfo("mayaHIK",q=1,l=1) else None
        pm.loadPlugin("mayaCharacterization") if not pm.pluginInfo("mayaCharacterization",q=1,l=1) else None
        pm.loadPlugin("OneClick") if not pm.pluginInfo("OneClick",q=1,l=1) else None
        pm.mel.source("hikInputSourceUtils")

        self.setWindowTitle(u"HumanIK 批量重定向工具 - timmyliang & 820472580@qq.com")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        
        
        self.rig_laoyut = QtWidgets.QHBoxLayout()
        self.rig_label = QtWidgets.QLabel("新绑定文件")
        self.rig_line = QtWidgets.QLineEdit()
        self.rig_button = QtWidgets.QPushButton("获取文件")
        self.rig_button.clicked.connect(self.getRigFile)
        self.rig_laoyut.addWidget(self.rig_label)
        self.rig_laoyut.addWidget(self.rig_line)
        self.rig_laoyut.addWidget(self.rig_button)

        self.target_laoyut = QtWidgets.QHBoxLayout()
        self.target_label = QtWidgets.QLabel("新绑定 HIK角色 名称")
        self.target_line = QtWidgets.QLineEdit()
        self.target_laoyut.addWidget(self.target_label)
        self.target_laoyut.addWidget(self.target_line)

        self.source_laoyut = QtWidgets.QHBoxLayout()
        self.source_label = QtWidgets.QLabel("旧绑定 HIK角色 名称")
        self.source_line = QtWidgets.QLineEdit()
        self.source_laoyut.addWidget(self.source_label)
        self.source_laoyut.addWidget(self.source_line)

        self.watcher = IFileWatcherList(fileFilter=[".ma",".mb"],getCurrentCallback=self.getCurrent)

        self.export_laoyut = QtWidgets.QHBoxLayout()
        self.export_label = QtWidgets.QLabel("输出路径")
        self.export_line = QtWidgets.QLineEdit()
        self.export_button = QtWidgets.QPushButton("获取文件")
        self.export_button.clicked.connect(lambda :self.export_line.setText(QtWidgets.QFileDialog.getExistingDirectory(self),self.saveSettings()))
        self.export_laoyut.addWidget(self.export_label)
        self.export_laoyut.addWidget(self.export_line)
        self.export_laoyut.addWidget(self.export_button)
        
        # TODO FBX 导出需要有相应的规范 
        # self.groupBox = QtWidgets.QGroupBox()
        # self.groupBox.setTitle("文件输出格式")
        # self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        # self.FBX_RB = QtWidgets.QRadioButton(self.groupBox)
        # self.FBX_RB.setText("FBX 文件")
        # self.MAYA_RB = QtWidgets.QRadioButton(self.groupBox)
        # self.MAYA_RB.setText("Maya 文件")
        # self.MAYA_RB.setChecked(True)
        # self.horizontalLayout.addWidget(self.FBX_RB)
        # self.horizontalLayout.addWidget(self.MAYA_RB)

        self.export_btn = QtWidgets.QPushButton('批量重定向',self)
        self.export_btn.clicked.connect(self.batchRetarget)

        layout.addLayout(self.rig_laoyut)
        layout.addLayout(self.target_laoyut)
        layout.addLayout(self.source_laoyut)
        layout.addWidget(HLine())
        layout.addWidget(self.watcher)
        layout.addWidget(HLine())
        layout.addLayout(self.export_laoyut)
        # layout.addWidget(self.groupBox)
        layout.addWidget(self.export_btn)

        self.loadSettings()

    def getRigFile(self):
        file_name,_ = QtWidgets.QFileDialog.getOpenFileName(self)
        if file_name:
            self.rig_line.setText(file_name)
            self.saveSettings()


    def getCurrent(self):
        path = pm.sceneName()
        self.watcher.addItem(path) if os.path.exists(path) else None
        self.saveSettings()
    
    def saveSettings(self):
        rig_line = self.rig_line.text()
        source_line = self.source_line.text()
        target_line = self.target_line.text()
        export_line = self.export_line.text()

        data = {
            "rig_line":rig_line,
            "source_line":source_line,
            "target_line":target_line,
            "export_line":export_line,
        }


        with open(self.json_file,'w') as f:
            json.dump(data,f)

    def loadSettings(self):
        
        if not os.path.exists(self.json_file):
            return

        with open(self.json_file,'r') as f:
            data = json.load(f)
        
        rig_line = data["rig_line"]
        source_line = data["source_line"]
        target_line = data["target_line"]
        export_line = data["export_line"]

        self.rig_line.setText(rig_line)
        self.source_line.setText(source_line)
        self.target_line.setText(target_line)
        self.export_line.setText(export_line)



    def batchRetarget(self):

        rig_path = self.rig_line.text()
        source = self.source_line.text()
        target = self.target_line.text()
        export_path = self.export_line.text()

        check = True
        if not os.path.exists(rig_path):
            QtWidgets.QMessageBox.warning(self,"警告","绑定文件路径不存在")
        elif not source:
            QtWidgets.QMessageBox.warning(self,"警告","新绑定 HIK角色 不存在")
        elif not target:
            QtWidgets.QMessageBox.warning(self,"警告","旧绑定 HIK角色 不存在")
        elif not os.path.exists(export_path):
            QtWidgets.QMessageBox.warning(self,"警告","输出路径 不存在")
        else:
            check = False
        
        if check: return

        self.saveSettings()

        # NOTE 保存当前文件
        if pm.isModified() and pm.sceneName().exists():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("当前文件存在修改！")
            msgBox.setInformativeText("是否要保存当前文件的修改")
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Ignore)
            msgBox.setEscapeButton(QtWidgets.QMessageBox.Cancel) 
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                pm.mel.SaveScene()
            elif ret == QtWidgets.QMessageBox.Cancel:
                return

        file_list = [self.watcher.File_List.item(i).toolTip() for i in range(self.watcher.File_List.count())]

        self.error_list = []
        for i in range(self.watcher.File_List.count()):
            path = self.watcher.File_List.item(i).toolTip()
            self.loadAnimFile(str(path),i)

        self.displayErrorInfo()
        
        # NOTE 打开输出路径 
        os.startfile(self.export_line.text())

    def loadAnimFile(self,file_path,index):

        # NOTE 打开文件
        pm.openFile(file_path,f=1)

        target = self.target_line.text()
        source = self.source_line.text()

        for hik_node in pm.ls(typ="HIKCharacterNode"):
            if source in str(hik_node):
                source = hik_node
                break
        else:
            err_msg = "%s - 找不到旧绑定 HIK角色 " % file_path
            self.error_list.append(err_msg)
            return 

        # NOTE 导入 reference
        rig_path = self.rig_line.text()
        name,ext = os.path.splitext(os.path.basename(rig_path))
        ref = pm.createReference(rig_path,r=1,namespace=name)

        target = "%s:%s" % (name,target) if ":" not in target else target
        if not pm.objExists(target):
            err_msg = "%s - 找不到新绑定 HIK角色 " % file_path
            self.error_list.append(err_msg)
            return

        # NOTE 重定向
        pm.mel.hikSetCharacterInput(target,source)

        export_path = self.export_line.text()
        pm.renameFile(os.path.join(export_path,pm.sceneName().basename()))
        pm.saveFile(f=1)
        
        # TODO FBX 导出需要有相应的规范 
        # if self.MAYA_RB.isChecked():
        #     pm.renameFile(os.path.join(export_path,pm.sceneName().basename()))
        #     pm.saveFile(f=1)
        # elif self.FBX_RB.isChecked():
        #     ref.importContents(True)
        #     SetFbxParameter()
        #     pm.select()

    def displayErrorInfo(self):
        if self.error_list:
            msg = "\n".join(self.error_list)
            QtWidgets.QMessageBox.warning(self,"警告",msg)

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

qt_resource_data = b"\
\x00\x00\x03\x04\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x20\x00\x00\x00\x20\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\
\x00\x00\x02\xcb\x49\x44\x41\x54\x58\x47\xed\x56\x4b\x68\x13\x51\
\x14\x3d\x67\x92\xfe\xcc\x8c\xd6\x96\x24\x15\xdc\xb5\x98\xa6\x20\
\xf4\xe7\x42\x11\x5a\x0a\x52\xd0\xaa\x6d\xc5\xad\xe0\x42\x41\x70\
\x51\xc5\x95\x28\x82\x82\xbb\x52\x41\x14\x45\x77\xee\x0a\x62\xa5\
\xf8\x59\xb8\x13\xdd\xb4\x88\x45\x93\x34\x6e\xec\x46\x30\x99\xba\
\x69\x32\xf1\xd3\xcc\x5c\x49\x74\xea\x98\x34\x26\x69\xa2\x45\xe8\
\xec\xe6\xcd\xbb\xf7\x9c\x7b\xee\x67\x2e\xb1\xce\x0f\xd7\x19\x1f\
\x2b\x04\xbe\xc4\xda\x5a\xd3\xa8\x7d\x01\xca\x9c\x07\xca\x11\xfa\
\x42\xc9\x72\xc8\x25\xf5\xe0\x98\x58\xbc\x48\x05\x57\x55\x6f\x78\
\xbc\x54\xdb\x15\x02\x86\xde\xde\x23\xa2\xcc\xfe\x34\x9c\xf1\x80\
\x03\x4e\x12\x89\x58\xc7\x14\x89\xc3\x10\x59\x00\x95\x11\xd5\x17\
\x7a\x6d\x83\x64\xc0\x21\x9c\xc8\xbe\x8b\xdc\x53\xfd\x91\x63\x65\
\x13\xc8\x18\x24\xe3\xc1\x09\x80\x63\xb9\x24\x7e\x03\xc8\x62\xe0\
\xa1\xe6\x0f\x0f\x67\x6d\x1c\xe0\x02\x89\xaa\xf5\xe6\x5e\x6e\x7e\
\xb7\xb8\x26\x02\x85\x48\x24\x45\xce\x91\xb8\xe4\x70\x3a\xa7\xfa\
\xc2\x9d\x95\x82\x67\xfc\xad\x5a\x84\x79\x4a\x28\x4b\x23\x49\x4b\
\x0b\x11\xdc\xf2\x83\x84\x75\x1c\x64\xa3\x2d\xfb\x5a\x22\xb7\x83\
\x29\xd8\x05\xb9\x24\xc8\xe5\xcb\x69\x28\x6d\x0a\xe4\xa3\x22\xae\
\x36\x01\xaf\x64\x53\xbe\x06\xd9\x9d\xe9\xf9\x63\x1b\xe6\x90\xc8\
\x4b\x6b\xa5\xe0\x05\x53\xe0\x44\x4a\xe8\xc1\x9b\x14\x9e\xca\x47\
\x97\x05\x4f\x83\xb9\xab\x9c\x82\x5b\xad\x30\x8b\x0e\x22\x43\x6f\
\x1f\x12\x51\xa6\x73\x8d\x45\x64\x4a\xf3\x47\x46\x8c\xc5\xe0\xb0\
\x98\xb8\x86\x1a\x39\xa8\x36\xcd\xbf\xb1\xef\x19\x7a\xa0\xd7\x52\
\xdc\x29\xad\x39\x14\xfe\x75\x16\x3c\x20\x82\x3b\x70\xcb\xa0\x7d\
\xb7\x72\x02\x7a\xa0\x57\xc4\xf5\x52\x80\x24\xdd\x56\x5f\xc6\x71\
\x22\xde\x71\x94\xc0\x24\x80\x34\x69\xee\xf6\x78\xa3\xb3\x89\xc5\
\xc0\x00\x4d\xd7\x13\x21\x0c\x77\xad\xd9\xd3\xd0\x18\x7d\x5f\x52\
\x0a\x8a\x29\x90\x6d\xdd\x58\x70\x1f\x80\x69\x21\x53\xb5\x4a\x7a\
\xcf\xb2\xe9\x3a\x09\xf2\x4c\x36\x72\xca\x59\x97\x28\x33\xa6\x58\
\xcf\x32\xdf\x09\x0e\x38\x87\x58\xc5\x0a\xd8\xf2\x26\xf4\xf6\x7e\
\x5a\x7c\x2a\xc0\x52\x5d\xbd\x39\xf4\xed\xab\xeb\x16\x80\x16\x12\
\x27\xc4\xe2\xa4\x40\x52\x70\xb3\x5f\x6b\x0e\x87\x4a\xee\x82\xcc\
\xc5\x52\x14\xc8\x21\xf1\x58\x00\x03\x84\x0d\xd4\x4d\x61\xca\xad\
\x98\x7d\xf5\xde\x68\x34\xb7\x96\xaa\xa6\x80\xed\x38\x15\x6b\x1f\
\xb5\xa8\xdc\x77\x02\x89\x5b\x76\x6a\x4d\x91\xb7\x7f\xa5\x0b\x72\
\x9d\x1a\xf1\x8e\x2e\x01\x5e\x39\xcf\x3d\xd6\x27\x95\x2d\x31\xe3\
\xff\x27\x20\x82\xdb\xa4\x1c\x02\xb8\xcd\x9e\x03\xff\x54\x01\x02\
\xdd\x02\xb9\x0b\xb0\x7b\x83\x40\x71\x05\xe4\x83\x80\x9b\x08\x6c\
\xad\x5a\x11\x96\x93\x02\x02\xd7\x05\xd8\x01\x60\x70\x83\xc0\x86\
\x02\xff\xb9\x02\xf1\xe0\x7e\x01\x1f\x65\x27\x9e\xa4\x3b\x41\x57\
\x66\x10\xf5\x8a\xc8\x03\xcd\x1f\x19\x2d\x34\x09\xab\xd6\x05\x89\
\x44\xab\x0f\x9f\xeb\xe6\x09\x24\x3d\xde\xa5\x40\x52\x57\x2f\x10\
\xca\x79\x81\x9c\xd6\x7c\x91\x1b\xf9\xab\xda\xf6\x06\x43\xd7\x9e\
\x83\x32\x0e\x8b\x35\x99\xc5\x44\xf5\x85\xbb\x56\xfb\x11\x95\xb4\
\x11\x15\x32\xac\xd6\x79\xd1\x7d\xa0\x5a\x40\x85\xfc\x7c\x07\x7d\
\x1e\x60\x3f\x65\xda\x7d\x4e\x00\x00\x00\x00\x49\x45\x4e\x44\xae\
\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x15\
\x02\xc7\xd3\x07\
\x00\x48\
\x00\x49\x00\x4b\x00\x5f\x00\x52\x00\x65\x00\x74\x00\x61\x00\x72\x00\x67\x00\x65\x00\x74\x00\x5f\x00\x54\x00\x6f\x00\x6f\x00\x6c\
\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x72\x3c\x77\xbc\x3f\
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

qInitResources()

def onMayaDroppedPythonFile(*args):
    qInitResources()
    parentTab = mel.eval('''global string $gShelfTopLevel;string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;''')
    module,ext = os.path.splitext(os.path.basename(__file__))
    pm.shelfButton( commandRepeatable = True, image1 = "HIK_Retarget_Tool.png",iol = "HIK" ,label = "Fight Export Window", parent = parentTab, command = dedent("""
        import {module}
        reload({module})
        from {module} import HIKBatchRetargetWin
        try:
            HIKBatchRetargetWin_UI = HIKBatchRetargetWin()
            HIKBatchRetargetWin_UI.mayaShow()
        except :
            import traceback
            traceback.print_exc()
        
    """.format(module=module)))
    
    # NOTE 构建 Mod
    createModFolder(module)

    try:
        HIKBatchRetargetWin_UI = HIKBatchRetargetWin()
        HIKBatchRetargetWin_UI.mayaShow()
    except :
        import traceback
        traceback.print_exc()

def createModFolder(module):

    MAYA_APP_DIR = os.environ["MAYA_APP_DIR"]
    folder_name = module+"Mod"
    
    # NOTE 构建 Mod 
    mod_path = os.path.join(MAYA_APP_DIR,folder_name)
    shutil.rmtree(mod_path) if os.path.exists(mod_path) else None
    os.mkdir(mod_path)
    
    scripts = os.path.join(mod_path,"scripts")
    os.mkdir(scripts) if not os.path.exists(scripts) else None
    userSetup = os.path.join(scripts,"userSetup.py")
    with open(userSetup,'w') as f:
        f.write(dedent('''
            import {module}
            {module}.qInitResources()
        '''.format(module=module)))
    
    DIR = os.path.dirname(__file__)
    sys.path.insert(0,DIR) if DIR not in sys.path else None
    shutil.copy(os.path.join(DIR,"%s.py" % module),os.path.join(scripts,"%s.py" % module))

    mod = os.path.join(MAYA_APP_DIR,"modules",folder_name + ".mod")
    with open(mod,'w') as f:
        f.write(dedent('''
        + MAYAVERSION:2014 {module} 1.1.0 {path}
        + MAYAVERSION:2015 {module} 1.1.0 {path}
        + MAYAVERSION:2016 {module} 1.1.0 {path}
        + MAYAVERSION:2017 {module} 1.1.0 {path}
        + MAYAVERSION:2018 {module} 1.1.0 {path}
        + MAYAVERSION:2019 {module} 1.1.0 {path}
        + MAYAVERSION:2020 {module} 1.1.0 {path}
        + MAYAVERSION:2021 {module} 1.1.0 {path}
        + MAYAVERSION:2022 {module} 1.1.0 {path}
        '''.format(path=mod_path,module=module)))

if __name__ == "__main__":
    try:
        HIKBatchRetargetWin_UI = HIKBatchRetargetWin()
        HIKBatchRetargetWin_UI.mayaShow()
    except :
        import traceback
        traceback.print_exc()

# import sys
# MODULE = r"F:\MayaTecent\MayaScript\rig"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import flimSkin2GameSkin
# reload(flimSkin2GameSkin)
# from flimSkin2GameSkin import HIKBatchRetargetWin
# HIKBatchRetargetWin_UI = HIKBatchRetargetWin()
# HIKBatchRetargetWin_UI.mayaShow()