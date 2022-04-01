# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-03-24 17:21:59"

# Import built-in modules
import os
import sys
import time

DIR = os.path.dirname(__file__)
index = sys.argv[1]

project_folder = os.path.join(DIR, "project")
test_file = os.path.join(project_folder, "test_{0}.txt".format(index))

localtime = time.asctime(time.localtime(time.time()))

with open(test_file, "a+") as f:
    f.write("{0}: write test".format(localtime))
