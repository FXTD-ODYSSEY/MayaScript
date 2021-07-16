
from maya import cmds
from maya import mel
from collections import OrderedDict
match_dict = OrderedDict()
adv_namespace = 'JinKe_rig:'
match_dict.update({"Root":"Hips"})
match_dict.update({"Spine1":"Spine"})
match_dict.update({"Chest":"Chest"})
match_dict.update({"Scapula":"Shoulder"})
match_dict.update({"Shoulder":"Arm"})
match_dict.update({"Elbow":"ForeArm"})
match_dict.update({"Wrist":"Hand"})
match_dict.update({"IndexFinger1":"Index1"})
match_dict.update({"IndexFinger2":"Index2"})
match_dict.update({"IndexFinger3":"Index3"})
match_dict.update({"IndexFinger4":"Index4"})
match_dict.update({"MiddleFinger1":"Middle1"})
match_dict.update({"MiddleFinger2":"Middle2"})
match_dict.update({"MiddleFinger3":"Middle3"})
match_dict.update({"MiddleFinger4":"Middle4"})
match_dict.update({"RingFinger1":"Ring1"})
match_dict.update({"RingFinger2":"Ring2"})
match_dict.update({"RingFinger3":"Ring3"})
match_dict.update({"RingFinger4":"Ring4"})
match_dict.update({"PinkyFinger1":"Pinky1"})
match_dict.update({"PinkyFinger2":"Pinky2"})
match_dict.update({"PinkyFinger3":"Pinky3"})
match_dict.update({"PinkyFinger4":"Pinky4"})
match_dict.update({"ThumbFinger1":"Thumb1"})
match_dict.update({"ThumbFinger2":"Thumb2"})
match_dict.update({"ThumbFinger3":"Thumb3"})
match_dict.update({"ThumbFinger4":"Thumb4"})
match_dict.update({"Neck":"Neck"})
match_dict.update({"Head":"Head"})
match_dict.update({"Hip":"UpLeg"})
match_dict.update({"Knee":"Leg"})
match_dict.update({"Ankle":"Foot"})

for adv,ue in match_dict.items():
    l_ue = "Left%s" % ue
    l_adv = adv_namespace + "%s_L" % adv
    m_adv = adv_namespace + "%s_M" % adv
    if cmds.objExists(l_ue) and cmds.objExists(l_adv):
        r_ue = "Right%s" % ue
        r_adv = adv_namespace + "%s_R" % adv
        con = cmds.parentConstraint(l_adv,l_ue)
        cmds.setKeyframe(l_ue)
        cmds.delete(con)
        con = cmds.parentConstraint(r_adv,r_ue)
        cmds.setKeyframe(r_ue)
        cmds.delete(con)
    elif cmds.objExists(m_adv):
        m_ue = ue
        con = cmds.parentConstraint(m_adv,m_ue)
        cmds.setKeyframe(m_ue)
        cmds.delete(con)


