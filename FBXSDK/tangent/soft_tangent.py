# -*- coding: utf-8 -*-
"""
Maya 利用 fbx SDK 将平均化法线合并到 tangent 里面
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-06-11 22:36:20'

import os
import tempfile


class SetTangentMixin(object):
    SOFT_FBX_PATH = os.path.join(tempfile.gettempdir(), "softRig.fbx")
    def _export_soft_fbx(self):
        import pymel.core as pm
        from maya import mel

        meshes = self._soft_mesh()
        pm.select(meshes, r=True)
        mel.eval('FBXExport -f "%s" -s' % self.SOFT_FBX_PATH.replace("\\", "/"))
        pm.delete(meshes)

    def _soft_mesh(self):
        import pymel.core as pm
        import pymel.core.nodetypes as nt

        new_meshes = []
        for mesh in pm.ls(sl=1, dag=1):
            if hasattr(mesh, "getShape") and isinstance(mesh.getShape(), nt.Mesh):
                # TODO 如果 outline 模型用调整的法线
                outline_mesh = mesh + "_outline"
                if not pm.objExists(outline_mesh):
                    outline_mesh = pm.duplicate(mesh, n=outline_mesh)[0]
                    pm.polyNormalPerVertex(outline_mesh, unFreezeNormal=True)
                    # NOTE 硬化边
                    pm.polySoftEdge(outline_mesh, angle=0, constructionHistory=False)
                    # NOTE 平均法线
                    pm.polyAverageNormal(outline_mesh)
                new_meshes.append(outline_mesh)
        return new_meshes

    @staticmethod
    def _read_fbx_attribute(path, attribute):
        import FbxCommon
        from fbx import FbxNodeAttribute

        manager, scene = FbxCommon.InitializeSdkObjects()
        result = FbxCommon.LoadScene(manager, scene, path)
        if not result:
            return

        data = {}
        for i in range(scene.GetNodeCount()):
            node = scene.GetNode(i)
            mesh = node.GetNodeAttribute()
            if not mesh or mesh.GetAttributeType() != FbxNodeAttribute.eMesh:
                continue

            attr = getattr(mesh, "GetElement%s" % attribute.capitalize())()
            if not attr:
                continue
            data[node.GetName()] = attr.GetDirectArray()

        return {"manager": manager, "scene": scene, "data": data}

    def set_tangent(self, fbx_path, meshes):
        import FbxCommon
        import pymel.core as pm

        pm.select(meshes)
        self._export_soft_fbx()
        origin_data = self._read_fbx_attribute(fbx_path, "Tangent")
        target_data = self._read_fbx_attribute(self.SOFT_FBX_PATH, "Normal")
        manager = origin_data["manager"]
        scene = origin_data["scene"]
        tangent_data = origin_data["data"]
        normal_data = target_data["data"]
        for name, array in tangent_data.items():
            normals = normal_data[name + "_outline"]
            array.Clear()
            for normal in normals:
                array.Add(normal)

        FbxCommon.SaveScene(manager, scene, fbx_path, 0)