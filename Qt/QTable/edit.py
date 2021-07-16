# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-14 14:43:59'

"""
NOTE https://stackoverflow.com/questions/39290017/how-to-intercept-key-events-when-editing-a-cell-in-qtablewidget-qtableview
"""
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *

class LineEditDelegate(QtWidgets.QStyledItemDelegate):

    moveCurrentCellBy = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(LineEditDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QLineEdit(parent)
        self.editor.setFrame(False)
        self.editor.installEventFilter(self)
        return self.editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        print "setModelData"
        print index
        value = editor.text()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def eventFilter(self, target, event):
        if target is self.editor:
            if event.type() == QtCore.QEvent.KeyPress:
                moveCell, row, column = False, 0, 0
                if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter, QtCore.Qt.Key_Down):
                    moveCell, row, column = True, 1, 0
                if event.key() in (QtCore.Qt.Key_Right, QtCore.Qt.Key_Tab):
                    moveCell, row, column = True, 0, 1
                if event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Backtab):
                    moveCell, row, column = True, 0, -1
                if event.key() == QtCore.Qt.Key_Up:
                    moveCell, row, column = True, -1, 0
                if moveCell:
                    self.commitData.emit(self.editor)
                    self.closeEditor.emit(self.editor, QtWidgets.QAbstractItemDelegate.NoHint)
                    self.moveCurrentCellBy.emit(row, column)
                    return True
        return False     


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        delegate = LineEditDelegate()
        delegate.moveCurrentCellBy.connect(self.moveCurrentCellBy)
        self.setItemDelegate(delegate)

    def moveCurrentCellBy(self, rowStep, columnStep):
        row = self.currentRow() + rowStep
        column = self.currentColumn() + columnStep
        if row >= self.rowCount():
            self.setRowCount(row + 1)
        if column >= self.columnCount():
            self.setColumnCount(column + 1)
        self.setCurrentCell(row, column)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle("fusion")
    tab = TableWidget()
    tab.setRowCount(3)
    tab.setColumnCount(2)
    tab.setItem(0,0, QtWidgets.QTableWidgetItem("Cell (1,1)"))
    tab.setItem(0,1, QtWidgets.QTableWidgetItem("Cell (1,2)"))
    tab.setItem(1,0, QtWidgets.QTableWidgetItem("Cell (2,1)"))
    tab.setItem(1,1, QtWidgets.QTableWidgetItem("Cell (2,2)"))
    tab.setItem(2,0, QtWidgets.QTableWidgetItem("Cell (3,1)"))
    tab.setItem(2,1, QtWidgets.QTableWidgetItem("Cell (3,2)"))
    tab.setItem(3,0, QtWidgets.QTableWidgetItem("Cell (4,1)"))
    tab.setItem(3,1, QtWidgets.QTableWidgetItem("Cell (4,2)"))
    tab.show()
    sys.exit(app.exec_())