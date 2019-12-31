# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-28 16:18:26'

"""
初始化动画视窗界面
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

def getWindowPos(screen,panel_width,panel_height,gap,pos,margin = 0):
    
    if pos == "top":
        h = margin + screen.top()
    elif pos == "bottom":
        h = -margin + screen.bottom()
    else:
        # NOTE 居中
        h = (screen.height() - panel_height)/2 + screen.top()
    w = (screen.width() - panel_width*2 - gap)/2 + screen.left()

    return w,h
    
def createExtraPanel(
    panel_width=0,
    panel_height=0,
    gap=0,
    margin=0,
    panel_height_percent=3.0/5,
    gap_percent=1.0/20,
    titleBar_height = 30,
    pos="top"):
    cmds.windowPref(enableAll=0)
    # NOTE 获取当前角色摄像机
    camera = None
    for cam in cmds.ls(type="camera"):
        cam = cmds.listRelatives(cam,p=1)[0]
        if "camera_001" in cam.lower():
            camera = cam
            break
    
    desktop = QtWidgets.QApplication.desktop()

    # NOTE 获取任意副屏幕
    for i in range(desktop.screenCount()):
        if desktop.primaryScreen() != i:
            screen = desktop.screenGeometry(i)
            break

    if panel_height <= 0:
        panel_height = screen.height() * panel_height_percent
    
    if gap <= 0:
        gap = screen.width() * gap_percent

    if panel_width <= 0:
        panel_width = (screen.width() - gap) / 2

    # NOTE 计算面板显示的位置
    w,h = getWindowPos(screen,panel_width,panel_height,gap,pos,margin)
    h += titleBar_height
    main_pos = [w,h,panel_width,panel_height]
    shadow_pos = [w+panel_width+gap,h,panel_width,panel_height]
    
    # NOTE 创建主视角视图
    main_panel_win = "main_panel_win"
    if cmds.window(main_panel_win,q=1,ex=1):
        cmds.deleteUI(main_panel_win)
    window = cmds.window(main_panel_win,t=u"主视角视图")
    cmds.paneLayout()
    main_panel = cmds.modelPanel()
    cmds.showWindow( window )

    mayaToQT(window).setGeometry(*main_pos)
    
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
    window = cmds.window(shadow_panel_win,t=u"剪影视图")
    cmds.paneLayout()
    shadow_panel = cmds.modelPanel()
    cmds.showWindow( window )

    mayaToQT(window).setGeometry(*shadow_pos)

    cmds.modelEditor(shadow_panel,e=1,allObjects=0)
    cmds.modelEditor(shadow_panel, e=1,
    polymeshes=1,
    locators=1,
    da= "smoothShaded",
    dl= "none",
    hud=0,
    grid=0,
    viewTransformName="Raw",
    displayTextures=0)
    if camera:
        cmds.lookThru(camera,shadow_panel)
    cmds.windowPref(enableAll=0)

    graph_win = mel.eval('tearOffRestorePanel "Graph Editor" "graphEditor" true')
    graph_win = mayaToQT(graph_win).window()
    width = screen.width()
    height = screen.height() * (1 - panel_height_percent) - gap - titleBar_height*2
    h += panel_height + titleBar_height + gap
    graph_win.setGeometry(w,h,width,height)


def main():
    
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
        # NOTE 删除自定义的视窗窗口
        if cmds.modelPanel(mp,q=1,tearOff=1):
            mayaToQT(mp).window().close()
            continue

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


    createExtraPanel(panel_width=0,panel_height=0,gap=30,margin=0,pos="top")

if __name__ == "__main__":
    main()

