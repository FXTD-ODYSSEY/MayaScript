# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-05 23:11:59'

"""
检查模型拓扑是否一致
选择两个模型所有环边 比对 环边数组是否一致判断拓扑结构是否一致 
"""
import json
import time
import hashlib
import pymel.core as pm
from maya import OpenMaya
from functools import partial, wraps

def endPorgress(func):
    def wrapper(*args, **kwargs):
        res = None
        try:
            res = func(*args, **kwargs)
        except:
            import traceback
            traceback.print_exc()
        finally:
            pm.progressWindow(ep=1)
        return res
    return wrapper

def logTime(func=None, msg="elapsed time:"):
    """logTime 
    log function running time

    :param func: function get from decorators, defaults to None
    :type func: function, optional
    :param msg: default print message, defaults to "elapsed time:"
    :type msg: str, optional
    :return: decorator function return
    :rtype: dynamic type
    """            
    if not func: return partial(logTime,msg=msg)
    @wraps(func)
    def wrapper(*args, **kwargs):
        curr = time.time()
        res = func(*args, **kwargs)
        print(msg,time.time() - curr)
        return res
    return wrapper

@logTime
@endPorgress
def checkTopology(display=False,sleep=0.05):
    
    sel_list = [mesh for mesh in pm.ls(pm.pickWalk(d="down"),type="mesh")]

    if len(sel_list) != 2:
        pm.headsUpMessage("Please select 2 Mesh")
        return 

    num_list = [(sel.numVertices(),sel.numEdges(),sel.numFaces()) for sel in sel_list]
    if num_list[0] != num_list[1]:
        return  False

    edge_num = num_list[0][1]

    pm.progressWindow(	
        title="Check Topology",
        progress=0.0,
        isInterruptable=True )

    res_list = []
    for i,sel in enumerate(sel_list):
        edge_loop_list = []
        edge_list = set(range(edge_num))
        pm.progressWindow( e=1, status = 'second mesh Analysis' if i else 'first mesh Analysis')
        while len(edge_list) > 1:
            idx = next(iter(edge_list), None)
            if pm.progressWindow( query=1, isCancelled=1 ) : 
                return
            pm.progressWindow( e=1, progress=(1-len(edge_list)/edge_num)*100 )

            if idx is None: break
            if display:
                edge_loop = pm.polySelect(sel,edgeLoop=idx,r=1)
                pm.refresh()
                time.sleep(sleep) if sleep > 0 else None
            else:
                edge_loop = pm.polySelect(sel,edgeLoop=idx,ns=1)
            edge_loop_list.append(edge_loop)
            edge_list -= set(edge_loop)
        res_list.append(edge_loop_list)

    return  res_list[0] == res_list[1]



class MeshTopology(object):
    def __init__(self, mesh_node):
        self.py_node = pm.PyNode(mesh_node)
        if self.py_node.type() == u'transform':
            self.py_node = self.py_node.getShape()
        if self.py_node.type() != u'mesh':
            raise TypeError('mesh_node must be a mesh type object.')

    @property
    def topology_structure(self):
        data = []

        # for f in self.py_node.f:
        #     data[f.index()] = f.getVertices()

        # NOTE OpenMaya 优化
        dag = self.py_node.__apimdagpath__()
        itr = OpenMaya.MItMeshPolygon(dag)
        while not itr.isDone():
            vtx_list = OpenMaya.MIntArray()
            itr.getVertices(vtx_list)
            data.append(list(vtx_list))
            itr.next()
        return data

    def to_json(self):
        return json.dumps(self.topology_structure)

    def to_md5(self):
        return hashlib.md5(self.to_json()).hexdigest()

    @logTime
    def __eq__(self, other):
        return self.to_md5() == other.to_md5()

def solution_1():
    i, j = pm.selected()
    print(MeshTopology(i) == MeshTopology(j))

def solution_2():
    print (checkTopology(display=False))


if __name__ == '__main__':
    # solution_1()
    solution_2()
