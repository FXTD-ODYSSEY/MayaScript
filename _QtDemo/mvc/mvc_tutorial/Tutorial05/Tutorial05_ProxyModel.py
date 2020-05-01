# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-01 22:46:39'

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

import pyside2uic
import xml.etree.ElementTree as xml
from cStringIO import StringIO

DIR = os.path.dirname(__file__)
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

class Node(object):
    
    def __init__(self, name, parent=None):
        
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
        
    def typeInfo(self):
        return "TRANSFORM"

class CameraNode(Node):
    
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
        
    def typeInfo(self):
        return "CAMERA"

class LightNode(Node):
    
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)
        
    def typeInfo(self):
        return "LIGHT"
    
    

class SceneGraphModel(QAbstractItemModel):
    
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

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return node.name()
            
        if role == Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()
                
                if typeInfo == "LIGHT":
                    return QIcon(QPixmap(":/Light.png"))
                
                if typeInfo == "TRANSFORM":
                    return QIcon(QPixmap(":/Transform.png"))
                
                if typeInfo == "CAMERA":
                    return QIcon(QPixmap(":/Camera.png"))



    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=Qt.EditRole):

        if index.isValid():
            
            if role == Qt.EditRole:
                
                node = index.internalPointer()
                node.setName(value)
                
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



base, form = loadUiType("Tutorial05.ui")

class WndTutorial05(base, form):
    
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        rootNode   = Node("Hips")
        childNode0 = TransformNode("RightPirateLeg",    rootNode)
        childNode1 = Node("RightPirateLeg_END",         childNode0)
        childNode2 = CameraNode("LeftFemur",            rootNode)
        childNode3 = Node("LeftTibia",                  childNode2)
        childNode4 = Node("LeftFoot",                   childNode3)
        childNode5 = LightNode("LeftFoot_END",          childNode4)
        
        self._proxyModel = QSortFilterProxyModel()
        
        """VIEW <------> PROXY MODEL <------> DATA MODEL"""

        self._model = SceneGraphModel(rootNode)
        self._model.insertLights(0, 10)
        
        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        self.uiTree.setModel(self._proxyModel)
        
        # QObject.connect(self.uiFilter, SIGNAL("textChanged(QString)"), self._proxyModel.setFilterRegExp)
        self.uiFilter.textChanged.connect(self._proxyModel.setFilterRegExp)
        self.uiTree.setSortingEnabled(True)
        

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle("cleanlooks")
    

    wnd = WndTutorial05()
    wnd.show()


    sys.exit(app.exec_())