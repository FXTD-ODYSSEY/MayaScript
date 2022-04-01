# -*- coding: utf-8 -*-
"""
多进程克隆仓库
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-25 11:03:15'



# Import built-in modules
from multiprocessing.dummy import Pool
import os
import shutil
import subprocess
import sys

THREAD_COUNT = 8
path = r'F:\lsr'

def main():
    pool = Pool(THREAD_COUNT)
    commands = [
        "git clone git@git.woa.com:LSR/LSR_pipeline.git",
        "git clone git@git.woa.com:LSR/maya-rigtools.git",
        "git clone git@git.woa.com:LSR/maya-rig.git",
        "git clone git@git.woa.com:LSR/ue-core.git",
        "git clone git@git.woa.com:LSR/launcher.git",
        "git clone git@git.woa.com:LSR/maya-core.git",
        "git clone git@git.woa.com:LSR/python-ext.git",
        "git clone git@git.woa.com:LSR/protostar.git",
        "git clone git@git.woa.com:LSR/qt-core.git",
        "git clone git@git.woa.com:LSR/maya-anim.git",
        "git clone git@git.woa.com:LSR/python-core.git",
        "git clone git@git.woa.com:LSR/maya-animtools.git",
        "git clone git@git.woa.com:LSR/lams.git",
        "git clone git@git.woa.com:LSR/maya-test-resource.git",
        "git clone git@git.woa.com:LSR/qt-resource.git",
        "git clone git@git.woa.com:LSR/devl.git",
        "git clone git@git.woa.com:LSR/hou-core.git",
        "git clone git@git.woa.com:LSR/hou-tools.git",
        "git clone git@git.woa.com:LSR/thm-repo.git",
        "git clone git@git.woa.com:LSR/open3d.git",
    ]

    pool.map(lambda command: subprocess.Popen(command,cwd=path), commands)
    pool.close()
    pool.join()
    print("done")


if __name__ == "__main__":
    main()
