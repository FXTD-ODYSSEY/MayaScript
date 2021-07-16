# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-22 11:06:11'

"""

"""

import pymel.core as pm
import pymel.core.nodetypes as nt

class NormalData(object):
    def __init__(self,mesh):
        mesh = mesh[0] if hasattr(mesh,"__iter__") else mesh
        mesh = mesh.node() if hasattr(mesh,"node") else mesh
        self.mesh = mesh.getShape() if hasattr(mesh,"getShape") else mesh
        if type(self.mesh) is not nt.Mesh:
            raise RuntimeError("Please Pass a Mesh object to NormalData Class")

    def __getitem__(self,item):
        vtxFace = self.mesh.vtxFace[item]
        return {face_idx:pm.polyNormalPerVertex(vtxFace[face_idx],q=1,normalXYZ=1) for _,face_idx in vtxFace.indicesIter()}

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__,self.mesh)

mesh_normal = NormalData(pm.selected())

print(mesh_normal[0])
