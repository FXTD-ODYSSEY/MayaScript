# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-10-20 20:59:04'

import pymel.core as pm

def main():
    # pm.deleteUI("ToolBox|MainToolboxLayout|sun_icon")
    # pm.deleteUI("ToolBox|MainToolboxLayout|frameLayout5|flowLayout2|sun_icon")
    # return
    pm.setParent(pm.melGlobals["gToolBox"])
    size = 36
    icon = pm.iconTextButton("sun_icon",image1="ambientLight.open.svg",w=size,h=size,command=lambda:print("ambientLight"))
    print(icon)
    # iconTextButton
	# 	-image1 "mayaIcon.png" -width $iconSize -height $iconSizeHeight
	# 	-command ("showHelp -absolute \"" + $MayaNewsURL + "\"") mayaWebButton

if __name__ == '__main__':
    main()
