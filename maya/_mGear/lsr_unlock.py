# -*- coding: utf-8 -*-
"""
lsr joint unlock
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-09-29 15:39:50'

import pymel.core as pm

# for con in pm.ls(sl=1,dag=1,type="constraint"):
#     pm.delete(con)
def main():

    for jnt in pm.ls(sl=1,dag=1,type="joint"):
        for attr in 'trs':
            for axis in 'xyz':
                attribute = getattr(jnt, attr+axis)
                attribute.setLocked(False)
                attribute.setKeyable(True)


if __name__ == "__main__":
    main()
\