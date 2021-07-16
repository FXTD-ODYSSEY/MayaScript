# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-31 18:00:41'

"""
# NOTE https://wiki.qt.io/Qt_for_Python_Tutorial_HelloQML
"""

# from PySide2.QtWidgets import QApplication
# from PySide2.QtQuick import QQuickView
# from PySide2.QtCore import QUrl

# app = QApplication([])
# view = QQuickView()
# url = QUrl("D:/Users/82047/Desktop/repo/MayaScript/_QtDemo/qml/view.qml")

# view.setSource(url)
# view.show()
# app.exec_()

import os
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

DIR = os.path.dirname(__file__)
qml = os.path.join(DIR,"view.qml")

app = QApplication([])
view = QQuickView()
url = QUrl.fromLocalFile(qml)

view.setSource(url)
view.show()
app.exec_()