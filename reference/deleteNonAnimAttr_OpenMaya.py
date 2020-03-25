# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-23 16:03:44'

"""
reference 清理脚本
"""

from maya import cmds
from maya import OpenMaya


# NOTE 取消所有的引用
for ref in cmds.ls(references=1):
    ref_path = cmds.referenceQuery( ref,filename=1,unresolvedName=1 )
    ref_node = cmds.file(ref_path,q=1,rfn=1)
    cmds.file(ref_path,unloadReference=ref_node)


ref_itr = OpenMaya.MItDependencyNodes(OpenMaya.MFn.kReference)
reload_path = []
edit_list = []


# NOTE 读取需要跑的信息
while not ref_itr.isDone():
    ref = ref_itr.thisNode()
    
    try:
        ref_node = OpenMaya.MFnReference(ref)
        ref_path = ref_node.fileName(1,0,0)
        reload_path.append(ref_path)
        del ref_node
    except:
        ref_itr.next()
        continue

    edit_itr = OpenMaya.MItEdits(ref)
    total = 0
    while not edit_itr.isDone():
        total += 1
        edit_itr.next()
    
    edit_list.append((edit_itr,total))

    ref_itr.next()

cmds.progressWindow(	
        title='remove unreleated edits in reference' ,
        progress=0.0,
        isInterruptable=True )

try:
    for ref_path,[edit_itr,total] in zip(reload_path,edit_list):
        cmds.progressWindow( e=True, status=ref_path )
        i = 0
        edit_itr.reset()
        while not edit_itr.isDone():
            i += 1 
            if cmds.progressWindow( query=True, isCancelled=True ) :
                cmds.progressWindow(endProgress=1)
                break
            amount = float(i)/total*100
            cmds.progressWindow( e=True, progress=amount )
                
            edit_type = edit_itr.currentEditType()
            # if edit_type != OpenMaya.MEdit.kSetAttrEdit and edit_type != OpenMaya.MEdit.kConnectDisconnectEdit :
            if edit_type != OpenMaya.MEdit.kSetAttrEdit :
                edit_itr.next()
                continue
            
            # edit_string = edit_itr.currentEditString()
            if edit_type == OpenMaya.MEdit.kSetAttrEdit:
                setAttrEdit = edit_itr.setAttrEdit()
                attr = setAttrEdit.plugName()
            elif edit_type == OpenMaya.MEdit.kConnectDisconnectEdit:
                setAttrEdit = edit_itr.connectDisconnectEdit()
                attr = setAttrEdit.srcPlugName()


            dagPath = attr.split('.')[0]
            # NOTE 过滤动画曲线
            if not cmds.objExists(dagPath):
                # NOTE 过滤绑定文件
                if "rig" not in dagPath:
                    # print dagPath,edit_itr.currentEditString()
                    try:
                        edit_itr.removeCurrentEdit()
                    except :
                        print "currentEditString",edit_itr.currentEditString()
            else:
                objectType = cmds.objectType(dagPath)
                if objectType != 'transform' and 'animCurve' not in objectType:
                    try:
                        edit_itr.removeCurrentEdit()
                    except:
                        print "currentEditString",edit_itr.currentEditString()

            edit_itr.next()

except:
    import  traceback
    traceback.print_exc()

cmds.progressWindow(ep=1)

# NOTE reload reference
for ref_path in reload_path:
    ref_node = cmds.file(ref_path,q=1,rfn=1)
    cmds.file(ref_path,loadReferenceDepth="asPrefs",loadReference=ref_node)

    