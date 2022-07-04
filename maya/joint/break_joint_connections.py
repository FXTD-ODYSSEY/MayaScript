import pymel.core as pm
import itertools

node_list = set()
for sel in pm.ls(sl=1,dag=1,type="joint"):
    for axis,attr in itertools.product('trs','xyz'):
        attribute = getattr(sel,axis+attr)
        attribute.setKeyable(True)
        node = attribute.listConnections()
        node_list.update(set(node))

pm.delete(node_list)
