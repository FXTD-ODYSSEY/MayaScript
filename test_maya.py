# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-24 21:30:52"


import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtWidgets

print(1245412)

def maya_to_qt(name,typ=QtWidgets.QWidget):
    # Maya -> QWidget
    ptr = OpenMayaUI.MQtUtil.findControl(name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(name)
    if ptr is not None:
        return wrapInstance(int(ptr),typ)


class NsRigSmoothOptionsWindow:
    # def __init__(self):
    #     self.nsrigSmoothOptions()

    def nsrigSmoothOptions(self):
        # 	STEP 1:  Get the option box.
        layout = mel.eval("string $layout=getOptionBox()")
        cmds.setParent(layout)
        # 	STEP 2:  Pass the command name to the option box.
        # mel.eval('setOptionBoxCommandName("nsrigSmooth"))')
        # 	STEP 3:  Activate the default UI template.
        cmds.setUITemplate("DefaultTemplate", pushTemplate=1)
        # 	STEP 4: Create option box contents.
        cmds.waitCursor(state=1)
        cmds.tabLayout(tabsVisible=0, scrollable=1)
        parent = str(cmds.columnLayout(adjustableColumn=1))
        self.createNsRigSmoothTabUI()
        cmds.waitCursor(state=0)
        # 	Step 5: Deactivate the default UI template.
        cmds.setUITemplate(popTemplate=1)
        # 	Step 6: Customize the buttons.
        # 	'Apply' button.
        applyBtn = str(mel.eval("getOptionBoxApplyBtn()"))
        cmds.button(
            applyBtn,
            edit=1,
            # command = 'print("test print")',
            command=lambda args: self.nsrigSmoothCallback(parent, str(0)),
            label=("Create"),
        )
        # 	'Save' button.
        saveBtn = str(mel.eval("getOptionBoxSaveBtn()"))
        cmds.button(
            saveBtn,
            edit=1,
            command=lambda args: self.nsrigSmoothCallback(parent, str(0)),
        )
        # 	'Reset' button.
        resetBtn = str(mel.eval("getOptionBoxResetBtn()"))
        print(resetBtn)
        # typ = cmds.objectTypeUI(resetBtn)
        # print(typ)
        # btn = maya_to_qt(resetBtn, QtWidgets.QPushButton)
        # btn.clicked.connect(lambda:print(1243))
        
        cmds.button(resetBtn, edit=1, command=lambda *args:print(1234))

        # 	Step 7: Set the option box title.
        mel.eval('setOptionBoxTitle("nsrigSmooth Options")')
        # 	Step 8: Customize the 'Help' menu item text.
        mel.eval('setOptionBoxHelpTag("help")')
        # 	Step 9: Set the current values of the option box.
        # eval (($setup + " " + $parent + " " + 0));
        # 	Step 10: Show the option box.
        mel.eval("showOptionBox()")

    def createNsRigSmoothTabUI(self):
        cmds.textFieldGrp("nsrigSmoothNode", tx="", label=("nsrigSmoothNode"))
        cmds.separator()
        cmds.optionMenuGrp("wsWidget", label=("Weighting Scheme"))
        cmds.menuItem(label=("Uniform"))
        cmds.menuItem(label=("Contangent"))
        cmds.menuItem(label=("Span-Aware"))
        cmds.optionMenuGrp("sdWidget", label=("Smoothing Direction"))
        cmds.menuItem(label=("Surrounding"))
        cmds.menuItem(label=("UV"))
        cmds.intSliderGrp(
            "siWidget",
            field=True,
            minValue=0,
            v=0,
            maxValue=100,
            label=("Smoothing Iteration"),
        )

    # Initialize the option values
    def setOptionVars(self, forceFactorySettings):
        if forceFactorySettings or not cmds.optionVar(exists="nsrigSmoothNode"):
            cmds.optionVar(stringValue=("nsrigSmoothNode", ""))

        if forceFactorySettings or not cmds.optionVar(exists="uniformScheme"):
            cmds.optionVar(stringValue=("uniformScheme", "Uniform"))

        if forceFactorySettings or not cmds.optionVar(exists="surroundingDirection"):
            cmds.optionVar(stringValue=("surroundingDirection", "Surrounding"))

        if forceFactorySettings or not cmds.optionVar(exists="smoothIteration"):
            cmds.optionVar(intValue=("smoothIteration", 0.0))

    def nsrigSmoothHelp(self):
        print("nsrigSmooth help")

    # Update the state of the option box UI to reflect the option values
    def nsrigSmoothSetup(self, parent, forceFactorySettings, *args):
        print("nsrigSmooth setup", parent, forceFactorySettings)
        return

        self.setOptionVars(forceFactorySettings)
        # Retrieve the option settings
        cmds.setParent(parent)
        # Weighting Scheme
        uniformScheme = str(cmds.optionVar(query="uniformScheme"))
        if cmds.optionMenuGrp("wsWidget", exists=1):
            if uniformScheme == "Uniform":
                cmds.optionMenuGrp("wsWidget", edit=1, select=1)

            elif uniformScheme == "Contangent":
                cmds.optionMenuGrp("wsWidget", edit=1, select=2)

            elif uniformScheme == "Span-Aware":
                cmds.optionMenuGrp("wsWidget", edit=1, select=3)

        surroundingDirection = str(cmds.optionVar(query="surroundingDirection"))
        # Smoothing Direction
        if cmds.optionMenuGrp("sdWidget", exists=1):
            if surroundingDirection == "Surrounding":
                cmds.optionMenuGrp("sdWidget", edit=1, select=1)

            else:
                cmds.optionMenuGrp("sdWidget", edit=1, select=2)

        if cmds.intSliderGrp("siWidget", exists=1):
            cmds.intSliderGrp(
                "siWidget", edit=1, value=cmds.optionVar(query="smoothIteration")
            )
            # Smoothing Iteration

    # Update the values with the current state of the option box UI
    def nsrigSmoothCallback(self, parent, doit):
        print("nsrigSmoothCallback", parent, doit)

        cmds.setParent(parent)
        # nsrigSmoothNode
        cmds.optionVar(
            stringValue=(
                "nsrigSmoothNode",
                cmds.textFieldGrp("nsrigSmoothNode", query=1, tx=1),
            )
        )
        # Weigting Scheme
        uniformScheme = "Uniform"
        if cmds.optionMenuGrp("wsWidget", q=1, select=1) == 1:
            uniformScheme = "Uniform"

        elif cmds.optionMenuGrp("wsWidget", q=1, select=1) == 2:
            uniformScheme = "Contangent"

        elif cmds.optionMenuGrp("wsWidget", q=1, select=1) == 3:
            uniformScheme = "Span-Aware"

        cmds.optionVar(stringValue=("uniformScheme", uniformScheme))
        # Smmoothing Direction
        surroundingDirection = "Surrounding"
        if cmds.optionMenuGrp("sdWidget", q=1, select=1) == 1:
            surroundingDirection = "Surrounding"

        else:
            surroundingDirection = "UV"

        cmds.optionVar(stringValue=("surroundingDirection", surroundingDirection))
        # Smmoothing Iteration
        if cmds.intSliderGrp("siWdiget", exists=1):
            cmds.optionVar(
                intValue=(
                    "smoothIteration",
                    cmds.intSliderGrp("siWidget", query=1, value=1),
                )
            )

        if doit:
            pass


window = NsRigSmoothOptionsWindow()
window.nsrigSmoothOptions()

