# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-19 14:25:53'

"""

"""
import os
import json
import tempfile
import subprocess
from textwrap import dedent

from maya import mel
import pymel.core as pm
import maya.api.OpenMaya as om

def SetFbxParameter():
    if not pm.pluginInfo('fbxmaya', q=True, loaded=True):
        pm.loadPlugin('fbxmaya')
    mel.eval('FBXResetExport')
    mel.eval('FBXExportFileVersion -v FBX201600')
    mel.eval('FBXExportUpAxis y')
    mel.eval('FBXExportShapes  -v false')
    mel.eval('FBXExportScaleFactor 1.0')
    mel.eval('FBXExportInAscii -v true')
    mel.eval('FBXExportConstraints -v false')
    mel.eval('FBXExportLights -v false')
    mel.eval('FBXExportSkins -v false')
    mel.eval('FBXExportSmoothingGroups -v true')
    mel.eval('FBXExportSmoothMesh -v true')
    mel.eval('FBXExportEmbeddedTextures -v false')
    mel.eval('FBXExportCameras -v false')
    mel.eval('FBXExportBakeResampleAnimation -v false')
    mel.eval('FBXExportSkeletonDefinitions -v false')

def generateFollowPlane(*args):
    startTime = pm.playbackOptions(q=1,min=1)
    endTime = pm.playbackOptions(q=1,max=1)


    sel_list = pm.ls(sl=1,ni=1,type="transform")
    if not sel_list:
        pm.confirmDialog( message='请选择物体', button=['确定'])
        return
        
    for sel in sel_list:
        # snapshot = pm.snapshot(sel,st=startTime,et=endTime)[1]
        snapshot = pm.createNode("snapshot")
        sel.selectHandle.connect(snapshot.localPosition)
        sel.worldMatrix[0].connect(snapshot.inputMatrix)
        snapshot.startTime.set(startTime)
        snapshot.endTime.set(endTime)
        snapshot.increment.set(1)
        anim_curve = pm.curve( n=sel+"_follow_curve",d=3,p=snapshot.pts.get())
        pm.delete(snapshot)
        
        curve_length = pm.arclen(anim_curve,ch=0)
        plane,plane_node = pm.polyPlane( n=sel+"_follow_plane",sx=20, sy=3, w=curve_length, h=20 )

        # NOTE 创建运动路径跟随
        motion_path = pm.pathAnimation(
            plane,
            anim_curve,
            fractionMode=1,
            follow=1 ,
            followAxis="x",
            upAxis = "y" ,
            worldUpType="vector",
            worldUpVector=(0,1,0) ,
            inverseUp=0 ,
            inverseFront=0 ,
            bank=0 ,
            startTimeU=startTime,
            endTimeU=endTime,
        )
        flow_node,ffd_node,lattice_node,ffd_base =pm.flow( plane,dv=(100, 2, 2))

        # NOTE 设置外部影响
        ffd_node.outsideLattice.set(1)
        ffd_node.local.set(1)
        plane_node.width.set(50)

        lattice_node.v.set(0)
        ffd_base.v.set(0)

        # NOTE 设置运动路径
        motion_path.fractionMode.set(1)
        animCurve = motion_path.listConnections(type="animCurve")[0]
        # NOTE 关键帧设置为线性
        animCurve.setTangentTypes(range(animCurve.numKeys()),inTangentType="linear",outTangentType="linear")

        # NOTE 打组
        pm.group(lattice_node,ffd_base,plane,anim_curve,n=sel+"_follow_grp")
        pm.select(plane)
        

def exportPlane(*args):
# for sel in pm.ls(sl=1,ni=1):
#     for i in range(pm.polyEvaluate(sel,v=1)):
#         print (sel.vtx[i].getPosition(space="world"))

    export_dir = pm.fileDialog2(dialogStyle=2,fileMode=3,startingDirectory=os.path.dirname(pm.sceneName()))
    if not export_dir:
        return
    export_dir = export_dir[0]
    for sel in pm.ls(sl=1,ni=1):
        if not sel.endswith("_follow_plane") or not sel.getParent().endswith("_follow_grp"):
            continue
        
        shape = sel.getShape()
        vtx_num = pm.polyEvaluate(sel,v=1)
        startTime = pm.playbackOptions(q=1,min=1)
        endTime = pm.playbackOptions(q=1,max=1)

        sel_list = om.MSelectionList()
        sel_list.add(str(sel))
        dagPath = sel_list.getDagPath(0)
        mesh = om.MFnMesh(dagPath)

        # NOTE 如果裁剪区域超过原图范围则限制到原图的边界上
        width = int(vtx_num)
        height = int(endTime - startTime)
        
        data = {}
        for h in range(height):
            data[h] = {}
            pm.currentTime(startTime+h)
            for w in range(width):
                vtx_pos = sel.vtx[w].getPosition(space="world")
                data[h][w] = vtx_pos.tolist()
                # data[h][w] = pm.pointPosition(sel.vtx[w],w=1).tolist()

        json_path = os.path.join(tempfile.gettempdir(),"pathTracker_EXR.json")
        with open(json_path,'w') as f:
            json.dump(data,f)     

        DIR = os.path.dirname(__file__)
        exr_exe = os.path.join(DIR,"dist","pathTracker_EXR.exe")

        basename = sel.replace(":","_")
        exr_path = os.path.join(export_dir,"%s_EXR.exr"%basename)

        # NOTE 执行 exr 输出
        subprocess.call([exr_exe,json_path,exr_path])
        
        # NOTE 导出 FBX
        SetFbxParameter()
        export_FBX = os.path.join(export_dir,"%s_FBX.fbx"%basename).replace("\\","/")
        plane = pm.duplicate(sel)
        pm.parent(plane,w=1)
        pm.select(plane)
        mel.eval('FBXExport -f "' + export_FBX + '" -s')
        pm.delete(plane)

        os.startfile(export_dir)
        pm.confirmDialog( message='输出成功', button=['确定'])

        # NOTE https://groups.google.com/forum/#!topic/python_inside_maya/Q9NuAd6Av20
        # pixels = bytearray(width*height*4)  
        # for w in range(width):
            # vtx_pos = sel.vtx[w].getPosition(space="world")
            # u,v,_ = mesh.getUVAtPoint(om.MPoint(vtx_pos),space=om.MSpace.kWorld)
            # fol_node = pm.createNode('follicle',ss = True)
            # fol = fol_node.getParent()
            # shape.outMesh.connect(fol_node.inputMesh)
            # shape.worldMatrix[0].connect(fol.inputWorldMatrix)
            # fol_node.outTranslate.connect(fol.translate)
            # fol_node.outRotate.connect(fol.rotate)

            # fol_node.parameterU.set(u)
            # fol_node.parameterV.set(v)
            # fol_node.simulationMethod.set(0)

            # for h in range(height):
            #     pos = (w+h*width)*4
            #     fol_pos = fol.t.get(time=startTime + h)
                # NOTE 这里加数字代表当前像素下 RGBA 四个通道的值
                # pixels[pos+0] = fol_pos[0]
                # pixels[pos+1] = fol_pos[1]
                # pixels[pos+2] = fol_pos[2]
                # pixels[pos+3] = 255 
            
            # pm.delete(fol)

        # # NOTE 返回裁剪的 Image
        # img = om.MImage()
        # img.setPixels(pixels, width, height)

        # img.writeToFile(r'C:\Users\timmyliang\Desktop\FX\test\1.tif', 'tif')

def onMayaDroppedPythonFile(*args):
    parentTab = mel.eval('''global string $gShelfTopLevel;string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;''')
    module,ext = os.path.splitext(os.path.basename(__file__))
    pm.shelfButton( commandRepeatable = True, image1 = "pythonFamily.png",iol = "FXPath" ,label = "Path_Tracker_Win", parent = parentTab, command = dedent("""
        import {module}
        reload({module})
        {module}.show()
    """.format(module=module)))

    show()
    
def show():
    UI_Name = "Path_Tracker_Win"
    if pm.window(UI_Name,ex=1):
        pm.deleteUI(UI_Name)

    window = pm.window(UI_Name,title=u"特效轨迹导出工具" )
    pm.columnLayout( adjustableColumn=True )
    pm.button( label=u'生成跟随面片',command=generateFollowPlane )
    pm.button( label=u'导出', command=exportPlane)
    pm.setParent( '..' )
    pm.showWindow( window )

if __name__ == "__main__":
    show()

# import sys
# MODULE = r"F:\MayaTecent\MayaScript\misc\pathTracker"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import pathTracker
# reload(pathTracker)
# pathTracker.show()