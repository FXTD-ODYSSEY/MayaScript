import pymel.core as pm

ctrl_match = {
    "head_ctrl": "head_ctrl",
    # "neck_B_M": "",
    "neck_C_M": "neck_B_M",
    "neck_D_M": "neck_C_M",
    "waist_FK2_ctrl": "waist_FK2_ctrl",
    "waist_FK1_ctrl": "waist_FK1_ctrl",
    "waist_Ctrl": "waist_Ctrl",


    "LfLeg_Leg_FK": "LfLeg_Leg_FK",
    "LfLeg_Knee_FK": "LfLeg_Knee_FK",
    "LfLeg_Ankle_FK": "LfLeg_Ankle_FK",
    "RtLeg_Leg_FK": "RtLeg_Leg_FK",
    "RtLeg_Knee_FK": "RtLeg_Knee_FK",
    "RtLeg_Ankle_FK": "RtLeg_Ankle_FK",


    "Rt_shoulder": "Rt_shoulder",
    "RtArm_UpArm_FK": "RtArm_UpArm_FK",
    "RtArm_Elbow_FK": "RtArm_Elbow_FK",
    "RtArm_Wrist_FK": "RtArm_Wrist_FK",
    "R_scapula_jnt_ctrl": "Rt_armor_Ctrl1",
    "Lf_shoulder": "Lf_shoulder",
    "LfArm_UpArm_FK": "LfArm_UpArm_FK",
    "LfArm_Elbow_FK": "LfArm_Elbow_FK",
    "LfArm_Wrist_FK": "LfArm_Wrist_FK",
    "L_scapula_jnt_ctrl": "Lf_armor_Ctrl1",

    "LfArm_Wrist_IK": "LfArm_Wrist_IK",
    "LfArm_Pole_ctrl": "LfArm_Pole_ctrl",
    "RtArm_Wrist_IK": "RtArm_Wrist_IK",
    "RtArm_Pole_ctrl": "RtArm_Pole_ctrl",

    "LfLeg_Leg_IK": "LfLeg_Leg_IK",
    "LfLeg_Pole_ctrl": "LfLeg_Pole_ctrl",
    "RtLeg_Leg_IK": "RtLeg_Leg_IK",
    "RtLeg_Pole_ctrl": "RtLeg_Pole_ctrl",

}

dst_namespace = "Male_rig_1__0003:"
src_namespace = "Darius_rig:"
for src,dst in ctrl_match.items():
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
