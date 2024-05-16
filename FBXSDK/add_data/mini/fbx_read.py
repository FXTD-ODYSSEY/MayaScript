# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-25 19:32:25"

import os
import pprint
import fbx
import FbxCommon


DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    fbx_path = r"D:\lumi\lumi_project\lumi_project_develop\Art\Assets\Actor\Daodao02\DaodaoFlat\Rigging\Live_Rig\Rig\Actor_Daodao02_DaodaoFlat_Mocap_Rig.fbx"
    manager, scene = FbxCommon.InitializeSdkObjects()
    assert FbxCommon.LoadScene(manager, scene, fbx_path)
    
    for i in range(scene.GetNodeCount()):
        node = scene.GetNode(i)
        if node.GetName() != "RightFoot":
            continue
        print(node)
        print(node.GetName())
        matrix = node.EvaluateGlobalTransform()
        pprint.pprint([list(vector) for vector in matrix])
    
    [   [0.9952108622130122, -0.0732065133593682, 0.06477766694623535, 0.0],
        [0.0667015006295785, 0.9930032334310129, 0.09744479570154559, 0.0],
        [-0.07145802647005506, -0.09265735155570912, 0.9931305884201163, 0.0],
        [37.059635162353516, 1.5427668822454166e-06, -2.599453182305922e-05, 1.0]
    ]
    
    

    [
        [-4.883195262044876e-16, -1.0000000000000002, -6.937297570820332e-16, 0.0],
        [0.09764988767612266, 6.808789643208971e-16, -0.9952208294830055, 0.0],
        [0.9952208294830049, -5.967448757360216e-16, 0.0976498876761227, 0.0],
        [-11.83171730372786, 5.979474131492758, -2.371368291147698, 1.0]
    ]
    
    [[-4.883195262044876e-16, -1.0000000000000002, -6.937297570820332e-16, 0.0],
    [0.09764988767612266, 6.808789643208971e-16, -0.9952208294830055, 0.0],
    [0.9952208294830049, -5.967448757360216e-16, 0.0976498876761227, 0.0],
    [-11.83171730372786, 5.979474131492758, -2.371368291147698, 1.0]]
    




if __name__ == "__main__":
    main()
