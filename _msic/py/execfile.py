# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/41658338
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-09-27 16:22:21'

SCRIPT_PATH = r"path"

def execfile(filepath, globals=None, locals=None):
    globals = {} if globals is None else globals
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

execfile(SCRIPT_PATH)

