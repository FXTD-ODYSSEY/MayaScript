from maya import cmds
from collections import OrderedDict
match_dict = OrderedDict()
match_dict.update({"Root":"pelvis"})
match_dict.update({"Spine1":"spine_01"})
match_dict.update({"Chest":"spine_03"})
match_dict.update({"Scapula":"clavicle"})
match_dict.update({"Shoulder":"upperarm"})
match_dict.update({"Elbow":"lowerarm"})
match_dict.update({"Wrist":"hand"})
match_dict.update({"Hip":"thigh"})
match_dict.update({"Knee":"calf"})
match_dict.update({"Ankle":"foot"})
match_dict.update({"Toes":"ball"})
match_dict.update({"Neck":"neck_01"})
match_dict.update({"Head":"head"})

match_dict.update({"IndexFinger1":"index_01"})
match_dict.update({"IndexFinger2":"index_02"})
match_dict.update({"IndexFinger3":"index_03"})

match_dict.update({"MiddleFinger1":"middle_01"})
match_dict.update({"MiddleFinger2":"middle_02"})
match_dict.update({"MiddleFinger3":"middle_03"})

match_dict.update({"RingFinger1":"ring_01"})
match_dict.update({"RingFinger2":"ring_02"})
match_dict.update({"RingFinger3":"ring_03"})

match_dict.update({"PinkyFinger1":"pinky_01"})
match_dict.update({"PinkyFinger2":"pinky_02"})
match_dict.update({"PinkyFinger3":"pinky_03"})

match_dict.update({"ThumbFinger1":"thumb_01"})
match_dict.update({"ThumbFinger2":"thumb_02"})
match_dict.update({"ThumbFinger3":"thumb_03"})

for adv,ue in match_dict.items():
    l_ue = "%s_l" % ue
    l_adv = "%s_L" % adv
    if cmds.objExists(l_ue) and cmds.objExists(l_adv):
        r_ue = "%s_r" % ue
        r_adv = "%s_R" % adv
        con = cmds.pointConstraint(l_adv,l_ue)
        cmds.delete(con)
        con = cmds.pointConstraint(r_adv,r_ue)
        cmds.delete(con)
    else:
        m_adv = "%s_M" % adv
        m_ue = ue
        con = cmds.pointConstraint(m_adv,m_ue)
        cmds.delete(con)

