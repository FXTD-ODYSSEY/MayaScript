import pymel.core as pm
from maya import mel
edge_list = [sel for sel in pm.ls(sl=1,fl=1) if type(sel) is pm.general.MeshEdge]
pm.select(edge_list)
# # NOTE 切断 UV 
# pm.polyMapCut(edge_list)

# NOTE 转换到 UV
mel.eval("ConvertSelectionToUVs;selectType -ocm -alc false;selectType -ocm -polymeshUV true")
uv_list = pm.ls(sl=1,fl=1)

for pt in uv_list:
    u,v = pm.polyEditUV(pt,q=1,u=1)
    pm.polyEditUV(pt,v=-v)
