# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/56292450/how-to-save-selected-items-to-qsettings-from-qlistwidget-qtablewidget
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-02 21:39:49'

from PyQt5 import QtCore, QtGui, QtWidgets

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.listwidget_1 = QtWidgets.QListWidget(
            objectName="listwidget_1", 
            selectionMode=QtWidgets.QAbstractItemView.MultiSelection
        )
        listwidget_2 = QtWidgets.QListWidget(
            objectName="listwidget_2", 
            selectionMode=QtWidgets.QAbstractItemView.MultiSelection
        )

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.listwidget_1)
        lay.addWidget(listwidget_2)

        self.read_settings()

    def closeEvent(self, event):
        self.write_settings()
        super().closeEvent(event)

    def read_settings(self):
        settings = QtCore.QSettings("data.ini", QtCore.QSettings.IniFormat)
        childrens = self.findChildren(QtWidgets.QWidget)
        for children in childrens:
            if isinstance(children, QtWidgets.QListWidget) and children.objectName():
                settings.beginGroup(children.objectName())
                items = settings.value("items")
                selecteditems = settings.value("selecteditems")
                selectionMode = settings.value("selectionMode", type=QtWidgets.QAbstractItemView.SelectionMode)
                children.setSelectionMode(selectionMode)
                # In the first reading the initial values must be established
                if items is None:
                    if children.objectName() == "listwidget_1":
                        for i in range(10):
                            children.addItem(QtWidgets.QListWidgetItem(str(i)))
                    elif children.objectName() == "listwidget_2":
                        for i in "abcdefghijklmnopqrstuvwxyz":
                            children.addItem(QtWidgets.QListWidgetItem(i))
                else:
                    stream = QtCore.QDataStream(items, QtCore.QIODevice.ReadOnly)
                    while not stream.atEnd():
                        it = QtWidgets.QListWidgetItem()
                        stream >> it
                        children.addItem(it)
                    stream = QtCore.QDataStream(selecteditems, QtCore.QIODevice.ReadOnly)
                    while not stream.atEnd():
                        row = stream.readInt()
                        it = children.item(row)
                        it.setSelected(True)
                settings.endGroup()

    def write_settings(self):
        settings = QtCore.QSettings("data.ini", QtCore.QSettings.IniFormat)
        childrens = self.findChildren(QtWidgets.QWidget)
        for children in childrens:
            if isinstance(children, QtWidgets.QListWidget) and children.objectName():
                settings.beginGroup(children.objectName())
                items = QtCore.QByteArray()
                stream = QtCore.QDataStream(items, QtCore.QIODevice.WriteOnly)
                for i in range(children.count()):
                    stream << children.item(i)
                selecteditems = QtCore.QByteArray()
                stream = QtCore.QDataStream(selecteditems, QtCore.QIODevice.WriteOnly)
                for it in children.selectedItems():
                    stream.writeInt(children.row(it))
                settings.setValue("items", items)
                settings.setValue("selecteditems", selecteditems)
                settings.setValue("selectionMode", children.selectionMode())
                settings.endGroup()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())