# -*- coding: utf-8 -*-
"""

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-12-15 23:00:57'

import contextlib
import signal
import sys
from Qt import QtWidgets
from Qt import QtCore


@contextlib.contextmanager
def application(*args):
    app = QtWidgets.QApplication.instance()

    if not app:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QtWidgets.QApplication(sys.argv)
        yield app
        app.exec_()
    else:
        yield app

class EventFilter(QtCore.QObject):
    
    def eventFilter(self, receiver,event):
        print(event.type())
        return super(EventFilter, self).eventFilter(receiver,event)

with application() as app:
    filter = EventFilter()
    widget = QtWidgets.QTabWidget()
    widget.installEventFilter(filter)
    
    print(widget.count())
    print(widget.property("count"))
    meta = widget.staticMetaObject
    widget.show()
    # widget.addTab(QtWidgets.QTabWidget(),'test')
    # for i in range(meta.propertyCount()):
    #     prop = meta.property(i)
    #     prop_name = prop.name()
    #     print(prop_name)
        
        



