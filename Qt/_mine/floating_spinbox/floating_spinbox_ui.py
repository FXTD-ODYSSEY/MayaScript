# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\repo\MayaScript\Qt\_mine\floating_spinbox\floating_spinbox.ui'
#
# Created: Wed Jun  8 09:54:38 2022
#      by: pyside2-uic  running on PySide2 5.15.2
#
# WARNING! All changes made in this file will be lost!

# Import local modules
from Qt import QtCompat
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(578, 238)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Graphic_View = QtWidgets.QGraphicsView(Form)
        self.Graphic_View.setObjectName("Graphic_View")
        self.verticalLayout.addWidget(self.Graphic_View)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.retranslateUi(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))


if __name__ == "__main__":
    # Import built-in modules
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
