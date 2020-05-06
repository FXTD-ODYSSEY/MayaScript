# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-05 23:11:59'

"""
检查模型拓扑是否一致
选择两个模型所有环边 比对 环边数组是否一致判断拓扑结构是否一致 
"""
import time
import pymel.core as pm


def checkTopology(display=False,sleep=0.05):
    
    sel_list = [mesh for mesh in pm.ls(pm.pickWalk(d="down"),type="mesh")]

    if len(sel_list) != 2:
        pm.headsUpMessage("Please select 2 Mesh")
        pm.warning("Please select 2 Mesh")
        return 

    num_list = [(sel.numVertices(),sel.numEdges(),sel.numFaces()) for sel in sel_list]
    if num_list[0] != num_list[1]:
        return  False

    edge_num = num_list[0][1]

    res_list = []
    pm.progressWindow(	
        title="Check Topology",
        progress=0.0,
        isInterruptable=True )

    for i,sel in enumerate(sel_list):
        edge_loop_list = []
        edge_list = set(range(edge_num))
        pm.progressWindow( e=1, status = 'second mesh Analysis' if i else 'first mesh Analysis')
        while len(edge_list) > 1:
            idx = next(iter(edge_list), None)
            if pm.progressWindow( query=1, isCancelled=1 ) : 
                pm.progressWindow(ep=1)
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

    pm.progressWindow(ep=1)

    return  res_list[0] == res_list[1]

if __name__ == "__main__":
    curr = time.time()
    print (checkTopology(display=True))
    print ("elapsed time: %s" % (time.time() - curr))
