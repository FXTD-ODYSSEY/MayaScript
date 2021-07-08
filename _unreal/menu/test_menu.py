# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-06-18 15:39:17'

import os
import imp
import unreal

PLUGIN = "RedArtToolkit"
plugins = unreal.Paths.project_plugins_dir()
init_unreal = os.path.join(plugins,PLUGIN,"Content","Python","init_unreal.py")
init_unreal = os.path.abspath(init_unreal)

module = imp.load_source("init_unreal",init_unreal)
module.create_menu()
