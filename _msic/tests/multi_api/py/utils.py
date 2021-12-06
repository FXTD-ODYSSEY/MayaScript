# -*- coding: utf-8 -*-
"""
Open Maya utilities.
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from itertools import product


def is_in_scene(obj_name):
    """
    Check if an geometry or joint with obj_name exists in maya scene

    Args:
        obj_name (str):

    Returns:
        bool
    """
    pass


# -------------------------------------------------
# Maya display methods
# -------------------------------------------------
def display_error(info):
    pass


def display_info(info):
    pass


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
    pass


def get_jnt_transform_list(jnt_list):
    pass


def get_jnt_delta_tranform_list(jnt_list, neutral_info_list):
    """
    Get a list of delta transform with every joint's neutral position

    Args:
        jnt_list (list): The list of joint names
        neutral_info_list (list): The list of joint transform info
    
    Returns:
        list:
    """
    pass


def set_jnt_transform_sel(delta_list, neutral_list):
    """
    Set joints transform when selection pose

    Args:
        delta_list (list): list of joint delta transform in pose.skeletons
        neutral_list ([type]): list of neutral joint transfrom
    """
    pass


def get_mirror_joint_name(joint_name):
    pass


