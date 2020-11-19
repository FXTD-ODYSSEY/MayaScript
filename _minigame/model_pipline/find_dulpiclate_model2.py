# -*- coding: utf-8 -*-
"""
材质拓扑一致的模型进行实例替换
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-17 00:00:27'

import os
import json
from collections import defaultdict

import pymel.core as pm
import pymel.core.nodetypes as nt


def error_log(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except:
            import traceback
            print(u"程序错误 | 请联系 梁伟添 timmyliang\n\n%s" % traceback.format_exc())

    return wrapper

@error_log
def main():
        
    export_dir = r"D:\_minigame\_scene\test"
    mtl_list = [mtl for mtl in pm.ls(materials=1) if isinstance(mtl,nt.Phong)]
    # m = pm.PyNode('bas_ca_wall_stone_12m_00_mat_wet')
    # mtl_list = [m]

    for i,mtl in enumerate(mtl_list):

        # if i > 20:
        #     break

        # obj_list = pm.hyperShade(objects=mtl)
        obj_list = [obj for se in mtl.connections()
                    if isinstance(se, nt.ShadingEngine)
                    for obj in se.connections()
                    if isinstance(obj, nt.Transform)]
        if not obj_list:
            continue

        grp = pm.group(obj_list,n="EXPORT_#",w=1)
        data = defaultdict(list)
        for mesh in obj_list:
            data[mesh.numTriangles()].append(mesh)
        # NOTE 清空小于等于 1 的模型
        obj_list = [data.pop(verts) for verts,m_list in data.items() if len(m_list) <= 1]
        # if not obj_list:
        #     pm.delete(grp)
            
        # if not data.values():
        #     continue
        # export_folder = os.path.join(export_dir,str(mtl))
        # if not os.path.exists(export_folder):
        #     os.makedirs(export_folder)
            
        # TODO 获取每个模型的位置
        for mesh_list in data.values():
            
            try:

                loc_list = []
                for i,mesh in enumerate(mesh_list):
                    # NOTE 居中轴心
                    pm.parent(mesh,w=1)
                    pm.xform(mesh,cp=1)
                    loc = pm.spaceLocator(n="SOCKET_#")
                    pm.parentConstraint(mesh,loc,mo=0)
                    pm.scaleConstraint(mesh,loc,mo=0)
                    loc_list.append(loc)
                
                m = mesh
                m_name = m.shortName().replace("|","_")
                m_name = m_name[1:] if m_name.startswith("_") else m_name
                pm.parent(mesh,w=1)
                pm.select(mesh)
                pm.mel.BakeCustomPivot()
                mesh.t.set(0,0,0)
                mesh.r.set(0,0,0)
                path = os.path.join(export_dir,"%s.fbx" % m_name)
                pm.mel.FBXExport(f=path,s=None)
                
                # pm.delete(mesh_list)
                
                tri = pm.polyCreateFacet( ch=0,p=[(0.0, 0.0, 0.0), (0.10, 0.0, 0.0), (0.10, 0.10, 0.0)],n="LocContainer")[0]
                pm.parent(loc_list,tri)
                pm.select(tri)
                pm.hyperShade( assign=mtl )
                path = os.path.join(export_dir,"%s_loc.fbx" % m_name)
                pm.mel.FBXExport(f=path,s=None)
                # pm.delete(tri)
            except:
                print("fail",mesh_list)
                continue
                
if __name__ == "__main__":
    main()