# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-01 22:56:26'

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

import Resources

from Data import Node, TransformNode, CameraNode, LightNode, LIGHT_SHAPES
from Models import SceneGraphModel
    
    
class XMLHighlighter(QSyntaxHighlighter):
 
    #INIT THE STUFF
    def __init__(self, parent=None):
        super(XMLHighlighter, self).__init__(parent)
 
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkMagenta)
        keywordFormat.setFontWeight(QFont.Bold)
 
        keywordPatterns = ["\\b?xml\\b", "/>", ">", "<"]
 
        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]
 
        xmlElementFormat = QTextCharFormat()
        xmlElementFormat.setFontWeight(QFont.Bold)
        xmlElementFormat.setForeground(Qt.green)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=[\s/>])"), xmlElementFormat))
 
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\=)"), xmlAttributeFormat))
 
        self.valueFormat = QTextCharFormat()
        self.valueFormat.setForeground(Qt.red)
 
        self.valueStartExpression = QRegExp("\"")
        self.valueEndExpression = QRegExp("\"(?=[\s></])")
 
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.gray)
        self.highlightingRules.append((QRegExp("<!--[^\n]*-->"), singleLineCommentFormat))
 
    #VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING
    def highlightBlock(self, text):
 
        #for every pattern
        for pattern, format in self.highlightingRules:
 
            #Create a regular expression from the retrieved pattern
            expression = QRegExp(pattern)
 
            #Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)
 
            #While the index is greater than 0
            while index >= 0:
 
                #Get the length of how long the expression is true, set the format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, format)
 
                #Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)
 
        #HANDLE QUOTATION MARKS NOW.. WE WANT TO START WITH " AND END WITH ".. A THIRD " SHOULD NOT CAUSE THE WORDS INBETWEEN SECOND AND THIRD TO BE COLORED
        self.setCurrentBlockState(0)
 
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.valueStartExpression.indexIn(text)
 
        while startIndex >= 0:
            endIndex = self.valueEndExpression.indexIn(text, startIndex)
 
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.valueEndExpression.matchedLength()
 
            self.setFormat(startIndex, commentLength, self.valueFormat)
 
            startIndex = self.valueStartExpression.indexIn(text, startIndex + commentLength);    











base, form = loadUiType("Views/Window.ui")

class WndTutorial06(base, form):
    

    def updateXml(self):
        
        print ("UPDATING XML")
        
        xml = self._rootNode.asXml()
        
        self.uiXml.setPlainText(xml)


        
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._rootNode   = Node("Root")
        childNode0 = TransformNode("A",    self._rootNode)
        childNode1 = LightNode("B",        self._rootNode)
        childNode2 = CameraNode("C",       self._rootNode)
        childNode3 = TransformNode("D",    self._rootNode)
        childNode4 = LightNode("E",        self._rootNode)
        childNode5 = CameraNode("F",       self._rootNode)
        childNode6 = TransformNode("G",    childNode5)
        childNode7 = LightNode("H",        childNode6)
        childNode8 = CameraNode("I",       childNode7)
       

        
        self._proxyModel = QSortFilterProxyModel(self)
        
        """VIEW <------> PROXY MODEL <------> DATA MODEL"""

        self._model = SceneGraphModel(self._rootNode, self)
        

        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        self._proxyModel.setFilterRole(SceneGraphModel.filterRole)
        self._proxyModel.setFilterKeyColumn(0)
        
        self.uiTree.setModel(self._proxyModel)
        

        # QObject.connect(self.uiFilter, SIGNAL("textChanged(QString)"), self._proxyModel.setFilterRegExp)
        self.uiFilter.textChanged.connect(self._proxyModel.setFilterRegExp)
        self._propEditor = PropertiesEditor(self)
        self.layoutMain.addWidget(self._propEditor)
        
        self._propEditor.setModel(self._proxyModel)
        
        

        
        # QObject.connect(self.uiTree.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self._propEditor.setSelection)
        self.uiTree.selectionModel().currentChanged.connect(self._propEditor.setSelection)
        # QObject.connect(self._model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.updateXml)
        self._model.dataChanged.connect(self.updateXml)
        
        #Create our XMLHighlighter derived from QSyntaxHighlighter
        highlighter = XMLHighlighter(self.uiXml.document())

        self.updateXml()


propBase, propForm = loadUiType("Views/Editors.ui")
nodeBase, nodeForm = loadUiType("Views/NodeEditor.ui") 
lightBase, lightForm = loadUiType("Views/LightEditor.ui")
cameraBase, cameraForm = loadUiType("Views/CameraEditor.ui")
transformBase, transformForm = loadUiType("Views/TransformEditor.ui")



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
   
        for i in LIGHT_SHAPES.names:
            if i != "End":
                self.uiShape.addItem(i)
   

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiLightIntensity, 2)
        self._dataMapper.addMapping(self.uiNear, 3)
        self._dataMapper.addMapping(self.uiFar, 4)
        self._dataMapper.addMapping(self.uiShadows, 5)
        self._dataMapper.addMapping(self.uiShape, 6, "currentIndex")
        
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
    app.setStyle("plastique")
    
    wnd = WndTutorial06()
    wnd.show()
    

 
 

    sys.exit(app.exec_())