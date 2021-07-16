#!/usr/bin/env python

"""PyQt4 port of the layouts/basiclayout example from Qt v4.x"""

from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(Dialog.NumButtons):
            button = QPushButton("Button %d" % (i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("Grid layout")
        layout = QGridLayout()

        for i in range(Dialog.NumGridRows):
            label = QLabel("Line %d:" % (i + 1))
            lineEdit = QLineEdit()
            layout.addWidget(label, i + 1, 0)
            layout.addWidget(lineEdit, i + 1, 1)

        self.smallEditor = QTextEdit()
        self.smallEditor.setPlainText("This widget takes up about two thirds "
                "of the grid layout.")

        layout.addWidget(self.smallEditor, 0, 2, 4, 1)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
