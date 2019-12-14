# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 08:49:49'

u"""
批量切分FBX动画
"""

import os
import re
import json
import webbrowser
from functools import partial
from collections import OrderedDict

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from Qt.QtCompat import loadUi
from Qt.QtCompat import QFileDialog
from Qt.QtCompat import wrapInstance

from maya import cmds
from maya import OpenMayaUI
from maya import mel

from AnimSpliterItem import AnimSpliterItem
from ExtendedComboBox import ExtendedCombo


REMOTE = r"\\10.125.42.47\KoProjecct\hzw\AnimSpliter"

class AnimSpliterWindow(QtWidgets.QWidget):
    """
    AnimSpliterWindow 摄像机设置界面的摄像机Item
    """
    def __init__(self):
        super(AnimSpliterWindow,self).__init__()

        self.setting = OrderedDict()

        DIR = os.path.dirname(__file__)
        ui_file = os.path.join(DIR,"ui","main.ui")
        loadUi(ui_file,self)

        self.Create_BTN.clicked.connect(self.addItem)
        self.Clear_BTN.clicked.connect(self.clearItem)
        self.Output_BTN.clicked.connect(self.output)
        
        self.menu = QtWidgets.QMenuBar(self)
        self.edit_menu = self.menu.addMenu(u'编辑')
        self.import_json_action = QtWidgets.QAction(u'导入设置', self)    
        self.export_json_action = QtWidgets.QAction(u'导出设置', self)  

        self.edit_menu.addAction(self.import_json_action)
        self.edit_menu.addAction(self.export_json_action)

        # NOTE 添加下拉菜单的功能触发
        self.import_json_action.triggered.connect(self.importJsonSetting)
        self.export_json_action.triggered.connect(self.exportJsonSetting)

        INSTRUNCTION_PATH = "file:///%s" % os.path.join(DIR,"instruction","README.html")
        help_menu = self.menu.addMenu(u'帮助')
        help_action = QtWidgets.QAction(u'使用帮助', self)    
        help_menu.addAction(help_action)
        help_action.triggered.connect(lambda:webbrowser.open_new_tab(INSTRUNCTION_PATH))

        self.Character_Combo = self.replaceWidget(self.Character_Combo,ExtendedCombo())
        self.Character_Combo.currentIndexChanged.connect(self.loadConfig)

        self.loadCombo()
        
        self.Save_BTN.clicked.connect(self.createNewConfig)
        self.Delete_BTN.clicked.connect(self.deleteConfig)

        self.setStyleSheet('font-family: Microsoft YaHei UI;')

    def deleteConfig(self):
        
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("删除确认")
        msgBox.setText("你确定要删除当前配置吗？")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)

        ret = msgBox.exec_()

        if ret == QtWidgets.QMessageBox.Cancel:
            return

        config_file = self.getCurrentConfigPath()
    
        if os.path.exists(config_file):
            directory = os.path.dirname(config_file)
            files = os.listdir(directory)
            os.remove(config_file)
            if len(files)<=1:
                os.rmdir(directory)

        self.loadCombo("refresh")


    def loadCombo(self,config_file=""):
        self.Character_Combo.clear()
        if not config_file:
            config_file = self.currentConfig()

        index = -1
        _index = 0
        for root, _, files in os.walk(REMOTE, topdown=False):
            for name in files:
                _index += 1
                label,_ = os.path.splitext(name)
                folder = os.path.basename(root)
                self.Character_Combo.addItem(folder + " | " + label)

                path = os.path.join(root,name)
                if config_file == path:
                    index = _index

        if index != -1:
            self.Character_Combo.setCurrentIndex(index-1)
    
    def getCurrentConfigPath(self):
        text = self.Character_Combo.currentText()
        if not text:
            return
        folder,name = text.split(" | ")
        return os.path.join(REMOTE,folder,name+".json")
        
    def currentConfig(self):

        file_name = cmds.file(q=1,sn=1)
        search = re.search(r"Characters(?:/|\\)(.*?)(?:/|\\)Animations",file_name)
        if not search:
            return
            # folder = "other"
        folder = search.group(1)
        
        folder = os.path.join(REMOTE,folder)

        _,file_name = os.path.split(file_name)
        file_name = file_name.rpartition(".")[0] + ".json"

        config_file = os.path.join(folder,file_name)
        self.createConfig(config_file)
        return config_file
    
    def createConfig(self,config_file=None):
        if not os.path.exists(config_file):
            folder = os.path.dirname(config_file)
            if not os.path.exists(folder):
                os.mkdir(folder)
            with open(config_file,'w') as f:
                f.write("{}")
            return True
        else:
            return False

    def createNewConfig(self):
        
        config_file = self.currentConfig()
        root,text = os.path.split(config_file)
        text,_ = os.path.splitext(text)
        text,OK = QtWidgets.QInputDialog.getText(self, u"创建新配置",u"配置名称",text=text)

        if not OK:
            return

        config_file = os.path.join(root,text+".json")
        if os.path.exists(config_file):
            QtWidgets.QMessageBox.warning(self, u"警告",u"当前配置名称已存在")
            return
        
        self.createConfig(config_file)
        self.loadCombo(config_file)

    def loadConfig(self,index):
        config_file = self.getCurrentConfigPath()
        if config_file:
            self.importJsonSetting(config_file)


    def replaceWidget(self,src,dst):
        
        self.updateWidgetState(src,dst)
        layout = src.parent().layout()
        layout,index = self.getTargetLayoutIndex(layout,src)
        layout.insertWidget(index,dst)
        src.setParent(None)
        
        return dst

    def updateWidgetState(self,src,dst):
        """updateWidgetState 同步组件状态
        
        Parameters
        ----------
        src : QWidget
            源组件
        dst : QWidget
            目标组件
        """
        dst.setAcceptDrops(src.acceptDrops())
        dst.setAccessibleDescription(src.accessibleDescription())
        dst.setBackgroundRole(src.backgroundRole())
        dst.setBaseSize(src.baseSize())
        dst.setContentsMargins(src.contentsMargins())
        dst.setContextMenuPolicy(src.contextMenuPolicy())
        dst.setCursor(src.cursor())
        dst.setFocusPolicy(src.focusPolicy())
        dst.setFocusProxy(src.focusProxy())
        dst.setFont(src.font())
        dst.setForegroundRole(src.foregroundRole())
        dst.setGeometry(src.geometry())
        dst.setInputMethodHints(src.inputMethodHints())
        dst.setLayout(src.layout())
        dst.setLayoutDirection(src.layoutDirection())
        dst.setLocale(src.locale())
        dst.setMask(src.mask())
        dst.setMaximumSize(src.maximumSize())
        dst.setMinimumSize(src.minimumSize())
        dst.setMouseTracking(src.hasMouseTracking ())
        dst.setPalette(src.palette())
        dst.setParent(src.parent())
        dst.setSizeIncrement(src.sizeIncrement())
        dst.setSizePolicy(src.sizePolicy())
        dst.setStatusTip(src.statusTip())
        dst.setStyle(src.style())
        dst.setToolTip(src.toolTip())
        dst.setUpdatesEnabled(src.updatesEnabled())
        dst.setWhatsThis(src.whatsThis())
        dst.setWindowFilePath(src.windowFilePath())
        dst.setWindowFlags(src.windowFlags())
        dst.setWindowIcon(src.windowIcon())
        dst.setWindowIconText(src.windowIconText())
        dst.setWindowModality(src.windowModality())
        dst.setWindowOpacity(src.windowOpacity())
        dst.setWindowRole(src.windowRole())
        dst.setWindowState(src.windowState())


    def getTargetLayoutIndex(self,layout,target):
        count = layout.count()
        for i in range(count):
            item = layout.itemAt(i).widget()
            if item == target:
                return layout,i
        else:
            for child in layout.children():
                layout,i = self.getTargetLayoutIndex(child,target)
                if layout:
                    return layout,i
            return [None,None]

    def refresh(self):
        self.clearItem(False)
        layout = self.Scroll_Widget.layout()
        for index,data in self.setting.items():
            start = data["start"]
            end = data["end"]
            item = AnimSpliterItem(paernt=self,index=index,start=start,end=end)
            count = layout.count()
            layout.insertWidget(count-1,item)

    def importJsonSetting(self,path=None):
        """
        importJsonSetting 导入Json
        
        Keyword Arguments:
            path {str} -- 导入路径 为空则弹出选择窗口获取 (default: {None})
        """
        if not path:
            path,_ = QFileDialog.getOpenFileName(self, caption=u"获取设置",filter= u"json (*.json)")
            if not path:return
        # NOTE 如果文件不存在则返回空
        if not os.path.exists(path):return

        with open(path,'r') as f:
            self.setting = json.load(f,encoding="utf-8",object_pairs_hook=OrderedDict)
        
        # NOTE 更新面板内容
        self.refresh()

    def exportJsonSetting(self,path=None):
        """
        exportJsonSetting 导出Json
        
        Keyword Arguments:
            path {str} -- 导出路径 为空则弹出选择窗口获取 (default: {None})
        """
        if not path:
            path,_ = QFileDialog.getSaveFileName(self, caption=u"输出设置",filter= u"json (*.json)")
            if not path:return
            
        with open(path,'w') as f:
            json.dump(self.setting,f,indent=4)


    def output(self,directory=""):

        output_directory = directory if directory else QtWidgets.QFileDialog.getExistingDirectory(self)

        if not output_directory:
            return
        
        fail_list = []
        layout = self.Scroll_Widget.layout()
        count = layout.count()
        scene = cmds.file(q=1,sn=1)
        # NOTE 开启关键帧烘焙
        mel.eval('FBXExportBakeComplexAnimation -v true')
        for i in range(count-1):
            item = layout.itemAt(i).widget()
            if not item.previewCheck():
                fail_list.append(i+1)
                continue
            start = self.setting[str(i+1)]["start"]
            end = self.setting[str(i+1)]["end"]
            mel.eval('FBXExportSplitAnimationIntoTakes -v "MF_FBXExport" %s %s'%(start,end))
            mel.eval('FBXExportBakeComplexStart -v %s' % start)
            mel.eval('FBXExportBakeComplexEnd -v %s' % end)

            if scene:
                name = "%s_%s_%s"%(scene,start,end)
            else:
                name = "%s_%s"%(start,end)

            path = os.path.join(output_directory,name)

            cmds.file(path,f=1,type="FBX export",pr=1,ea=1)
            mel.eval('FBXExportSplitAnimationIntoTakes -c')

                
        if fail_list:
            msg = "\n".join(fail_list)
            QtWidgets.QtWidgets.QMessageBox.warning(self, u"警告", u"下列序号起始时间和结束时间相等 - 跳过\n %s" % msg)

        

    def clearItem(self,save=True):
        layout = self.Scroll_Widget.layout()
        count = layout.count()
        for i in range(count-1):
            item = layout.itemAt(i).widget()
            item.deleteLater()
            if self.setting.has_key(str(i+1)) and save:
                del self.setting[str(i+1)]

        if save:
            config_path = self.getCurrentConfigPath()
            self.exportJsonSetting(config_path)

    def addItem(self):

        layout = self.Scroll_Widget.layout()
        count = layout.count()
        _item = layout.itemAt(count-2)
        if _item:
            start = int(_item.widget().End_SP.text())
        else:
            start = 0
        item = AnimSpliterItem(paernt=self,index=count,start=start+1,end=start+2)
        layout.insertWidget(count-1,item)

        self.setting[str(count)]={"start":start+1,"end":start+2}

        config_path = self.getCurrentConfigPath()
        self.exportJsonSetting(config_path)
    
    def mayaShow(self,name=u"MF_AnimSpliterWindow"):
        # NOTE 如果变量存在 就检查窗口多开
        if cmds.window(name,q=1,ex=1):
            cmds.deleteUI(name)
        window = cmds.window(name,title=self.windowTitle())
        cmds.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        ptr = self.mayaToQT(window)
        ptr.setLayout(QtWidgets.QVBoxLayout())
        ptr.layout().setContentsMargins(0,0,0,0)
        ptr.layout().addWidget(self)
        ptr.destroyed.connect(self._close)
        
    def _close(self):
        # NOTE 脱离要删除的窗口
        window = OpenMayaUI.MQtUtil.mainWindow()
        window = wrapInstance(long(window), QtWidgets.QMainWindow)
        self.setParent(window)
    
    def mayaToQT( self,name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )
    