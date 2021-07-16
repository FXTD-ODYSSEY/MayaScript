from maya import cmds

# NOTE 取消所有 reference 的加载
for ref in cmds.ls(references=1):
    # NOTE 文件没有路径名称
    try:
        ref_path = cmds.referenceQuery( ref,filename=1,unresolvedName=1 )
    except RuntimeError:
        continue
    referenceUnloaded = cmds.file(ref_path,q=1,dr=1)
    if not referenceUnloaded:
        ref_node = cmds.file(ref_path,q=1,rfn=1)
        cmds.file(ref_path,unloadReference=ref_node)


# NOTE C:\Program Files\Autodesk\Maya2017\scripts\others\referenceEditsWindow.mel
remove_dict = {
    "addAttr":lambda buffer: "%s.%s" % (buffer[-1],buffer[2]),
    "deleteAttr":lambda buffer: buffer[1],
    "setAttr":lambda buffer: buffer[1],
    "relationship":lambda buffer: buffer[2],
    "parent":lambda buffer: buffer[-1] if buffer[-2] == "-w" else buffer[-2],
}

cmds.progressWindow(	
        title='remove unreleated edits in reference' ,
        progress=0.0,
        isInterruptable=True )

for ref in cmds.ls(references=1):
    
    # NOTE 获取引用文件的名称
    try:
        file_name = cmds.referenceQuery( ref,filename=1,unresolvedName=1 )
    except:
        continue

    # NOTE 查询文件是否加载进场景中
    referenceUnloaded = cmds.file(file_name,q=1,dr=1)

    cmds.progressWindow( e=1, status='%s' % ref)
    edit_list = cmds.referenceQuery( ref,editStrings=True,showDagPath=1 )
    count = len(edit_list)
    # NOTE 获取当前引用节点的编辑信息
    for i,edit in enumerate(edit_list):

        if cmds.progressWindow( query=True, isCancelled=True ) :
            cmds.progressWindow(endProgress=1)
            break
        amount = float(i)/count*100
        cmds.progressWindow( e=1, progress=amount)
        

        buffer = edit.split()
        command,attr = buffer[:2]

        if command != "setAttr":
            continue
        attr = buffer[1]
        if '[' in attr:
            print attr
            cmds.referenceEdit( attr, editCommand=command, failedEdits = True, successfulEdits = True, removeEdits = True )
    
    if i > 2:
        break

cmds.progressWindow( ep=1)