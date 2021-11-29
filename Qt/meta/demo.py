# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-24 09:40:41'

import sys
from Qt import QtWidgets,QtCore

app = QtWidgets.QApplication(sys.argv)

list_widget = QtWidgets.QListWidget()
list_widget.addItem("test")

model = list_widget.model()
meta = list_widget.metaObject()
meta = model.metaObject()
for i in range(meta.propertyCount()):
    prop = meta.property(i)
    print(prop.name())
    
for i in range(meta.methodCount()):
    method = meta.method(i)
    if method.methodType() == QtCore.QMetaMethod.Signal:
        print(method.name())

print(model.property("data"))



