# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-23 16:03:44'

"""
reference 清理脚本
"""
import re
from maya import cmds
from maya import OpenMaya


# # NOTE 取消所有的引用
# for ref in cmds.ls(references=1):
#     # NOTE 文件没有路径名称
#     try:
#         ref_path = cmds.referenceQuery( ref,filename=1,unresolvedName=1 )
#     except RuntimeError:
#         continue
#     referenceUnloaded = cmds.file(ref_path,q=1,dr=1)
#     if not referenceUnloaded:
#         ref_node = cmds.file(ref_path,q=1,rfn=1)
#         cmds.file(ref_path,unloadReference=ref_node)


ref_itr = OpenMaya.MItDependencyNodes(OpenMaya.MFn.kReference)
reload_path = []
edit_list = []


# NOTE 读取需要跑的数量信息
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
        
    for j,(ref_path,(edit_itr,total)) in enumerate(zip(reload_path,edit_list)):
    
        cmds.progressWindow( e=True, status=ref_path )
        i = 0
        edit_itr.reset()
        while not edit_itr.isDone():
            i += 1 
            if cmds.progressWindow( query=True, isCancelled=True ) :
                break
            amount = float(i)/total*100
            cmds.progressWindow( e=True, progress=amount )
                
            edit_type = edit_itr.currentEditType()
            edit_string = edit_itr.currentEditString()
            if edit_type == OpenMaya.MEdit.kSetAttrEdit:
                EDIT = edit_itr.setAttrEdit()
                attr = EDIT.plugName()
                # NOTE [] 通常都是非动画操作才有的
                if '[' in edit_string:
                    edit_itr.removeCurrentEdit()
                elif re.search(r'Shape\d*.',edit_string):
                    edit_itr.removeCurrentEdit()
            elif edit_type == OpenMaya.MEdit.kConnectDisconnectEdit:
                EDIT = edit_itr.connectDisconnectEdit()
                attr = [EDIT.srcPlugName(),EDIT.dstPlugName()]
                buffer = edit_string.split()[0]
                if '[' in edit_string:
                    edit_itr.removeCurrentEdit()
                elif re.search(r'Shape\d*.',edit_string):
                    edit_itr.removeCurrentEdit()

            edit_itr.next()

except:
    import traceback
    traceback.print_exc()
# cmds.progressWindow( e=True, progress=0.0,status='clean setAttr Edit' )
# total = len(attr_dict)
# for i,(attr,editCommand) in enumerate(attr_dict.items()):
#     if cmds.progressWindow( query=True, isCancelled=True ) :
#         break
#     amount = float(i)/total*100
#     cmds.progressWindow( e=True, progress=amount )
#     cmds.referenceEdit( attr, editCommand=editCommand, failedEdits = 1, successfulEdits = 1, removeEdits = 1 )

# for editCommand,data in connectAttr_dict.items():
#     cmds.progressWindow( e=True, progress=0.0,status='clean %s Edit' % editCommand )
#     total = len(data)
#     for i,(src,dst) in enumerate(data):
#         if cmds.progressWindow( query=True, isCancelled=True ) :
#             break
#         amount = float(i)/total*100
#         cmds.progressWindow( e=True, progress=amount )
#         cmds.referenceEdit( src,dst, editCommand=editCommand, failedEdits = 1, successfulEdits = 1, removeEdits = 1 )


cmds.progressWindow(ep=1)

# # NOTE reload reference
# for ref_path in reload_path:
#     ref_node = cmds.file(ref_path,q=1,rfn=1)
#     cmds.file(ref_path,loadReferenceDepth="asPrefs",loadReference=ref_node)
