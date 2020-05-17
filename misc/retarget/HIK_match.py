import pymel.core as pm
from maya import mel
 

# NOTE 导入 reference
pm.createReference(r"X:\Characters\Fight\jnt.mb",r=1,namespace="jnt")
pm.createReference(r"X:\Characters\Fight\Rig\Darius_rig.mb",r=1,namespace="new")

org_namespace = "Darius_rig:"
src_namespace = "jnt:"
dst_namespace = "new:"

# NOTE 改为 FK 模式
switch_list = ["LfArm_Switch",
"RtArm_Switch",
"LfLeg_Switch",
"RtLeg_Switch",]

for switch in switch_list:
    switch = pm.PyNode(dst_namespace + switch)
    switch.IKFK.set(0)


# NOTE FBX 骨骼 匹配原来骨骼的位置
for fbx_jnt in pm.ls(src_namespace+"root",dag=1,ni=1):
    fbx_base = fbx_jnt.split(':')[1]
    skin_jnt = dst_namespace + ':' + fbx_base
    if pm.objExists(skin_jnt):
        # change jointOrientX and key it
        for tmp in 'XYZ':
            pm.setKeyframe('%s.jointOrient%s'%(fbx_jnt,tmp))
            or_value = pm.getAttr('%s.jointOrient%s'%(skin_jnt,tmp))
            pm.setAttr('%s.jointOrient%s'%(fbx_jnt,tmp),or_value)
        for trs in 'trs':
            for xyz in 'xyz':
                attr = trs + xyz
                try:
                    v = pm.getAttr(skin_jnt + '.' + attr)
                    fbx_anim_node = pm.findKeyframe(fbx_jnt, curve=True, at=attr)
                    if not fbx_anim_node:
                        #key
                        pm.setKeyframe('%s.%s'%(fbx_jnt,attr))

                    # key it first
                    #pm.setKeyframe('pCube1.scaleX')
                    pm.setAttr(fbx_jnt + '.' + attr, v)
                except BaseException:
                    print("error",skin_jnt)
                    pass

# keyframe_match = {
#     "LfArm_Switch" : "LfArm_Switch",
#     "RtArm_Switch" : "RtArm_Switch",
#     "LfLeg_Switch" : "LfLeg_Switch",
#     "RtLeg_Switch" : "RtLeg_Switch",
# }

# start = pm.playbackOptions(q=1,min=1)
# end = pm.playbackOptions(q=1,max=1)

# for src,dst in keyframe_match.items():
#     dst = dst_namespace + dst
#     src = org_namespace + src
#     src = pm.PyNode(src)
#     dst = pm.PyNode(dst)
#     pm.copyKey( src,time=(start,end) )
#     pm.pasteKey(dst)

jnt_ctrl_match = {
    "Lf_shoulder" : "Lf_clavicle1_jnt_skin"  ,
    "LfArm_UpArm_FK" : "Lf_Arm1_jnt_skin" ,
    "LfArm_Elbow_FK" : "Lf_Arm6_jnt_skin" ,
    "LfArm_Wrist_FK" : "Lf_Arm9_jnt_skin" ,
    "Rt_shoulder" : "Rt_clavicle1_jnt_skin" ,
    "RtArm_UpArm_FK" : "Rt_Arm1_jnt_skin" ,
    "RtArm_Elbow_FK" : "Rt_Arm6_jnt_skin" ,
    "RtArm_Wrist_FK" : "Rt_Arm9_jnt_skin" ,

    "LfLeg_Leg_FK" : "Lf_Leg1_jnt_skin"  ,
    "LfLeg_Knee_FK" : "Lf_Leg6_jnt_skin"  ,
    "LfLeg_Ankle_FK" : "Lf_Leg9_jnt_skin"  ,
    "LfLegLeg_ball_FK" : "Lf_foot_drv_skin"  ,
    "RtLeg_Leg_FK" : "Rt_Leg1_jnt_skin"  ,
    "RtLeg_Knee_FK" : "Rt_Leg6_jnt_skin"  ,
    "RtLeg_Ankle_FK" : "Rt_Leg9_jnt_skin"  ,
    "RtLegLeg_ball_FK" : "Rt_foot_drv_skin"  ,

    "Lf_hip_ctrl" : "Lf_Leg1_jnt_skin" ,
    "Rt_hip_ctrl" : "Rt_Leg1_jnt_skin" ,

    "waist_Ctrl" : "spline1_jnt_skin" ,
    "root_waist_ikCtrl" : "spline1_jnt_skin" ,
    "waist_FK1_ctrl" : "spline3_jnt_skin" ,
    "waist_FK2_ctrl" : "spline5_jnt_skin" ,
    "neck_C_M" : "neck1_jnt1_skin" ,
    "head_ctrl" : "head_jnt_skin" ,
    "neck_B_M" : "neck1_jnt2_skin" ,

    "Lf_thumb1" : "Lf_thumb1_jnt_skin" ,
    "Lf_thumb2" : "Lf_thumb2_jnt_skin" ,
    "Lf_thumb3" : "Lf_thumb3_jnt_skin" ,
    "Lf_index1" : "Lf_index1_jnt_skin" ,
    "Lf_index2" : "Lf_index2_jnt_skin" ,
    "Lf_index3" : "Lf_index3_jnt_skin" ,
    "Lf_mid1" : "Lf_mid1_jnt_skin" ,
    "Lf_mid2" : "Lf_mid2_jnt_skin" ,
    "Lf_mid3" : "Lf_mid3_jnt_skin" ,
    "Lf_ring1" : "Lf_ring1_jnt_skin" ,
    "Lf_ring2" : "Lf_ring2_jnt_skin" ,
    "Lf_ring3" : "Lf_ring3_jnt_skin" ,
    "Lf_pinky1" : "Lf_pinky1_jnt_skin" ,
    "Lf_pinky2" : "Lf_pinky2_jnt_skin" ,
    "Lf_pinky3" : "Lf_pinky3_jnt_skin" ,

    "Rt_thumb1" : "Rt_thumb1_jnt_skin" ,
    "Rt_thumb2" : "Rt_thumb2_jnt_skin" ,
    "Rt_thumb3" : "Rt_thumb3_jnt_skin" ,
    "Rt_index1" : "Rt_index1_jnt_skin" ,
    "Rt_index2" : "Rt_index2_jnt_skin" ,
    "Rt_index3" : "Rt_index3_jnt_skin" ,
    "Rt_mid1" : "Rt_mid1_jnt_skin" ,
    "Rt_mid2" : "Rt_mid2_jnt_skin" ,
    "Rt_mid3" : "Rt_mid3_jnt_skin" ,
    "Rt_ring1" : "Rt_ring1_jnt_skin" ,
    "Rt_ring2" : "Rt_ring2_jnt_skin" ,
    "Rt_ring3" : "Rt_ring3_jnt_skin" ,
    "Rt_pinky1" : "Rt_pinky1_jnt_skin" ,
    "Rt_pinky2" : "Rt_pinky2_jnt_skin" ,
    "Rt_pinky3" : "Rt_pinky3_jnt_skin" ,
}


dst_namespace = "Darius_rig:"

for dst,src in jnt_ctrl_match.items():
    dst = dst_namespace + dst
    # src = src_namespace + src
    src = pm.PyNode(src)
    dst = pm.PyNode(dst)

    # print "%s --> %s" % (src,dst)

    t_list,r_list = [[axis for axis in 'xyz' if getattr(dst,attr + axis).isLocked()] for attr in "tr"]

    pm.parentConstraint(src,dst,skipTranslate=t_list,skipRotate=r_list,mo=1)

    # parent_fbx_grp = pm.group(em=1)
    # parent_grp = pm.group()
    # pm.delete(pm.parentConstraint(src,parent_grp))
    # pm.parentConstraint(parent_fbx_grp,dst,skipTranslate=t_list,skipRotate=r_list,mo=1)
    # parent_grp.setParent(src)

# NOTE 约束武器
wp = "wp_jnt_ctrl"
org_wp = org_namespace + wp
dst_wp = dst_namespace + wp
pm.parentConstraint(org_wp,dst_wp,mo=0)

# NOTE HIK 匹配
for i,item in enumerate(pm.optionMenuGrp("hikCharacterList",q=1,itemListLong=1),1):
    label = pm.menuItem(item,q=1,label=1).strip()
    if label.startswith("jnt:"):
        pm.optionMenuGrp("hikCharacterList",e=1,select=i)
        break

mel.eval("hikUpdateCurrentCharacterFromUI(); hikUpdateContextualUI()")

for i,item in enumerate(pm.optionMenuGrp("hikSourceList",q=1,itemListLong=1),1):
    label = pm.menuItem(item,q=1,label=1).strip()
    if label.startswith("Darius_rig:"):
        pm.optionMenuGrp("hikSourceList",e=1,select=i)
        break
    
mel.eval("hikUpdateCurrentSourceFromUI(); hikUpdateContextualUI();")



# import pymel.core as pm
# pm.select([ dst_namespace+ctrl for ctrl in jnt_ctrl_match.values()])


# cmds.select("Darius_rig:bodySet")
# cmds.select("Darius_rig:wp_jnt_ctrl",add=1)

# time_list = cmds.keyframe("root",q=1,timeChange=1)
# timeStart = min(time_list)
# timeEnd = max(time_list)
# print timeStart,timeEnd
# cmds.bakeResults(
#     # wind_loc,
#     simulation = 1,
#     t = (timeStart,timeEnd),
#     oversamplingRate = 1, 
#     disableImplicitControl = 1, 
#     preserveOutsideKeys = 1, 
#     at = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
# )

# cmds.delete("root")