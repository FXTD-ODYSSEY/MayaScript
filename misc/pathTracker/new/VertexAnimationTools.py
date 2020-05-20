# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-20 16:32:05'

"""

"""

# "Vertex Animations Tools for Maya" converted to python from Maxscript by Jared Taylor
# Original Maxscript "Vertex Animation Tools" by Jonathan Lindquist at Epic Games
# modified by Makoto Hiura 2020/02/07
import os
from textwrap import dedent

import pymel.core as pm
import maya.cmds as cm
import maya.mel as mel # added by Hiura
from functools import partial
import EXR_Dumper as exr
import VertexAnimationTools_CMDS as ac
from VertexAnimationTools_CMDS import Undo
from VertexAnimationTools_CMDS import rpartial
from VertexAnimationTools_CMDS import hideViewport

# >>>> added by Hiura
import struct
from PySide2 import QtGui
QImage = QtGui.QImage
# <<<< added by Hiura

##############################################################################
##  save to PNG file
##############################################################################

def create_normal_img(width=8, height=8):
    img = QImage(width, height, QImage.Format_ARGB32)
    img.fill(0)
    return img

def set_normal_image(img, frameNum, vertexNum, bufferData):
    imgData_ptr = img.bits()
    buffer_size = img.byteCount()

    for i in range(frameNum):
        data = bufferData[i]
        for j in range(vertexNum):
            data = bufferData[i]
            normal = data[j]
            R = int(normal[0]*255.0)
            G = int(normal[1]*255.0)
            B = int(normal[2]*255.0)
            A = 255
            pixel = A * 256 * 256 * 256 + R * 256 * 256 + G * 256 + B
            normal_color = struct.pack("I", pixel)

            idx = i * vertexNum + j
            imgData_ptr[idx*4:idx*4+4] = normal_color

    return

##############################################################################


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

def auto_frames(min_if, max_if, *args):
    with Undo(0):
        cm.intField(min_if, e=1, v=cm.playbackOptions(q=1, min=1))
        cm.intField(max_if, e=1, v=cm.playbackOptions(q=1, max=1))


class UI(object):
    def __init__(self):
        # Core Functions
        def get_frame_start():
            return cm.intField(self.frame_start, q=1, v=1)

        def get_frame_end():
            return cm.intField(self.frame_end, q=1, v=1)

        def get_vert_count(model):
            return cm.polyEvaluate(model, v=1)

        def check_model(model):
            return model and cm.objectType(cm.listRelatives(model, c=1, s=1)[0]) == "mesh" and get_vert_count(model) > 0

        def get_vert_pos(model, index):  # 183
            # return cm.xform(model[0] + ".vtx[" + str(index) + "]", q=1, ws=1, t=1)
            return cm.xform(model + ".vtx[" + str(index) + "]", q=1, ws=1, t=1) # modified by Hiura

        def remove_meshes():  # 295
            if len(self.morph_array[0]) > 0 and self.morph_array[0]:
                # for mesh in self.morph_array[0]:
                for mesh in self.morph_array: # modified by Hiura
                    cm.delete(mesh)
                self.morph_array = []

        def snapshot(model, time):
            cm.currentTime(time)
            snap_node = cm.snapshot(model, st=time, et=time, ch=0)
            snap = cm.listRelatives(snap_node, c=1)[0]
            snap = cm.parent(snap, w=1)
            cm.delete(snap_node)
            return snap

        def store_original_vert_positions(progressBar, progressStep):  # 138
            self.original_vert_positions = []
            lastProgress = 0 # added by Hiura
            for i in range(self.vert_count):
                pos = cm.xform(self.original_mesh + ".vtx[" + str(i) + "]", q=1, ws=1, t=1)
                self.original_vert_positions.append(pos)
                # >>>> added by Hiura
                nowProgress = int(float(progressStep) * float(i) / float(self.vert_count))
                if nowProgress > lastProgress:
                    cm.progressBar(progressBar, edit=True, step=int(nowProgress - lastProgress))
                    lastProgress = nowProgress;
                # <<<< added by Hiura
            return self.original_vert_positions

        def smooth_copy(mesh, progressBar, progressStep):  # 331
            # orig_name = mesh[0]
            orig_name = self.static_base_meshes[0] # modified by Hiura
            # self.original_mesh = snapshot(mesh[0], 0)
            self.original_mesh = snapshot(mesh, 0) # modified by Hiura
            self.original_mesh = cm.rename(self.original_mesh, orig_name + "_MorphExport")
            cm.polySoftEdge(self.original_mesh, a=180, ch=0)
            self.vert_count = get_vert_count(self.original_mesh)
            store_original_vert_positions(progressBar, progressStep)

        def pack_vert_uvs(mesh, progressBar, progressStep):  # 151
            cm.polyTriangulate(mesh, ch=0)
            anim_uvs = cm.polyUVSet(mesh, create=1, uvSet="anim_map")
            cm.polyUVSet(mesh, currentUVSet=1, uvSet=anim_uvs[0])
            cm.polyAutoProjection(mesh, lm=0, pb=0, ibd=1, cm=0, l=2, sc=1, o=1, p=6, ps=0.2, ws=0, ch=0)
            cm.polyMapSewMove(mesh)
            lastProgress = 0 # added by Hiura
            for i in range(self.vert_count):
                current_position = (float(i) + 0.5) / self.vert_count
                # cm.polyColorPerVertex(mesh, rgb=[current_position, .5, 0]) # deleted by Hiura
                # >>>> modified by Hiura ( based on bryan_smyth'post )
                # cm.polyEditUV(mesh + ".map[" + str(i) + "]", u=current_position, v=.501961, r=0)
                cm.polyEditUV(mesh + ".map[" + cm.polyListComponentConversion(mesh+".vtx[%d]"%i, fv=True, tuv=True)[0].split("[")[-1][:-1] + "]", u=current_position, v=.501961, r=0)
                # <<<< modified by Hiura
                self.vertex_uv_position.append(current_position)
                # >>>> added by Hiura
                nowProgress = int(float(progressStep) * float(i) / float(self.vert_count))
                if nowProgress > lastProgress:
                    cm.progressBar(progressBar, edit=True, step=int(nowProgress - lastProgress))
                    lastProgress = nowProgress;
                # <<<< added by Hiura

        def make_snapshots_array(model_snap):  # 229 - create morph targets
            frame_array = []
            frame_skip = cm.intField(self.frame_skip, q=1, v=1)
            # >>>> deleted by Hiura
            # for frame in range(get_frame_end()+1):
            #    if frame % (frame_skip + 1) == 0:  # frame skipping logic
            #       new_time = get_frame_start() + frame
            # <<<< deleted by Hiura
            for frame in range(get_frame_start(), get_frame_end()+1, (frame_skip + 1)): # modified by Hiura
                new_time = frame
                snap = snapshot(model_snap, new_time)
                # snap = cm.parent(snap, w=1)
                cm.polyNormal(snap, nm=2, ch=0)
                frame_array.append(snap)
            return frame_array

        def make_merge_snapshots(model_array):  # 250
            # reinit_vars()
            if len(model_array) > 0:  # model_array is the static base meshes
                for model in model_array:
                    if check_model(model):
                        self.morph_array.append(make_snapshots_array(model))

                # combine multiple objects into one object so morph texture can be shared
                morph_count = len(self.morph_array)

                # >>>> deleted by Hiura
                # if morph_count > 1:
                #     for i in range(1, len(morph_count)):
                #         for frame in range(morph_count):
                #             current_master = self.morph_array[0][frame]
                #             cm.parent(self.morph_array[i][frame], current_master)

                # morph_initial = self.morph_array[0][0]
                # self.morph_array.append(morph_initial)
                # <<<< deleted by Hiura

                # >>>> added by Hiura
                unite_array = []
                if morph_count <= 1:
                    for frame in range(len(self.morph_array[0])):
                        tmp_mesh = self.morph_array[0][frame]
                        unite_array.append(tmp_mesh[0])
                else:
                    for i in range(1, morph_count):
                        for frame in range(len(self.morph_array[i])):
                            current_master = self.morph_array[0][frame]
                            cm.parent(self.morph_array[i][frame], current_master)

                    for frame in range(len(self.morph_array[0])):
                        current_master = self.morph_array[0][frame]
                        tmp_mesh = cm.polyUnite(current_master)
                        unite_array.append(tmp_mesh[0])
                        cm.delete(current_master)

                self.morph_array = []
                self.morph_array = unite_array
                # <<<< added by Hiura

        def populate_morph_arrays(progressBar, progressStep):  # 193
            # morph_count = len(self.morph_array[0])
            morph_count = len(self.morph_array) # modified by Hiura
            lastProgress = 0 # added by Hiura
            for i in range(morph_count):
                self.current_morph_normal_array = []
                self.current_morph_offset_array = []
                # current_morph = self.morph_array[0][i]
                current_morph = self.morph_array[i] # modified by Hiura
                # >>>> added by Hiura
                nowProgress = int(float(progressStep) * float(i) / float(morph_count))
                if nowProgress > lastProgress:
                    cm.progressBar(progressBar, edit=True, step=int(nowProgress - lastProgress))
                    lastProgress = nowProgress;
                # <<<< added by Hiura
                for j in range(self.vert_count):
                    # normals
                    # old_normal = cm.polyNormalPerVertex(current_morph[0] + ".vtx[" + str(j) + "]", q=1, xyz=1)[0:3]
                    old_normal = cm.polyNormalPerVertex(current_morph + ".vtx[" + str(j) + "]", q=1, xyz=1)[0:3] # modified by Hiura
                    old_normal = ac.normalize(old_normal)
                    old_normal[0] = (((old_normal[0] * 1.0) + 1.0) * 0.5)
                    # old_normal[1] = (((old_normal[1] * -1.0) + 1.0) * 0.5) # deleted by Hiura
                    old_normal[1] = (((old_normal[1] * 1.0) + 1.0) * 0.5) # modified by Hiura
                    old_normal[2] = (((old_normal[2] * 1.0) + 1.0) * 0.5)
                    # >>>> modified by Hiura
                    # old_normal = [old_normal[2], old_normal[1], old_normal[0]]
                    # swap y-up and z-up
                    old_normal = [old_normal[0], old_normal[2], old_normal[1]]
                    # <<<< modified by Hiura
                    self.current_morph_normal_array.append(old_normal)

                    # offsets
                    original_vert_pos = self.original_vert_positions[j]
                    # swap y-up and z-up
                    original_vert_pos = [original_vert_pos[0], original_vert_pos[2], original_vert_pos[1]] # added by Hiura

                    current_model_vert_pos = get_vert_pos(current_morph, j)
                    # swap y-up and z-up
                    current_model_vert_pos = [current_model_vert_pos[0], current_model_vert_pos[2], current_model_vert_pos[1]] # added by Hiura
                    current_offset = ac.sub(current_model_vert_pos, original_vert_pos)
                    # current_offset = [current_offset[2], current_offset[1] * -1.0, current_offset[0]] # deleted by Hiura

                    # swap R and B In RGB
                    current_offset = [current_offset[2], current_offset[1], current_offset[0]] # added by Hiura

                    # >>>> deleted by Hiura
                    # current_offset = [cm_to_inch / 2.54 for cm_to_inch in current_offset]
                    # current_offset[1] *= 0.5
                    # <<<< deleted by Hiura

                    self.current_morph_offset_array.append(current_offset)

                self.morph_vert_offset_array.append(self.current_morph_offset_array)
                self.morph_normal_array.append(self.current_morph_normal_array)

        def render_out_textures():  # 271
            ext = ".exr"
            texture_file = cm.fileDialog2(fm=0, ff="*" + ext)[0]
            normals_file = texture_file.replace(ext, "_Normals" + ext)
            if texture_file:
                width = self.vert_count
                height = len(self.morph_vert_offset_array)

                # >>>> added by Hiura
                normal_img = create_normal_img(width, height)
                ext2 = ".png"
                normals2_file = texture_file.replace(ext, "_Normals" + ext2)
                buf = "sysFile -delete \"" + texture_file + "\"" # delete old file
                mel.eval(buf);
                buf = "sysFile -delete \"" + normals2_file + "\"" # delete old file
                mel.eval(buf);
                set_normal_image(normal_img, height, width, self.morph_normal_array)
                normal_img.save(normals2_file, "PNG")
                # <<<< added by Hiura

                pixels = [
                               pixel for
                               sub_list in self.morph_vert_offset_array for
                               pixel_list in sub_list for
                               pixel in pixel_list
                ]
                # >>>> deleted by Hiura
                #normal_pixels = [
                #               pixel for
                #               sub_list in self.morph_normal_array for
                #               pixel_list in sub_list for
                #               pixel in pixel_list
                #]
                # <<<< deleted by Hiura

                exr.dump_to_exr_rgb16uncomp(height, width, pixels, texture_file)
                # exr.dump_to_exr_rgb16uncomp(height, width, normal_pixels, normals_file) # deleted by Hiura

                self.exportFBX(texture_file.replace(ext, "_mesh.fbx"))

        @hideViewport
        def process_keyframe_animation_btn(*args):  # 377
            reinit_vars()
            #
            with Undo():
                for selected in cm.ls(sl=1):
                    if check_model(selected):
                        self.static_base_meshes.append(selected)

                # >>>> added by Hiura
                bCanceled = False
                if len(self.static_base_meshes) > 0:
                    for one_mesh in self.static_base_meshes:
                        time = 0

                        tmp_node = cm.snapshot(one_mesh, st=time, et=time, ch=0)
                        tmp_snap = cm.listRelatives(tmp_node, c=1)[0]
                        tmp_snap = cm.parent(tmp_snap, w=1)

                        cm.polySoftEdge(tmp_snap, a=180, ch=0)
                        cm.polyTriangulate(tmp_snap, ch=0)
                        org_num = get_vert_count(one_mesh)
                        new_num = get_vert_count(tmp_snap)
                        if org_num != new_num:
                            buf = 'Warning! Vertex Number Change.\n  original=' + str(org_num) + ' new=' + str(new_num) + '\n\nMaybe not working properly.\nContinue?'
                            ret = cm.confirmDialog( title='Confirm', message=buf, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
                            if ret != 'Yes':
                                bCanceled = True
                        cm.delete(tmp_snap)
                        cm.delete(tmp_node)
                # <<<< added by Hiura

                if not bCanceled:
                    if len(self.static_base_meshes) > 0:
                        # >>>> added by Hiura
                        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar');
                        cm.progressBar( gMainProgressBar,
                                          edit=True,
                                          beginProgress=True,
                                          isInterruptable=False,
                                          status='"VAT Converting ...',
                                          minValue=0,
                                          maxValue=100 )
                        # <<<< added by Hiura

                        make_merge_snapshots(self.static_base_meshes)
                        cm.progressBar(gMainProgressBar, edit=True, step=5) # added by Hiura
                        # smooth_copy(self.morph_array[0][0], gMainProgressBar, 15)
                        smooth_copy(self.morph_array[0], gMainProgressBar, 15) # modified by Hiura
                        pack_vert_uvs(self.original_mesh, gMainProgressBar, 30)
                        populate_morph_arrays(gMainProgressBar, 50)
                        remove_meshes()

                        cm.progressBar(gMainProgressBar, edit=True, endProgress=True) # added by Hiura

                        render_out_textures()
                        #..
                    else:
                        cm.warning("No applicable meshes selected")

        def reinit_vars():
            self.morph_array = []
            self.static_base_meshes = []
            self.original_vert_positions = []
            self.original_mesh = None
            self.vert_count = 0
            self.vertex_uv_position = []
            self.morph_normal_array = []
            self.morph_vert_offset_array = []
            self.current_morph_normal_array = []
            self.current_morph_offset_array = []

        self.morph_array = []
        self.static_base_meshes = []
        self.original_vert_positions = []
        self.original_mesh = None
        self.vert_count = 0
        self.vertex_uv_position = []
        self.morph_normal_array = []
        self.morph_vert_offset_array = []
        self.current_morph_normal_array = []
        self.current_morph_offset_array = []

        with Undo(0):
            if cm.window("VertexAnimToolsWindow", exists=1):
                cm.deleteUI("VertexAnimToolsWindow")

            self.window = cm.window("VertexAnimToolsWindow", title="Vertex Anim Tools", w=150)
            self.layout = cm.rowColumnLayout(nr=2, p=self.window)

            self.tools_layout = cm.frameLayout(l="Vertex Animation Tools", mh=10)

            # -- Vertex Animation -- #
            self.vertex_layout = cm.frameLayout(l="Plane Animation", cll=1, mh=2, p=self.tools_layout)
            self.plane_button = cm.button(l="Generate Plane", h=25,c=partial(self.generateFollowPlane, "generateFollowPlane"))

            self.keyframe_layout = cm.frameLayout(l="Keyframe Animation", cll=1)
            self.keyframe_split = cm.rowColumnLayout(nc=2)
            self.frame_range_layout = cm.rowColumnLayout(nr=3)

            # -- Keyframe Animation Fields & Buttons -- #
            cm.rowColumnLayout(nc=2, p=self.frame_range_layout)
            cm.text(l="Start Frame: ")
            self.frame_start = cm.intField(v=0)

            cm.rowColumnLayout(nc=2, p=self.frame_range_layout)
            cm.text(l="End Frame:  ")
            self.frame_end = cm.intField(v=0)

            cm.rowColumnLayout(nc=2, p=self.frame_range_layout)
            cm.text(l="Frame Skip: ")
            self.frame_skip = cm.intField(v=0)

            self.auto_frames_btn = cm.button(l="<< Slider", w=55, p=self.keyframe_split)
            self.keyframe_btn = cm.button(l="Process Keyframe Animation", h=25, p=self.keyframe_layout)

            # -- Button Commands -- #
            cm.button(self.auto_frames_btn, e=1, c=partial(auto_frames, self.frame_start, self.frame_end))
            cm.button(self.keyframe_btn, e=1, c=rpartial(process_keyframe_animation_btn, "Process Keyframe Animation"))

            # # -- Sequence Processor -- #
            # self.image_layout = cm.frameLayout(l="Export FBX", cll=1, cl=1, p=self.layout)
            # self.export_button = cm.button(l="Select Mesh To Export", h=25,c=rpartial(self.exportFBX, "Export FBX"))

            # -- Initial functions & Show UI -- #
            auto_frames(self.frame_start, self.frame_end)
            cm.showWindow(self.window)
            cm.window(self.window, e=1, resizeToFitChildren=1, wh=(1, 1))

    def exportFBX(self,export_FBX):
        SetFbxParameter()
        mel.eval('FBXExport -f "' + export_FBX + '" -s')

    def generateFollowPlane(self,*args):
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
            motion_path = pm.PyNode(motion_path)
            flow_node,ffd_node,lattice_node,ffd_base =pm.flow( plane,dv=(100, 2, 2))

            # NOTE 设置外部影响
            ffd_node.outsideLattice.set(1)
            ffd_node.local.set(1)
            plane_node.width.set(50)

            lattice_node.v.set(0)
            ffd_base.v.set(0)

            # NOTE 设置 Parametric Length 匹配位置
            motion_path.fractionMode.set(0)
            animCurve = motion_path.listConnections(type="animCurve")[0]
            # NOTE 关键帧设置为线性
            animCurve.setTangentTypes(range(animCurve.numKeys()),inTangentType="linear",outTangentType="linear")

            # NOTE 打组
            pm.group(lattice_node,ffd_base,plane,anim_curve,n=sel+"_follow_grp")
            pm.select(plane)


def onMayaDroppedPythonFile(*args):
    parentTab = mel.eval('''global string $gShelfTopLevel;string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;''')
    DIR = os.path.dirname(__file__)
    module,ext = os.path.splitext(os.path.basename(__file__))
    pm.shelfButton( commandRepeatable = True, image1 = "pythonFamily.png",iol = "FXPath" ,label = "Path_Tracker_Win", parent = parentTab, command = dedent("""
        import sys
        MODULE = r"{DIR}"
        sys.path.insert(0,MODULE) if MODULE not in sys.path else None
        import VertexAnimationTools
        VertexAnimationTools.UI()
    """.format(DIR=DIR)))

    import sys
    MODULE = DIR
    sys.path.insert(0,MODULE) if MODULE not in sys.path else None
    import VertexAnimationTools
    VertexAnimationTools.UI()

# import sys
# MODULE = r"C:\Users\timmyliang\Desktop\VertexAnimationTools_Maya"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import VertexAnimationTools_CMDS
# reload(VertexAnimationTools_CMDS)
# import VertexAnimationTools
# reload(VertexAnimationTools)
# VertexAnimationTools.UI()