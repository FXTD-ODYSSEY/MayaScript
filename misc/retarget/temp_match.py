import pymel.core as pm
from maya import mel
import os
import time
from functools import partial
animation_path = r"X:\Characters\Fight\90302_Darius"
retarget_dir = r"X:\Characters\Fight\90302_Darius\FBX"
hik_rig = r"X:\Characters\Fight\jnt.mb"

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
    mel.eval('FBXExportSmoothMesh -v false')
    mel.eval('FBXExportEmbeddedTextures -v false')
    mel.eval('FBXExportCameras -v false')
    mel.eval('FBXExportBakeResampleAnimation -v false')
    mel.eval('FBXExportSkeletonDefinitions -v true')

# NOTE 导出文件
def exportFBX(file_path):
    SetFbxParameter()
    # NOTE 更新重定向
    mel.eval("""
    optionMenuGrp -e -select 2 hikCharacterList;
    hikUpdateCurrentCharacterFromUI(); hikUpdateContextualUI();
    optionMenuGrp -e -select 2 hikSourceList;
    hikUpdateCurrentSourceFromUI(); hikUpdateContextualUI();
    """)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    export_path = os.path.join(retarget_dir,base_name+".fbx").replace("\\","/")
    print ("export_path",export_path)

    timeStart = pm.playbackOptions(q=1,min=1)
    timeEnd = pm.playbackOptions(q=1,max=1)
    pm.bakeResults(
        pm.ls("root",dag=1,ni=1),
        simulation = 1,
        t = (timeStart,timeEnd),
        sampleBy = 1, 
        disableImplicitControl = 1, 
        preserveOutsideKeys = 1, 
        minimizeRotation = 1, 
        at=['tx','ty','tz','rx','ry','rz','sx','sy','sz']
    )
    pm.select("root")
    pm.evalDeferred(lambda:mel.eval('FBXExport -f "' + export_path + '" -s'))

def batchExport(file_path):
    
    # NOTE 导入 reference
    ref = pm.createReference(hik_rig,r=1,namespace="jnt")
    ref.importContents(True)

    # org_namespace = "Darius_rig_:"
    # NOTE 约束武器
    org_wp = "*:wp_jnt_ctrl"
    pm.parentConstraint(pm.ls(org_wp),"wp_jnt_skin",mo=0)

    pm.evalDeferred(lambda:exportFBX(file_path))

def loadFile(file_path,open_file=True):
    # NOTE 打开文件
    if open_file:
        pm.openFile(file_path,f=1)
    batchExport(file_path)


mel.eval("ToggleCharacterControls;")

for i,file_name in enumerate(os.listdir(animation_path)):
    if not file_name.endswith(".mb") and not file_name.endswith(".ma"):
        continue
    print("file_name",file_name)
    file_path = os.path.join(animation_path,file_name)
    
    pm.evalDeferred( partial (loadFile,file_path) ,lowestPriority=1)
    
    # if i > 3:
    #     break

# NOTE 单个文件处理
# file_path = pm.sceneName()
# pm.evalDeferred( partial (loadFile,file_path,False) ,lowestPriority=1)
