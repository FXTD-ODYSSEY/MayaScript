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
if MODULE not in sys.path:
    sys.path.insert(0,MODULE)

from Qt import QtCore,QtGui,QtWidgets

def bind(typ,objectName, propertyName ,getter = None ,setter = None):

    def _getter(self):
        print ("getter objectName ",objectName)
        return self.findChild(QtCore.QObject, objectName).property(propertyName)
    
    def _setter(self, value):
        print ("setter objectName ",objectName,value)
        self.findChild(QtCore.QObject, objectName).setProperty(propertyName, value)
    
    return QtCore.Property(typ,_getter,_setter)

class Window(QtWidgets.QWidget):

    line1_text = bind(str,"line1", "text")
    line2_text = bind(str,"line2", "text")
    # line2_text = bind(str,"line2", "text")
    display = bind(str,"display_label", "text")

    def __init__(self, parent = None):
        super(Window,self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        line1 = QtWidgets.QLineEdit()
        line1.setObjectName("line1")
        line2 = QtWidgets.QLineEdit()
        line2.setObjectName("line2")
        display_label = QtWidgets.QLabel()
        display_label.setObjectName("display_label")
        button = QtWidgets.QPushButton('click')
        button.clicked.connect(lambda: [None for self.display in [self.line1_text]] )

        layout.addWidget(line1)
        layout.addWidget(line2)
        layout.addWidget(display_label)
        layout.addWidget(button)
        
        self.display = "init"
        line1.textChanged.connect(lambda *args: [None for self.display in ["%s %s" % (self.line1_text,self.line2_text)]])
        line2.textChanged.connect(lambda *args: [None for self.display in ["%s %s" % (self.line1_text,self.line2_text)]])
        # self.text = "asd"
    
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())