# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-07-18 23:29:36'

import os
from functools import partial
from PySide2 import QtCore, QtWidgets, QtGui

class IconWidget(QtWidgets.QWidget):

    def __init__(self,parent=None):
        super(IconWidget, self).__init__(parent)
        DIR = os.path.dirname(__file__)
        
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        style = QtWidgets.QApplication.style()

        container = QtWidgets.QWidget()
        container.setLayout(QtWidgets.QVBoxLayout())
        layout.addWidget(container)

        index = 0
        for attr in dir(QtWidgets.QStyle):
            if not attr.startswith("SP_"):
                continue

            index += 1
            ref = getattr(QtWidgets.QStyle,attr)

            # NOTE 保存图片到本地
            # pixmap = style.standardPixmap(ref)
            # path = os.path.join(DIR,"icon","%s.png" % attr)
            # pixmap.save(path,"PNG")

            icon = style.standardIcon(ref)
            button = QtWidgets.QPushButton()
            button.setIcon(icon)
            button.setText(attr)
            button.clicked.connect(partial(self.copy_text,"QtWidgets.QStyle.%s" % attr))
            container.layout().addWidget(button)

            if index % 18 == 0:
                container = QtWidgets.QWidget()
                container.setLayout(QtWidgets.QVBoxLayout())
                layout.addWidget(container)
        
    def copy_text(self,text):
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(text, mode=cb.Clipboard)

def main():
    app = QtWidgets.QApplication([])
    widget = IconWidget()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
