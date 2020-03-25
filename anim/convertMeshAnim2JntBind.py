from maya import cmds

# NOTE https://stackoverflow.com/questions/45764093/

def hierarchyTree(parent, tree):
    children = cmds.listRelatives(parent, c=True, type='transform')
    if children:
        tree[parent] = (children, {})
        for child in children:
            hierarchyTree(child, tree[parent][1])
    else:
        del tree

def retrive2Jnt(tree,jnt_list=[]):
    for parent, data in tree.items():
        cmds.select(cl=1)
        parent_jnt = cmds.joint(n="%s_jnt" % parent)
        cmds.parentConstraint(parent,parent_jnt)
        children, child_tree = data

        jnt_list.append((parent_jnt,parent))
        for child in children:
            if not cmds.keyframe(child, q=True):
                continue
            cmds.select(cl=1)
            child_jnt = cmds.joint(n="%s_jnt" % child)
            jnt_list.append((child_jnt,child))
            cmds.parent(child_jnt,parent_jnt)
            cmds.parentConstraint(child,child_jnt)
        retrive2Jnt(child_tree,jnt_list)

def retriveSkin(jnt_tree):
    for parent, data in jnt_tree.items():
        
        retrive2Jnt


hierarchy_tree = {}
hierarchyTree('DS_01_Deck_a:DS_01_Deck',hierarchy_tree)

if hierarchy_tree:
    jnt_obj_list = []
    retrive2Jnt(hierarchy_tree,jnt_obj_list)

    # NOTE bake 关键帧
    start_time = cmds.playbackOptions(q=1,min=1)
    end_time = cmds.playbackOptions(q=1,max=1)
    jnt_list = [jnt for jnt,obj in jnt_obj_list]

    cmds.bakeResults(jnt_list,
        simulation=False, 
        t=(start_time,end_time)
    )

    # NOTE 删除约束
    con_list = cmds.ls(jnt_list[0],dag=1,ni=1,type="constraint")
    cmds.delete(con_list)
    
    # NOTE 绑定骨骼
    for jnt,obj in jnt_obj_list:
        try:
            cmds.skinCluster( jnt, obj, 
                dr=4,
                bindMethod=0,
                toSelectedBones=1,
            )   
        except:
            pass


    # bakeResults -simulation true -t "61:92" -sampleBy 1 -oversamplingRate 1 -disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -removeBakedAnimFromLayer false -bakeOnOverrideLayer false -minimizeRotation true -controlPoints false -shape true {"DS_01_Deck_a:DS_01_Deck_jnt"};


