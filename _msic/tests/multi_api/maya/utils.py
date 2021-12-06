# -*- coding: utf-8 -*-
"""
Open Maya utilities.
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from itertools import product

from maya import cmds
from maya.api import OpenMaya


def is_in_scene(obj_name):
    """
    Check if an geometry or joint with obj_name exists in maya scene

    Args:
        obj_name (str):

    Returns:
        bool
    """
    return cmds.objExists(obj_name)


# -------------------------------------------------
# Maya display methods
# -------------------------------------------------
def display_error(info):
    OpenMaya.MGlobal.displayError(info)


def display_info(info):
    OpenMaya.MGlobal.displayInfo(info)


def log_message(pose_name, percent):
    print("{}%% {}".format(percent, pose_name))



# -------------------------------------------------
# Joint related methods
# -------------------------------------------------
def get_skincluster_from_mesh():
    """
    Get jnt list in bind with selected mesh

    Returns:
        mesh_name (str):
        jnt_list (list):
    """
    sel = cmds.ls(sl=1)
    if len(sel) > 0:
        try:
            shapes = cmds.listRelatives(sel[0], shapes=1)
            if shapes:
                mesh_name = sel[0]
                jnt_list = cmds.skinCluster(sel[0], inf=1, q=1)
                return mesh_name, jnt_list
        except:
            display_error("Not a Mesh Obj with SkinCluster!")
            return None, None
    else:
        return None, None


def get_jnt_transform_list(jnt_list):
    """
    Get a list of every joint under root_jnt, each item is a dict
    including jnt's name and its 9 transfrom value.

    Args:
        root_jnt (str): The Name of root joint
        type (int): 0 - info list. Defaults to be 0
                    1 - name list
    Returns:
        list: 
    """

    if not jnt_list:
        display_error("Selection is null list")
        return

    neutral_jnts = [
        {
            "name": val,
            "transform": [
                cmds.getAttr(val + ".translateX"),
                cmds.getAttr(val + ".translateY"),
                cmds.getAttr(val + ".translateZ"),
                cmds.getAttr(val + ".rotateX"),
                cmds.getAttr(val + ".rotateY"),
                cmds.getAttr(val + ".rotateZ"),
                cmds.getAttr(val + ".scaleX"),
                cmds.getAttr(val + ".scaleY"),
                cmds.getAttr(val + ".scaleZ"),
            ],
        }
        for i, val in enumerate(jnt_list)
    ]

    return neutral_jnts


def get_jnt_delta_tranform_list(jnt_list, neutral_info_list):
    """
    Get a list of delta transform with every joint's neutral position

    Args:
        jnt_list (list): The list of joint names
        neutral_info_list (list): The list of joint transform info
    
    Returns:
        list:
    """
    new_jnts = get_jnt_transform_list(jnt_list)

    for i in range(len(jnt_list)):
        neu_transform = neutral_info_list[i].get("transform")
        delta_transform = new_jnts[i].get("transform")
        for j in range(len(delta_transform)):
            delta_transform[j] = delta_transform[j] - neu_transform[j]

        new_jnts[i]["transform"] = delta_transform

    return new_jnts


def set_jnt_transform_sel(delta_list, neutral_list):
    """
    Set joints transform when selection pose

    Args:
        delta_list (list): list of joint delta transform in pose.skeletons
        neutral_list ([type]): list of neutral joint transfrom
    """
    for i, val in enumerate(neutral_list):
        neu_trans = val["transform"]
        dlt_trans = delta_list[i]["transform"]
        name = val["name"]

        for j, (axis, attr) in enumerate(product("trs", "xyz")):
            attr = "." + axis + attr
            cmds.setAttr(name + attr, neu_trans[j] + dlt_trans[j])


def get_mirror_joint_name(joint_name):
    if joint_name[-1:] == "L":
        return joint_name[:-1]+"R"
    if joint_name[-1:] == "R":
        return joint_name[:-1]+"L"
    if joint_name.find("_L_") != -1:
        return joint_name.replace("_L_", "_R_")
    if joint_name.find("_R_") != -1:
        return joint_name.replace("_R_", "_L_")
    return joint_name


