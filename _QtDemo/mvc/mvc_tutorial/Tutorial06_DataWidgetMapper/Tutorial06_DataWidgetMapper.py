# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-01 22:42:43'

"""

"""

import os
DIR = os.path.dirname(__file__)

import sys
MODULE = os.path.join(DIR,"..","..","..","..","_vendor","Qt")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

import icons_rc

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyside2uic
import xml.etree.ElementTree as xml
from cStringIO import StringIO

def loadUiType(uiFile):
    """
    Pyside "loadUiType" command like PyQt4 has one, so we have to convert the 
    ui file to py code in-memory first and then execute it in a special frame
    to retrieve the form_class.
    """
    uiFile = os.path.join(DIR,uiFile) if not os.path.exists(uiFile) else uiFile
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        pyside2uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type
        # in the xml from designer
        form_class = frame['Ui_%s'%form_class]
        base_class = eval('%s'%widget_class)

    return form_class, base_class

class Node(QObject):
    
    def __init__(self, name, parent=None):
        
        super(Node, self).__init__()
        
        self._name = name
        self._children = []
        self._parent = parent
        
        if parent is not None:
            parent.addChild(self)


    def typeInfo(self):
        return "NODE"

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        
        if position < 0 or position > len(self._children):
            return False
        
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        
        if position < 0 or position > len(self._children):
            return False
        
        child = self._children.pop(position)
        child._parent = None

        return True


    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]
    
    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent
    
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)


    def log(self, tabLevel=-1):

        output     = ""
        tabLevel += 1
        
        for i in range(tabLevel):
            output += "\t"
        
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
        
        tabLevel -= 1
        output += "\n"
        
        return output

    def __repr__(self):
        return self.log()



class TransformNode(Node):
    
    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)

        self._x = 0
        self._y = 0
        self._z = 0

    def typeInfo(self):
        return "TRANSFORM"

    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z
    
    def setX(self, x):
        self._x = x
        
    def setY(self, y):
        self._y = y
        
    def setZ(self, z):
        self._z = z




class CameraNode(Node):
    
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
          
        self._motionBlur = True
        self._shakeIntensity = 50.0
                    
    def typeInfo(self):
        return "CAMERA"

    def motionBlur(self):
        return self._motionBlur

    def setMotionBlur(self, blur):
        self._motionBlur = blur

    def shakeIntensity(self):
        return self._shakeIntensity

    def setShakeIntensity(self, intensity):
        self._shakeIntensity = intensity
        
        
        

class LightNode(Node):
    
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

        self._lightIntensity = 1.0
        self._nearRange = 40.0
        self._farRange = 80.0
        self._castShadows = True

    def typeInfo(self):
        return "LIGHT"
    
    def lightIntensity(self):
        return self._lightIntensity
    
    def nearRange(self):
        return self._nearRange
    
    def farRange(self):
        return self._farRange
    
    def castShadows(self):
        return self._castShadows
    
    
    def setLightIntensity(self, intensity):
        self._lightIntensity = intensity
    
    def setNearRange(self, range):
        self._nearRange = range
    
    def setFarRange(self, range):
        self._farRange = range
    
    def setCastShadows(self, cast):
        self._castShadows = cast
    
    
    

class SceneGraphModel(QAbstractItemModel):
    
    
    sortRole   = Qt.UserRole
    filterRole = Qt.UserRole + 1
    
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root


    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 1
    

    
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        
        if not index.isValid():
            return None

        node = index.internalPointer()
        typeInfo = node.typeInfo()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return node.name()
            
            if index.column() == 1:
                return typeInfo

            if typeInfo == "CAMERA":
                if index.column() == 2:
                    return node.motionBlur()
                if index.column() == 3:
                    return node.shakeIntensity()
       
            if typeInfo == "LIGHT":
                if index.column() == 2:
                    return node.lightIntensity()
                if index.column() == 3:
                    return node.nearRange()
                if index.column() == 4:
                    return node.farRange()
                if index.column() == 5:
                    return node.castShadows()
                
            if typeInfo == "TRANSFORM":
                if index.column() == 2:
                    return node.x()
                if index.column() == 3:
                    return node.y()
                if index.column() == 4:
                    return node.z()
                
        
        if role == Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()
                
                if typeInfo == "LIGHT":
                    return QIcon(QPixmap(":/Light.png"))
                
                if typeInfo == "TRANSFORM":
                    return QIcon(QPixmap(":/Transform.png"))
                
                if typeInfo == "CAMERA":
                    return QIcon(QPixmap(":/Camera.png"))

        
        if role == SceneGraphModel.sortRole:
            return node.typeInfo()

        if role == SceneGraphModel.filterRole:
            return node.typeInfo()


    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=Qt.EditRole):

        if index.isValid():
            
            node = index.internalPointer()
            typeInfo = node.typeInfo()
            
            if role == Qt.EditRole:
                
                
                if index.column() == 0:
                    node.setName(value)
                    
                    
                if typeInfo == "CAMERA":
                    if index.column() == 2:
                        node.setMotionBlur(value)
                    if index.column() == 3:
                        node.setShakeIntensity(value)
           
                if typeInfo == "LIGHT":
                    if index.column() == 2:
                        node.setLightIntensity(value)
                    if index.column() == 3:
                        node.setNearRange(value)
                    if index.column() == 4:
                        node.setFarRange(value)
                    if index.column() == 5:
                        node.setCastShadows(value)
                    
                if typeInfo == "TRANSFORM":
                    if index.column() == 2:
                        node.setX(value)
                    if index.column() == 3:
                        node.setY(value)
                    if index.column() == 4:
                        node.setZ(value)
                    


                self.dataChanged.emit(index, index)
                return True
            
        return False

    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"

        
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):
        
        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)


        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()



    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    
    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QModelIndex()):
        
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success
    
    def insertLights(self, position, rows, parent=QModelIndex()):
        
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = LightNode("light" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success

    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QModelIndex()):
        
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            success = parentNode.removeChild(position)
            
        self.endRemoveRows()
        
        return success



base, form = loadUiType("Tutorial06.ui")

class WndTutorial06(base, form):
    
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        rootNode   = Node("hips")
        childNode0 = TransformNode("a",    rootNode)
        childNode1 = LightNode("b",        rootNode)
        childNode2 = CameraNode("c",       rootNode)
        childNode3 = TransformNode("d",    rootNode)
        childNode4 = LightNode("e",        rootNode)
        childNode5 = CameraNode("f",       rootNode)
        childNode6 = TransformNode("g",    childNode5)
        childNode7 = LightNode("h",        childNode6)
        childNode8 = CameraNode("i",       childNode7)
       
        
        self._proxyModel = QSortFilterProxyModel(self)
        
        """VIEW <------> PROXY MODEL <------> DATA MODEL"""

        self._model = SceneGraphModel(rootNode, self)
        

        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        self._proxyModel.setFilterRole(SceneGraphModel.filterRole)
        self._proxyModel.setFilterKeyColumn(0)
        
        self.uiTree.setModel(self._proxyModel)
        
        QObject.connect(self.uiFilter, SIGNAL("textChanged(QString)"), self._proxyModel.setFilterRegExp)
        
        self.uiTree.setSortingEnabled(True)

        

        
        self._propEditor = PropertiesEditor(self)
        self.layoutMain.addWidget(self._propEditor)
        
        self._propEditor.setModel(self._proxyModel)
        
        

        
        QObject.connect(self.uiTree.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self._propEditor.setSelection)



propBase, propForm = loadUiType("Tutorial06_Properties.ui")
nodeBase, nodeForm = loadUiType("Tutorial06_NodeProperties.ui") 
lightBase, lightForm = loadUiType("Tutorial06_LightProperties.ui")
cameraBase, cameraForm = loadUiType("Tutorial06_CameraProperties.ui")
transformBase, transformForm = loadUiType("Tutorial06_TransformProperties.ui")


"""PROPERTIESEDITOR"""
class PropertiesEditor(propBase, propForm):
    
    def __init__(self, parent = None):
        super(propBase, self).__init__(parent)
        self.setupUi(self)

        self._proxyModel = None

        self._nodeEditor = NodeEditor(self)
        self._lightEditor = LightEditor(self)
        self._cameraEditor = CameraEditor(self)
        self._transformEditor = TransformEditor(self)

        
        self.layoutNode.addWidget(self._nodeEditor)
        self.layoutSpecs.addWidget(self._lightEditor)
        self.layoutSpecs.addWidget(self._cameraEditor)
        self.layoutSpecs.addWidget(self._transformEditor)

        self._lightEditor.setVisible(False)
        self._cameraEditor.setVisible(False)
        self._transformEditor.setVisible(False)
               
    """INPUTS: QModelIndex, QModelIndex"""
    def setSelection(self, current, old):

        current = self._proxyModel.mapToSource(current)

        node = current.internalPointer()
        
        if node is not None:
            
            typeInfo = node.typeInfo()
            
        if typeInfo == "CAMERA":
            self._cameraEditor.setVisible(True)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)
        
        elif typeInfo == "LIGHT":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(True)
            self._transformEditor.setVisible(False)
             
        elif typeInfo == "TRANSFORM":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(True)
        else:
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)

        self._nodeEditor.setSelection(current)
        self._cameraEditor.setSelection(current)
        self._lightEditor.setSelection(current)
        self._transformEditor.setSelection(current)
        


        
    
    
    def setModel(self, proxyModel):
        
        self._proxyModel = proxyModel
        
        self._nodeEditor.setModel(proxyModel)
        self._lightEditor.setModel(proxyModel)
        self._cameraEditor.setModel(proxyModel)
        self._transformEditor.setModel(proxyModel)


"""NODE"""
class NodeEditor(nodeBase, nodeForm):
    
    def __init__(self, parent=None):
        super(nodeBase, self).__init__(parent)
        self.setupUi(self)
        
        self._dataMapper = QDataWidgetMapper()
        
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiName, 0)
        self._dataMapper.addMapping(self.uiType, 1)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        


"""LIGHT"""
class LightEditor(lightBase, lightForm):
    
    def __init__(self, parent=None):
        super(lightBase, self).__init__(parent)
        self.setupUi(self)
        
        self._dataMapper = QDataWidgetMapper()
        

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiLightIntensity, 2)
        self._dataMapper.addMapping(self.uiNear, 3)
        self._dataMapper.addMapping(self.uiFar, 4)
        self._dataMapper.addMapping(self.uiShadows, 5)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        
        
"""CAMERA"""
class CameraEditor(cameraBase, cameraForm):
    
    def __init__(self, parent=None):
        super(cameraBase, self).__init__(parent)
        self.setupUi(self)
        
        self._dataMapper = QDataWidgetMapper()
        
        
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiMotionBlur, 2)
        self._dataMapper.addMapping(self.uiShakeIntensity, 3)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        
"""TRANSFORM"""
class TransformEditor(transformBase, transformForm):
    
    def __init__(self, parent=None):
        super(transformBase, self).__init__(parent)
        self.setupUi(self)

        self._dataMapper = QDataWidgetMapper()
        
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiX, 2)
        self._dataMapper.addMapping(self.uiY, 3)
        self._dataMapper.addMapping(self.uiZ, 4)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle("cleanlooks")
    
    wnd = WndTutorial06()
    wnd.show()

    sys.exit(app.exec_())