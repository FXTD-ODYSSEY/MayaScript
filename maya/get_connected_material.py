# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-11 15:37:23'


import pymel.core as pm
import json
material_map = {}
for mesh in pm.ls(sl=1,dag=1,ni=1,v=1,type="mesh"):
    mat_list = [mat for sg in pm.mel.getConnectedShaders(mesh,0) for mat in pm.PyNode(sg).listConnections(type="shadingDependNode")]
    material_map[str(mesh)] =str(mat_list[0])
    
print(json.dumps(material_map,indent=4))

material_map = {
    "eye_crystalRShape": "Mat_Pupil", 
    "eyefresh_fadeLShape": "Mat_EyeFreshFade", 
    "eye_crystalLShape": "Mat_Pupil", 
    "tongue_lowresShape": "Mat_Tongue", 
    "teethdown1Shape": "Mat_Teeth", 
    "eyeballRShape": "Mat_Cornea", 
    "irisRShape": "Mat_Iris", 
    "eyetransitionLShape": "Mat_Tearline", 
    # "ladyori_head_meshShape": "Mat_Head", 
    "eyeballLShape": "Mat_Cornea", 
    "eyefresh_fadeRShape": "Mat_EyeFreshFade", 
    "irisLShape": "Mat_Iris", 
    "eyefreshShape": "Mat_Head", 
    "eyeball_shadowLShape": "Mat_Eyeshadow", 
    "teethUP1Shape": "Mat_Teeth", 
    "eyetransitionRShape": "Mat_Tearline"
}

for mesh,material in material_map.items():
    sg = pm.mel.getConnectedShaders(mesh,0)[0]
    sg = pm.PyNode(sg)
    material = pm.PyNode(material)
    material.outColor.connect(sg.surfaceShader,f=1)