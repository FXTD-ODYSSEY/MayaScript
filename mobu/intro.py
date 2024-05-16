# -*- coding: utf-8 -*-
"""
https://help.autodesk.com/view/MOBPRO/2018/ENU/?guid=__files_GUID_AB029633_946C_4CCB_879C_C533FDE236AB_htm#SECTION_3570B32D78E5450C80327305959CEABA

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-17 11:20:21"


# from pyfbsdk import *
import pyfbsdk as mobu
import os


app = mobu.FBApplication()
app.FileNew()

# Get a reference to the underlying system properties of MotionBuilder.
system = mobu.FBSystem()

# Get a reference to the current MotionBuilder scene.
scene = system.Scene


def get_mobu_path():
    r"""
    Get the MotionBuilder installation directory.

    Note: FBSystem().ApplicationPath returns a string similar to:
        'C:\Program Files\Autodesk\MotionBuilder <year>\bin\x64'.
        We only want to return the substring:
        'C:\Program Files\Autodesk\MotionBuilder <year>\
    """
    application_path = mobu.FBSystem().ApplicationPath
    return os.path.dirname(os.path.dirname(application_path))


# Use the sample PlasticMan.fbx file in the default installation directory.
sdk_path = os.path.join(get_mobu_path(), "OpenRealitySDK")
fbx_path = os.path.join(sdk_path, "scenes", "PlasticMan.fbx")
app.FileOpen(fbx_path, False)

hipEffector = mobu.FBFindModelByLabelName("Plasticman_Ctrl:HipsEffector")

print(hipEffector)


# Create a mouse device and append it to the scene.
mouseDevice = mobu.FBCreateObject("Browsing/Templates/Devices", "Mouse", "MyMouse")
mouseDevice.OnLine = True
mouseDevice.Live = True
scene.Devices.append(mouseDevice)

# Create a constraint relation.
constraintRelation = mobu.FBConstraintRelation("DanceConstraint")
constraintRelation.Active = True

print(constraintRelation)
