# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-05 23:11:59'

"""
检查模型拓扑是否一致
选择两个模型所有环边 比对 环边的数量是否一致 
"""

import pymel.core as pm

# sel_list = pm.ls(sl=1)
def checkTopology():
    
    sel_list = [mesh for mesh in pm.ls(pm.pickWalk(d="down"),type="mesh")]

    if len(sel_list) != 2:
        pm.headsUpMessage("Please select 2 Mesh")
        return 

    res_list = []
    for sel in sel_list:
        edge_loop_list = []
        edge_list = set(range(sel.numEdges()))
        while len(edge_list) > 1:
            idx = next(iter(edge_list), None)
            if idx is None: break
            edge_loop = pm.polySelect(sel,edgeLoop=idx,ns=1)
            edge_loop_list.append(edge_loop)
            edge_list -= set(edge_loop) 
        res_list.append(len(edge_loop_list))

    if res_list[0] == res_list[1]:
        pm.headsUpMessage("Topology Same")
    else:
        pm.headsUpMessage("Topology not Same")

if __name__ == "__main__":
    checkTopology()