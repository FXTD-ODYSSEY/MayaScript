import pymel.core as pm
import pymel.core.datatypes as dt
from maya import OpenMaya
from maya import OpenMayaUI

from Qt import QtCore, QtGui, QtWidgets
from Qt.QtCompat import wrapInstance

class AVG_Normal_UI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AVG_Normal_UI, self).__init__(parent)
        self.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Vertex_BTN = QtWidgets.QPushButton(self)
        self.Vertex_BTN.setObjectName("Vertex_BTN")
        self.Vertex_BTN2 = QtWidgets.QPushButton(self)
        self.Vertex_BTN2.setObjectName("Vertex_BTN2")
        self.verticalLayout.addWidget(self.Vertex_BTN)
        self.verticalLayout.addWidget(self.Vertex_BTN2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Ratio_Slider = QtWidgets.QSlider(self)
        self.Ratio_Slider.setMinimum(0)
        self.Ratio_Slider.setMaximum(100)
        self.Ratio_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Ratio_Slider.setObjectName("Ratio_Slider")
        self.horizontalLayout.addWidget(self.Ratio_Slider)
        self.Ration_SP = QtWidgets.QSpinBox(self)
        self.Ration_SP.setPrefix("")
        self.Ration_SP.setMaximum(100)
        self.Ration_SP.setObjectName("Ration_SP")
        self.horizontalLayout.addWidget(self.Ration_SP)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Normal_BTN = QtWidgets.QPushButton(self)
        self.Normal_BTN.setObjectName("Normal_BTN")
        self.verticalLayout.addWidget(self.Normal_BTN)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi()
        self.Ratio_Slider.valueChanged.connect(self.Ration_SP.setValue)
        self.Ration_SP.valueChanged.connect(self.Ratio_Slider.setValue)

        self.Vertex_BTN.clicked.connect(lambda:self.selectFaceVertex(False))
        self.Vertex_BTN2.clicked.connect(self.selectFaceVertex)
        self.Normal_BTN.clicked.connect(self.fixNormal)

    def retranslateUi(self):
        self.setWindowTitle(u"self")
        self.Vertex_BTN.setText(u"获取顶点相邻顶点")
        self.Vertex_BTN2.setText(u"顶点转面顶点")
        self.label.setText(u"ratio")
        self.Normal_BTN.setText(u"自动校正法线")

    def selectFaceVertex(self,face=False):
        # NOTE 获取当前选择的顶点
        vtx_list = [sel for sel in pm.ls(sl=1,fl=1) if type(sel) is pm.general.MeshVertex]
        mesh = sel.node()
        
        vtx_data = []
        for vtx in vtx_list:
            if vtx.node() is not mesh:
                QtWidgets.QMessageBox.warning(self,u"警告",u"请选择一个模型上的顶点")
                return
            vtx_pos = vtx.getPosition(space="world")
            
            # NOTE 生成 BoudingBox 来获取相邻的顶点
            vec = dt.Vector(0.1)
            min_pt = dt.Point.apicls(vtx_pos-vec)
            max_pt = dt.Point.apicls(vtx_pos+vec)
            bbox = dt.BoundingBox.apicls(min_pt,max_pt)

            vtx_data.append({'bbox':bbox,'vtx_list':{vtx.index()}})


        # NOTE 遍历所有的 bbox 获取相邻顶点
        itr = OpenMaya.MItMeshVertex(mesh.__apimdagpath__())
        idx_list = set()
        while not itr.isDone():
            idx = itr.index()

            if idx in vtx_data:
                itr.next()
                continue

            pt = itr.position(OpenMaya.MSpace.kWorld)
            
            for data in vtx_data:
                vtx_list = data['vtx_list']
                if idx in vtx_list:
                    continue
                bbox = data['bbox']
                if bbox.contains(pt):
                    vtx_list.add(idx)
                    break
            itr.next()

        if face:
            pm.select(["%s.vtxFace[%s]" % (mesh,idx) for idx in vtx_list])
        else:
            pm.select(["%s.vtx[%s]" % (mesh,idx) for idx in vtx_list])


    def getCamPos(self):
        # NOTE 获取当前摄像机
        cur_mp = None
        for mp in pm.getPanel(type="modelPanel"):
            if pm.modelEditor(mp, q=1, av=1):
                cur_mp = mp
                break
        cam = pm.modelEditor(cur_mp, q=1,cam=1)
        cam_pos = dt.Vector(pm.xform(cam,q=1,ws=1,t=1))
        return cam_pos

    def fixNormal(self):

        # NOTE 获取当前选择的顶点
        vtx_list = [sel for sel in pm.ls(sl=1,fl=1) if type(sel) is pm.general.MeshVertex]
        mesh = sel.node()

        vtx_data = []
        for vtx in vtx_list:
            
            # NOTE 获取朝向摄像机的向量
            vtx_pos = vtx.getPosition(space="world")
            toCam = self.getCamPos() - dt.Vector(vtx_pos)
            toCam.normalize()

            # NOTE 生成 BoudingBox 来获取相邻的顶点
            vec = dt.Vector(0.1)
            min_pt = dt.Point.apicls(vtx_pos-vec)
            max_pt = dt.Point.apicls(vtx_pos+vec)
            bbox = dt.BoundingBox.apicls(min_pt,max_pt)

            vtx_data.append({'toCam':toCam,'bbox':bbox,'vtx_list':{vtx.index()}})


        # NOTE 遍历所有的 bbox 获取相邻顶点
        itr = OpenMaya.MItMeshVertex(mesh.__apimdagpath__())
        idx_list = set()
        while not itr.isDone():
            idx = itr.index()

            if idx in vtx_data:
                itr.next()
                continue

            pt = itr.position(OpenMaya.MSpace.kWorld)
            
            for data in vtx_data:
                vtx_list = data['vtx_list']
                if idx in vtx_list:
                    continue
                bbox = data['bbox']
                if bbox.contains(pt):
                    vtx_list.add(idx)
                    break
            itr.next()

        ratio = 0.5
        for data in vtx_data:
            face_vtx_data = {}
            toCam = data['toCam']
            
            # NOTE 单个顶点平均化
            avg_set_list = set()
            for idx in data['vtx_list']:
                vtx = pm.PyNode("%s.vtx[%s]" % (mesh,idx))

                # NOTE 法线 ToFace
                pm.polySetToFaceNormal(vtx,su=True)
                N_data = {}
                for face in vtx.connectedFaces():
                    N = face.getNormal()
                    N.normalize()
                    N_data[face.index()] = N
                    
                avg_set_1 = set()
                avg_set_2 = set()
                for face_idx,normal in N_data.items():
                    if abs(normal.dot(N)) > ratio or abs(normal.dot(toCam)) < ratio:
                        avg_set_1.add("%s.vtxFace[%s][%s]" % (mesh,idx,face_idx))
                    else:
                        avg_set_2.add("%s.vtxFace[%s][%s]" % (mesh,idx,face_idx))

                if avg_set_1:
                    pm.polyAverageNormal(avg_set_1)
                if avg_set_2:
                    pm.polyAverageNormal(avg_set_2)

                avg_set_list.update(avg_set_2)

            pm.polyAverageNormal(avg_set_list)
            
    def mayaShow(self,name="MF_AVG_NORMAL"):
        # NOTE 如果变量存在 就检查窗口多开
        try:
            if pm.workspaceControl(name,q=1,ex=1):
                pm.deleteUI(name)
            window = pm.workspaceControl(name,label=self.windowTitle())
        except:
            if pm.window(name,q=1,ex=1):
                pm.deleteUI(name)
            window = pm.window(name,label=self.windowTitle())

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
        MF_NormalUnlocker = AVG_Normal_UI()
        MF_NormalUnlocker.mayaShow()
    except :
        import traceback
        traceback.print_exc()
