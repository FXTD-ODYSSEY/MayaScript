import pymel.core as pm
from maya import mel
 

# NOTE 导入 reference
pm.createReference(r"C:\Users\timmyliang\Desktop\test\jnt.mb",r=1,namespace="jnt")
pm.createReference(r"C:\Users\timmyliang\Desktop\test\Male_rig_poss.mb",r=1,namespace="new")

org_namespace = "Darius_rig:"
src_namespace = "jnt:"
dst_namespace = "new:"

# NOTE 改为 FK 模式
# switch_list = ["LfArm_Switch",
# "RtArm_Switch",
# "LfLeg_Switch",
# "RtLeg_Switch",]

# for switch in switch_list:
#     switch = pm.PyNode(dst_namespace + switch)
#     switch.IKFK.set(0)

keyframe_match = {
    "LfArm_Switch" : "LfArm_Switch",
    "RtArm_Switch" : "RtArm_Switch",
    "LfLeg_Switch" : "LfLeg_Switch",
    "RtLeg_Switch" : "RtLeg_Switch",
}

start = pm.playbackOptions(q=1,min=1)
end = pm.playbackOptions(q=1,max=1)

for src,dst in keyframe_match.items():
    dst = dst_namespace + dst
    src = src_namespace + src
    src = pm.PyNode(src)
    dst = pm.PyNode(dst)
    pm.copyKey( src,time=(start,end) )
    pm.pasteKey(dst)



jnt_ctrl_match = {
    "Lf_clavicle1_jnt_skin" : "Lf_shoulder" ,
    "Lf_Arm1_jnt_skin" : "LfArm_UpArm_FK",
    "Lf_Arm6_jnt_skin" : "LfArm_Elbow_FK",
    "Lf_Arm9_jnt_skin" : "LfArm_Wrist_FK",
    "Rt_clavicle1_jnt_skin" : "Rt_shoulder",
    "Rt_Arm1_jnt_skin" : "RtArm_UpArm_FK",
    "Rt_Arm6_jnt_skin" : "RtArm_Elbow_FK",
    "Rt_Arm9_jnt_skin" : "RtArm_Wrist_FK",

    "Lf_Leg1_jnt_skin" : "LfLeg_Leg_FK" ,
    "Lf_Leg6_jnt_skin" : "LfLeg_Knee_FK" ,
    "Lf_Leg9_jnt_skin" : "LfLeg_Ankle_FK" ,
    "Lf_foot_drv_skin" : "LfLegLeg_ball_FK" ,
    "Rt_Leg1_jnt_skin" : "RtLeg_Leg_FK" ,
    "Rt_Leg6_jnt_skin" : "RtLeg_Knee_FK" ,
    "Rt_Leg9_jnt_skin" : "RtLeg_Ankle_FK" ,
    "Rt_foot_drv_skin" : "RtLegLeg_ball_FK" ,

    "Lf_Leg1_jnt_skin" : "Lf_hip_ctrl",
    "Rt_Leg1_jnt_skin" : "Rt_hip_ctrl",

    "spline1_jnt_skin" : "waist_Ctrl",
    "spline1_jnt_skin" : "root_waist_ikCtrl",
    "spline3_jnt_skin" : "waist_FK1_ctrl",
    "spline5_jnt_skin" : "waist_FK2_ctrl",
    "neck1_jnt1_skin" : "neck_C_M",
    "head_jnt_skin" : "head_ctrl",
    "neck1_jnt2_skin" : "neck_B_M",

    "Lf_thumb1_jnt_skin" : "Lf_thumb1",
    "Lf_thumb2_jnt_skin" : "Lf_thumb2",
    "Lf_thumb3_jnt_skin" : "Lf_thumb3",
    "Lf_index1_jnt_skin" : "Lf_index1",
    "Lf_index2_jnt_skin" : "Lf_index2",
    "Lf_index3_jnt_skin" : "Lf_index3",
    "Lf_mid1_jnt_skin" : "Lf_mid1",
    "Lf_mid2_jnt_skin" : "Lf_mid2",
    "Lf_mid3_jnt_skin" : "Lf_mid3",
    "Lf_ring1_jnt_skin" : "Lf_ring1",
    "Lf_ring2_jnt_skin" : "Lf_ring2",
    "Lf_ring3_jnt_skin" : "Lf_ring3",
    "Lf_pinky1_jnt_skin" : "Lf_pinky1",
    "Lf_pinky2_jnt_skin" : "Lf_pinky2",
    "Lf_pinky3_jnt_skin" : "Lf_pinky3",

    "Rt_thumb1_jnt_skin" : "Rt_thumb1",
    "Rt_thumb2_jnt_skin" : "Rt_thumb2",
    "Rt_thumb3_jnt_skin" : "Rt_thumb3",
    "Rt_index1_jnt_skin" : "Rt_index1",
    "Rt_index2_jnt_skin" : "Rt_index2",
    "Rt_index3_jnt_skin" : "Rt_index3",
    "Rt_mid1_jnt_skin" : "Rt_mid1",
    "Rt_mid2_jnt_skin" : "Rt_mid2",
    "Rt_mid3_jnt_skin" : "Rt_mid3",
    "Rt_ring1_jnt_skin" : "Rt_ring1",
    "Rt_ring2_jnt_skin" : "Rt_ring2",
    "Rt_ring3_jnt_skin" : "Rt_ring3",
    "Rt_pinky1_jnt_skin" : "Rt_pinky1",
    "Rt_pinky2_jnt_skin" : "Rt_pinky2",
    "Rt_pinky3_jnt_skin" : "Rt_pinky3",
}



for src,dst in jnt_ctrl_match.items():
    dst = dst_namespace + dst
    src = src_namespace + src
    src = pm.PyNode(src)
    dst = pm.PyNode(dst)
    t_list = []
    tx = dst.tx.isConnected() or dst.tx.isLocked()
    ty = dst.ty.isConnected() or dst.ty.isLocked()
    tz = dst.tz.isConnected() or dst.tz.isLocked()
    if tx:
        t_list.append('x')  
    if ty:
        t_list.append('y')  
    if tz:
        t_list.append('z')  
    if not t_list:
        t_list = "none"

    r_list = []
    rx = dst.rx.isConnected() or dst.rx.isLocked()
    ry = dst.ry.isConnected() or dst.ry.isLocked()
    rz = dst.rz.isConnected() or dst.rz.isLocked()
    if rx:
        r_list.append('x')  
    if ry:
        r_list.append('y')  
    if rz:
        r_list.append('z')  
    if not r_list:
        r_list = "none"
    pm.parentConstraint(src,dst,skipTranslate=t_list,skipRotate=r_list,mo=1)

# NOTE 约束武器
wp = "wp_jnt_ctrl"
org_wp = org_namespace + wp
dst_wp = dst_namespace + wp
pm.parentConstraint(org_wp,dst_wp,mo=0)

# NOTE HIK 

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
    
mel.eval("hikUpdateCurrentCharacterFromUI(); hikUpdateContextualUI()")



import pymel.core as pm
pm.select([ dst_namespace+ctrl for ctrl in jnt_ctrl_match.values()])