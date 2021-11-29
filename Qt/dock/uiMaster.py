# -*- coding: utf-8 -*-
"""
https://clamdragon3d.com/blog/2017/1/8/uimaster-for-maya
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# uiMaster - A Python plugin for Autodesk Maya
# Copyright (C) 2016 by Brendan Kelly - Seattle, USA
#
__author__ = "Brendan Kelly"
__version__ = "1.0"
__email__ = "clamdragon@gmail.com"
__mayaVersion__ = "2014, 2015, 2016, 2016.5"
__copyYear__ = "2016"
__title__ = "uiMaster for Maya"

#----------------------------------------------------------------------
# UIMASTER BETA LICENSE AGREEMENT
# By using any part of uiMaster (the contents of this file),
# you agree to the terms of this license.
# 
# uiMaster (the "software") is the property of Brendan Kelly and, therefore,
# is protected by international copyright law. And international copyright
# ASSASSINS, probably.
#
# The software shall be licensed ONLY to individual humans, not to any
# non-human entities, such as corporations, birds, or Mars rovers.
# The software is provided to you, the human licensee, for whatever purposes,
# commercial or otherwise, you wish to use it for - excluding ILLEGAL activity.
# Seriously, don't blow people up with it.
# Blowing up 3D models of people in Maya is fine and, indeed, encouraged.
#
# You may not, under any circumstances, remove or in any way alter 
# this license agreement.
#
# You are prohibited from re-distributing copies of uiMaster to others.
# Just tell them to be nice and get their own. It's not expensive.
# You may use uiMaster on an unlimited number of YOUR OWN machines.
#
# You are prohibited from removing any copyrights or credits
# from the software. You are free to edit the software FOR YOUR OWN PURPOSES,
# but you must explicitly take credit for ANYTHING which is changed, and you
# are prohibited from distributing your edited version of the software.
#
# The software is provided "AS IS", without any warranty for its past,
# current or future functionality. Under no circumstances shall the 
# author of the software be held liable for any claims or damages 
# arising from the use of or other activities involving the software.
#----------------------------------------------------------------------
#
# Now that that's out of the way... what's it do?
#
# Maya has lots of windows and editors. Things can easily get cluttered.
# uiMaster is an easy-to-use tool for consolidating GUI windows in Maya.
# It works with custom GUIs, (.ui, .py or .mel formats) 
# as well as native Maya editors.
# Custom interfaces retain full functionality.
# Initially designed for Rig UIs in busy scenes.
#
# As is, uiMaster does not support model (persp/ortho) panels.
# Behavior is undefined when you have copies of the same UI
# in both uiMaster and Maya's native panel layout. (don't know why you would)
#
"""
# With uiMaster.py in your plugins path,
# call "uiMaster" from MEL command line in Maya.
"""
#
# Special thanks to Nathan Horne & Chris Zurbrigg -
# for their excellent Qt for Maya learning resources!
#
import os
import sys
import shiboken
import maya.cmds as cmds
from pymel import core as pm
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.OpenMayaMPx as omPx
from Qt import QtCore, QtGui, QtUiTools
from functools import partial
import inspect
import re
import urllib
from __main__ import __dict__ as mainDict


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------


8888888b. 888                d8b         
888   Y88b888                Y8P         
888    888888                            
888   d88P888888  888 .d88b. 88888888b.  
8888888P" 888888  888d88P"88b888888 "88b 
888       888888  888888  888888888  888 
888       888Y88b 888Y88b 888888888  888 
888       888 "Y88888 "Y88888888888  888 
                          888            
                     Y8b d88P            
                      "Y88P"   

#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""

# Boilerplate
class UiMasterCmd(omPx.MPxCommand):
    def __init__(self):
        omPx.MPxCommand.__init__(self)
    
    # Instead of making Ui_uiMaster a subclass of QDockWidget,
    # (which results in Maya misinterpreting it a bit)
    # Just make a generic dockWidget, then build the Ui_uiMaster class, 
    # instantiate, and stuff the instance inside the dockWidget.
    #
    def doIt(self, argList):
        # get auto flag - to see if it's being called
        # by a script node from a new scene
        auto = (argList.flagIndex("a", "auto") != om.MArgList.kInvalidArgIndex)
        makeUiMaster(auto)

#
def cmdCreator():
    return omPx.asMPxPtr(UiMasterCmd())

#
def initializePlugin(obj):
    plugin = omPx.MFnPlugin(obj, __author__, __version__, __mayaVersion__)
    try:
        plugin.registerCommand("uiMaster", cmdCreator)
    except:
        cmds.warning("Failed to register uiMaster plugin!")
        raise

#
def uninitializePlugin(obj):
    plugin = omPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand("uiMaster")
    except:
        cmds.warning("Failed to deregister uiMaster plugin!")
        raise


# For internal testing - non-plugin mode
#
def makeUiMaster(auto=False):
    print("Making uiMaster - auto: {0}".format(auto))
    # Check for silliness - if this was 
    # called by scriptWin, do nothing.
    # Otherwise, delete old widget, make new one - 
    # settings and uis should be saved
    mayaName = "uiMasterDockWidget"
    main = getMayaMainWindow()
    for c in main.children():
        if c.objectName() == mayaName and c.widget():
            if c.widget().scriptWin.safeMode:
                cmds.warning("Right, stop that! Stop it. "
                            "It's silly, very silly.")
                return
            elif auto:
                # just try to add from tabsNode using restoreSavedState
                c.widget().additiveRestore()
                return
            else:
                c.close()
            break

    uimDock = QtGui.QDockWidget(getMayaMainWindow())
    uimDock.setObjectName(mayaName)
    uimDock.setWindowIcon(QtGui.QPixmap(":/mayaIcon"))
    uimDock.setWindowTitle(__title__)

    UiMasterWin = buildClass(Ui_uiMaster)
    uiMaster = UiMasterWin(uimDock)
    uimDock.setWidget(uiMaster)
    
    uimDock.topLevelChanged.connect(uiMaster.reFloat)
    uimDock.visibilityChanged.connect(uiMaster.visChanged)
    # Event filter to pass uimDock's close signal to
    # uiMaster's closeEvent method
    filters = CloseResizeFilter(uimDock)
    uimDock.installEventFilter(filters)
    # resize stretches graphicsScene, reducing the graphics artifacts
    # caused by it expanding
    s = uimDock.size()
    uimDock.resize(5000, 5000)
    uimDock.resize(s)
    uiMaster.reFloat(uimDock.isFloating())
    
    return uimDock


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------


888     888888   d8b888d8b888   d8b                 
888     888888   Y8P888Y8P888   Y8P                 
888     888888      888   888                       
888     888888888888888888888888888 .d88b. .d8888b  
888     888888   888888888888   888d8P  Y8b88K      
888     888888   888888888888   88888888888"Y8888b. 
Y88b. .d88PY88b. 888888888Y88b. 888Y8b.         X88 
 "Y88888P"  "Y888888888888 "Y888888 "Y8888  88888P'


#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""

# Check website for new versions of uiMaster
#
def selfUpdate():
    main = getMayaMainWindow()
    win = QtGui.QMessageBox(main)
    win.setIcon(QtGui.QMessageBox.Information)
    win.setWindowTitle("uiMaster Updater")
    targ = "http://www.clamdragon3d.com/s/uiMaster.py"
    try:
        newest = urllib.urlopen(targ)
    except IOError:
        win.setText("\nUpdate URL invalid, please contact author.\n")
        win.exec_()
        return
    
    content = newest.read()
    frame = {}
    try:
        exec content in frame
    except SyntaxError:
        win.setText("\nToo many URL requests, try again later.\n")
        win.exec_()
        return

    if frame["__version__"] == __version__:
        win.setText("\nuiMaster is up do date.\n")
        win.exec_()
    else:
        print("Updating uiMaster to newest version...")
        f = cmds.pluginInfo("uiMaster", q=True, path=True)
        with open(f, "w") as new:
            new.write(content)
        
        win.setText("\nUpdate successful! Click OK to restart uiMaster.\n")
        win.exec_()
        cmds.unloadPlugin("uiMaster")
        cmds.loadPlugin("uiMaster")
        cmds.uiMaster()


# compile .ui to .py - made easy.
# pass file as argument, or else a file browser opens
# for you to select one
#
def compileUI(inFile=None):
    #import sys, pprint
    from pysideuic import compileUi
    
    # File browser if no file given
    if inFile is None:
        inFile = cmds.fileDialog2(caption="Compile Qt Ui",
                    dialogStyle=2, fileMode=1,
                    fileFilter="Qt Designer Files (*.ui)")[0]
    outFile = inFile.replace(".ui", ".py")
    pyFile = open(outFile, "w")
    try:
        compileUi(inFile, pyFile, False, 4, False)
    except:
        result = "Failed. Pass in valid file name."
    else:
        result = "Success! Result: {0}".format(outFile)
    finally:
        pyFile.close()

    return result


# Get maya main window for parenting
#
def getMayaMainWindow():
    # returns a QWidget wrapper for the main maya window,
    # to allow uiMaster to be parented to it
    mayaWin = omui.MQtUtil.mainWindow()
    return QGraphicsProxyWidget
    if mayaWin:
        return shiboken.wrapInstance(long(mayaWin), QtGui.QMainWindow)
    

# remember for entire Maya session
customPaths = set()
# Add given directory to the maya default search path
# (for this session)
# f arg is FULL FILE NAME, not just directory
#
def addPathToSession(f=None):
    # File browser if no file given
    if f is None:
        f = cmds.fileDialog2(caption="Add directory to path", 
                                dialogStyle=2, fileMode=2)[0]

    add = False
    d = os.path.dirname(f).replace(os.sep, os.altsep)
    melPaths = mel.eval("getenv MAYA_SCRIPT_PATH").replace(os.sep, os.altsep)
    if d not in melPaths:
        new = melPaths + os.pathsep + d
        mel.eval("putenv MAYA_SCRIPT_PATH \"{0}\"".format(new))
        customPaths.add(d)
        print("uiMaster: Added {0} to Maya Script Path".format(d))
    paths = [p.replace(os.sep, os.altsep) for p in sys.path]
    # make sure it's root path of package, if applicable
    i = os.altsep+"__init__.py"
    while os.path.exists(d+i):
        d = os.path.dirname(d)
    if d not in paths:
        sys.path.append(d)
        customPaths.add(d)
        print("uiMaster: Added {0} to sys.path".format(d))


# Factory Function to build a QMainWindow from
# compiled .py files - subclasses the given clsName
# and a QMainWindow, run __init__ and setupUi
#
def buildClass(clsName):
    #clsName = parse file arg for class name
    class UiWidg(clsName, QtGui.QMainWindow):
        def __init__(self, parent=None):
            super(UiWidg, self).__init__(parent)
            # the compiled .py file has the content,
            # this class provides the QMainWindow to fill
            self.setupUi(self)
    return UiWidg


# Convenience function to get mainwindow child window of given name
#
def getMayaChild(title):
    for w in getMayaMainWindow().children():
        if w.isWidgetType() and w.windowTitle() == title:
            return w


# Resolve file dependencies outside of the command itself.
# could be files, could be multiples. But they always come in pairs:
# absFile and relFile are two possible locations for any module
#
def resolveDependencies(lang, dependencies):
    if lang == "python":
        addPyModules(dependencies)
    elif lang == "mel":
        addMelSourceFiles(dependencies)
    else:
        cmds.warning("Unrecognized file type for restore")
        

# import modules which were found to be required for py cmd
#
def addPyModules(dependencies):
    for word, mod, name, isModule, absPath, rel in dependencies:
        # ensure we're not being redundant and importing
        # existing module/name pairs
        if word in mainDict and mod in sys.modules:
            # safe to say this word is already imported
            continue

        # first of all, try to add directory
        if absPath:
            proj = cmds.workspace(q=True, rootDirectory=True)
            relPath = os.path.normpath(proj+rel).replace(os.sep, os.altsep)
            for f in (absPath, relPath):
                if os.path.exists(f):
                    addPathToSession(f)
                    # don't try relPath is absPath works
                    break

        # in case path was not added, enclose in try block
        try:
            __import__(mod)
            mod = sys.modules[mod]
        except ImportError:
            cmds.warning("Couldn't find module {0}".format(name))
            # Does not exist - skip word
            continue

        # mod is the module object now, just get it or object from it
        # to add to __main__ console dict
        if isModule:
            obj = mod
        else:
            obj = getattr(mod, name)
        mainDict[word] = obj
        print("Successfully imported {0}({1}) as {2}".format(
                                                    name, mod, word))

        # old code using imp.load_source
        """
        # first case split: if file was determined to be in default
        # search path or not. If not, absPath and relPath are None
        if not absPath:
            __import__(mod)
            mod = sys.modules[mod]

        else:
            proj = cmds.workspace(q=True, rootDirectory=True)
            relPath = os.path.normpath(proj+rel).replace(os.sep, os.altsep)
            for f in (absPath, relPath):
                if not os.path.exists(f):
                    continue
                # resolve .py vs (.pyc, .pyn, .pyo)
                # i.e. load_source vs load_compiled
                py = f[:-1]
                if os.path.exists(py):
                    mod = imp.load_source(name, py)
                else:
                    mod = imp.load_compiled(name, f)
                # break so that else only triggers when
                # neither path exists
                break
            else:
                # may as well
                try:
                    __import__(mod)
                    mod = sys.modules[mod]
                except ImportError:
                    # DNE - skip this word
                    cmds.warning("Couldn't find module {0}".format(name))
                    continue
        """


# Source files which were found to be required for MEL cmd
#
def addMelSourceFiles(dependencies):
    for word, absPath, rel in dependencies:
        # try a couple whatIs checks to see if:
        # 1) proc exists already, or
        # 2) file exists in script path 
        result = mel.eval("whatIs \"{0}\"".format(word))
        if result.startswith("Mel procedure"):
            # already in
            continue
        fileName = os.path.basename(absPath)
        result = mel.eval("whatIs \"{0}\"".format(fileName))
        if result.startswith("Script found"):
            # script file found in default path
            mel.eval("source \"{0}\"".format(filename))
            continue

        # check in saved abspath and project relative path
        proj = cmds.workspace(q=True, rootDirectory=True)
        relPath = os.path.normpath(proj+rel).replace(os.sep, os.altsep)
        for f in (absPath, relPath):
            if os.path.exists(f):
                addPathToSession(f)
                mel.eval("source \"{0}\"".format(f))
                break
        else:
            # skip this word
            cmds.warning("Couldn't find source file {0}".format(rel))


# Root function for finding file dependencies
# in a given bit of py or mel code.
# On uiMaster reload, any directory dependencies outside of
# normal script path are added and all imports are performed
#
def getDependenciesInCode(lang, cmd):
    # separated by special characters or whitespace
    words = set(re.findall("[a-zA-Z]\w+", cmd))

    if lang == "python":
        # modData is set of (word, module, fullModuleName, isModule)
        modData = getPyModules(words)
        # dependencies is a list of tuples (name, absPath, relPath)
        return getModuleDependencies(modData)
    elif lang == "mel":
        return getMelSourceFiles(words)
    else:
        cmds.warning("Specify \"python\" or \"mel\".")
        return []


# For each word, find if it's dependent on a module,
# and import that module
# *-style imports are not supported.
#
def getPyModules(words):
    modData = set()

    for word in words:
        if word in mainDict:
            # w is a global Maya variable. not necessarily a module.
            obj = mainDict[word]
            mod, name = None, None
            if hasattr(obj, "__module__"):
                mod = obj.__module__
                # obj could be an instance of something in module,
                # if it is then IGNORE this word!
                if obj.__class__.__name__ in sys.modules[mod].__dict__:
                    continue
            # if mod is a module now, then w is an object inside that module
            if hasattr(obj, "__name__"):
                name = obj.__name__
            # name is a module, w is the console var for it
            isModule = False
            if not mod or mod in ("__main__", "__builtin__"):
                mod = name
                isModule = True
            if mod not in sys.modules:
                continue
            data = (word, mod, name, isModule)
            modData.add(data)
    
    return modData


# Python only. Takes modData (word, module, name)
# and checks if module is in sys.path.
# if so, just add import statement to cmd,
# if not, add entry to dependencies (word, absFile, relFile)
#
def getModuleDependencies(modData):
    #paths = [a.replace(os.sep, os.altsep) for a in sys.path]
    # dependencies is a list of form (name, absFile, relFile)
    dependencies = []
    for word, mod, name, isModule in modData:
        # some built-in modules do not have __file__ attribute
        # if it doesn't just set it inside sys.path
        try:
            f = sys.modules[mod].__file__
        except AttributeError:
            f, relPath = None, None
        else:
            f = f.replace(os.sep, os.altsep)
            d = os.path.dirname(f)
            i = os.altsep+"__init__.py"
            while os.path.exists(d+i):
                d = os.path.dirname(d)
            # test if directory is in customPaths,
            # a list of directories which have been added to sys.path
            # and MSP via loading a file
            if d in customPaths:
                proj = cmds.workspace(q=True, rootDirectory=True)
                try:
                    relPath = os.path.relpath(f, proj).replace(os.sep, os.altsep)
                except ValueError:
                    relPath = ""
            else:
                f, relPath = None, None
            """
            if d in paths:
                f, relPath = None, None
            else:
                proj = cmds.workspace(q=True, rootDirectory=True)
                relPath = os.path.relpath(f, proj).replace(os.sep, os.altsep)
            """

        dep = (word, mod, name, isModule, f, relPath)
        dependencies.append(dep)

    return dependencies


# For each word, find if it's file dependent and 
# add f and relPath to dependencies
#
def getMelSourceFiles(words):
    dependencies = set()
    #paths = os.getenv("MAYA_SCRIPT_PATH")
    #paths = paths.replace(os.sep, os.altsep).split(os.pathsep)

    for word in words:
        try:
            result = mel.eval("whatIs \"{0}\"".format(word))
        except RuntimeError:
            # means there was a MEL problem with the word
            continue
        # positive result is "mel/script: {file}"
        result = result.split(": ")
        if result[0] in ("Mel procedure found in", "Script found in"):
            f = result[1].replace(os.sep, os.altsep)
            d = os.path.dirname(f)
            if d in customPaths:
                proj = cmds.workspace(q=True, rootDirectory=True)
                try:
                    relPath = os.path.relpath(f, proj).replace(os.sep, os.altsep)
                except ValueError:
                    relPath = ""
                dependencies.add((word, f, relPath))
            """
            if d not in paths:
                proj = cmds.workspace(q=True, rootDirectory=True)
                relPath = os.path.relpath(f, proj).replace(os.sep, os.altsep)
                dependencies.add((word, f, relPath))
            """

    return list(dependencies)


# Function to update the setAllMainWindowComponents MEL script
# so that it ignores any "special" Maya UIs which are loaded in uiMaster
# MUST BE CALLED AFTER ALLUIs HAS BEEN UPDATED
#
def fixFullscreenScript(name, allUIs):
    # Dictionary of all of the "special" Maya UIs, which are
    # hidden by fullscreen mode and need a bit of special treatment
    #
    stupidUiDict = {"Tool Settings": "setToolSettingsVisible",
                "Channel Box": "setChannelsVisible",
                "Layer Editor": "setLayersVisible",
                "Channel Box / Layer Editor": "setChannelsLayersVisible",
                "Attribute Editor": "setAttributeEditorVisible"}
    if name in stupidUiDict.keys():
        # have to make a new version of setAllMainWindowComponentsVisible script
        # and run it WITHOUT making a new file
        # so there's no danger if it interfering with later stuff
        #
        original = (mel.eval("getenv MAYA_LOCATION")
                +"/scripts/startup/setAllMainWindowComponentsVisible.mel")
        with open(original) as f:
            contents = f.read()
        names = list(set([a[0] for a in allUIs]) & set(stupidUiDict.keys()))
        for n in names:
            cmd = stupidUiDict[n]
            # basically just comment out the lines which set visible state
            contents = contents.replace(cmd, ("//"+cmd))
        # eval in mel to overwrite existing proc
        mel.eval(contents)

        # POSSIBLY ALSO: restoreLastPanelWithFocus


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------


 

888    888        888                           .d8888b. 888                                         
888    888        888                          d88P  Y88b888                                         
888    888        888                          888    888888                                         
8888888888 .d88b. 88888888b.  .d88b. 888d888   888       888 8888b. .d8888b .d8888b  .d88b. .d8888b  
888    888d8P  Y8b888888 "88bd8P  Y8b888P"     888       888    "88b88K     88K     d8P  Y8b88K      
888    88888888888888888  88888888888888       888    888888.d888888"Y8888b."Y8888b.88888888"Y8888b. 
888    888Y8b.    888888 d88PY8b.    888       Y88b  d88P888888  888     X88     X88Y8b.         X88 
888    888 "Y8888 88888888P"  "Y8888 888        "Y8888P" 888"Y888888 88888P' 88888P' "Y8888  88888P' 
                     888                                                                             
                     888                                                                             
                     888      


#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""

# Object to handle reference callbacks - creating, removing
# and functions for when they trigger
#
class SceneCallbackHandler():
    def __init__(self):
        self.ref = None
        # BEFORE new reference callback
        self.beforeID = om.MSceneMessage.addCallback(
                om.MSceneMessage.kBeforeCreateReference, self.beforeRef)
        # AFTER new reference callback
        self.afterID = om.MSceneMessage.addCallback(
                om.MSceneMessage.kAfterCreateReference, self.afterRef)

    # perhaps append/pop? 
    # since nested references will trigger as begin-begin-end-end
    def beforeRef(self, *argsList):
        self.ref = om.MFileIO.beforeReferenceFilename()

        print("beginning {0}".format(self.ref))
    
    def afterRef(self, *argsList):
        if not self.ref:
            return
        print("ending {0}".format(self.ref))
        self.ref = None

    def remove(self):
        om.MMessage.removeCallback(self.beforeID)
        om.MMessage.removeCallback(self.afterID)


# Reimplementation of QTabBar - to change tabSizeHint()
# And make drag & drop between TabBar objects possible
#
class TabBar(QtGui.QTabBar):
    def __init__(self, parent):
        self.base = super(TabBar, self)
        self.base.__init__(parent)
        self.pane = None
        #self.setAcceptDrops(True)
        self.dragData = None
        self.dragPix = None
    
    def tabSizeHint(self, index):
        old = self.base.tabSizeHint(index)
        return (old+QtCore.QSize(100, 20)) / 2

    def mouseMoveEvent(self, event):
        self.base.mouseMoveEvent(event)
        mPos = event.pos()
        index = self.tabAt(mPos)
        self.setCurrentIndex(index)
        if event.buttons() != QtCore.Qt.LeftButton or index == -1:
            return
        
        d = QtGui.QDrag(self)
        data = QtCore.QMimeData()
        data.setParent(self)
        rect = self.tabRect(index)
        leftD = mPos.x() - rect.left()
        rightD = rect.right() - mPos.x()
        stuff = [index, self.tabText(index), leftD, rightD]
        data.setData("uiTabData", str(stuff))
        d.setMimeData(data)
        
        rect.setWidth(rect.width() - 1)
        self.dragPix = QtGui.QPixmap.grabWidget(self, rect)

        d.setDragCursor(QtGui.QPixmap(1, 1), QtCore.Qt.MoveAction)
        d.start(QtCore.Qt.MoveAction)


    # New tab bar receives event!
    # If it's not the source, move tab to new pane
    #
    def dragEnterEvent(self, event):
        data = event.mimeData()
        stuff = data.data("uiTabData")
        if not stuff:
            event.ignore()
            return
        stuff = eval(stuff.__str__())
        event.accept()
        index = stuff[0]
        name = stuff[1]
        self.buttonVis(False)
        self.setTabsClosable(False)

        # add to tabbar right here, 
        # transition to regular tab moving
        prev = data.parent()
        if self != prev:
            index = self.pane.uim.moveTabToNewPane(
                                            index, prev.pane, self.pane)
            stuff[0] = index
            
            # fix leftD and rightD for possible new rect size
            rect = self.tabRect(index)
            leftD = stuff[2]
            rightD = stuff[3]
            extra = rect.width() - leftD - rightD
            stuff[2] = leftD + (extra/2)
            stuff[3] = rightD + (extra/2) + (extra%2)
            
            #prev.setTabsClosable(True)
            #prev.buttonVis(True)
            #self.buttonVis(False)
            #self.setTabsClosable(False)
            rect.setWidth(rect.width() - 1)
            self.dragPix = QtGui.QPixmap.grabWidget(self, rect)
            data.setData("uiTabData", str(stuff))
            data.setParent(self)
        #self.tabButton(index, QtGui.QTabBar.RightSide).hide()
        self.dragData = stuff

    
    # Move tabs within tabbar - 
    def dragMoveEvent(self, event):
        if not self.dragData:
            event.ignore()
            return
        event.accept()
        data = event.mimeData()
        stuff = eval(data.data("uiTabData").__str__())
        index = stuff[0]
        leftD = stuff[2]
        rightD = stuff[3]

        # get neighbors
        leftI = index - 1
        rightI = index + 1
        leftNeighbor = self.tabRect(leftI)
        rightNeighbor = self.tabRect(rightI)
        
        # answerRect is a more accurate version of where the mouse is than .pos()
        horPos = event.answerRect().left()
        left = horPos - leftD
        right = horPos + rightD
        
        # test if user has dragged cursor so that 
        # tabRect goes more than halfway into its neighbor -
        # if so, swap em.
        for n, i in ((leftNeighbor, leftI), (rightNeighbor, rightI)):
            if n:
                center = n.center().x()
                condition = False
                if n is leftNeighbor:
                    condition = left < center
                elif n is rightNeighbor:
                    condition = right > center
                if condition:
                    self.moveTab(index, i)
                    self.setCurrentIndex(i)
                    stuff[0] = i
                    data.setData("uiTabData", str(stuff))
                    self.dragData = stuff
        
        self.repaint(self.rect())
        
    
    def dropEvent(self, event):
        #if not self.dragData:
        #    event.ignore()
        #    return
        i = self.dragData[0]
        self.setTabsClosable(True)
        self.buttonVis(True)
        self.dragData = None
        self.repaint(self.rect())
        event.accept()
        
    def dragLeaveEvent(self, event):
        #if not self.dragData:
        #    event.ignore()
        #    return
        i = self.dragData[0]
        self.setTabsClosable(True)
        self.buttonVis(True)
        self.dragData = None
        self.repaint(self.rect())
        event.accept()
    
    def paintEvent(self, event):
        self.base.paintEvent(event)
        if self.dragData:
            index = self.dragData[0]
            rect = self.tabRect(index)
            p = QtGui.QPainter(self)
            color = self.palette().color(self.palette().Button)
            p.fillRect(rect, color)
            loc = self.mapFromGlobal(QtGui.QCursor.pos())
            offset = loc.x() - self.dragData[2]
            rect.moveLeft(offset)
            #button = self.tabButton(index, QtGui.QTabBar.RightSide)
            #button.move((rect.right() - 36), button.y())
            p.drawPixmap(rect, self.dragPix)
            del(p)

    def buttonVis(self, state):
        count = self.count()
        for i in range(0, count):
            b = self.tabButton(i, QtGui.QTabBar.RightSide)
            if b:
                b.setVisible(state)

    # Force the ui to re-enable when tabbar is clicked on
    #
    def mousePressEvent(self, event):
        self.base.mousePressEvent(event)
        self.currentChanged.emit(self.currentIndex())


# Subclass of QGraphicsProxyWidget - 
# to deal with wheel events and resizing
#
class GraphicsProxy(QtGui.QGraphicsProxyWidget):
    def __init__(self, parent=None, view=None):
        self.base = super(GraphicsProxy, self)
        self.base.__init__(parent)
        self.view = view
        self.destroyed.connect(self.view.widgetKilled)

    # Have to explicitly accept a bunch of events to stop them
    # from propogating up to the view/scene
    #
    def wheelEvent(self, event):
        self.base.wheelEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        self.base.mouseMoveEvent(event)
        event.accept()

    def mousePressEvent(self, event):
        self.base.mousePressEvent(event)
        event.ignore()
        # if there's a popup, ignore so that it will get the event
        popup = QtGui.QApplication.activePopupWidget()
        if not popup:
            event.accept()

    def mouseReleaseEvent(self, event):
        self.base.mouseReleaseEvent(event)
        event.accept()

    # Responds to Maya hotkey-induced showing of UI elements -
    # use to switch active tab to whatever user wanted
    #
    def showEvent(self, event):
        self.base.showEvent(event)
        init = self.view.pane.uim.initializing
        if not init:
            if self.view.currProxy() is not self:
                # change it!
                for i, x in enumerate(self.view.pane.loadedUIs):
                    if x[3] is self:
                        break
                self.view.pane.uiTabBar.setCurrentIndex(i)
            w = self.widget()
            if w and w.windowTitle() == "Tool Settings":
                # more stupid tool settings edge cases...
                # no, please, tool settings, please tell me more stories 
                # about what it was like to grow up in the 1930s...
                # oh what's that? 
                # you remember when movies had values and soul?
                # great...
                cmds.ToolSettingsWindow()


    # instead of global enable/disable for focus in/out,
    # find all hotkeys and block their signals
    #
    def setHotkeysEnabled(self, state):
        w = self.widget()
        if not w:
            return
        for a in w.findChildren(QtGui.QAction):
            if state:
                valid = a.property("uiMasterEnabled")
                if valid is not None:
                    a.setEnabled(valid)
            else:
                a.setProperty("uiMasterEnabled", a.isEnabled())
                a.setEnabled(False)
                #a.blockSignals(not state)


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------




8888888b.                                   888     888d8b                      
888   Y88b                                  888     888Y8P                      
888    888                                  888     888                         
888   d88P888d888 .d88b. 888  888888  888   Y88b   d88P888 .d88b. 888  888  888 
8888888P" 888P"  d88""88b`Y8bd8P'888  888    Y88b d88P 888d8P  Y8b888  888  888 
888       888    888  888  X88K  888  888     Y88o88P  88888888888888  888  888 
888       888    Y88..88P.d8""8b.Y88b 888      Y888P   888Y8b.    Y88b 888 d88P 
888       888     "Y88P" 888  888 "Y88888       Y8P    888 "Y8888  "Y8888888P"  
                                      888                                       
                                 Y8b d88P                                       
                                  "Y88P"                                      


#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""
# Reimplementation of QGraphicsView - so that when resized,
# it resizes the widget (via proxy) that it displays
# Also catches focusIn/focusOut events to enable/disable current proxy
#
class WidgProxyView(QtGui.QGraphicsView):
    def __init__(self, scene=None, parent=None, pane=None):
        self.base = super(WidgProxyView, self)
        self.base.__init__(scene, parent)
        self.pane = pane
        self.prevProxy = None
        self.proxyDrag = False
        self.dragTarget = None
        self.topLevelTarget = None
        # each view needs a child focus filter, so that 
        # currProxy and widget can be reliably found
        self.childFocusFilter = ChildFocusFilter(self)

    
    def currProxy(self):
        index = self.pane.uiTabBar.currentIndex()
        proxy = None
        if index != -1:
            proxy = self.pane.loadedUIs[index][3]
        return proxy
    
    def resizeEvent(self, event):
        self.base.resizeEvent(event)
        proxy = self.currProxy()
        if proxy and proxy.widget():
            size = event.size()
            #proxy.widget().resize(size)
            proxy.widget().setMinimumSize(size)
            proxy.widget().setMaximumSize(size)
            self.matchPos(proxy)
        event.accept()

    # Wheel event should be good for reactivation
    #
    def wheelEvent(self, event):
        if not self.hasFocus():
            self.activateWindow()
            self.setFocus()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # try different step values
            step = event.delta() / 4

            p = self.pane.position
            self.incrementSplitter(self.pane.uim.mainSplitter, p[0], step)
            self.incrementSplitter(self.pane.parent(), p[1], step)

            event.accept()
            return 
        self.base.wheelEvent(event)


    # increase/decrease size of given widget within parent splitter
    #
    def incrementSplitter(self, spl, widgIndex, step):
        sizes = spl.sizes()
        n = len(sizes)
        for i in range(n):
            # this is the one, increment
            if i == widgIndex:
                sizes[i] += step
            else:
                sizes[i] -= (step / (n - 1))
        
        spl.setSizes(sizes)
    
    
    # catch focusIn and make it enable currUI
    #
    def focusInEvent(self, event):
        self.base.focusInEvent(event)
        proxy = self.currProxy()
        if not proxy or not proxy.widget():
            return
        proxy.widget().setEnabled(True)
        #proxy.setHotkeysEnabled(True)
        proxy.show()
        self.scene().setFocusItem(proxy)

        self.prevProxy = proxy
        self.matchPos(proxy)
        
        # refocusing from a popup bugs out the popup, making it unusable
        # and at times generating fatal errors
        if event.reason() != QtCore.Qt.FocusReason.PopupFocusReason:
            focus = proxy.widget().property("proxyFocus")
            if focus:
                # Directly using focus causes fatal errors,
                # so need to refresh the reference because obviously
                # something is wrong with it. It could be stale.
                c = proxy.widget().findChildren(type(focus))
                for w in c:
                    if w is focus:
                        w.setFocus()
                        break
            else:
                proxy.widget().setFocus()

    
    # Disable currUI when focus is lost, unless
    # focus is being given to a child
    #
    def focusOutEvent(self, event):
        self.base.focusOutEvent(event)
        if not self.prevProxy or not self.prevProxy.widget():
            return
        widg = self.prevProxy.widget()
        newF = QtGui.QApplication.focusWidget()
        isSelf = newF is self

        # when widgets vanish, they cause fatal errors upon
        # trying to refocus. solution is simple!
        focus = widg.focusWidget()
        if not focus or focus.isVisible():
            widg.setProperty("proxyFocus", focus)

        # If new focus is not the uiView, either it's modal or not.
        # Kind of need to tiptoe around modal widgets, 
        # they tend to blow up if you use findChildren().
        # In either case, check for abstract scroll areas
        # due to Qt bug with bypassgraphicsproxy flag and scroll areas.
        # Then ensure focus is sent back to the uiView
        if not isSelf:
            modal = QtGui.QApplication.activeModalWidget()
            if modal:
                self.forceScrollAreaUpdate(modal)
                modal.destroyed.connect(self.forceRefocus)
            else:
                # NOW it's safe to check if focus is a child,
                # but newF may still be None
                if not newF:
                    newF = QtGui.QApplication.activeWindow()
                isChild = newF in widg.findChildren(type(newF))
                if isChild:
                    win = newF.window()
                    self.forceScrollAreaUpdate(win)
                    win.removeEventFilter(self.childFocusFilter)
                    win.installEventFilter(self.childFocusFilter)
                else:
                    # "regular" case: focusing on main maya window,
                    # model editor, etc.
                    # disable NOT the widget itself, but actions/shortcuts?
                    self.scene().setFocusItem(None)
                    widg = self.prevProxy.widget()
                    widg.setEnabled(False)
                    #self.prevProxy.setHotkeysEnabled(False)
        # this is the case for popups - focus IS self still.
        # docs say both parent and popup are "active window"
        elif event.reason() == QtCore.Qt.FocusReason.PopupFocusReason:
            popup = QtGui.QApplication.activePopupWidget()
            self.forceScrollAreaUpdate(popup)
            # graphicsScene item grabs mouse events,
            # and when the popup "steals" the mouseReleaseEvent,
            # this prevents mouse clicks from going where they should
            # fix by just explicitly ungrabbing mouse
            grabber = self.scene().mouseGrabberItem()
            if grabber:
                grabber.ungrabMouse()


    def forceRefocus(self):
        self.activateWindow()
        self.pane.uiTabBar.setFocus()
        self.setFocus()

    # Scroll areas in child windows of graphics proxy'd widgets
    # are BUGGED if the bypassgraphicsproxywidget flag is set.
    # They do not properly update on their own when scrolled.
    # 
    def forceScrollAreaUpdate(self, win):
        self.forceScrollAreaInstantiation(win)
        scrollAreas = win.findChildren(QtGui.QAbstractScrollArea)
        for a in scrollAreas:
            v = a.viewport()
            # get both bars
            for s in [a.verticalScrollBar(), a.horizontalScrollBar()]:
                try:
                    s.valueChanged.disconnect(v.update)
                except RuntimeError:
                    # if it's not already connected, it throws an error
                    # when you try to disconnect. ignore.
                    pass
                s.valueChanged.connect(v.update)

    # Some viewports do not exist until they are accessed
    # by user or by code.
    # This method forces their creation, just in case
    # any are QAbstractScrollAreas (which they often are)
    def forceScrollAreaInstantiation(self, widg):
        for c in widg.children():
            if hasattr(c, "viewport"):
                c.viewport()
            if hasattr(c, "view"):
                c.view()
            self.forceScrollAreaInstantiation(c)


    # React to being moved, move proxy along with
    #
    def moveEvent(self, event):
        self.base.moveEvent(event)
        proxy = self.currProxy()
        if proxy and proxy.widget():
            self.matchPos(proxy)
        event.accept()

    # Match position
    def matchPos(self, proxy):
        proxy.show()
        proxy.widget().show()
        pos = self.mapToGlobal(QtCore.QPoint(0, 0))
        proxy.widget().move(pos)
        self.centerOn(proxy)

    # Attempt to deal with proxy/widget being destroyed
    # by means outside of uiMaster's control - e.g., cmds.deleteUI
    # Sometimes, though, widgets refresh themselves on scene reset,
    # resulting in a false triggering of this. 
    #
    def widgetKilled(self):
        l = self.pane.loadedUIs
        for i in xrange(len(l)):
            try:
                # WILL throw error if it's been destroyed
                l[i][3].widget()
            except RuntimeError:
                n = l[i][0]
                src = l[i][1]
                curr = self.pane.uiTabBar.currentIndex()
                cmds.warning("uiMaster: Error retrieving UI \"{0}\". "
                                "Removed.".format(n))
                self.pane.deleteTab(i, True)
                QtCore.QTimer.singleShot(300, partial(
                                    self.delayedRefreshCheck, n, src, i, curr))
                break
            except:
                raise
        

    # immediate check of getMayaChild results in error because
    # object construction is not yet complete
    #
    def delayedRefreshCheck(self, name, src, index, curr):
        newVer = getMayaChild(name)
        if newVer:
            cmds.warning("uiMaster: Just kidding, found it again. Reloading.")
            newI = len(self.pane.loadedUIs)
            self.pane.widgToTab(newVer, name, src)
            self.pane.uiTabBar.moveTab(newI, index)
            self.pane.uiTabBar.setCurrentIndex(curr)

    
    # UIVIEW is the first to receive drag and drop events,
    # so have to filter through and see who accepts it.
    # order: proxy -> (tab -> pane) (-> auto accept, so that
    # move events will still trigger dragEnterEvents which the proxy
    # may want)
    def dragEnterEvent(self, event):
        # enabled view's currently visible ui so that it can accept
        # whatever drag events it would normally.
        # If it's a uiTab drag, it will be disabled again
        # in uiTabbar.dragEnterEvent
        p = self.currProxy()
        if not p or not p.widget():
            self.pane.dragEnterEvent(event)
            return
        w = p.widget()
        w.setEnabled(True)

        target = self.getDragDropTarget(event, w)
        # attempt to save relative reference as a property in widget
        w.setProperty("topDragTarget", target)
        # Send dragEnter event that propogates up 
        # proxyDrag is True if the widget wants the event
        self.proxyDrag = self.tryEnterEvent(event, target, w)


    # Move events are much different, because they are all
    # possible enter events for a different widget inside the graphicsscene
    #
    def dragMoveEvent(self, event):
        # Move events are auto-accepted, so have to 
        # explicitly ignore so that it goes to the right place
        event.setAccepted(False)
        p = self.currProxy()
        if not p or not p.widget():
            self.pane.dragMoveEvent(event)
            return
        w = p.widget()

        savedTopLevel = w.property("topDragTarget")
        target = self.getDragDropTarget(event, w)
        # if target is different from saved target, then try dragEnterEvents
        if target is not savedTopLevel:
            w.setProperty("topDragTarget", target)
            # send dragLeave enter to previous target
            dragTarget = w.property("dragTarget")
            if dragTarget:
                QtGui.QApplication.sendEvent(
                                    dragTarget, QtGui.QDragLeaveEvent())
            # Send enter event to new target and propogate up
            self.proxyDrag = self.tryEnterEvent(event, target, w)
        
        if self.proxyDrag:# and self.dragTarget:
            # if an enter event has been accepted, send 
            # the regular move event to self.dragTarget
            dragTarget = w.property("dragTarget")
            tPos = dragTarget.mapFrom(w, event.pos())
            widgEvent = QtGui.QDragMoveEvent(tPos, event.possibleActions(), 
                                event.mimeData(), event.mouseButtons(), 
                                event.keyboardModifiers())
            widgEvent.setDropAction(event.dropAction())
            self.sendDragDropEvent(event, widgEvent, dragTarget)

        #if self.proxyDrag:
            #self.base.dragMoveEvent(event)
            #self.sendDragDropEvent(event)
        if not event.isAccepted():
            self.pane.dragMoveEvent(event)


    def dragLeaveEvent(self, event):
        if self.proxyDrag:# and self.dragTarget:
            w = self.currProxy().widget()
            #w.setEnabled(False)
            dragTarget = w.property("dragTarget")
            QtGui.QApplication.sendEvent(
                                dragTarget, QtGui.QDragLeaveEvent())
            self.proxyDrag = False
            w.setProperty("dragTarget", None)
            w.setProperty("topDragTarget", None)
        else:
            self.pane.dragLeaveEvent(event)


    def dropEvent(self, event):
        if self.proxyDrag:# and self.dragTarget:
            w = self.currProxy().widget()
            dragTarget = w.property("dragTarget")
            tPos = dragTarget.mapFrom(w, event.pos())
            widgEvent = QtGui.QDropEvent(tPos, event.possibleActions(), 
                                event.mimeData(), event.mouseButtons(), 
                                event.keyboardModifiers())
            self.sendDragDropEvent(event, widgEvent, dragTarget)
            self.proxyDrag = False
            w.setProperty("dragTarget", None)
            w.setProperty("topDragTarget", None)
        else:
            self.pane.dropEvent(event)
        
        self.activateWindow()
        self.pane.uiTabBar.setFocus()
        self.setFocus()


    # isolate the current CHILD WIDGET - send event to it
    # perform checks, enable, send event.
    # There is a bit of offset so a new event of the same type
    # must be sent because stupid drag events don't have a 
    # stupid .setPos() method
    def getDragDropTarget(self, event, w):
        t = w.childAt(event.pos())
        if not t:
            t = w
        return t


    def sendDragDropEvent(self, event, widgEvent, target):
        QtGui.QApplication.sendEvent(target, widgEvent)
        event.setAccepted(widgEvent.isAccepted())
        return event.isAccepted()


    # Send new dragEnter event to target 
    # and propgate it up to all parents.
    #
    def tryEnterEvent(self, event, target, w):
        if not w.isAncestorOf(target):
            w.setProperty("dragTarget", None)
            # PASS THE ENTER EVENT ALONG TO PANE!
            self.pane.dragEnterEvent(event)
            # Sometimes, event is still not accepted.
            # However, we want move events anyway, because
            # target may change. So just accept.
            if not event.isAccepted():
                event.accept()
                event.setDropAction(QtCore.Qt.IgnoreAction)
            return False
        if not target.isEnabled() or not target.acceptDrops():
            return self.tryEnterEvent(event, target.parentWidget(), w)

        # Base case - make new enter event
        tPos = target.mapFrom(w, event.pos())
        widgEvent = QtGui.QDragEnterEvent(tPos, event.possibleActions(), 
                                event.mimeData(), event.mouseButtons(), 
                                event.keyboardModifiers())
        widgEvent.setDropAction(event.proposedAction())
        
        result = self.sendDragDropEvent(event, widgEvent, target)
        event.setDropAction(widgEvent.dropAction())

        # send event and set new self.dragTarget
        if result:
            w.setProperty("dragTarget", target)
            return True
        else:
            return self.tryEnterEvent(event, target.parentWidget(), w)


    # Try to intercept help events so tooltips can last longer
    #
    def viewportEvent(self, event):
        t = event.type()
        if t in [QtCore.QEvent.ToolTip, QtCore.QEvent.WhatsThis]:
            p = self.currProxy()
            if p and p.widget():
                w = p.widget()
                # send a manufactured help event event to subwidget
                # 
                gPos = QtGui.QCursor.pos()
                pos = w.mapFromGlobal(gPos)
                targ = w.childAt(pos)
                ttEvent = QtGui.QHelpEvent(t, pos, gPos)

                QtGui.QApplication.sendEvent(targ, ttEvent)
                event.setAccepted(ttEvent.isAccepted())
                return event.isAccepted()
            
        return self.base.viewportEvent(event)


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------




888     888d8b8888888b.                          
888     888Y8P888   Y88b                         
888     888   888    888                         
888     888888888   d88P 8888b. 88888b.  .d88b.  
888     8888888888888P"     "88b888 "88bd8P  Y8b 
888     888888888       .d888888888  88888888888 
Y88b. .d88P888888       888  888888  888Y8b.     
 "Y88888P" 888888       "Y888888888  888 "Y8888    




#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""
class UiPane(QtGui.QWidget):
    def __init__(self, parent, vIndex, hIndex, uim):
        self.base = super(UiPane, self)
        self.base.__init__(parent)
        # loadedUIs[i][0] = name
        # loadedUIs[i][1] = source 
        # loadedUIs[i][2] = size
        # loadedUIs[i][3] = proxy(not saved)
        # loadedUIs[i][4] = focus widget
        # loadedUIs[i][5] = position
        self.loadedUIs = []
        # parent is the horizontal splitter
        self.position = (vIndex, hIndex)
        self.uim = uim
        self.fileDrop = False
        self.setAcceptDrops(True)

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.setLayout(self.verticalLayout)

        self.welcomeScreen = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.welcomeScreen)
        self.welcomeScreen.setLayout(self.layout)
        self.label = QtGui.QLabel("Drag and drop tabs or files here.", 
                                    self.welcomeScreen)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.horiz = QtGui.QHBoxLayout(self.welcomeScreen)
        self.layout.addLayout(self.horiz)
        self.button = QtGui.QPushButton(self.welcomeScreen)
        self.button.setText("Delete Pane")
        self.button.setToolTip("Delete this pane")
        self.button.setSizePolicy(QtGui.QSizePolicy.Maximum, 
                                    QtGui.QSizePolicy.Maximum)
        self.horiz.addWidget(self.button)
        self.verticalLayout.addWidget(self.welcomeScreen)

        # uiWidget - tabbar and uiview
        self.uiWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiWidget.sizePolicy().hasHeightForWidth())
        self.uiWidget.setSizePolicy(sizePolicy)
        self.uiWidget.setObjectName("uiWidget")
        self.meatLayout = QtGui.QVBoxLayout(self.uiWidget)
        self.uiWidget.setLayout(self.meatLayout)
        self.meatLayout.setContentsMargins(0, 0, 0, 0)
        self.meatLayout.setSpacing(0)
        self.meatLayout.setObjectName("meatLayout")
        self.verticalLayout.addWidget(self.uiWidget)

        # the MEAT of a UiPane - the uiTabBar and uiView
        #
        self.uiTabBar = TabBar(self.uiWidget)
        self.uiTabBar.pane = self
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, 
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiTabBar.sizePolicy().hasHeightForWidth())
        self.uiTabBar.setSizePolicy(sizePolicy)
        self.uiTabBar.setMinimumSize(QtCore.QSize(20, 24))
        self.uiTabBar.setFixedHeight(24)
        self.uiTabBar.setObjectName("uiTabBar")
        self.meatLayout.addWidget(self.uiTabBar)

        self.uiView = WidgProxyView(self.uim.uiScene, self.uiWidget, self)
        self.uiView.setMinimumSize(QtCore.QSize(20, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, 
            QtGui.QSizePolicy.Expanding)
        self.uiView.setSizePolicy(sizePolicy)
        self.uiView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.uiView.setAcceptDrops(True)
        self.uiView.setStyleSheet("")
        self.uiView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.uiView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.uiView.setFrameShape(QtGui.QFrame.Shape.NoFrame)
        #self.uiView.setFrameShape(QtGui.QFrame.Shape.Box)
        self.uiView.setFrameShadow(QtGui.QFrame.Shadow.Raised)
        self.uiView.setObjectName("uiView")
        self.meatLayout.addWidget(self.uiView)
        self.welcomeScreen.show()
        self.uiWidget.hide()

        # occasional runtime errors - not sure why
        self.button.clicked.connect(partial(self.uim.deletePane, self))
        self.uiTabBar.setTabsClosable(True)
        self.uiTabBar.setExpanding(False)
        self.uiTabBar.setElideMode(QtCore.Qt.ElideRight)
        self.uiTabBar.tabCloseRequested.connect(self.deleteTab)
        self.uiTabBar.currentChanged.connect(self.changeTab)
        self.uiTabBar.tabMoved.connect(self.moveTab)


    def minimumSizeHint(self):
        return QtCore.QSize(75, 75)


    # TAB METHODS - mostly lifted from Ui_uiWidg
    # Close a tab - removes associated entry in loadedUIs
    # and uiStack, then checks if this is the last tabs
    #
    def deleteTab(self, index, alreadyDestroyed=False):
        info = self.loadedUIs.pop(index)
        self.uim.allUIs.remove(info)
        if not alreadyDestroyed:
            self.returnWinToMaya(info[3], info[2], info[0])
        self.uiTabBar.removeTab(index)
        if self.uiTabBar.count() == 0:
            self.uiWidget.hide()
            self.welcomeScreen.show()
        self.uim.saveState()


    # Called by signal "currentChanged"
    # Gets size of the widget inside the new tab
    # and resizes uiMaster
    #
    def changeTab(self, index):
        par = self.uim.parent()
        main = getMayaMainWindow()

        # Resize conditions:
        # (option is checked OR initializing[=initial sizing]) 
        # AND not maximized
        conditions = ((self.uim.settingsWin.resizeCheck.isChecked()
                    or self.uim.initializing)
                    and not par.isMaximized())
        if index != -1:
            # FIRST - ensure valid index
            try:
                self.loadedUIs[index]
            except IndexError:
                # no data, remove tab
                self.uiTabBar.removeTab(index)
                return

            # changing visibility of built-in docks (AE, tools, etc)
            # causes an evalDeferred(restoreLastPanelWithFocus)
            # so overwrite restoreLastPanelWithFocus proc to nothing
            mel.eval("global proc restoreLastPanelWithFocus(){}")
            # force focusOut to save focus widget
            # MUST trigger before widget is disabled
            self.uiTabBar.setFocus()

            deadProxies = []
            for x in self.loadedUIs:
                # changeTab is a good place to catch ghost proxies
                p = x[3]
                if p and p.widget():
                    # Stack correctly -
                    if x == self.loadedUIs[index]:
                        # p is new active tab
                        val = 1
                    else:
                        val = 0
                    p.setZValue(val)
                    #p.widget().setEnabled(val)
                    p.widget().setVisible(val)
                else:
                    deadProxies.append(self.loadedUIs.index(x))

            for i in deadProxies:
                self.deleteTab(i)

            # evalDeferred the re-source, AFTER visibility change
            mel.eval("evalDeferred \"source restoreLastPanelWithFocus.mel\"")
            # cycle focus back to trigger focusInEvent
            self.activateWindow()
            self.uiView.setFocus()

            #mainDict["uiMasterFocus"] = self.uiView
            #cmds.evalDeferred("uiMasterFocus.setFocus()")
           
            # if whole window resize is not desired
            # AND it's NOT initializing
            # proxy must resize to fill uiView. trigger resizeEvent.
            if (not self.uim.settingsWin.resizeCheck.isChecked() 
                    or par.isMaximized() 
                    or self.uim.mode == "panes" 
                    and not self.uim.initializing):
                s = self.uiView.size()
                self.uiView.resizeEvent(QtGui.QResizeEvent(s, s))

        # resize parent dock/window
        if conditions:
            # Maya docking system uses the "savedSize" widget property to
            # manage dockWidgets. Had to dig real deep to find that out.
            size = self.uim.sizeHint()
            if self.uim.floating:
                par.resize(size)
            else:
                par.setProperty("savedSize", size)
                # force update
                par.updateGeometry()


    # Convert widget size to uiMaster size
    #
    def padWidgSize(self, s):
        # For tab mode, size must be the size to resize uiMaster
        # For pane mode, size must be... what? Doesn't matter, since
        # pane mode ignores the stored size. So size should be the same.
        q = QtCore.QSize(s[0], s[1])
        size = (q + self.uim.size() 
                - self.uim.mainSplitter.size() 
                + QtCore.QSize(0, self.uiTabBar.height()))
        if not size.isValid():
            size = QtCore.QSize(300, 485)
        return size   


    # Called when a tab is moved:
    # inputs are old and new index
    # Rearranges the loadedUIs list
    # hopefully garbage collection doesn't delete
    # widg before insert needs to use it
    #
    def moveTab(self, old, new):
        widgData = self.loadedUIs.pop(old)
        self.loadedUIs.insert(new, widgData)
        # doesn't seem necessary ?
        self.uim.saveState()

    
    # Take widget, make it a new tab
    # and manage state
    #
    def widgToTab(self, widg, baseName, source):
        notAllowed = [getMayaMainWindow(), self.uim, self.uim.parent(),
                        self.uim.scriptWin, self.uim.infoWin, 
                        self.uim.settingsWin, self.uim.newPaneWin]
        if widg in notAllowed or baseName == __title__ or isinstance(
                                                        widg, Ui_uiMaster):
            # derp
            if not self.uim.initializing:
                cmds.warning(
                        "Right, stop that! Stop it. It's silly, very silly.")
            return
        # fix name if necessary, add tab
        name = self.fixName(baseName, source)
        self.uim.fixEdgeCases(name, widg, True)

        #widg.show()
        size = widg.size()
        widg.setMinimumSize(50, 50)
        widg.setMaximumSize(524287, 524287)
        
        widg.setWindowFlags(QtCore.Qt.BypassGraphicsProxyWidget |
                        QtCore.Qt.Window)
        # EMBED PROXY IN uiScene, TO AVOID FATAL ERRORS
        # This way, Maya gets to maintain ownership of its widgets
        # but uiMaster can still do whatever it needs to with them
        #
        # if it already has a proxy, DISCONNET
        # and try to clean up if it's in uiMaster
        p = widg.graphicsProxyWidget()
        if p:
            for i, w in enumerate(self.loadedUIs):
                if p == w[3]:
                    cmds.warning("Widget already loaded in!")
                    self.deleteTab(i)
                    break
            else:
                p.setWidget(None)

        proxy = GraphicsProxy(None, self.uiView)
        proxy.setWidget(widg)
        self.uim.uiScene.addItem(proxy)
        #self.uim.uiLayout.addItem(proxy)
        if not proxy.widget():
            cmds.warning("uiMaster: Problem connecting proxy to widget.")
            return

        self.loadedUIs.append([name, source, size.toTuple(), 
                    proxy, proxy.widget().focusWidget(), self.position])
        print("uiMaster: Adding {0}".format(name))

        # let UIM keep track of UIs in order added
        self.uim.allUIs.append(self.loadedUIs[-1])
        
        if not self.uiWidget.isVisible():
            self.uiWidget.show()
            self.welcomeScreen.hide()
        widg.show()

        index = self.uiTabBar.addTab(name)
        self.uiTabBar.setCurrentIndex(index)
        self.uiTabBar.currentChanged.emit(index)
        
        # allUIs is updated, check for "special" UIs
        fixFullscreenScript(name, self.uim.allUIs)

        # Save loadedUIs to script node in scene
        #
        self.uim.saveState()


    # Make sure name of pending tab is unique and isn't already loaded
    #
    def fixName(self, baseName, source):
        if not baseName:
            baseName = "Untitled Ui"
        name = baseName
        num = 0
        nameList = []
        
        for x in self.loadedUIs:
            nameList.append(x[0])
            if source in x:
                cmds.warning(
                    "Duplicate copies of the same UI could "
                    "result in unwanted behavior!")
    
        while name in nameList:
            num+=1
            name = baseName+" "+str(num)
        return name

    
    # Remove a widget from the uiScene and perform all
    # necessary internal cleanup
    #
    def returnWinToMaya(self, proxy, size, name):
        main = getMayaMainWindow()
        #proxy.show()
        #proxy.setHotkeysEnabled(True)
        widg = proxy.widget()
        if widg and widg not in main.children():
            widg.setParent(main)
        s = proxy.size().toSize()
        for c in main.children():
            if c is widg:
                proxy.setWidget(None)
                self.uim.fixEdgeCases(name, c, False)
                c.setWindowFlags(QtCore.Qt.Window)
                c.setEnabled(True)
                c.setMinimumSize(50, 50)
                c.setMaximumSize(524287, 524287)
                pos = c.pos()
                if pos.x() < 1:
                    pos.setX(100)
                if pos.y() < 1:
                    pos.setY(100)
                c.move(pos)
                if self.uim.settingsWin.disperseCheck.isChecked():
                    c.show()
                #c.resize(size[0], size[1])
                c.resize(s)
                break
        self.uim.uiScene.removeItem(proxy)
        proxy.close()
        # allUIs is updated
        fixFullscreenScript(name, self.uim.allUIs)


    # Receive two type of drag events - suitable files
    # and tabs dragged from other tabbars
    # If it's tab data, try just forwarding the event
    #
    def dragEnterEvent(self, event):
        data = event.mimeData()
        tabData = data.data("uiTabData")
        if tabData:
            self.uiTabBar.dragEnterEvent(event)
            return
        #self.uiTabBar.dragEnterEvent(event)
        #if event.isAccepted():
        #    return
        #self.uiView.dragEnterEvent(event)
        files = data.urls()
        if files:
            for f in files:
                if f.toLocalFile().endswith((".py", ".mel", ".ui")):
                    event.accept()
                    self.fileDrop = True
                    return

    
    # Move tabs within tabbar - 
    def dragMoveEvent(self, event):
        event.setAccepted(False)
        if self.uiTabBar.dragData:
            self.uiTabBar.dragMoveEvent(event)
            return
        if self.fileDrop:
            event.accept()

    
    def dropEvent(self, event):
        if self.uiTabBar.dragData:
            self.uiTabBar.dropEvent(event)
            return
        data = event.mimeData()
        qUrls = data.urls()
        files = [u.toLocalFile() for u in qUrls]
        uis = self.uim.uiFileHandler.getWidgets(None, files, False, None)
        for x in uis:
            w, n, s = x
            self.widgToTab(w, n, s)
        if self.fileDrop:
            event.accept()
            self.fileDrop = False

    
    def dragLeaveEvent(self, event):
        if self.uiTabBar.dragData:
            self.uiTabBar.dragLeaveEvent(event)
            return
        if self.fileDrop:
            event.accept()
            self.fileDrop = False


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------




8888888888d8b888           888    888                     888888                
888       Y8P888           888    888                     888888                
888          888           888    888                     888888                
8888888   888888 .d88b.    8888888888 8888b. 88888b.  .d88888888 .d88b. 888d888 
888       888888d8P  Y8b   888    888    "88b888 "88bd88" 888888d8P  Y8b888P"   
888       88888888888888   888    888.d888888888  888888  88888888888888888     
888       888888Y8b.       888    888888  888888  888Y88b 888888Y8b.    888     
888       888888 "Y8888    888    888"Y888888888  888 "Y88888888 "Y8888 888    




#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""
# Class for handling files, 
# whether passed in, user-select or auto-search
# Attempt to get a widget from ecah file 
# and return a tuple of object, name and source
#
class UiFileHandler(QtCore.QObject):
    def __init__(self, parent=None):
        self.base = super(UiFileHandler, self)
        self.base.__init__(parent)

    # the jumping off point for accessing all file handler methods
    #
    def getWidgets(self, method, files, quiet, savedName):
        if method == "auto":
            files = self.autoSearch()
        elif method == "manual":
            files = self.uiFileBrowser()

        uis = []
        for f in files:
            # safety first
            if not os.path.exists(f):
                if not quiet:
                    cmds.warning("File {0} does not exist!".format(f))
                continue

            f = f.replace(os.altsep, os.sep)
            baseName = os.path.basename(f).split(".")[0]
            # Make sure user isn't trying to load
            # uiMaster into itself
            #this = __file__.replace("\\", "/")
            if baseName == "uiMaster":# or this == f:
                cmds.warning("Right, stop that! Stop it. "
                        "It's silly, very silly.")
                return
            # new is a dict of form new[name] = widg
            new = self.getWidgFromFile(f, baseName, quiet, savedName)
            
            # get f relative to current Maya project directory
            proj = cmds.workspace(q=True, rootDirectory=True)
            try:
                relPath = os.path.relpath(f, proj).replace(os.sep, os.altsep)
            except ValueError:
                relPath = ""
            s = ("file", f, relPath)
            for n in new:
                w = new[n]
                uis.append((w, n, s))
        return uis


    # Auto find files: finds directories associated with each
    # reference in Maya scene, then returns any
    # .ui files or .py/.mel files with "ui" in their name
    def autoSearch(self):
        files = []
        refList = cmds.ls(references=True)
        for r in refList:
            d = os.path.dirname(cmds.referenceQuery(r, filename=True))
            """
            # Smart-stop feature?
            for x in self.loadedUIs:
                if dir in x:
                    continue
            """
            entries = os.listdir(d)
            for e in entries:
                e = e.lower()
                ui = ".ui" in e
                py = ".py" in e and "ui" in e
                mel = ".mel" in e and "ui" in e
                if ui or py or mel:
                    files.append(os.altsep.join((d, e)))
        if not files:
            win = QtGui.QMessageBox(self.parent())
            win.setWindowTitle("No UIs found")
            win.setText("Autosearch did not find any UIs"
                        "\n     in referenced directories.")
            win.addButton("Ok", QtGui.QMessageBox.AcceptRole)
            win.exec_()
            win.setParent(None)
        return files


    # Open a file browser for the user to choose a GUI file
    #
    def uiFileBrowser(self):
        fileWin = QtGui.QFileDialog(self.parent(), 
                    filter="Maya UI Files (*.ui *.py *.mel)")
        if fileWin.exec_():
            tarUI = fileWin.selectedFiles()
        else:
            tarUI = []
        # Condense loadedUIs, check for duplicates
        fileWin.setParent(None)
        loadedUIs = []
        for r in self.parent().panes:
            for p in r:
                for x in p.loadedUIs:
                    loadedUIs.append((x, p))
        for x, p in loadedUIs:
            if tarUI and tarUI[0] in x[1]:
                win = QtGui.QMessageBox(self.parent())
                win.setWindowTitle("Duplicate file")
                win.setIcon(QtGui.QMessageBox.Warning)
                win.setText("The selected file has already been loaded "
                        "into uiMaster!\n\nMultiple copies of the same UI can "
                        "cause unwanted behavior.")
                win.addButton("Load anyway", QtGui.QMessageBox.AcceptRole)
                win.addButton("Go to", QtGui.QMessageBox.YesRole)
                win.addButton("Choose another file", QtGui.QMessageBox.NoRole)
                win.addButton("Cancel", QtGui.QMessageBox.RejectRole)
                win.exec_()
                choice = win.clickedButton().text()
                if choice == "Choose another file":
                    tarUI = self.uiFileBrowser()
                elif choice == "Go to":
                    tarUI = []
                    p.uiTabBar.setCurrentIndex(p.loadedUIs.index(x))
                elif choice == "Cancel":
                    tarUI = []
                win.setParent(None)
                break
        return tarUI
    
    
    # Given a .ui, .py or .mel file, find any new widgets in them
    # by QUiLoader, running the file contents, or finding compiled 
    # QT code. Return widgets and their names. However, some files
    # will need commands to be called. 
    #
    def getWidgFromFile(self, f, name, quiet, savedName):
        new = {}
        if ".ui" in f:
            loader = QtUiTools.QUiLoader()
            widg = loader.load(f, self.parent())
            new[widg.windowTitle()] = widg
        elif ".py" in f:           
            # try RUNNING it straight up BEFORE searching for
            # compiled python "Ui_" classes
            new = self.runFileStraightUp(name, "python", f, savedName)
            if new == {}:
                new = self.getCompiledWidgets(f, name, quiet, savedName)
            if new == {} and not quiet:
                cmd = name + "."
                self.suggestCode(f, self.parent().scriptWin.pyWidg, cmd)

        elif ".mel" in f:
            new = self.runFileStraightUp(name, "mel", f, savedName)
            if new == {} and not quiet:
                self.suggestCode(f, self.parent().scriptWin.melWidg, "")
        else:
            cmds.error("Unrecognized file type. "
                    "Please load a Maya-compatible UI file"
                    "('.ui', '.py' or 'mel').")
        
        if new == "Invalid":
            new = {}

        return new


    # Given a file, either .py or .mel, run it via
    # mel.eval(source f) or exec(import)
    # For self-executing files, this will create a new widget
    # so need to be ready to catch it.
    #
    def runFileStraightUp(self, uiName, lang, f, savedName):
        new = {}
        # both python and MEL paths
        addPathToSession(f)
        # find main window children - checking for visibility too
        oldWins, oldVis = self.parent().findMayaChildWindows()

        try:
            if lang == "python":
                # see if main console knows it as a module
                # exec reload/import inside main dict
                if uiName in mainDict and inspect.ismodule(mainDict[uiName]):
                    print("Reloading {0}".format(uiName))
                    exec("reload({0})".format(uiName), mainDict)
                else:
                    print("Importing {0}".format(uiName))
                    exec("import {0}".format(uiName), mainDict)

            elif lang == "mel":
                # source runs code inside file, making procs available
                mel.eval("source \"{0}\"".format(uiName))
        except Exception as e:
            cmds.warning("uiMaster - Error importing {0} UI file. "
                    "Check file for validity. \nError:\n{1}".format(lang, 
                                                                    str(e)))
            # return "Invalid" so getWidgFromFile knows
            return("Invalid")

        newWins, newVis = self.parent().findMayaChildWindows()
        # get the set of windows which are either new OR newly visible
        widgList = (newWins - oldWins) | (newVis - oldVis)
        for w in widgList:
            # make sure it's a widget and get name
            if w.isWidgetType() and savedName in [w.windowTitle(), None]:
                new[w.windowTitle()] = w

        return new


    # Find all compiled Qt classes
    # ASK USER ABOUT EACH CLASS,
    # and return instances of each one they 'ok'
    #
    def getCompiledWidgets(self, f, name, quiet, savedName):
        new = {}
        clsList = []
        
        # At this point, module has been tested and is refreshed
        mod = mainDict[name]
        if not inspect.ismodule(mod):
            cmds.warning("Name is not a module")
            return
        # get all compiled Qt classes in module
        members = inspect.getmembers(mod, inspect.isclass)
        for m in members:
            # directly compiled QT code does NOT inherit QWidgets
            #if issubclass(m[1], QtGui.QWidget):
            if m[0].startswith("Ui_"):
                # accepted as compiled QT
                clsList.append(m)
        
        acceptAll = False
        i = 0
        #c[0] is clsName, c[1] is class object
        for c in clsList:
            i+=1
            clsName = c[0]
            cls = c[1]
            
            # Window to present user with found UIs
            if not acceptAll and not quiet:
                win = QtGui.QMessageBox(self.parent())
                win.setWindowTitle("Load specified widget?")
                win.setIcon(QtGui.QMessageBox.Question)
                win.setText("Found {0} class(es) recognized\n"
                            "as compiled QT widget(s).\n\n"
                            "Widget {1} of {0}: \"{2}\".\n\n"
                            "Load?".format(len(clsList), i, clsName))
                win.addButton("Load", QtGui.QMessageBox.AcceptRole)
                win.addButton("Load all", QtGui.QMessageBox.YesRole)
                win.addButton("Skip", QtGui.QMessageBox.NoRole)
                win.addButton("Cancel", QtGui.QMessageBox.RejectRole)
                win.exec_()
                response = win.clickedButton().text()
                if response == "Load all":
                    acceptAll = True
                elif response == "Skip":
                    win.setParent(None)
                    continue
                elif response == "Cancel":
                    win.setParent(None)
                    break
                win.setParent(None)
            
            try:
                widg = buildClass(cls)(getMayaMainWindow())
            except Exception as e:
                cmds.warning("Problem with class {0}:\n{1}".format(clsName, e))
            else:
                n = widg.windowTitle()
                # If restore is in progress (quiet),
                # right widget has windowTitle == savedName.
                # Add if it's the right one,
                # or if a regular load (not quiet)
                if not quiet or (quiet and savedName == n):
                    new[n] = widg
            win.setParent(None)
        return new


    # Run when nothing is found in a .py or .mel file
    #
    def suggestCode(self, f, cmdWidg, cmd):
        # need user input
        sWin = self.parent().scriptWin
        msg = ("No new UI found from running file: \n\n{0}\n\nMaybe a "
                "MEL or Python command is needed?\n\nEnter any "
                "additional code in the Script Box.".format(f))
        win = QtGui.QMessageBox(self.parent())
        win.setWindowTitle("No UI found")
        win.setIcon(QtGui.QMessageBox.Question)
        win.setText(msg)
        win.exec_()
        if not sWin.stackedWidget.currentWidget() is cmdWidg:
            sWin.changeLang()
        if cmd:
            cmdWidg.setText(cmd)
        else:
            cmdWidg.setText("")
        cmdWidg.moveCursor(QtGui.QTextCursor.End)
        self.parent().openSecondaryWin(sWin, self.parent().actionScript_Window)
        cmdWidg.setFocus()
        win.setParent(None)


"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------




8888888888                        888      8888888888d8b888888                           
888                               888      888       Y8P888888                           
888                               888      888          888888                           
8888888   888  888 .d88b. 88888b. 888888   8888888   888888888888 .d88b. 888d888.d8888b  
888       888  888d8P  Y8b888 "88b888      888       888888888   d8P  Y8b888P"  88K      
888       Y88  88P88888888888  888888      888       888888888   88888888888    "Y8888b. 
888        Y8bd8P Y8b.    888  888Y88b.    888       888888Y88b. Y8b.    888         X88 
8888888888  Y88P   "Y8888 888  888 "Y888   888       888888 "Y888 "Y8888 888     88888P'  




#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""


# Filter, installed on a loaded UI's child windows as they are given focus.
# Passes activation to uiMaster when they are closed/hidden/minimized,
# and re-activates its parent when it is activated
#
class ChildFocusFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        t = event.type()
        if t == QtCore.QEvent.WindowActivate:
            # reactivate widget
            self.parent().currProxy().widget().setEnabled(True)
            #self.parent().currProxy().setHotkeysEnabled(True)
            return True
        elif t == QtCore.QEvent.WindowDeactivate:
            # active window exists if user has selected a new window - 
            # in that case, disable proxy widget
            # active does not exist if the window was just closed -
            # in that case, send focus back to uiView
            act = QtGui.QApplication.activeWindow()
            if act:
                self.parent().currProxy().widget().setEnabled(False)
                #self.parent().currProxy().setHotkeysEnabled(False)
            else:
                self.parent().forceRefocus()
            return True
        elif t == QtCore.QEvent.Hide:
            obj.removeEventFilter(self)
            return True
        return QtCore.QObject.eventFilter(self, obj, event)


# Event filter for window activation changes:
# to allow uiMaster to hook windows into tabs
# Different behavior if docked
#
class ActiveWinFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        uiMaster = self.parent()
        main = getMayaMainWindow()
        if event.type() == QtCore.QEvent.ActivationChange:
            widg = QtGui.QApplication.activeWindow()
            if widg in main.children() and widg is not obj:
                pane = uiMaster.findBestPane()
                pane.widgToTab(widg, widg.windowTitle(), ("internal", widg))
            elif widg is main:
                uiMaster.unhookWins()
            # Else nothing
            # Make sure obj has focus to receive all events
            obj.activateWindow()
            obj.setFocus()
            return True
        # Any key press will end grabber mode
        #
        elif event.type() is QtCore.QEvent.KeyPress:
            uiMaster.unhookWins()
            return True
        else:
            # standard event processing
            return QtCore.QObject.eventFilter(self, obj, event)


# Another filter, for the cmdScrollFieldExecuter
# This one just watches for an "execute" command:
# numpad enter or ctrl + e
#
class CmdFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            ctrl = event.modifiers() == QtCore.Qt.ControlModifier
            e = event.key() == QtCore.Qt.Key_E
            numEnter = event.key() == QtCore.Qt.Key_Enter
            if ctrl and e or numEnter:
                self.parent().addWidgFromCode()
                return True
        return QtCore.QObject.eventFilter(self, obj, event)


# Event filter to add hotkey switching between tabs
# 1-8, can turn off in settings
#
class HotkeyFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            hotkeys = {QtCore.Qt.Key_1: 0, QtCore.Qt.Key_2: 1,
                       QtCore.Qt.Key_3: 2, QtCore.Qt.Key_4: 3,
                       QtCore.Qt.Key_5: 4, QtCore.Qt.Key_6: 5,
                       QtCore.Qt.Key_7: 6, QtCore.Qt.Key_8: 7}
            m = QtGui.QApplication.mouseButtons()
            rmb = (m == QtCore.Qt.RightButton)
            k = event.key()
            if rmb and k in hotkeys.keys():
                self.installRefocus(obj)

                par = self.parent()
                par.activateWindow()
                par.defaultPane.uiTabBar.setCurrentIndex(hotkeys[event.key()])
                par.defaultPane.uiTabBar.setFocus()
                return True
            elif rmb and k == QtCore.Qt.Key_Space:
                # show/hide uim
                dock = self.parent().parent()
                vis = dock.isVisible()
                if not vis:
                    self.installRefocus(obj)
                    focus = dock.focusWidget()
                    if type(focus) is WidgProxyView:
                        focus.pane.uiTabBar.setFocus()
                dock.setVisible(not vis)
                return True
        # global else
        return QtCore.QObject.eventFilter(self, obj, event)


    # A way to refocus on uiMaster after RMB release event gives
    # focus back to obj
    def installRefocus(self, obj):
        par = self.parent( )
        pos = QtGui.QCursor.pos()
        # widg is the marking menu if it exists, or widget under mouse
        widg = QtGui.QApplication.widgetAt(pos)
        if widg and not par.hotkeying:
            # widget under mouse gets the event filter in all cases
            # but one: uiM is floating and the click is in Maya.
            # In this case, have to ignore the marking menu
            if widg.window() is not par.parent() and par.floating:
                widg = obj.focusWidget()
            widg.removeEventFilter(par.hotkeyRefocusFilter)
            widg.installEventFilter(par.hotkeyRefocusFilter)

        par.hotkeying = True


# Filter applied to widget under mouse during hotkey event, to make it
# send focus back to uiMaster upon completion of the hotkey change (rmb release)
#
class HotkeyRefocusFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if (self.parent().hotkeying 
                and QtGui.QApplication.mouseButtons() != QtCore.Qt.RightButton):
            par = self.parent()
            par.hotkeying = False
            par.activateWindow()
            focus = par.focusWidget()
            if type(focus) is TabBar:
                focus = focus.pane.uiView
            if not focus:
                focus = par
            focus.setFocus()
            obj.removeEventFilter(self)
        
        return QtCore.QObject.eventFilter(self, obj, event)


# Event filter to run behaviors 
# upon the dockwidget envelope being closed, resized, or moved
# Spontaneity helps determine whether resize is saved
# move all UIs to match position upon dock moving
#
class CloseResizeFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        t = event.type()
        if t == QtCore.QEvent.Close:
            # protect the script box from being abused to make trouble
            if obj.widget().scriptWin.safeMode:
                cmds.warning("Right, stop that! Stop it. It's silly, very silly.")
                event.ignore()
                return True
            obj.widget().close()
            return True
        elif t == QtCore.QEvent.Resize:
            obj.widget().dockResized(event.spontaneous())
            return True
        elif t == QtCore.QEvent.Move:
            obj.widget().paneMoveResize()
        return QtCore.QObject.eventFilter(self, obj, event)
  
"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------




888b     d888        d8b            .d8888b. 888                         
8888b   d8888        Y8P           d88P  Y88b888                         
88888b.d88888                      888    888888                         
888Y88888P888 8888b. 88888888b.    888       888 8888b. .d8888b .d8888b  
888 Y888P 888    "88b888888 "88b   888       888    "88b88K     88K      
888  Y8P  888.d888888888888  888   888    888888.d888888"Y8888b."Y8888b. 
888   "   888888  888888888  888   Y88b  d88P888888  888     X88     X88 
888       888"Y888888888888  888    "Y8888P" 888"Y888888 88888P' 88888P' 




#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""
# QT -> PY COMPILED CODE:
# uiMaster, the filling for the mainWindow to be factory-made later on
#----------------------------------------------------------------------
# MAIN CLASS
# MAIN CLASS
# MAIN CLASS

class Ui_uiMaster(object):
    def setupUi(self, uiMaster):    
        uiMaster.setObjectName("uiMaster")
        uiMaster.resize(300, 485)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(uiMaster.sizePolicy().hasHeightForWidth())
        uiMaster.setSizePolicy(sizePolicy)
        uiMaster.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.Widget)
        self.centralwidget = QtGui.QWidget(uiMaster)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        #self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        #self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout_4.addWidget(self.scrollArea)

        self.mainSplitter = QtGui.QSplitter(self.centralwidget)
        self.mainSplitter.setOrientation(QtCore.Qt.Vertical)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.mainSplitter.setSizePolicy(sizePolicy)
        self.verticalLayout_4.addWidget(self.mainSplitter)
        self.mainSplitter.splitterMoved.connect(self.paneMoveResize)
        #colors
        bg = self.palette().color(QtGui.QPalette.Base).name()
        hover = self.palette().color(QtGui.QPalette.WindowText).name()
        ss = ("QSplitter::handle{{background: {0};}} "
            "QSplitter::handle:hover{{background: {1};}}".format(bg, hover))
        self.mainSplitter.setStyleSheet(ss)
        #self.scrollArea.setWidget(self.mainSplitter)

        self.uiScene = QtGui.QGraphicsScene(self.mainSplitter)

        self.newPaneWin = PaneOverlay(self)
        self.newPaneWin.splitter = self.mainSplitter

        # need to keep references to the row and pane objects around
        # or else they can get unceremoniously garbage collected
        self.layoutMode = "rows"
        self.rows = []
        self.panes = []
        self.defaultRow = self.addNewRow()
        self.defaultPane = self.defaultRow.widget(0)

        # This is the welcomeScreen for defaultPane
        self.welcomeScreen = QtGui.QLabel(self.centralwidget)
        self.welcomeScreen.setEnabled(False)
        self.welcomeScreen.setMinimumSize(155, 40)
        font = QtGui.QFont()
        font.setFamily("Cordia New")
        font.setPointSize(18)
        self.welcomeScreen.setFont(font)
        self.welcomeScreen.setMouseTracking(True)
        self.welcomeScreen.setTextFormat(QtCore.Qt.AutoText)
        self.welcomeScreen.setScaledContents(False)
        self.welcomeScreen.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.welcomeScreen.setObjectName("welcomeScreen")

        # uiView will be replaced by multiple instances of UiPane,
        # which each is made up of a TabBar and a WidgProxyView
        #
        uiMaster.setCentralWidget(self.centralwidget)
        
        self.toolBar = QtGui.QToolBar(uiMaster)
        self.toolBar.setStyleSheet("QToolButton { width: 20px; height: 20px; }")
        self.toolBar.layout().setContentsMargins(1, 1, 1, 1)
        self.toolBar.layout().setSpacing(3)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.separatorWidg3 = QtGui.QWidget(uiMaster)
        self.separatorWidg3.setFixedSize(6, 6)
        self.toolBar.addWidget(self.separatorWidg3)
        self.actionAutoLoad_UIs = QtGui.QAction(uiMaster)
        self.actionAutoLoad_UIs.setText("")
        self.actionAutoLoad_UIs.setObjectName("actionAutoLoad_UIs")
        self.actionManually_Load_UI = QtGui.QAction(uiMaster)
        self.actionManually_Load_UI.setText("")
        self.actionManually_Load_UI.setIconText("")
        self.actionManually_Load_UI.setObjectName("actionManually_Load_UI")
        self.actionDock_Native_UIs = QtGui.QAction(uiMaster)
        self.actionDock_Native_UIs.setText("")
        self.actionDock_Native_UIs.setObjectName("actionDock_Native_UIs")
        self.actionScript_Window = QtGui.QAction(uiMaster)
        self.actionScript_Window.setText("")
        self.actionScript_Window.setObjectName("actionScript_Window")
        self.actionClose = QtGui.QAction(uiMaster)
        self.actionClose.setObjectName("actionClose")
        self.actionAddPanes = QtGui.QAction(uiMaster)
        self.actionAddPanes.setText("")
        self.actionAddPanes.setObjectName("actionAddPanes")
        self.actionSettings = QtGui.QAction(uiMaster)
        self.actionSettings.setText("")
        self.actionSettings.setObjectName("actionSettings")
        self.actionInfo = QtGui.QAction(uiMaster)
        self.actionInfo.setText("")
        self.actionInfo.setObjectName("actionInfo")
        self.toolBar.addAction(self.actionAutoLoad_UIs)
        self.toolBar.addAction(self.actionManually_Load_UI)
        self.toolBar.addAction(self.actionDock_Native_UIs)
        self.toolBar.addAction(self.actionScript_Window)
        self.separatorWidg = QtGui.QWidget(uiMaster)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.separatorWidg.setSizePolicy(sizePolicy)
        self.toolBar.addWidget(self.separatorWidg)
        self.toolBar.addAction(self.actionAddPanes)
        self.separatorWidg2 = QtGui.QWidget(uiMaster)
        self.separatorWidg2.setSizePolicy(sizePolicy)
        self.toolBar.addWidget(self.separatorWidg2)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionInfo)

        self.retranslateUi(uiMaster)

        # shove global welcome screen in place of usual one
        self.defaultPane.welcomeScreen.setParent(None)
        self.defaultPane.welcomeScreen = self.welcomeScreen
        self.defaultPane.verticalLayout.addWidget(
                    self.defaultPane.welcomeScreen)


        # custom
        #
        self.initializing = True
        #self.loadedUIs = []
        ptr = shiboken.getCppPointer(self.parent())
        # should be "uiMasterDockWidget"
        self.mayaName = omui.MQtUtil.fullName(ptr[0])
        self.tabsNode = "uiMasterLoadedUIs"
        self.openNode = "uiMasterConfigScriptNode"
        self.hook = 0
        self.floating = True
        self.hotkeying = False
        self.mode = "tabs"
        self.paneModeSize = QtCore.QSize(300, 485)
        # allUIs is self's shortcut to pane's loadedUIs entries
        self.allUIs = []
        self.hookFilter = ActiveWinFilter(self)
        self.hotkeyFilter = HotkeyFilter(self)
        self.hotkeyRefocusFilter = HotkeyRefocusFilter(self)

        ExecWin = buildClass(Ui_ExecWin)
        self.scriptWin = ExecWin(self)
        SettingsWin = buildClass(Ui_settingsWin)
        self.settingsWin = SettingsWin(self)
        self.settingsWin.restoreSettings()
        # get value right after settingsWin runs restore
        self.floating = self.parent().isFloating()
        InfoWin = buildClass(Ui_infoWin)
        self.infoWin = InfoWin(self)
        self.uiFileHandler = UiFileHandler(self)
        
        # button icons - first one is overlaid using QPainter
        # on a transparent background
        #
        autoIcon = QtGui.QPixmap(32, 32)
        autoIcon.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(autoIcon)
        stackPix = QtGui.QPixmap(":/layerEditor")
        searchPix = QtGui.QPixmap(":/zoom")
        painter.drawPixmap(2, 10, stackPix)
        painter.drawPixmap(3, -1, searchPix)
        painter.end()
        self.actionAutoLoad_UIs.setIcon(autoIcon)
        self.actionManually_Load_UI.setIcon(QtGui.QPixmap(":/fileOpen"))
        
        autoIcon2 = QtGui.QPixmap(32, 32)
        autoIcon2.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(autoIcon2)
        magnetPix = QtGui.QPixmap(":/makeLiveIcon").scaled(24, 24)
        painter.drawPixmap(0, 12, stackPix)
        painter.drawPixmap(8, 4, magnetPix)
        painter.end()
        self.actionDock_Native_UIs.setIcon(autoIcon2)
        
        self.actionScript_Window.setIcon(QtGui.QPixmap(":/cmdWndIcon"))
        self.actionAddPanes.setIcon(QtGui.QPixmap(":/defaultFourQuadLayout"))
        self.actionSettings.setIcon(QtGui.QPixmap(":/toolSettings"))
        self.actionInfo.setIcon(QtGui.QPixmap(":/info"))
        
        # connect actions to methods
        self.actionAutoLoad_UIs.triggered.connect(partial(self.addTab, "auto"))
        self.actionManually_Load_UI.triggered.connect(partial(self.addTab, "manual"))
        self.actionDock_Native_UIs.triggered.connect(self.hookWins)
        self.actionScript_Window.triggered.connect(partial(
                    self.openSecondaryWin, self.scriptWin, self.actionScript_Window))
        self.actionAddPanes.triggered.connect(self.newPaneWin.redraw)
        self.actionSettings.triggered.connect(partial(
                    self.openSecondaryWin, self.settingsWin, self.actionSettings))
        self.actionInfo.triggered.connect(partial(
                    self.openSecondaryWin, self.infoWin, self.actionInfo))
        
        self.toolBar.topLevelChanged.connect(self.toolBarDocked)

        if self.floating:
            self.reFloat(True)
        if cmds.objExists(self.tabsNode):
            self.restoreSavedState()
        else:
            self.settingsWin.restoreDefaultState()
        self.initializing = False

        QtCore.QMetaObject.connectSlotsByName(uiMaster)

    def retranslateUi(self, uiMaster):
        #uiMaster.setWindowTitle(QtGui.QApplication.translate("uiMaster", __title__, None, QtGui.QApplication.UnicodeUTF8))
        self.welcomeScreen.setText(QtGui.QApplication.translate("uiMaster", 
                "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; color:#b5b5b5;\">"
                "<br/>Welcome to Maya uiMaster."
                "<br/><br/><br/>No UIs are loaded right now."
                "<br/><br/>Use the Action Bar to load UIs:"
                "<br/><t/>&bull; From files"
                "<br/><t/>&bull; From command line"
                "<br/><t/>&bull; From existing windows"

                #"<br/>from files, command-line or existing windows."
                "</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("uiMaster", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoLoad_UIs.setToolTip(QtGui.QApplication.translate("uiMaster", "Search relevant directories for .ui files and files with \"ui\"\n"
"in the name, then attempt to load them into uiMaster", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManually_Load_UI.setToolTip(QtGui.QApplication.translate("uiMaster", "Load UI from file (.ui, .py, .mel).\n\nAlso adds the directory to MAYA_SCRIPT_PATH and Python module path.", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDock_Native_UIs.setToolTip(QtGui.QApplication.translate("uiMaster", "Enter window magnet mode, where you click on\n"
"other maya windows to pull them into uiMaster.\nPress any key to exit this mode.\n\nCustom UIs will need to be re-sourced from\nscript or file upon reloading scene", None, QtGui.QApplication.UnicodeUTF8))
        self.actionScript_Window.setToolTip(QtGui.QApplication.translate("uiMaster", "Open the nested script box. Any floating UIs created\n"
"with this tool are automatically pulled into uiMaster", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddPanes.setText(QtGui.QApplication.translate("uiMaster", "Create new rows and panes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("uiMaster", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setToolTip(QtGui.QApplication.translate("uiMaster", "Open uiMaster settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInfo.setToolTip(QtGui.QApplication.translate("uiMaster", "uiMaster software information", None, QtGui.QApplication.UnicodeUTF8))


    #----------------------------------------------------------------------
    # END COMPILED CODE:
    # General methods for main class
    #

    # Find sets of all child widgets of main
    # used in addWidgFromCode and runFileStraightUp
    #
    def findMayaChildWindows(self):
        wins = set()
        vis = set()
        for c in getMayaMainWindow().children():
            isTopLevel = (c.isWidgetType() and c.isWindow() or 
                                            c.inherits("QDockWidget"))
            if not isTopLevel:
                continue
            # only relevant windows/dockwidgets remain
            wins.add(c)
            if c.isVisible():
                vis.add(c)

        return wins, vis


    # weird-ass edge cases for the Tool Settings window,
    # presumably because it's ancient and losing its marbles
    #
    def fixEdgeCases(self, name, widg, loading):
        if name == "Tool Settings":
            if type(widg) != QtGui.QDockWidget:
                # it fucking forgets that it's a dockwidget
                # and somehow re-wraps itself as a QWidget
                # WHICH FUCKING INHERITS QDOCKWIDGET (?!?)
                # WHAT THE FACK, TOOL SETTINGS
                ptr = shiboken.getCppPointer(widg)[0]
                widg = shiboken.wrapInstance(long(ptr), QtGui.QDockWidget)
            main = getMayaMainWindow()
            if loading:
                widg.setFloating(True)
                main.removeDockWidget(widg)
                widg.setAllowedAreas(0)
            else:
                widg.setAllowedAreas(3)


    # Easier way to handle resizing - particularly when docked
    def sizeHint(self):
        if self.mode == "panes":
            return self.paneModeSize
        else:
            # tab mode, return current widget's size
            i = self.defaultPane.uiTabBar.currentIndex()
            if i == -1:
                return QtCore.QSize(300, 485)
            s = self.defaultPane.loadedUIs[i][2]
            return self.defaultPane.padWidgSize(s)


    # Response to visibility changing, for when it is in
    # a tabbed dock layout - must force the resize
    def visChanged(self, vis):
        if vis:
            self.parent().updateGeometry()
            # might as well try to catch the delay
            QtCore.QTimer.singleShot(900, self.parent().updateGeometry)
            QtCore.QTimer.singleShot(1800, self.parent().updateGeometry)

    
    # Called by parent dockwidget's resize event
    # 
    def dockResized(self, spon):
        # this value is returned by sizeHint to help docked mode work right
        if (self.floating and spon) or not self.floating:
            # This leaves behind the case of floating,
            # but not spontaneous - such as the auto resize
            # when control is docked
            self.saveSize()


    # Actually set the loadedUIs size value
    #
    def saveSize(self):
        par = self.parent()
        pms = par.size()

        for r in self.panes:
            for p in r:
                index = p.uiTabBar.currentIndex()
                if index == -1:
                    continue
                size = p.uiView.size().toTuple()
                if not self.floating:
                    area = getMayaMainWindow().dockWidgetArea(par)
                    # save new width only
                    if area in (1, 2):
                        size = (p.uiView.width(), p.loadedUIs[index][2][1])
                        pms = QtCore.QSize(par.width(), 
                                            self.paneModeSize.height())
                    elif area in (4, 8):
                        pass
                try:
                    p.loadedUIs[index][2] = size
                except IndexError:
                    # delayed call from last tab being closed, do nothing
                    pass
                except:
                    raise

        if self.mode == "panes":
            self.paneModeSize = pms
        self.saveState()


    # Called by dock move events and splitterMoved signal
    # EITHER - saves sizes OR explicitly calls pane.matchPos()
    #
    def paneMoveResize(self, pos=None, index=None):
        # if index is passed in, this means that it was a splitterMoved signal
        # so saveSize in this case
        if index:
            self.saveSize()
        else:
            for r in self.panes:
                for p in r:
                    proxy = p.uiView.currProxy()
                    if proxy and proxy.widget():
                        p.uiView.matchPos(proxy)

    
    # Parent method for tab adding
    #
    def addTab(self, method, files=[], quiet=False, savedName=None):
        # if files are passed in, type argument is None
        uis = self.uiFileHandler.getWidgets(method, files, quiet, savedName)

        for x in uis:
            # get widget, name and source
            w, n, s = x
            pane = self.findBestPane()
            pane.widgToTab(w, n, s)

    
    # Called whenever window is undocked,
    # this fixes the style
    #
    def reFloat(self, floating):
        par = self.parent()
        self.floating = floating
        if floating:
            par.setWindowFlags(QtCore.Qt.WindowType.Window)
            par.show()
            self.settingsWin.saveSettings("dockArea", 0)
            self.settingsWin.saveSettings("floating", True)
        else:
            area = getMayaMainWindow().dockWidgetArea(self.parent())
            self.settingsWin.saveSettings("dockArea", int(area))
            self.settingsWin.saveSettings("floating", False)
        
        # emit tab change to force resize
        self.defaultPane.uiTabBar.currentChanged.emit(
                            self.defaultPane.uiTabBar.currentIndex())


    # Change layout of splitters from vertical/horizontal
    #
    def setRowMode(self, state):
        if state:
            self.mainSplitter.setOrientation(QtCore.Qt.Vertical)
            for r in self.rows:
                r.setOrientation(QtCore.Qt.Horizontal)
            self.layoutMode = "rows"
        else:
            self.mainSplitter.setOrientation(QtCore.Qt.Horizontal)
            for r in self.rows:
                r.setOrientation(QtCore.Qt.Vertical)
            self.layoutMode = "columns"
        #self.saveSize()
        self.settingsWin.saveSettings("rowMode", state)


    # toolBar is docked - save location
    #
    def toolBarDocked(self, floating):
        if not floating:
            area = self.toolBarArea(self.toolBar)
            self.settingsWin.saveSettings("toolBarArea", area)


    # Enter window-hook mode, activated by user action
    # Change cursor and install event filter.
    #
    def hookWins(self):
        if self.hook == 0:
            curs = QtGui.QCursor(":/makeLiveIcon.png")
            QtGui.QApplication.setOverrideCursor(curs)
            self.hook = 1
            self.mainSplitter.setEnabled(False)
            if self.floating:
                self.parent().installEventFilter(self.hookFilter)
            else:
                getMayaMainWindow().installEventFilter(self.hookFilter)
            # Make sure uiMaster has focus so it receives
            # all events
            self.parent().activateWindow()
            self.parent().setFocus()

    
    # Undo window-hook mode
    #
    def unhookWins(self):
        QtGui.QApplication.restoreOverrideCursor()
        self.hook = 0
        self.parent().removeEventFilter(self.hookFilter)
        getMayaMainWindow().removeEventFilter(self.hookFilter)
        self.mainSplitter.setEnabled(True)
        self.mainSplitter.setFocus()


    """
    # Reimplementation to create "smart-focus" feature,
    # Smart focus resonds to mouse events, 
    # focusing or unfocusing uiMaster and the current UI
    #
    def enterEvent(self, event):
        if (self.hook == 0 and self.settingsWin.focusCheck.isChecked()
                    and not self.scriptWin.isActiveWindow()
                    and not self.settingsWin.isActiveWindow()
                    and not self.infoWin.isActiveWindow()):
            self.activateWindow()
            self.uiView.setFocus()
    
    
    # "Smart-focus": Leave disables current UI, sets new focus
    #
    def leaveEvent(self, event):
        index = self.uiTabBar.currentIndex()
        if (index != -1 and self.hook == 0 
                    and self.settingsWin.focusCheck.isChecked()
                    and not self.scriptWin.isActiveWindow()
                    and not self.settingsWin.isActiveWindow()
                    and not self.infoWin.isActiveWindow()):

            # widget under mouse - IGNORING uiMaster itself
            # and to make sure we're still in Maya
            self.parent().setAttribute(
                        QtCore.Qt.WA_TransparentForMouseEvents, True)
            target = QtGui.QApplication.widgetAt(QtGui.QCursor.pos())
            self.parent().setAttribute(
                        QtCore.Qt.WA_TransparentForMouseEvents, False)
            proxy = self.uiView.currProxy()
            active = QtGui.QApplication.activeWindow()
            # check for NoneTypes
            if None in [target, active, proxy] or not proxy.widget():
                return
            # avoid if active window is a child of proxy
            if active in proxy.widget().children():
                return
            
            #main = getMayaMainWindow()
            #panel = main.centralWidget().focusWidget()
            #main.activateWindow()
            target.activateWindow()
            target.setFocus()
    """

    
    # The function to make self.scriptWin/self.settings/self.info show
    #
    def openSecondaryWin(self, win, button):
        # move scriptWin to under action button - 
        # or above if it's docked on bottom
        rect = self.toolBar.actionGeometry(button)
        bottom = QtCore.Qt.ToolBarArea.BottomToolBarArea
        if self.toolBarArea(self.toolBar) == bottom:
            p = self.toolBar.mapToGlobal(rect.topLeft())
            height = QtCore.QPoint(0, win.height())
            p -= height
        else:
            p = self.toolBar.mapToGlobal(rect.bottomLeft())
        win.move(p)
        # Make sure windows don't go off right side of screen
        main = getMayaMainWindow()
        edge = main.x() + main.width()
        if win.x() + win.width() > edge:
            x = edge - win.width()
            win.move(x, win.y())
        edge = main.y() + main.height()
        win.show()
        if win.y() + win.height() > edge:
            y = edge - win.height()
            win.move(win.x(), y)
    
    
    # release all widgets back to maya
    # WITHOUT CALLING saveState() or altering loadedUIs
    def removeAllUIs(self):
        for r in self.panes:
            for p in r:
                # can cause problems with ghost proxies
                p.uiTabBar.currentChanged.disconnect(p.changeTab)
                for l in p.loadedUIs:
                    # to ensure name is correct
                    #w = l[3].widget()
                    #if w: print(w)
                    #else: print("NOTHING")
                    l[0] = l[3].widget().windowTitle()
                    self.allUIs.remove(l)
                    p.returnWinToMaya(l[3], l[2], l[0])


    # redefine close - possible use to save session
    # for restoration later??
    #
    def closeEvent(self, event):
        main = getMayaMainWindow()
        # check if close has been called by
        # scriptWin method - if so, REJECT.
        if self.scriptWin.safeMode:
            cmds.warning("Right, stop that! Stop it. It's silly, very silly.")
            event.ignore()
            return
        
        self.removeAllUIs()

        # Get rid of self.openNode (the one which
        # auto-opens uiMaster on scene load),
        # but LEAVE self.tabsNode in case user wants to
        # open another
        #
        if cmds.objExists(self.openNode):
            # Suspend Maya undo queue
            cmds.undoInfo(stateWithoutFlush=False)
            cmds.delete(self.openNode)
            cmds.undoInfo(stateWithoutFlush=True)

        cmds.setParent(topLevel=True)
        self.scriptWin.close()
        self.settingsWin.close()
        self.infoWin.close()
        main.removeEventFilter(self.hotkeyFilter)
        self.mainSplitter.removeEventFilter(self.hotkeyFilter)
        if self.hook == 1:
            self.unhookWins()
        main.removeDockWidget(self.parent())
        self.parent().close()
        cmds.deleteUI(self.mayaName)
        #event.accept()
    
    """
    #----------------------------------------------------------------------


    88888888888     888                                     888   8888888b.                                  
        888         888                                     888   888   Y88b                                 
        888         888                                     888   888    888                                 
        888  8888b. 88888b. .d8888b     8888b. 88888b.  .d88888   888   d88P 8888b. 88888b.  .d88b. .d8888b  
        888     "88b888 "88b88K            "88b888 "88bd88" 888   8888888P"     "88b888 "88bd8P  Y8b88K      
        888 .d888888888  888"Y8888b.   .d888888888  888888  888   888       .d888888888  88888888888"Y8888b. 
        888 888  888888 d88P     X88   888  888888  888Y88b 888   888       888  888888  888Y8b.         X88 
        888 "Y88888888888P"  88888P'   "Y888888888  888 "Y88888   888       "Y888888888  888 "Y8888  88888P' 


    #----------------------------------------------------------------------
    """

    # Called when user changes the "mode" radio setting
    # Re-draws the insides and saves settings
    #
    def setTabMode(self, state):
        # switch to tab mode if it has been turned ON
        if state:
            self.mode = "tabs"
            # suspend size saving til over with self.floating
            # to prevent size saving
            old = self.floating
            self.floating = True
            # Look at each UiPane, take every tab and
            # stuff them all into default UiPane
            toDelete = []
            for r in self.panes:
                ps = [p for p in r if p is not self.defaultPane]
                for p in ps:
                    while p.loadedUIs:
                        self.moveTabToNewPane(0, p, self.defaultPane)
                    # mark for deletion
                    toDelete.append(p)
            for p in toDelete:
                self.deletePane(p)
            self.floating = old
        # make sure new setting is saved
        self.settingsWin.saveSettings("tabMode", state)
    

    # switch to pane mode if it has been turned ON
    # examine each loadedUIs entry and
    # if position is NOT (0, 0), 
    # move tab to correct pane, creating new ones as needed
    #
    def setPaneMode(self, state):
        if state:
            self.mode = "panes"
            if self.layoutMode == "rows":
                wGetter = 0
                hGetter = 1
            else:
                wGetter = 1
                hGetter = 0
            # loadedUIs[i][5] is (row, col)
            # which only changes if self.mode == "panes"
            heights = {}
            widths = {}
            for w in self.allUIs:
                pos = w[5]
                # get new pane sizes based on averaging sizes
                vPos = pos[0]
                paneH = w[2][hGetter]
                if heights.has_key(vPos):
                    # height and divisor for averaging
                    h = heights[vPos][0] + paneH
                    n = heights[vPos][1] + 1
                    heights[vPos] = (h, n)
                else:
                    heights[vPos] = (paneH, 1)
                
                # now widths - almost guaranteed to be a bigger dict
                paneW = w[2][wGetter]
                if widths.has_key(pos):
                    l = widths[pos][0] + paneW
                    n = widths[pos][1] + 1
                    widths[pos] = (l, n)
                else:
                    widths[pos] = (paneW, 1)

                i = self.defaultPane.loadedUIs.index(w)
                newPane = self.getPaneAtPosition(pos)
                assert newPane.position == pos, \
                        "New pane position does not match saved position!"
                self.moveTabToNewPane(i, self.defaultPane, newPane)

            self.parent().resize(self.paneModeSize)
            # figure out the pane sizes based on saved
            # tab sizes - splitter automatically figures out conflicts

            v = []
            for i in xrange(len(heights)):
                r = self.rows[i]
                v.append(heights[i][0] / heights[i][1])
                rowWidths = []
                for n in xrange(r.count()):
                    val = widths[i, n]
                    avg = val[0] / val[1]
                    rowWidths.append(avg)
                r.setSizes(rowWidths)
            self.mainSplitter.setSizes(v)

        # make sure new setting is saved
        self.settingsWin.paneLayout.setEnabled(state)
        self.actionAddPanes.setEnabled(state)
        self.settingsWin.saveSettings("paneMode", state)


    # Take a tuple representing position, and make panes until
    # the specified one can be returned
    #
    def getPaneAtPosition(self, pos):
        row = pos[0]
        col = pos[1]
        newPane = self.defaultPane
        # create AS MANY PANES AS NECESSARY
        # til there are enough rows & columns
        while row > (len(self.panes) - 1):
            newRow = self.addNewRow()
            # must set newPane to the newly created 0 pane
            newPane = newRow.widget(0)
        while col > (len(self.panes[row]) - 1):
            newPane = self.addNewPaneToRow(
                                self.mainSplitter.widget(row))
        newPane = self.panes[row][col]
        return newPane


    # Move a tab from one UiPane to another
    # source and target are both UiPane objects
    #
    def moveTabToNewPane(self, index, source, target):
        if source is target:
            return
        # don't need to do anything besides
        # move loadedUIs entry and tab, since
        # changeTab just looks to loadedUIs and the scene
        info = source.loadedUIs.pop(index)
        if self.mode == "panes":
            info[5] = target.position
        target.loadedUIs.append(info)

        proxy = info[3]
        old = proxy.view
        proxy.destroyed.disconnect(old.widgetKilled)
        proxy.view = target.uiView
        proxy.destroyed.connect(proxy.view.widgetKilled)

        source.uiTabBar.removeTab(index)
        i = target.uiTabBar.addTab(info[0])

        if source.uiTabBar.count() == 0:
            source.uiWidget.hide()
            source.welcomeScreen.show()
        if target.uiTabBar.count() == 1:
            target.uiWidget.show()
            target.welcomeScreen.hide()

        self.saveState()
        target.uiTabBar.setCurrentIndex(i)
        target.uiTabBar.currentChanged.emit(i)
        return i


    # Add new widget to vertical splitter (global)
    #
    def addNewRow(self):
        newRow = QtGui.QSplitter(self)
        if self.layoutMode == "columns":
            newRow.setOrientation(QtCore.Qt.Vertical)
        # Set new row's height to 1/count
        # are other rows scaled automatically?
        count = self.mainSplitter.count() + 1
        heights = self.mainSplitter.sizes()
        newHeights = []
        for h in heights:
            newHeights.append(h * (count - 1) / count)
        newHeights.append(self.mainSplitter.height() / count)
        self.mainSplitter.addWidget(newRow)
        self.rows.append(newRow)
        self.panes.append([])
        self.addNewPaneToRow(newRow)
        self.newPaneWin.addButton(newRow)
        self.mainSplitter.setSizes(newHeights)
        newRow.splitterMoved.connect(self.paneMoveResize)
        return newRow


    # Add new pane to a particular row (local)
    #
    def addNewPaneToRow(self, row):
        vIndex = self.mainSplitter.indexOf(row)
        hIndex = row.count()
        newPane = UiPane(self, vIndex, hIndex, self)
        # other panes... SHOULD scale automatically
        widths = row.sizes()
        newWidths =  []
        for w in widths:
            newWidths.append(w * hIndex / (hIndex + 1))
        newWidths.append(row.width() / (hIndex + 1))
        row.addWidget(newPane)
        self.panes[vIndex].append(newPane)
        row.setSizes(newWidths)
        return newPane


    # Analyze the current pane layout to determine
    # where a new pane should be added.
    # It basically comes down to this:
    # Make new row, or not? If not, which one?
    #
    def findBestPane(self):
        # Keep it try, check for tab mode here
        if self.mode == "tabs":
            return self.defaultPane
        # First: gather intel. Find out:
        # If there are any empty panes;
        # Minimum and maximum panes per row
        numRows = len(self.panes)
        #maxPanes = self.defaultRow.count()
        #maxRow = self.defaultRow
        minPanes = self.defaultRow.count()
        minRow = self.defaultRow
        for i, r in enumerate(self.panes):
            for p in r:
                if not p.loadedUIs:
                    # 1) Empty pane = ideal. just return it and be done.
                    return p
            if len(r) < minPanes:
                minPanes= len(r)
                minRow = self.mainSplitter.widget(i)
        # 2) next choice is minRow - IF the number of rows is greater 
        # or equal to # of panes in any particular row
        if len(self.panes) >= minPanes:
            return self.addNewPaneToRow(minRow)
        #if maxPanes > minPanes:
        #    return self.addNewPaneToRow(minRow)
        # 3) last choice is to just add a new row
        newRow = self.addNewRow()
        return newRow.widget(0)


    # Delete rows/columns? Not automatic.
    # Perhaps a close button on the empty default screen?
    # 
    def deletePane(self, pane):
        if pane is self.defaultPane:
            return
        row = pane.parent()
        pos = pane.position
        vIndex = pos[0]
        hIndex = pos[1]
        self.panes[vIndex].pop(hIndex)
        pane.setParent(None)
        del(pane)
        count = row.count()
        # Position attribute needs to be updated when "middle"
        # panes are removed, as well as loadedUIs pos
        for i in range(hIndex, count):
            p = self.panes[vIndex][i]
            p.position = (vIndex, i)
            for l in p.loadedUIs:
                l[5] = (vIndex, i)

        # if it's the LAST PANE in a row, kill the row
        if count == 0:
            self.rows.pop(vIndex)
            self.panes.pop(vIndex)
            self.newPaneWin.deleteButton(row)
            row.setParent(None)
            del(row)
            # for each row after fix its "position" attribute
            for i in range(vIndex, self.mainSplitter.count()):
                for p in self.panes[i]:
                    p.position = (i, p.position[1])

        self.saveSize()

    """
    #----------------------------------------------------------------------


    8888888b.                        d8b        888                                    
    888   Y88b                       Y8P        888                                    
    888    888                                  888                                    
    888   d88P .d88b. 888d888.d8888b 888.d8888b 888888 .d88b. 88888b.  .d8888b .d88b.  
    8888888P" d8P  Y8b888P"  88K     88888K     888   d8P  Y8b888 "88bd88P"   d8P  Y8b 
    888       88888888888    "Y8888b.888"Y8888b.888   88888888888  888888     88888888 
    888       Y8b.    888         X88888     X88Y88b. Y8b.    888  888Y88b.   Y8b.     
    888        "Y8888 888     88888P'888 88888P' "Y888 "Y8888 888  888 "Y8888P "Y8888  


    #----------------------------------------------------------------------
    """
    
    # Method for saving current loadedUIs to node in scene
    # For "internal" type sources, widget is flattened because
    # pickling QWidgets isn't supported.
    #
    def saveState(self):
        # Flatten uncooperative widgtypes,
        # get relevant data from loadedUIs
        saveList = []
        vSizes = self.mainSplitter.sizes()
        hSizes = []
        for i, r in enumerate(self.panes):
            for p in r:
                for l in p.loadedUIs:
                    a = l[0]
                    b = l[1]
                    if l[1][0] == "internal":
                        b = ("internal", "")
                    c = l[2]
                    d = l[5]
                    # name, size, source
                    saveList.append([a, b, c, d])
            s = self.mainSplitter.widget(i).sizes()
            hSizes.append(s)
        paneSizes = [self.paneModeSize.toTuple(), vSizes, hSizes]
        
        # SUSPEND MAYA UNDO QUEUE - to avoid flooding it,
        # And avoid user conflict.
        cmds.undoInfo(stateWithoutFlush=False)
        
        # Create both save state nodes if they don't exist yet
        #
        if not cmds.objExists(self.openNode):
            # if it's loaded, start it up
            # when maya is starting, leave it to userSetup.mel
            cmd = "if (`pluginInfo -q -l \"uiMaster\"`) {uiMaster -a;}"
            # cmd also needs to check for namespace...
            # which, more and more, is seeming impossible

            #cmd = ("import uiMasterBeta; uiMasterBeta.makeUiMaster()")
            cmds.scriptNode(name=self.openNode, st=2, bs=cmd, stp="mel")
        if not cmds.objExists(self.tabsNode):
            cmds.scriptNode(name=self.tabsNode, st=0, stp="python")

        cmds.scriptNode(self.tabsNode, edit=True, 
                                            bs=str([saveList, paneSizes]))
        
        # Restore undo queue
        cmds.undoInfo(stateWithoutFlush=True)
    
    
    # called when uiMaster is auto-opened by a new scene -
    # 
    def additiveRestore(self):
        try:
            data = eval(cmds.getAttr(self.tabsNode+".before"))
            savedNames = [n[0] for n in data[0]]
            currNames = [n[0] for n in self.allUIs]
        except:
            return
        newNames = list(set(savedNames) - set(currNames))
        if newNames:
            newData = [a for a in data[0] if a[0] in newNames]
            win = QtGui.QMessageBox(self)
            win.setWindowTitle("New UIs found")
            win.setIcon(QtGui.QMessageBox.Question)
            win.setText("New scene has its own uiMaster tabs.\n\n"
                        "What's the plan?\n")
            win.addButton("Add to existing", QtGui.QMessageBox.AcceptRole)
            win.addButton("Replace existing", QtGui.QMessageBox.YesRole)
            win.addButton("Ignore", QtGui.QMessageBox.NoRole)
            win.exec_()
            response = win.clickedButton().text()
            if response == "Add to existing":
                self.restoreSavedState([newData, None], True)
            elif response == "Replace existing":
                # need to explicitly empty uiMaster, WITHOUT UIs dispersing
                oldDispVal = self.settingsWin.disperseCheck.isChecked()
                self.settingsWin.disperseCheck.setChecked(False)
                for r in self.panes:
                    for p in r:
                        while p.loadedUIs:
                            p.deleteTab(0)
                self.settingsWin.disperseCheck.setChecked(oldDispVal)
                # empty case restore, with data ALREADY RETRIEVED
                self.restoreSavedState(data)
            elif response == "Ignore":
                pass
            win.setParent(None)


    # Run only once, during initialization
    # Find old uiMasterLoadedUIs node in maya scene
    # the node's "before" attribute is the old loadedUIs list
    #
    def restoreSavedState(self, data=None, additive=False):
        # retrieve the list which is saved with the scene
        if not data:
            data = eval(cmds.getAttr(self.tabsNode+".before"))

        failedToLoad = self.addSavedUIs(data[0])
        
        if not additive:
            self.restorePaneSizes(data[1])

        # don't need saveSize, only saveState
        self.saveState()
        # Present single dialog alerting of the failures
        # Single all-purpose choice between script and file
        #
        if failedToLoad:
            self.skippedUIs(failedToLoad)
    

    # Now, go through each source in the list
    # "internal", "file", "mel", and "python"
    #
    def addSavedUIs(self, savedUIs):
        failedToLoad = []

        for t in savedUIs:
            sIndex = len(self.allUIs)
            name = t[0]
            # source is tuple of form (type, source)
            source = t[1]
            size = t[2]
            position = t[3]
            pane = self.defaultPane
            if self.mode == "panes":
                pane = self.getPaneAtPosition(position)

            # Check for existing first, but in a preliminary fashion.
            # This is a cautious check, which IGNORES uis which
            # exist but are not visible. It is assumed that they may
            # have random init behavior hidden in the cmd
            # (looking at you, charcoal). Besides, if it's hidden, 
            # duplicates are irrelevant.
            result = self.loadInternalWidg(name, source, pane, False)

            # THEN try from source
            if not result:
                self.loadFromSource(name, source, pane)

            # Only happens if nothing is found already,
            # and DO NOT need to skip anything this time
            if sIndex == len(self.allUIs):
                result = self.loadInternalWidg(name, source, pane)
            
            # Still nothing? Add to failedToLoad list
            if sIndex == len(self.allUIs):
                failedToLoad.append(name)
            else:
                for i in range(sIndex, len(self.allUIs)):
                    self.allUIs[i][5] = position
                    self.fixSize(i, size)

        return failedToLoad

    
    # Fix size for pane mode - both size of whole
    # dockWidget parent AND sizes of each pane within uiMaster
    #
    def restorePaneSizes(self, paneSizes):
        if self.mode != "panes":
            return
        pms = QtCore.QSize(paneSizes[0][0], paneSizes[0][1])
        par = self.parent()
        # set maya docking property "savedSize" to saved pms
        if not self.floating:
            par.setProperty("savedSize", pms)
            par.updateGeometry()
        self.paneModeSize = pms
        par.resize(pms)
        # [1] is a list of saved mainSplitter sizes,
        # [2] is a list for each sub-splitter
        self.mainSplitter.setSizes(paneSizes[1])
        for i, s in enumerate(paneSizes[2]):
            row = self.mainSplitter.widget(i)
            if row:
                row.setSizes(s)


    # Assign saved size to loadedUIs
    #
    def fixSize(self, i, size):
        self.allUIs[i][2] = size
        pos = self.allUIs[i][5]
        if self.mode == "panes":
            pane = self.panes[pos[0]][pos[1]]
        elif self.mode == "tabs":
            pane = self.defaultPane
        pane.uiTabBar.currentChanged.emit(pane.uiTabBar.currentIndex())


    # Look at Maya's children and see if the widget we
    # want to restore is already there.
    #
    def loadInternalWidg(self, name, source, pane, invis=True):
        # remove number identifiers from end of name string
        # e.g. "outliner1" to "outliner"
        noNumName = name.rstrip("0123456789")
        # Get child array NOW, so that references 
        # are used while they are fresh!
        # "Internal c++ object deleted" = FATAL ERROR
        #
        for w in getMayaMainWindow().children():
            # invis or w.isVisible ensures that prelim call
            # only collects visible widgets, but later call gets all
            if (w.isWidgetType() and w.windowTitle() in [noNumName, name]
                                and (invis or w.isVisible())):
                # maintain source if possible
                if source[0] == "internal":
                    source = ("internal", w)
                # Different cases for tab mode and pane mode
                try:
                    pane.widgToTab(w, w.windowTitle(), source)
                    return True
                except:
                    cmds.warning(
                        "uiMaster: Error restoring {0} UI".format(name))
        else:
            return False


    # Go through different source types and load
    #
    def loadFromSource(self, name, source, pane):
        if source[0] == "file":
            # Just reload the file, specific pane
            # pane.addTab(source[1], True, name)
            f = source[1]
            if not os.path.exists(f):
                # if absolute path is invalid, redefine as 
                # current project directory + saved relative path
                proj = cmds.workspace(q=True, rootDirectory=True)
                f = os.path.normpath(proj+source[2]).replace(os.sep, os.altsep)
            uis = self.uiFileHandler.getWidgets(None, [f], True, name)
            for x in uis:
                # possibly problematic if there is more than one UI
                # in a file... there will be duplicates
                w, n, s = x
                pane.widgToTab(w, n, s)
        elif source[0] == "mel":
            # re-run mel command with self.scriptWin
            if self.scriptWin.lang == "python":
                self.scriptWin.changeLang()

            # resolve file dependencies through source
            resolveDependencies("mel", source[2])

            cmds.cmdScrollFieldExecuter(
                        self.scriptWin.melCmd, edit=True, text=source[1])
            self.scriptWin.addWidgFromCode(True, pane)
        elif source[0] == "python":
            # re-run python command with self.scriptWin
            if self.scriptWin.lang == "mel":
                self.scriptWin.changeLang()

            # check for file dependencies
            resolveDependencies("python", source[2])

            cmds.cmdScrollFieldExecuter(
                        self.scriptWin.pyCmd, edit=True, text=source[1])
            self.scriptWin.addWidgFromCode(True, pane)
        elif source[0] == "internal":
            # Consult nativeUiDict - list of the commands for all native UIs
            # Tidy up the name
            niceName = name.rstrip("0123456789")
            try:
                cmd = nativeUiDict[niceName]
            except KeyError:
                return
            cmd = "catchQuiet(`"+cmd+"`)"
            # mel it
            if self.scriptWin.lang == "python":
                self.scriptWin.changeLang()
            cmds.cmdScrollFieldExecuter(
                        self.scriptWin.melCmd, edit=True, text=cmd)
            self.scriptWin.addWidgFromCode(True, pane)
        else:
            cmds.warning("Unrecognized source found in previous "
                        "session! Skipping {0}".format(name))


    # Open messagebox to ask about skipped UIs
    #
    def skippedUIs(self, failedToLoad):
        win = QtGui.QMessageBox(getMayaMainWindow())
        win.setWindowTitle("Error restoring UIs")
        win.setIcon(QtGui.QMessageBox.Warning)
        win.setText("Couldn't find valid sources for the "
                    "following UIs: \n\n{0}\n\n"
                    "Re-Source now?".format("\n".join(failedToLoad)))
        win.addButton("Open file", 
                        QtGui.QMessageBox.YesRole)
        win.addButton("Enter command", 
                        QtGui.QMessageBox.NoRole)
        win.addButton("Ignore", QtGui.QMessageBox.RejectRole)
        win.exec_()
        choice = win.clickedButton().text()
        if choice == "Open file":
            self.addTab("manual")
        if choice == "Enter command":
            self.openSecondaryWin(self.scriptWin, 
                            self.actionScript_Window)
        win.setParent(None)

"""
#----------------------------------------------------------------------
#----------------------------------------------------------------------




8888888b.                             .d88888b.                        888                 
888   Y88b                           d88P" "Y88b                       888                 
888    888                           888     888                       888                 
888   d88P 8888b. 88888b.  .d88b.    888     888888  888 .d88b. 888d888888 8888b. 888  888 
8888888P"     "88b888 "88bd8P  Y8b   888     888888  888d8P  Y8b888P"  888    "88b888  888 
888       .d888888888  88888888888   888     888Y88  88P88888888888    888.d888888888  888 
888       888  888888  888Y8b.       Y88b. .d88P Y8bd8P Y8b.    888    888888  888Y88b 888 
888       "Y888888888  888 "Y8888     "Y88888P"   Y88P   "Y8888 888    888"Y888888 "Y88888 
                                                                                       888 
                                                                                  Y8b d88P 
                                                                                   "Y88P" 


#----------------------------------------------------------------------
#----------------------------------------------------------------------
"""
# The semi-transparent overlay for creating new panes and rows
#
class PaneOverlay(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.base = super(PaneOverlay, self)
        self.base.__init__(parent)
        self.splitter = None

        self.setWindowFlags(QtCore.Qt.Popup)
        self.setWindowOpacity(0.7)
        self.buttonDict = {}

        # icons
        self.newPaneIcon = QtGui.QPixmap(22, 20)
        self.newPaneIcon.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(self.newPaneIcon)
        plus = QtGui.QPixmap(":/setEdAddCmd")
        right = QtGui.QPixmap(":/rightArrow")
        painter.drawPixmap(-4, 1, plus)
        painter.drawPixmap(10, 0, right)
        painter.end()

        self.newRowIcon = QtGui.QPixmap(20, 22)
        self.newRowIcon.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(self.newRowIcon)
        plus = QtGui.QPixmap(":/setEdAddCmd")
        down = QtGui.QPixmap(":/downArrow")
        painter.drawPixmap(0, -2, plus)
        painter.drawPixmap(3, 9, down)
        painter.end()

        self.rowButton = QtGui.QPushButton(self)
        self.rowButton.resize(80, 80)
        self.rowButton.clicked.connect(self.addRowAndUpdate)

    # Called whenever shown or a new row/pane is made.
    # 
    def redraw(self):
        if not self.splitter:
            return

        widg = self.parent().centralwidget
        self.move(self.parent().mapToGlobal(widg.pos()))
        self.resize(widg.size())

        rows = self.parent().layoutMode == "rows"
        # button for each row/col
        for row in self.buttonDict:
            but = self.buttonDict[row]
            rect = row.geometry()
            x, y, w, h = self.getButtonGeo(but, rect, rows)
            but.move(x, y)
            but.resize(w, h)
            #index = self.splitter.indexOf(row)
            # problem: when called, EVERYTHING is behind. It's like
            # redraw is being called BEFORE the window's geometry is updated

        # and one for new rows
        rect = self.splitter.geometry()
        if rows:
            x = rect.left() + 20
            y = rect.bottom() - 100
            self.rowButton.setIconSize(QtCore.QSize(40, 44))
            self.rowButton.setIcon(self.newRowIcon.scaled(40, 44))
        else:
            x = rect.right() - 100
            y = rect.top() + 20
            self.rowButton.setIconSize(QtCore.QSize(44, 40))
            self.rowButton.setIcon(self.newPaneIcon.scaled(44, 40))
        self.rowButton.move(x, y)
        
        self.show()

    def getButtonGeo(self, but, rect, rows):
        if rows:
            x = rect.right() - 120
            w = 80
            h = rect.height() * .75
            y = rect.center().y() - (h / 2)
            but.setIconSize(QtCore.QSize(44, 40))
            but.setIcon(self.newPaneIcon.scaled(44, 40))
        else:
            y = rect.bottom() - 120
            w = rect.width() * .75
            h = 80
            x = rect.center().x() - (w / 2)
            but.setIconSize(QtCore.QSize(40, 44))
            but.setIcon(self.newRowIcon.scaled(40, 44))
        return x, y, w, h

    def addButton(self, row):
        but = QtGui.QPushButton(self)
        but.clicked.connect(partial(self.addPaneAndUpdate, row))
        self.buttonDict[row] = but
        but.setVisible(True)

    def addRowAndUpdate(self):
        self.parent().addNewRow()
        self.redraw()

    def addPaneAndUpdate(self, row):
        self.parent().addNewPaneToRow(row)
        self.redraw()

    def deleteButton(self, row):
        but = self.buttonDict.pop(row)
        but.setParent(None)
        del(but)

    # Catch mouse presses so that the overlay hides when 
    # the background is clicked (not a button)
    #
    def mousePressEvent(self, event):
        self.base.mousePressEvent(event)
        self.hide()

"""
#----------------------------------------------------------------------


 .d8888b.                d8b        888   888       888d8b         
d88P  Y88b               Y8P        888   888   o   888Y8P         
Y88b.                               888   888  d8b  888            
 "Y888b.   .d8888b888d88888888888b. 888888888 d888b 88888888888b.  
    "Y88b.d88P"   888P"  888888 "88b888   888d88888b888888888 "88b 
      "888888     888    888888  888888   88888P Y88888888888  888 
Y88b  d88PY88b.   888    888888 d88PY88b. 8888P   Y8888888888  888 
 "Y8888P"  "Y8888P888    88888888P"  "Y888888P     Y888888888  888 
                            888                                    
                            888                                    
                            888         

#----------------------------------------------------------------------
"""
# Runs MEL and python code to load new UIs
#
class Ui_ExecWin(object):
    def setupUi(self, execWin):
        execWin.setObjectName("execWin")
        execWin.resize(400, 220)
        self.centralwidget = QtGui.QWidget(execWin)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(200)
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.langLabel = QtGui.QLabel(self.centralwidget)
        self.langLabel.setObjectName("langLabel")
        self.horizontalLayout.addWidget(self.langLabel)
        self.langButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langButton.sizePolicy().hasHeightForWidth())
        self.langButton.setSizePolicy(sizePolicy)
        self.langButton.setObjectName("langButton")
        self.horizontalLayout.addWidget(self.langButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        
        # make cmdsScrollFieldExecuter maya ui and get py obj of it
        # to yonik it
        #
        derWin = cmds.window()
        derCol = cmds.columnLayout()
        self.cmdFilter = CmdFilter(self)
        
        self.pyCmd = cmds.cmdScrollFieldExecuter(st="python", 
                            showTooltipHelp=False)#, objectPathCompletion=False)
        ptr = omui.MQtUtil.findControl(self.pyCmd)
        self.pyWidg = shiboken.wrapInstance(long(ptr), QtGui.QTextEdit)
        self.pyWidg.setObjectName("pyCmdWidget")
        self.pyWidg.setFixedHeight(124)
        self.pyWidg.setParent(self)
        self.stackedWidget.addWidget(self.pyWidg)
        self.pyWidg.installEventFilter(self.cmdFilter)
        
        self.melCmd = cmds.cmdScrollFieldExecuter(st="mel")
        ptr = omui.MQtUtil.findControl(self.melCmd)
        self.melWidg = shiboken.wrapInstance(long(ptr), QtGui.QTextEdit)
        self.melWidg.setObjectName("melCmdWidget")
        self.melWidg.setFixedHeight(124)
        self.melWidg.setParent(self)
        self.stackedWidget.addWidget(self.melWidg)
        self.melWidg.installEventFilter(self.cmdFilter)
        
        self.verticalLayout.addWidget(self.stackedWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        execWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(execWin)
        QtCore.QMetaObject.connectSlotsByName(execWin)
        
        #custom
        self.setWindowFlags(QtCore.Qt.Popup)
        self.langButton.clicked.connect(self.changeLang)
        self.lang = "python"
        self.pyWidg.setFocus()
        # safe mode is True during execution of code in scriptWin
        # protects against fatal errors caused by trying to
        # close uiMaster or load uiMaster into itself.
        #
        self.safeMode = False
        self.stackedWidget.setCurrentIndex(0)
        # get re-mapped name of cmdScrollFieldExecuter
        #
        self.pyCmd = omui.MQtUtil.fullName(shiboken.getCppPointer(self.pyWidg)[0])
        self.melCmd = omui.MQtUtil.fullName(shiboken.getCppPointer(self.melWidg)[0])
        cmds.deleteUI(derWin)

    def retranslateUi(self, execWin):
        execWin.setWindowTitle(QtGui.QApplication.translate("execWin", "Script Executer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("execWin", "<html><head/><body><p>Any new windows created with this script box<br/>will be loaded into uiMaster</p><p>(execute with CTRL+E / numpad Enter)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.langLabel.setText(QtGui.QApplication.translate("execWin", "Python:", None, QtGui.QApplication.UnicodeUTF8))
        self.langButton.setText(QtGui.QApplication.translate("execWin", "Switch to MEL", None, QtGui.QApplication.UnicodeUTF8))
    
    # Change the cmdScrollFieldExecuter box language - change page in stackedWidget
    #
    def changeLang(self):
        
        if self.lang == "mel":
            self.lang = "python"
            self.langLabel.setText("Python:")
            self.langButton.setText("Switch to MEL")
            self.stackedWidget.setCurrentIndex(0)
            self.pyWidg.setFocus()
            self.parent().settingsWin.saveSettings("lang", "python")
        elif self.lang == "python":
            self.lang = "mel"
            self.langLabel.setText("MEL:")
            self.langButton.setText("Switch to Python")
            self.stackedWidget.setCurrentIndex(1)
            self.melWidg.setFocus()
            self.parent().settingsWin.saveSettings("lang", "mel")

    
    # Detect windows before and after code is run
    # by looking for new children of Maya
    # AND ones that are visible now but weren't before
    # and embed those new windows
    #
    def addWidgFromCode(self, quiet=False, pane=None):
        par = self.parent()
        oldWins, oldVis = par.findMayaChildWindows()
        #
        cmd = self.runCode(quiet)

        newWins, newVis = par.findMayaChildWindows()
        # get the set of windows which are either new OR newly visible
        widgList = (newWins - oldWins) | (newVis - oldVis)
        if widgList == set([]) and not quiet:
            cmds.warning("Code entered did not create any new UIs")
            return
        # find modules/files used by cmd,
        # edit cmd to include import/source statements
        # and dependencies is a list of files which are outside of path
        dependencies = getDependenciesInCode(self.lang, cmd)
        
        for w in widgList:
            # Shrug. I guess construction of the new object 
            # has a chance of not being complete by the time we get here
            # so sometimes QObjects make it through to here
            #if not w.isWidgetType():
            #    continue
            name = w.windowTitle()
            if pane:
                p = pane
            else:
                p = par.findBestPane()

            p.widgToTab(w, name, (self.lang, cmd, dependencies))


    # Actually execute code, return cmd
    #
    def runCode(self, quiet):
        cmd = ""
        self.safeMode = True
        # to quiet Maya's "No window found" bug
        # Don't think it does anything else
        try:
            if self.lang == "python":
                cmd = self.pyWidg.toPlainText()
                pos = self.pyWidg.textCursor()
                cmds.cmdScrollFieldExecuter(
                        self.pyCmd, edit=True, execute=True)
                if not quiet:
                    self.pyWidg.setText(cmd)
                    self.pyWidg.setTextCursor(pos)
            elif self.lang == "mel":
                cmd = self.melWidg.toPlainText()
                pos = self.melWidg.textCursor()
                cmds.cmdScrollFieldExecuter(
                        self.melCmd, edit=True, execute=True)
                if not quiet:
                    self.melWidg.setText(cmd)
                    self.melWidg.setTextCursor(pos)
        except:
            raise
        self.safeMode = False
        return cmd



"""
#----------------------------------------------------------------------


 .d8888b.         888   888   d8b                        888       888d8b         
d88P  Y88b        888   888   Y8P                        888   o   888Y8P         
Y88b.             888   888                              888  d8b  888            
 "Y888b.   .d88b. 88888888888888888888b.  .d88b. .d8888b 888 d888b 88888888888b.  
    "Y88b.d8P  Y8b888   888   888888 "88bd88P"88b88K     888d88888b888888888 "88b 
      "88888888888888   888   888888  888888  888"Y8888b.88888P Y88888888888  888 
Y88b  d88PY8b.    Y88b. Y88b. 888888  888Y88b 888     X888888P   Y8888888888  888 
 "Y8888P"  "Y8888  "Y888 "Y888888888  888 "Y88888 88888P'888P     Y888888888  888 
                                              888                                 
                                         Y8b d88P                                 
                                          "Y88P"  

#----------------------------------------------------------------------
"""
#
class Ui_settingsWin(object):
    def setupUi(self, settingsWin):
        settingsWin.setObjectName("settingsWin")
        settingsWin.resize(300, 180)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settingsWin.sizePolicy().hasHeightForWidth())
        settingsWin.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(settingsWin)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(30, 11, 30, -1)
        self.verticalLayout.setObjectName("verticalLayout")

        self.updateLayout = QtGui.QVBoxLayout()
        self.updateLayout.setContentsMargins(50, -1, 50, -1)
        self.updateLayout.setObjectName("updateLayout")
        self.updateButton = QtGui.QPushButton(self.centralwidget)
        self.updateButton.setObjectName("updateButton")
        self.updateLayout.addWidget(self.updateButton)
        self.verticalLayout.addLayout(self.updateLayout)
        
        self.mode = QtGui.QGroupBox(self.centralwidget)
        self.mode.setObjectName("mode")
        self.gridLayout_3 = QtGui.QGridLayout(self.mode)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabMode = QtGui.QRadioButton(self.mode)
        self.tabMode.setObjectName("tabMode")
        self.gridLayout_3.addWidget(self.tabMode, 0, 0, 1, 1)
        self.paneMode = QtGui.QRadioButton(self.mode)
        self.paneMode.setObjectName("paneMode")
        self.gridLayout_3.addWidget(self.paneMode, 0, 1, 1, 2)
        self.verticalLayout.addWidget(self.mode)

        self.paneLayout = QtGui.QGroupBox(self.mode)
        self.paneLayout.setObjectName("mode")
        self.gridLayout_4 = QtGui.QGridLayout(self.paneLayout)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.rowMode = QtGui.QRadioButton(self.paneLayout)
        self.rowMode.setObjectName("rowMode")
        self.gridLayout_4.addWidget(self.rowMode, 0, 0, 2, 1)
        self.columnMode = QtGui.QRadioButton(self.paneLayout)
        self.columnMode.setObjectName("columnMode")
        self.gridLayout_4.addWidget(self.columnMode, 0, 1, 2, 2)
        self.gridLayout_3.addWidget(self.paneLayout, 1, 0, 2, 3)
        #self.verticalLayout.addWidget(self.paneLayout)        

        self.autoOpenCheck = QtGui.QCheckBox(self.centralwidget)
        self.autoOpenCheck.setObjectName("autoOpenCheck")
        self.verticalLayout.addWidget(self.autoOpenCheck)
        self.resizeCheck = QtGui.QCheckBox(self.centralwidget)
        self.resizeCheck.setObjectName("resizeCheck")
        self.verticalLayout.addWidget(self.resizeCheck)
        """
        self.focusCheck = QtGui.QCheckBox(self.centralwidget)
        self.focusCheck.setObjectName("focusCheck")
        self.verticalLayout.addWidget(self.focusCheck)
        """
        self.disperseCheck = QtGui.QCheckBox(self.centralwidget)
        self.disperseCheck.setObjectName("disperseCheck")
        self.verticalLayout.addWidget(self.disperseCheck)
        self.hotkeyCheck = QtGui.QCheckBox(self.centralwidget)
        self.hotkeyCheck.setObjectName("hotkeyCheck")
        self.verticalLayout.addWidget(self.hotkeyCheck)
        
        self.defaultUIs = QtGui.QGroupBox(self.centralwidget)
        self.defaultUIs.setObjectName("defaultUIs")
        self.gridLayout = QtGui.QGridLayout(self.defaultUIs)
        self.gridLayout.setObjectName("gridLayout")
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 0, 0, 2, 1)
        self.delButton = QtGui.QPushButton(self.centralwidget)
        self.delButton.setObjectName("delButton")
        self.gridLayout.addWidget(self.delButton, 0, 1, 2, 2)
        
        self.dockable = QtGui.QGroupBox(self.centralwidget)
        self.dockable.setObjectName("dockable")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockable)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.leftCheck = QtGui.QCheckBox(self.dockable)
        self.leftCheck.setObjectName("leftCheck")
        self.gridLayout_2.addWidget(self.leftCheck, 0, 0, 1, 1)
        self.rightCheck = QtGui.QCheckBox(self.dockable)
        self.rightCheck.setObjectName("rightCheck")
        self.gridLayout_2.addWidget(self.rightCheck, 0, 1, 1, 2)

        self.topCheck = QtGui.QCheckBox(self.dockable)
        self.topCheck.setObjectName("topCheck")
        self.gridLayout_2.addWidget(self.topCheck, 1, 0, 2, 1)
        self.bottomCheck = QtGui.QCheckBox(self.dockable)
        self.bottomCheck.setObjectName("bottomCheck")
        self.gridLayout_2.addWidget(self.bottomCheck, 1, 1, 2, 2)

        self.verticalLayout.addWidget(self.defaultUIs)
        self.verticalLayout.addWidget(self.dockable)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(50, -1, 50, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        settingsWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(settingsWin)
        QtCore.QMetaObject.connectSlotsByName(settingsWin)
        
        # custom
        self.setWindowFlags(QtCore.Qt.Popup)
        self.pushButton.clicked.connect(self.close)
        self.prefs = cmds.internalVar(upd=True)+"uiMasterPrefs.ini"
        self.dockAreas = {"leftCheck": 0, "rightCheck": 0,
                            "topCheck": 0, "bottomCheck": 0}

        # Connect signals
        self.updateButton.clicked.connect(selfUpdate)
        self.tabMode.toggled.connect(self.parent().setTabMode)
        self.paneMode.toggled.connect(self.parent().setPaneMode)
        self.rowMode.toggled.connect(self.parent().setRowMode)
        self.columnMode.toggled.connect(
                        partial(self.saveSettings, "columnMode"))
        self.autoOpenCheck.toggled.connect(self.setAutoOpen)
        self.resizeCheck.toggled.connect(
                        partial(self.saveSettings, "resizeCheck"))
        #self.focusCheck.toggled.connect(
        #                partial(self.saveSettings, "focusCheck"))
        self.disperseCheck.toggled.connect(
                        partial(self.saveSettings, "disperseCheck"))
        self.hotkeyCheck.toggled.connect(
                        partial(self.toggleHotkeys, "hotkeyCheck"))
        self.leftCheck.toggled.connect(
                        partial(self.setDockAreas, "leftCheck",
                        QtCore.Qt.LeftDockWidgetArea))
        self.rightCheck.toggled.connect(
                        partial(self.setDockAreas, "rightCheck",
                        QtCore.Qt.RightDockWidgetArea))
        self.topCheck.toggled.connect(
                        partial(self.setDockAreas, "topCheck",
                        QtCore.Qt.TopDockWidgetArea))
        self.bottomCheck.toggled.connect(
                        partial(self.setDockAreas, "bottomCheck",
                        QtCore.Qt.BottomDockWidgetArea))
        self.saveButton.clicked.connect(self.saveDefaultState)
        self.delButton.clicked.connect(self.deleteDefaultState)
    

    def retranslateUi(self, settingsWin):
        settingsWin.setWindowTitle(QtGui.QApplication.translate("settingsWin", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("settingsWin", "Update uiMaster", None, QtGui.QApplication.UnicodeUTF8))
        self.mode.setTitle(QtGui.QApplication.translate("settingsWin", "UI display mode", None, QtGui.QApplication.UnicodeUTF8))
        self.tabMode.setText(QtGui.QApplication.translate("settingsWin", "Tabs Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.paneMode.setText(QtGui.QApplication.translate("settingsWin", "Panes Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.paneLayout.setTitle(QtGui.QApplication.translate("settingsWin", "Pane Layout", None, QtGui.QApplication.UnicodeUTF8))
        self.rowMode.setText(QtGui.QApplication.translate("settingsWin", "Rows", None, QtGui.QApplication.UnicodeUTF8))
        self.columnMode.setText(QtGui.QApplication.translate("settingsWin", "Columns", None, QtGui.QApplication.UnicodeUTF8))
        self.autoOpenCheck.setText(QtGui.QApplication.translate("settingsWin", "Open uiMaster on startup", None, QtGui.QApplication.UnicodeUTF8))
        self.resizeCheck.setText(QtGui.QApplication.translate("settingsWin", "Auto-resize (Tab Mode)", None, QtGui.QApplication.UnicodeUTF8))
        #self.focusCheck.setText(QtGui.QApplication.translate("settingsWin", "Mouseover Focus", None, QtGui.QApplication.UnicodeUTF8))
        self.disperseCheck.setText(QtGui.QApplication.translate("settingsWin", "Disperse windows when closed", None, QtGui.QApplication.UnicodeUTF8))
        self.hotkeyCheck.setText(QtGui.QApplication.translate("settingsWin", "Hotkeys: RMB + 1-8 to change tabs\n"+" "*15+"RMB + Spacebar to show/hide", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultUIs.setTitle(QtGui.QApplication.translate("settingsWin", "Open default UIs on creation", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("settingsWin", "Set Current as Default", None, QtGui.QApplication.UnicodeUTF8))
        self.delButton.setText(QtGui.QApplication.translate("settingsWin", "Delete Default", None, QtGui.QApplication.UnicodeUTF8))
        self.dockable.setTitle(QtGui.QApplication.translate("settingsWin", "Dockable", None, QtGui.QApplication.UnicodeUTF8))
        self.leftCheck.setText(QtGui.QApplication.translate("settingsWin", "Left", None, QtGui.QApplication.UnicodeUTF8))
        self.rightCheck.setText(QtGui.QApplication.translate("settingsWin", "Right", None, QtGui.QApplication.UnicodeUTF8))
        self.topCheck.setText(QtGui.QApplication.translate("settingsWin", "Top", None, QtGui.QApplication.UnicodeUTF8))
        self.bottomCheck.setText(QtGui.QApplication.translate("settingsWin", "Bottom", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("settingsWin", "Ok", None, QtGui.QApplication.UnicodeUTF8))
    
    
    # Change dock areas
    #
    def setDockAreas(self, name, area, state):
        # When turned on, add 0 or DockWidgetArea to dict
        if state:
            self.dockAreas[name] = area
        else:
            self.dockAreas[name] = 0
        # assumes that self.parent().parent() is the dockwidget
        # created by makeUiMaster ... perhaps bad
        self.parent().parent().setAllowedAreas(
                    self.dockAreas["leftCheck"] | self.dockAreas["rightCheck"] |
                    self.dockAreas["topCheck"] | self.dockAreas["bottomCheck"])
        self.saveSettings(name, state)
    

    # Install/remove hotkey event filter
    #
    def toggleHotkeys(self, name, state):
        main = getMayaMainWindow()
        par = self.parent()
        if state:
            main.installEventFilter(par.hotkeyFilter)
            self.parent().mainSplitter.installEventFilter(par.hotkeyFilter)
        else:
            main.removeEventFilter(par.hotkeyFilter)
            self.parent().mainSplitter.removeEventFilter(par.hotkeyFilter)
        self.saveSettings(name, state)


    # script that puts stuff in userSetup.mel -
    # triggered by a new setting "Open on startup",
    #
    def setAutoOpen(self, state):
        setupCmd = (
"""import maya.cmds as cmds

n = cmds.internalVar(upd=True)+"pluginPrefs.mel"
cmd = ("evalDeferred(\\\"if (`pluginInfo -q -l \\\\\\\"uiMaster\\\\\\\"`)"
            " {uiMaster;}\\\");")
with open(n, "a+") as f:
    contents = f.read()
    if cmd not in contents:
        f.seek(0)
        f.write("\\n\\n"+cmd)""")

        n = cmds.internalVar(usd=True)+"userSetup.py"
        # first, ensure file exists
        # and get contents
        with open(n, "a+") as f:
            contents = f.read()
        contents = contents.replace(setupCmd, "")
        lines = [x for x in contents.split("\n") if x]

        if state:  
            lines.append(setupCmd)
            cmds.pluginInfo("uiMaster", e=True, a=True)
        contents = "\n".join(lines)
        with open(n, "w") as f:
            f.write(contents)
            
        self.saveSettings("autoOpenCheck", state)

    
    # Run whenever any setting is changed
    #
    def saveSettings(self, name, state):
        qSet = QtCore.QSettings(self.prefs, QtCore.QSettings.IniFormat)
        qSet.setIniCodec("UTF-8")
        if type(state) is bool:
            state = int(state)
        qSet.setValue(name, state)
    
    
    # On startup, load previous QSettings
    #
    def restoreSettings(self):
        qSet = QtCore.QSettings(self.prefs, QtCore.QSettings.IniFormat)
        qSet.setIniCodec("UTF-8")
        # Set to whether saved value == "true", 
        # to get around silly auto-decapitalization
        # performed by qSettings
        dock = self.parent().parent()
        self.tabMode.setChecked(int(qSet.value("tabMode", 1)))
        self.paneMode.setChecked(int(qSet.value("paneMode", 0)))
        self.rowMode.setChecked(int(qSet.value("rowMode", 1)))
        self.columnMode.setChecked(int(qSet.value("columnMode", 0)))
        self.autoOpenCheck.setChecked(int(qSet.value("autoOpenCheck", 0)))
        self.resizeCheck.setChecked(int(qSet.value("resizeCheck", 1)))
        #self.focusCheck.setChecked(
        #            qSet.value("focusCheck", "false") == "true")
        self.disperseCheck.setChecked(int(qSet.value("disperseCheck", 1)))
        self.hotkeyCheck.setChecked(int(qSet.value("hotkeyCheck", 1)))
        self.leftCheck.setChecked(int(qSet.value("leftCheck", 1)))
        self.rightCheck.setChecked(int(qSet.value("rightCheck", 0)))
        self.topCheck.setChecked(int(qSet.value("topCheck", 0)))
        self.bottomCheck.setChecked(int(qSet.value("bottomCheck", 0)))

        self.parent().addToolBar(
                    QtCore.Qt.ToolBarArea(int(qSet.value("toolBarArea", 4))),
                    self.parent().toolBar)
        """getMayaMainWindow().addDockWidget(
                    QtCore.Qt.DockWidgetArea(int(qSet.value("dockArea", 0))),
                    dock)"""
        area = int(qSet.value("dockArea", 0))
        pos = {1: "left", 2: "right", 4: "top", 8: "bottom"}
        if area:
            # Gotta do it the Maya way with cmds, or else it 
            # splits the dock area in half 
            # PySide bug (?)
            cmds.dockControl(self.parent().mayaName, edit=True, area=pos[area])
        dock.setFloating(int(qSet.value("floating", 1)))

        lang = qSet.value("lang", "python")
        if self.parent().scriptWin.lang != lang:
            self.parent().scriptWin.changeLang()
        self.parent().setRowMode(self.rowMode.isChecked())

    
    # User can save a default state which uiMaster opens with
    # if there is no saved state. Accessed through settings menu.
    #
    def saveDefaultState(self):
        self.saveSettings("defaultUIs", 
                        cmds.getAttr(self.parent().tabsNode+".before"))


    # Reset saved value for defaultUIs to nothing
    #
    def deleteDefaultState(self):
        self.saveSettings("defaultUIs", "[]")


    # Auto-called if tabsNode doesn't exist, restores the 
    # previously set default UIs
    #
    def restoreDefaultState(self):
        qSet = QtCore.QSettings(self.prefs, QtCore.QSettings.IniFormat)
        qSet.setIniCodec("UTF-8")
        # Simplest way to do it is just take advantage of 
        # existing state management
        uiList = eval(qSet.value("defaultUIs", "[]"))
        if uiList:
            self.parent().restoreSavedState(uiList)

"""
#----------------------------------------------------------------------


8888888         .d888        888       888d8b         
  888          d88P"         888   o   888Y8P         
  888          888           888  d8b  888            
  888  88888b. 888888 .d88b. 888 d888b 88888888888b.  
  888  888 "88b888   d88""88b888d88888b888888888 "88b 
  888  888  888888   888  88888888P Y88888888888  888 
  888  888  888888   Y88..88P8888P   Y8888888888  888 
8888888888  888888    "Y88P" 888P     Y888888888  888 


#----------------------------------------------------------------------
"""
# Software version information
#
class Ui_infoWin(object):
    def setupUi(self, infoWin):
        infoWin.setObjectName("infoWin")
        infoWin.resize(300, 222)
        self.centralwidget = QtGui.QWidget(infoWin)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        infoWin.setCentralWidget(self.centralwidget)
        infoWin.setWindowTitle(QtGui.QApplication.translate("infoWin", "Software Info", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("infoWin", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">"+__title__+"</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Version: "+__version__+"</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Author: "+__author__+"</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">email: "+__email__+"</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright &copy; "+__copyYear__+" "+__author__+"</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All rights reserved</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">... or something</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        QtCore.QMetaObject.connectSlotsByName(infoWin)
        self.setWindowFlags(QtCore.Qt.Popup)





#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Make it a plugin!
#



# Dictionary of name: creation command
# Some of these are dock controls instead of windows...
# will have to think of something for those
nativeUiDict = {"Attribute Editor": "AttributeEditor",
                "Outliner": "OutlinerWindow",
                "Node Editor": "NodeEditorWindow",
                "Create Node": "CreateNodeWindow",
                "Hypergraph Heirarchy": "HypergraphWindow",
                "Hypergraph InputOutput": "HypergraphWindow",
                "Paint Effects": "PaintEffectsWindow",
                "UV Texture Editor": "TextureViewWindow",
                "Component Editor": "ComponentEditor",
                "Attribute Spread Sheet": "SpreadSheetEditor",
                "Connection Editor": "ConnectionEditor",
                "Visor": "VisorWindow",
                "Asset Editor": "AssetEditor",
                "Namespace Editor": "NamespaceEditor",
                "File Path Editor": "FilePathEditor",
                "Channel Control": "ChannelControlEditor",
                "Script Editor": "ScriptEditor",
                "Command Shell": "CommandShell",
                "Render View": "RenderViewWindow",
                "Render Settings": "unifiedRenderGlobalsWindow",
                "Hypershade": "HypershadeWindow",
                
                "Rendering Flags": "RenderFlagsWindow",
                "Hardware Render Buffer": "HardwareRenderBuffer",
                "Graph Editor": "GraphEditor",
                "Trax Editor": "CharacterAnimationEditor",
                "Camera Sequencer": "SequenceEditor",
                "Dope Sheet": "DopeSheetEditor",
                "Character Controls": "HIKCharacterControlsTool",
                "Blend Shape": "BlendShapeEditor",
                "Expression Editor": "ExpressionEditor",
                "Relationship Editor": "SetEditor",
                "Dynamic Relationships Editor": "DynamicRelationshipEditor",
                "Tool Settings": "ToolSettingsWindow",
                "Channel Box": "ToggleChannelBox",
                "Layer Editor": "ToggleLayerBar",
                "Channel Box / Layer Editor": "ToggleChannelsLayers"}



# safety check
# & is finding which BITS the two items have in common, so this is a 
# very sturdy check for if a widget is popup-ish
"""

def focusOutEvent(self, event):
    self.base.focusOutEvent(event)
    if not self.prevProxy or not self.prevProxy.widget():
        return
    widg = self.prevProxy.widget()
    newF = QtGui.QApplication.focusWidget()
    isSelf = newF is self

    # investigate new focus - is it window, and REAL window at that?
    if (newF.isWindow() 
            and newF.windowType() not in [QtCore.Qt.Popup, QtCore.Qt.ToolTip]
            and not (newF.windowFlags() & QtCore.Qt.FramelessWindowHint)):
        print("Real window.")

"""