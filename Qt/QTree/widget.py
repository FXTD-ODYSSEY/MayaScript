# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/15300205
"""

from __future__ import absolute_import, division, print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-29 21:45:52"


import os
from Qt import QtWidgets
from Qt.QtCore import QModelIndex, Qt
from Qt.QtWidgets import QApplication, QPushButton, QTreeView

from Qt.QtGui import QStandardItem, QStandardItemModel
from Qt.QtCompat import loadUi


class PrvTreeviewNest(QTreeView):
    def __init__(self):
        super(PrvTreeviewNest, self).__init__()

        # loadUi('/home/user/yourproject/resource/treeview_nest.ui')

        # row can be 0 even when it's more than 0.
        self._datamodel = QStandardItemModel(0, 2)
        self.setModel(self._datamodel)

        for i in range(4):da
            self._add_widget(i + 1)

        self.show()

    def _add_widget(self, n):
        item_toplevel = QStandardItem('{}th item'.format(n))
        self._datamodel.setItem(n, 0, item_toplevel)

        widget_toplevel = QPushButton('{}th button'.format(n))
        qindex_toplevel = self._datamodel.index(n, 1, QModelIndex())
        self.setIndexWidget(qindex_toplevel, widget_toplevel)

        if n == 2:
            item_child_col0 = QStandardItem('child col0')
            item_child_col1 = QStandardItem('child col1')
            #item_toplevel.appendRow(item_child_col0)

            item_toplevel.insertRow(0, [item_child_col0, item_child_col1])

            widget_child = QPushButton('child widget')
            qindex_child = item_child_col1.index()
            self.setIndexWidget(qindex_child, widget_child)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # window = TreeviewWidgetSelectProve()
    window = PrvTreeviewNest()
    # window = TreeviewWidgetSelectProve()
    window.resize(320, 240)
    # window.show();
    window.setWindowTitle(QApplication.translate("toplevel", "Top-level widget"))
    # window.add_cols()

    sys.exit(app.exec_())