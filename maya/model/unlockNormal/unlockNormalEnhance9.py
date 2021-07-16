# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 15:30:31'

"""
完美解决 FBX 法线解锁 丢失问题
"""
import sys
import time
import pymel.core as pm
import maya.api.OpenMaya as om
from maya import OpenMaya
from maya import OpenMayaUI


from Qt import QtCore, QtGui, QtWidgets
from Qt.QtCompat import wrapInstance

class EdgeError(Exception):
    pass

def errorLog(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except EdgeError:
            pass
        except:
            import traceback
            err = traceback.format_exc()
            msg = u"运行出错，请联系 timmyliang\n%s" % err
            QtWidgets.QMessageBox.warning(QtWidgets.QApplication.activeWindow(),u"警告",msg)
        finally:
            pm.progressWindow(ep=1)

    return wrapper

def unlockNormal(sel,thersold=0.05):

    smooth_list = set()
    edit_list = set()
    
    # # NOTE 执行一个 mesh 命令 - 更新模型数据 避免获取的法线数据不对
    # pm.polyConnectComponents(sel,ch=0)

    # NOTE OpenMaya 加速遍历过程 
    sel_list = om.MSelectionList()
    sel_list.add(sel.fullPathName())
    dagPath = sel_list.getDagPath(0)
    
    # NOTE 获取 mesh 所有的法线信息
    mesh_normal = {}
    itr = om.MItMeshFaceVertex(dagPath)
    while not itr.isDone():
        face_id = itr.faceId()
        vert_id = itr.vertexId()
        normal  = itr.getNormal()

        if not mesh_normal.has_key(vert_id):
            mesh_normal[vert_id] = {}
        mesh_normal[vert_id][face_id] = normal
        itr.next()
    
    pm.progressWindow(	
        title='Unlock normal' ,
        progress=0.0,
        status='%s - colleting data...' % dagPath.fullPathName(),
        isInterruptable=True )
        
    mesh = om.MFnMesh(dagPath)
    face_itr = om.MItMeshPolygon(dagPath)
    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    while not edge_itr.isDone():

        if edge_itr.onBoundary():
            edge_itr.next()
            continue
        
        edge_id = edge_itr.index()

        if pm.progressWindow( query=True, isCancelled=True ) :
            pm.progressWindow(endProgress=1)
            return
        amount = float(edge_id)/edge_itr.count()*100
        pm.progressWindow( e=1, progress=amount)

        smooth_flag = 0
        for i in range(2):
            vert_id = edge_itr.vertexId(i)
     
            face_list = edge_itr.getConnectedFaces()

            if len(face_list) != 2:
                edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_id)
                print edge
                msg = u"模型的边存在同时连接三个面\n边序号为 : %s" % edge
                QtWidgets.QMessageBox.warning(QtWidgets.QApplication.activeWindow(),u"警告",msg)
                raise EdgeError(msg)
            
            face_1,face_2 = face_list

            normal_1 = mesh_normal[vert_id][face_1]
            normal_2 = mesh_normal[vert_id][face_2]

            # NOTE 法线不分叉 说明是 软边边
            if normal_1 == normal_2:
                vert_itr.setIndex(vert_id)

                vert_avg_normal = om.MVector(0.0, 0.0, 0.0)
                edge_avg_normal = om.MVector(0.0, 0.0, 0.0)
                vtx_face_list = vert_itr.getConnectedFaces()
                for face in vtx_face_list:
                    face_itr.setIndex(face)
                    normal = face_itr.getNormal()

                    if face in face_list:
                        edge_avg_normal += normal

                    vert_avg_normal += normal
                vert_avg_normal = vert_avg_normal/len(vtx_face_list)
                edge_avg_normal = edge_avg_normal/2

                
                vert_avg_1 = (vert_avg_normal - normal_1).length()
                vert_avg_2 = (vert_avg_normal - normal_2).length()
                edge_avg_1 = (edge_avg_normal - normal_1).length()
                edge_avg_2 = (edge_avg_normal - normal_2).length()
                # NOTE 判断顶点是否近似 average 
                if (vert_avg_1 < thersold and vert_avg_2 < thersold)\
                or (edge_avg_1 < thersold and edge_avg_2 < thersold):
                    smooth_flag += 1
                # NOTE 特殊调整的且统一的法线
                else:
                    edit_list.add(vert_id)
            else:
                # NOTE 硬边或特殊调整的法线
                edit_list.add(vert_id)
                break


        # NOTE smooth_flag 1 为 1个点 smooth
        # NOTE smooth_flag 2 为 2个点 smooth
        if smooth_flag >= 1:
            edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_id)
            smooth_list.add(edge)
            
        edge_itr.next()
    
    # NOTE 获取特殊法线要修改的数据
    pm.progressWindow( e=1, progress=0.0,status='%s - get edited normal...'  % dagPath.fullPathName())
    normal_list = []
    face_list = []
    vtx_list = []
    print "edit_list",edit_list
    for i,vert_id in enumerate(edit_list):

        if pm.progressWindow( query=True, isCancelled=True ) :
            pm.progressWindow(endProgress=1)
            return
        amount = float(i)/len(edit_list)*100
        pm.progressWindow( e=1, progress=amount)

        for face_id,normal in mesh_normal[vert_id].items():
            normal_list.append(normal)
            face_list.append(face_id)
            vtx_list.append(vert_id)

    pm.progressWindow( e=1, progress=0.0,status='%s - modify normal...' % dagPath.fullPathName())
    # NOTE 解锁法线
    pm.polyNormalPerVertex(sel,ufn=1)
    pm.progressWindow( e=1, progress=10)
    # NOTE 批量设置法线
    mesh.setFaceVertexNormals(normal_list,face_list,vtx_list)
    pm.progressWindow( e=1, progress=70)

    if smooth_list:
        pm.polySoftEdge(smooth_list,a=180,ch=0)

    pm.progressWindow(endProgress=1)

    # pm.select(["%s.e[%s]" % (dagPath.fullPathName(),vtx) for vtx in edit_list],add=1)

@errorLog
def normalUnlocker(thersold=0.05):
    curr = time.time()
    pm.undoInfo(ock=1)
    for sel in pm.ls(sl=1,dag=1,ni=1,type="mesh"):
        unlockNormal(sel,thersold=thersold)
    pm.undoInfo(cck=1)
    print "elapsed time : %s s" % (time.time() - curr)


class NormalUnlockerUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(474, 217)
        Form.setStyleSheet("font: bold 18pt \"Microsoft YaHei\";")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Help_Label = QtWidgets.QLabel(Form)
        self.Help_Label.setObjectName("Help_Label")
        self.verticalLayout.addWidget(self.Help_Label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Slider = QtWidgets.QSlider(Form)
        self.Slider.setMaximum(100)
        self.Slider.setSingleStep(1)
        self.Slider.setPageStep(10)
        self.Slider.setProperty("value", 5)
        self.Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Slider.setObjectName("Slider")
        self.horizontalLayout.addWidget(self.Slider)
        self.SP = QtWidgets.QDoubleSpinBox(Form)
        self.SP.setFrame(False)
        self.SP.setProperty("value", 0.05)
        self.SP.setObjectName("SP")
        self.SP.setMaximum(1)
        self.SP.setSingleStep(0.01)
        self.horizontalLayout.addWidget(self.SP)
        self.Unlock_BTN = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(18)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.Unlock_BTN.setFont(font)
        self.Unlock_BTN.setObjectName("Unlock_BTN")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(u"Maya 解锁法线")
        self.Help_Label.setText(u"<html><head/><body><p align=\"center\">使用帮助</p><p align=\"center\"><span style=\" font-size:16pt;\">解锁阈值越大,锁定区域就越少,法线解锁越不准确</span></p><p align=\"center\"><span style=\" font-size:16pt;\">解锁阈值越小,锁定区域就越多,推荐用默认值0.05</span></p></body></html>")
        self.label.setText(u"解锁阈值")
        self.Unlock_BTN.setText(u"解锁法线")

class NormalUnlockerWin(QtWidgets.QWidget,NormalUnlockerUI):
    def __init__(self,*args, **kwargs):
        super(NormalUnlockerWin,self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.spliter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.container.setLayout(layout)

        layout.addLayout(self.horizontalLayout)
        layout.addWidget(self.Unlock_BTN)

        self.spliter.addWidget(self.Help_Label)
        self.spliter.addWidget(self.container)

        self.verticalLayout.addWidget(self.spliter)

        self.Slider.valueChanged.connect(lambda v: self.SP.setValue(float(v)/100))
        self.SP.valueChanged.connect(lambda v: self.Slider.setValue(v*100))
        self.Unlock_BTN.clicked.connect(lambda:normalUnlocker(self.SP.value()))
    
    def mayaShow(self,name="MF_NormalUnlocker"):
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
        MF_NormalUnlocker = NormalUnlockerWin()
        MF_NormalUnlocker.mayaShow()
    except :
        import traceback
        traceback.print_exc()
