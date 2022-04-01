# -*- coding: utf-8 -*-
"""
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-03-26 16:58:36"

# Import built-in modules
from multiprocessing.dummy import Pool
import os
import shutil
import subprocess
import sys

THREAD_COUNT = 8
script_path = r"F:\repo\MayaScript\maya\_maya_batch\python_dummy_pool\script.py"
BIN = os.path.dirname(sys.executable)
mayapy = os.path.join(BIN, "mayapy.exe")

project_folder = os.path.join(script_path, "..", "project")
if os.path.exists(project_folder):
    shutil.rmtree(project_folder)
os.mkdir(project_folder)


def main():
    pool = Pool(THREAD_COUNT)
    commands = []
    for index in range(30):
        command = [mayapy, script_path, str(index)]
        commands.append(command)

    pool.map(lambda command: subprocess.Popen(command, shell=True), commands)
    pool.close()
    pool.join()
    print("done")


if __name__ == "__main__":
    main()
