# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-25 15:45:54'

import os
from pymel import core as pm


capture_path = os.path.dirname(pm.sceneName())

for p in os.listdir(capture_path):
    path = os.path.join(capture_path,p)
    if not path.endswith("ma"):
        continue
    pm.openFile(path,f=1)

    png = "%s.png" % os.path.splitext(pm.sceneName())[0]

    pm.playblast(completeFilename=png,
                format="image",
                sequenceTime=0,
                frame=[1],
                clearCache=1,
                viewer=0,
                showOrnaments=0,
                percent=100,
                compression="png",
                quality=100,
                forceOverwrite=1,
                )
