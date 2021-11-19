# coding:utf-8
from __future__ import division, print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-05-04 11:13:09"

"""
https://stackoverflow.com/questions/53349623/how-to-change-languagestranslations-dynamically-on-pyqt5
"""

import os
import sys

repo = (lambda f: lambda p=__file__: f(f, p))(
    lambda f, p: p
    if [
        d
        for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p))
        if d == ".git"
    ]
    else None
    if os.path.dirname(p) == p
    else f(f, os.path.dirname(p))
)()
MODULE = os.path.join(repo, "_vendor", "Qt")
sys.path.insert(0, MODULE) if MODULE not in sys.path else None

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import load_ui
from window_ui import Ui_Form
from dayu_widgets import dayu_theme
DIR = os.path.dirname(__file__)




class UIWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(UIWindow, self).__init__()
        # ui_file = os.path.join(DIR, "window.ui")
        # load_ui(ui_file, self)
        self.setupUi(self)
        dayu_theme.apply(self)
        self.trans = QtCore.QTranslator(self)
        # print(self.retranslateUi)

        # self.combo = QtWidgets.QComboBox(self)
        # chinese_qm = os.path.join(DIR,"eng_chs.qm")
        # options = ([('English', ''), ('中文', chinese_qm), ])

        # for i, (text, lang) in enumerate(options):
        #     self.combo.addItem(text)
        #     self.combo.setItemData(i, lang)
        # self.retranslateUi()

    def change_func(self, index):
        path = self.combo.itemData(index)
        if os.path.isfile(path):
            self.trans.load(path)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        super(UIWindow, self).changeEvent(event)

    # def retranslateUi(self):
    #     self.button.setText(QtWidgets.QApplication.translate("Demo", "Start"))
    #     self.label.setText(QtWidgets.QApplication.translate("Demo", "Hello, World"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    demo = UIWindow()
    demo.show()
    sys.exit(app.exec_())
