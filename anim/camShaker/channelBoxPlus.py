# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-04 09:10:56'

"""
源码源于 channelBoxPlus 插件
做了一些小修改
"""

import difflib
from maya import OpenMaya, OpenMayaUI, cmds, mel

# import colour palette
DIVIDER_COLOUR = [0.150, 0.150, 0.150]
USER_COLOURS = [
    [
        [0.764, 0.266, 0.266], 
        [0.662, 0.168, 0.168], 
        [0.564, 0.086, 0.086], 
        [0.466, 0.007, 0.007],
    ], 
    [
        [0.301, 0.662, 0.168], 
        [0.211, 0.564, 0.086], 
        [0.129, 0.466, 0.007], 
        [0.054, 0.364, 0.000],
    ], 
    [
        [0.266, 0.301, 0.764], 
        [0.168, 0.203, 0.662], 
        [0.086, 0.117, 0.564], 
        [0.007, 0.039, 0.466],
    ], 
    [
        [0.764, 0.266, 0.701], 
        [0.662, 0.168, 0.600], 
        [0.564, 0.086, 0.501], 
        [0.466, 0.007, 0.403],
    ]
]


# ----------------------------------------------------------------------------


# import pyside, do qt version check for maya 2017 >

from Qt.QtGui import *
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtCompat import wrapInstance

import pymel.core as pm
from QtLib import IMouseClickSignal,ICompleterComboBox

# ----------------------------------------------------------------------------


global CHANNELBOX_PLUS
CHANNELBOX_PLUS = None

CHANNELBOX_SEARCH = "mainChannelBoxSearch"


# ----------------------------------------------------------------------------

def mayaToQT(name):
    """
    Maya -> QWidget

    :param str name: Maya name of an ui object
    :return: QWidget of parsed Maya name
    :rtype: QWidget
    """
    ptr = OpenMayaUI.MQtUtil.findControl( name )
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findLayout( name )    
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
    if ptr is not None:     
        return wrapInstance( long( ptr ), QWidget )

# ----------------------------------------------------------------------------


class SearchWidget(QWidget):
    def __init__( self, channelBox ,CamShakerWidget,parent=None, threshold=0.75):
        # initialize
        super(SearchWidget, self).__init__(parent)
        self.CamShakerWidget = CamShakerWidget
        # self.setObjectName(CHANNELBOX_SEARCH)
        self.CHANNELBOX = channelBox
        self.parent = parent
                
        # variable
        self.threshold = threshold
        
        # set ui
        self.setMaximumHeight(30)
        
        # create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(3,5,3,5)
        layout.setSpacing(3)
        
        # # create seleted shaker rig
        # self.selector = ICompleterComboBox()
        # self.updateShakerList()
        # signal = IMouseClickSignal(self.selector)
        # signal.LClicked.connect(self.updateShakerList)
        # layout.addWidget(self.selector)

        # create search widget
        self.edit = QLineEdit(self)
        self.edit.textChanged.connect(self.update)
        self.edit.setPlaceholderText("Search...")
        layout.addWidget(self.edit)
        
        # create clear widget
        button = QPushButton(self)
        button.setText("x")
        button.setFlat(True)
        button.setMinimumHeight(20)
        button.setMinimumWidth(20)
        button.released.connect(self.clear)
        layout.addWidget(button)
                
        # register callback
        self.id = self.registerCallback()
        self.update()
        
    # ------------------------------------------------------------------------

    # def updateShakerList(self):
    #     pass
    #     # text = self.Cam_Combo.currentText()
    #     # self.Cam_Combo.clear()
    #     shaker_grp = "Cam_Shaker_GRP"
    #     if not pm.objExists(shaker_grp):
    #         return
        
    #     shaker_grp = pm.PyNode(shaker_grp)
        
    #     for shaker in shaker_grp.listRelatives():
    #         pass

    #     # for i,cam in enumerate(pm.ls(ca=1)):
    #     #     cam = cam.getParent()
    #     #     if str(cam) in self.exclude_list:continue
    #     #     self.Cam_Combo.addItem(str(cam))
            
    #     # self.Cam_Combo.setCurrentText(text)
    
    # ------------------------------------------------------------------------
    
    def registerCallback(self):
        """
        Register a callback to run the update function every time the
        selection list is modified.
        
        :return: Callback id
        :rtype: int
        """
        return OpenMaya.MModelMessage.addCallback(
            OpenMaya.MModelMessage.kActiveListModified, 
            self.update
        )
        
    def removeCallback(self):
        """
        Remove the callback that updates the ui every time the selection
        list is modified.
        """
        OpenMaya.MMessage.removeCallback(self.id)
        
    # ------------------------------------------------------------------------
    
    def deleteLater(self):
        """
        Subclass the deleteLater function to first remove the callback, 
        this callback shouldn't be floating around and should be deleted
        with the widget.
        """
        self.removeCallback()
        QWidget.deleteLater(self)
        
    # ------------------------------------------------------------------------
    
    def update(self, *args): 
        """
        Update the main channel box with the input data, filter attributes 
        based on the search term and colour user attributes.
        """
        # get selected nodes
        nodes = cmds.ls(sl=True) or []
        self.parent.display_label.hide()
        cmds.channelBox(self.CHANNELBOX, edit=1, visible=0)
        idx = self.CamShakerWidget.Cam_Combo.currentIndex()
        cam = self.CamShakerWidget.Cam_Combo.itemText(idx)

        if not cam:
            self.parent.display_label.show()
            self.parent.display_label.setText(u"<center>请选择摄像机</center>")
            return

        CAM_CTRL = "%s_CAM_CTRL" % cam
        if not pm.objExists(CAM_CTRL) :
            self.parent.display_label.show()
            self.parent.display_label.setText(u"<center>请点击按钮生成相机约束</center>")
            return

        
        if not nodes or nodes[0] != CAM_CTRL:
            self.parent.display_label.show()
            self.parent.display_label.setText(u"<center>请点击按钮选择抖动节点</center>")
            return

        cmds.channelBox(self.CHANNELBOX, edit=1, visible=1)
            
        # colour user attributes
        self.updateColour(nodes)
        
        # filter attributes
        string = self.edit.text()
        self.updateSearch(string, nodes)
        
        QWidget.update(self)
        
    # ------------------------------------------------------------------------
 
    def clear(self):
        """
        Clear the text in the search line edit.
        """
        self.edit.setText("")
        
    # ------------------------------------------------------------------------
        
    def matchSearch(self, attr, searchArguments):
        """
        Check if all search arguments exist in the attribute string.
        
        :param str attr: Attribute channel name
        :param list searchArguments: List of arguments to match
        :return: Does attribute match with search arguments
        :rtype: bool
        """
        return all([s in attr.lower() for s in searchArguments])
        
    def updateSearch(self, matchString, nodes):    
        """
        Loop over all keyable attributes and match them with the search string.
        
        :param str matchString: Search string to match with attributes
        :param list nodes: List of nodes to process the attributes from
        """
        # reset of search string is empty
        if not matchString:
            cmds.channelBox(self.CHANNELBOX, edit=True, fixedAttrList=[])
            return
    
        # split match string
        matches = []
        matchStrings = matchString.lower().split()
        
        # get matching attributes
        for node in nodes:
            attrs = cmds.listAttr(node, k=True, v=True)
            
            for attr in attrs:
                if (
                    not attr in matches and 
                    self.matchSearch(attr, matchStrings)
                ):
                    matches.append(attr)
               
        # append null if not matches are found ( cannot use empty list )
        if not matches:
            matches.append("null")

        # filter channel box
        cmds.channelBox(self.CHANNELBOX, edit=True, fixedAttrList=matches)
        
    # ------------------------------------------------------------------------
    
    def updateColour(self, nodes):  
        """
        Loop over the selected objects user defined attributes, and generate 
        a colour for them, nodeRegex is not used because it slows down the 
        displaying of the the Channel Box in scenes with many user defined 
        attributes. 
        
        :param list nodes: list of selected nodes
        """
        for node in nodes:
            # get user defined attributes
            attrs = cmds.listAttr(node, userDefined=True) or []
            
            # set default colour indices
            mainColour, subColour = 0, 0
            
            # loop attributes
            for i, attr in enumerate(attrs):
                # get attribute state
                isLocked = cmds.getAttr("{0}.{1}".format(node, attr), l=True)
                isKeyable = cmds.getAttr("{0}.{1}".format(node, attr), k=True)
                
                # catch divider
                if isLocked or not isKeyable:
                    # update colour indices
                    mainColour += 1
                    subColour = 0
                    

                    if mainColour == len(USER_COLOURS):
                        mainColour = 0
                     
                    # update colour
                    cmds.channelBox(
                        self.CHANNELBOX, 
                        edit=True, 
                        attrRegex=attr, 
                        attrBgColor=DIVIDER_COLOUR
                    ) 
                    
                    continue
               
                # match string with previous attribute to get sub colour
                if i != 0:
                    # get match ratio
                    ratio = difflib.SequenceMatcher(
                        None,
                        attr,
                        attrs[i-1]
                    ).ratio()
                    
                    # compare match ratio with threshold
                    if ratio < self.threshold:
                        subColour += 1
                        
                        if subColour == len(USER_COLOURS[mainColour]):
                            subColour = 0
                  
                # update colour
                colour = USER_COLOURS[mainColour][subColour]                
                cmds.channelBox(
                    self.CHANNELBOX, 
                    edit=True, 
                    attrRegex=attr, 
                    attrBgColor=colour
                )


# ----------------------------------------------------------------------------
