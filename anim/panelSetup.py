# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-28 16:18:26'

"""
初始化动画文件的界面
"""
from maya import cmds
from maya import mel
from maya import OpenMayaUI

from Qt import QtWidgets
from Qt.QtCompat import wrapInstance

def mayaToQT( name ):
    # Maya -> QWidget
    ptr = OpenMayaUI.MQtUtil.findControl( name )
    if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
    if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
    if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )

def getWindowPos(panel_width,panel_height,gap,pos):
    desktop = QtWidgets.QApplication.desktop()

    # NOTE 获取任意副屏幕
    for i in range(desktop.screenCount()):
        if desktop.primaryScreen() != i:
            screen = desktop.screenGeometry(i)
            break
    
    if pos == "top":
        h = 20 + screen.top()
    elif pos == "bottom":
        h = -20 + screen.bottom()
    else:
        # NOTE 居中
        h = (screen.height() - panel_height)/2 + screen.top()
    w = (screen.width() - panel_width*2 - gap)/2 + screen.left()

    return w,h
    

def main(panel_width=600,panel_height=400,gap=100,pos="top"):
    
    # NOTE 修复 Maya2017 大纲视图显示多余 set 的 Bug
    for outliner in cmds.getPanel(type="outlinerPanel"):
        cmds.outlinerEditor(outliner,e=1,sf="defaultSetFilter")

    # NOTE 四视图切换
    mel.eval('setNamedPanelLayout "Four View"; ')
    # NOTE 禁用骨骼和模型选择
    mel.eval("""
    setObjectPickMask "Joint" false;
    setObjectPickMask "Surface" false;
    """)

    # NOTE 只显示曲线和模型 
    for mp in cmds.getPanel(type="modelPanel"):
        # NOTE 隐藏所有
        cmds.modelEditor(mp, e=1,allObjects=0)
        cmds.modelEditor(mp, e=1,
        nurbsCurves=1,
        locators=1,
        polymeshes=1,
        hud=0,
        grid=0,
        da= "smoothShaded",
        displayTextures=1)
        cmds.viewFit(cmds.modelEditor(mp,q=1,cam=1),all=True )

    # NOTE 获取当前角色摄像机
    camera = None
    for cam in cmds.ls(type="camera"):
        cam = cmds.listRelatives(cam,p=1)[0]
        if "camera_001" in cam.lower():
            camera = cam
            break
    
    # NOTE 计算面板显示的位置
    panel_wh = [panel_width,panel_height]
    w,h = getWindowPos(panel_width,panel_height,gap,pos)
    main_pos = [w,h]
    shadow_pos = [w+panel_width+gap,h]
    
    # NOTE 创建主视角视图
    main_panel_win = "main_panel_win"
    if cmds.window(main_panel_win,q=1,ex=1):
        cmds.deleteUI(main_panel_win)
    window = cmds.window(main_panel_win,t=u"主视角视图",wh=panel_wh)
    cmds.paneLayout()
    main_panel = cmds.modelPanel()
    cmds.showWindow( window )

    mayaToQT(window).move(*main_pos)

    cmds.modelEditor(main_panel,e=1,allObjects=0)
    cmds.modelEditor(main_panel, e=1,
    polymeshes=1,
    locators=1,
    da= "smoothShaded",
    hud=0,
    grid=0,
    displayTextures=1)
    if camera:
        cmds.lookThru(camera,main_panel)

    # NOTE 创建剪影视图
    shadow_panel_win = "shadow_panel_win"
    if cmds.window(shadow_panel_win,q=1,ex=1):
        cmds.deleteUI(shadow_panel_win)
    window = cmds.window(shadow_panel_win,t=u"剪影视图",wh=panel_wh,tlc=shadow_pos)
    cmds.paneLayout()
    shadow_panel = cmds.modelPanel()
    cmds.showWindow( window )

    mayaToQT(window).move(*shadow_pos)

    cmds.modelEditor(shadow_panel,e=1,allObjects=0)
    cmds.modelEditor(shadow_panel, e=1,
    polymeshes=1,
    locators=1,
    da= "smoothShaded",
    dl= "none",
    hud=0,
    grid=0,
    displayTextures=0)
    if camera:
        cmds.lookThru(camera,shadow_panel)

if __name__ == "__main__":
    main()

