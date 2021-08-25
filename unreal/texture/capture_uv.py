# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-18 17:16:54'



import unreal
from functools import partial
from Qt import QtCore

red_lib = unreal.RedArtToolkitBPLibrary
render_lib = unreal.RenderingLibrary
level_lib = unreal.EditorLevelLibrary
sys_lib = unreal.SystemLibrary
static_mesh_lib = unreal.EditorStaticMeshLibrary
defer = QtCore.QTimer.singleShot

path = "/Game/Test/NewFolder9/BP_UVCapture.BP_UVCapture"
bp = unreal.load_asset(path)
RT = unreal.load_asset("/Game/Test/NewFolder9/RT_UV.RT_UV")


# NOTE 记录和隐藏所有 Actor 的显示
vis_dict = {}
for actor in level_lib.get_all_level_actors():
    vis = actor.is_temporarily_hidden_in_editor()
    vis_dict[actor] = vis
    actor.set_is_temporarily_hidden_in_editor(True)

# NOTE 蓝图生成到场景里面
uv_material = unreal.load_asset("/Game/Test/NewFolder9/M_UVCapture.M_UVCapture")


mesh_2 = unreal.load_asset(
    "/Game/Test/NewFolder9/aaa_magellan002_body_d1.aaa_magellan002_body_d1"
)
# mesh_1 = unreal.load_asset("/Game/Test/NewFolder9/aaa.aaa")
mesh_1 = unreal.load_asset(
    "/Game/ArtResources/Characters/A_Arlong/Skel_Mesh/Skel_Arlong01_L_rig.Skel_Arlong01_L_rig"
)
meshes = [mesh_1, mesh_2]


def get_static_materials(mesh):
    return [
        mesh.get_material(i) for i in range(static_mesh_lib.get_number_materials(mesh))
    ]


def get_skeletal_materials(mesh):
    return [
        m.get_editor_property("material_interface")
        for m in mesh.get_editor_property("materials")
    ]


def capture(mesh):
    # NOTE 删除 capture
    capture_actor = level_lib.spawn_actor_from_object(bp, unreal.Vector())
    capture_comp = capture_actor.get_editor_property("capture")

    if isinstance(mesh, unreal.StaticMesh):
        static_comp = capture_actor.get_editor_property("static")
        static_comp.set_editor_property("static_mesh", mesh)
        static_comp = capture_actor.get_editor_property("static")
        materials = get_static_materials(mesh)
        static_comp.set_editor_property(
            "override_materials", [uv_material] * len(materials)
        )
    elif isinstance(mesh, unreal.SkeletalMesh):
        skeletal_comp = capture_actor.get_editor_property("skeletal")
        skeletal_comp.set_editor_property("skeletal_mesh", mesh)
        skeletal_comp = capture_actor.get_editor_property("skeletal")
        materials = get_skeletal_materials(mesh)
        skeletal_comp.set_editor_property(
            "override_materials", [uv_material] * len(materials)
        )

    capture_comp.capture_scene()
    defer(
        500,
        lambda: (
            render_lib.render_target_create_static_texture2d_editor_only(RT, "UV_map"),
            capture_actor.destroy_actor(),
        ),
    )


def end_call(vis_dict):
    # NOTE 删除蓝图 & 恢复场景的显示
    for actor, vis in vis_dict.items():
        actor.set_is_temporarily_hidden_in_editor(vis)


interval = 1000
for i, mesh in enumerate(meshes, 1):
    defer(interval * i, partial(capture, mesh))
defer(interval * (i + 1), partial(end_call, vis_dict))
