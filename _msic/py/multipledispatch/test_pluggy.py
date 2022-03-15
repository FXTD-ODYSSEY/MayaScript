# -*- coding: utf-8 -*-
"""
fail
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-04 17:31:42'


import sys
import pluggy  # type: ignore
from multipledispatch import dispatch

hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")


class MySpec:
    """A hook specification namespace."""

    @hookspec()
    def myhook(self, args):
        """My special little hook that you can customize."""
        return type("WidgetDockMixin", (), {})


class Plugin_1:
    """A hook implementation namespace."""

    @hookimpl
    def myhook(self, args):
        print("inside Plugin_1.myhook()")

class Plugin_2:
    """A 2nd hook implementation namespace."""

    @hookimpl
    @dispatch(int)
    def myhook(self, args):
        print("inside Plugin_2.myhook()")


# create a manager and add the spec
pm = pluggy.PluginManager("myproject")
pm.add_hookspecs(MySpec)


def callback(result):
    print("historic call result is {result}".format(result=result))


# register plugins
pm.register(Plugin_1())
pm.register(Plugin_2())

mixin = pm.hook.myhook(args=1)
print(mixin)


