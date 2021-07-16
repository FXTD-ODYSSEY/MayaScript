# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/4100139
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-14 12:07:56'

import sys
from PySide2 import QtCore,QtGui,QtWidgets

class MTreeExpandHook(QtCore.QObject):
    """
    MTreeExpandHook( QTreeView )
    """

    def __init__(self, tree):
        super(MTreeExpandHook, self).__init__()
        self.setParent(tree)
        # NOTE viewport for MouseButtonPress event listen
        tree.viewport().installEventFilter(self)
        self.tree = tree

    def eventFilter(self, receiver, event):
        if (
            # NOTE mouse left click 
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            # NOTE keyboard shift press
            and event.modifiers() & QtCore.Qt.ShiftModifier
        ):
            # NOTE get mouse local position
            pos = self.tree.mapFromGlobal(QtGui.QCursor.pos())
            index = self.tree.indexAt(pos)
            if not self.tree.isExpanded(index):
                # NOTE expand all child
                self.tree.expandRecursively(index)
                return True
        return super(MTreeExpandHook, self).eventFilter(self.tree, event)
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    model = QtGui.QStandardItemModel()
    
    # NOTE create nested data
    for i in range(3):
        parent = QtGui.QStandardItem('Family {}'.format(i))
        for j in range(3):
            child = QtGui.QStandardItem('Child {}'.format(i*3+j))
            for k in range(3):
                sub_child = QtGui.QStandardItem("Sub Child")
                child.appendRow([sub_child])
                for x in range(2):
                    sub_child_2 = QtGui.QStandardItem("Sub Child 2")
                    sub_child.appendRow([sub_child_2])
            parent.appendRow([child])
        model.appendRow(parent)

        
    treeView = QtWidgets.QTreeView()
    # NOTE hide header to get the correct position index
    treeView.setHeaderHidden(True)
    MTreeExpandHook(treeView)
    treeView.setModel(model)
    treeView.show()
    
    sys.exit(app.exec_())
    
    
    