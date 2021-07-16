# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-03 12:45:19'

"""
https://wiki.python.org/moin/PyQt/Binding%20widget%20properties%20to%20Python%20variables?action=AttachFile&do=view&target=bindable.py
"""

import os
def getGitRepo(p):
    return p if [f for f in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if f == '.git'] else None if os.path.dirname(p) == p else getGitRepo(os.path.dirname(p))
repo = getGitRepo(__file__)

import sys
MODULE = os.path.join(repo,"_vendor","Qt")
sys.path.insert(0,MODULE) if MODULE not in sys.path else None
    

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

def bind(objectName, propertyName, typ):

    def getter(self):
        return typ(self.findChild(QObject, objectName).property(propertyName))
    
    def setter(self, value):
        self.findChild(QObject, objectName).setProperty(propertyName, value)
    
    return property(getter, setter)

class Window(QWidget):

    name = bind("nameEdit", "text", str)
    address = bind("addressEdit", "plainText", str)
    contact = bind("contactCheckBox", "checked", bool)

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        nameEdit = QLineEdit()
        nameEdit.setObjectName("nameEdit")
        addressEdit = QTextEdit()
        addressEdit.setObjectName("addressEdit")
        contactCheckBox = QCheckBox()
        contactCheckBox.setObjectName("contactCheckBox")

        button = QPushButton("click")
        button.clicked.connect(lambda:[None for self.contact in [False]])
        
        layout = QFormLayout(self)
        layout.addRow(self.tr("Name:"), nameEdit)
        layout.addRow(self.tr("Address:"), addressEdit)
        layout.addRow(self.tr("Receive extra information:"), contactCheckBox)
        layout.addRow(self.tr("get name"), button)

        nameEdit.textChanged.connect(lambda text: print("name",self.name) )
    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())