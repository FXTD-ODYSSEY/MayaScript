# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-18 16:46:16'

from dependencies import Injector
import attr


@attr.s(frozen=True)
class SetupLayout(object):
    """Setup Layout Height for high dpi screen."""
    editor = attr.ib()
    scale_x = attr.ib()
    scale_y = attr.ib()
    def __call__(self):
        print(self.editor)
        print(self.scale_x)
        print(self.scale_y)

def call(editor,scale_x,scale_y):
    print([editor])
    class Container(object):
        print(globals())
        editor = editor
        scale_x = scale_x
        scale_y = scale_y
        setup_layout = SetupLayout
    Container.setup_layout()

call("editor",1,1)
