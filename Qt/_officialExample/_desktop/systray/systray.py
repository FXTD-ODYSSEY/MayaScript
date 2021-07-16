#!/usr/bin/env python

############################################################################
#
#  Copyright (C) 2006-2007 Trolltech ASA. All rights reserved.
#
#  This file is part of the example classes of the Qt Toolkit.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://trolltech.com/products/qt/licenses/licensing/opensource/
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://trolltech.com/products/qt/licenses/licensing/licensingoverview
#  or contact the sales department at sales@trolltech.com.
#
#  In addition, as a special exception, Trolltech gives you certain
#  additional rights. These rights are described in the Trolltech GPL
#  Exception version 1.0, which can be found at
#  http://www.trolltech.com/products/qt/gplexception/ and in the file
#  GPL_EXCEPTION.txt in this package.
#
#  In addition, as a special exception, Trolltech, as the sole copyright
#  holder for Qt Designer, grants users of the Qt/Eclipse Integration
#  plug-in the right for the Qt/Eclipse Integration to link to
#  functionality provided by Qt Designer and its related libraries.
#
#  Trolltech reserves all rights not expressly granted herein.
#
#  Trolltech ASA (c) 2007
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QVariant', 2)

from PySide2 import QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import systray_rc


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.createIconGroupBox()
        self.createMessageGroupBox()

        self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())

        self.createActions()
        self.createTrayIcon()

        self.showMessageButton.clicked.connect(self.showMessage)
        self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
        self.iconComboBox.currentIndexChanged[int].connect(self.setIcon)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.iconGroupBox)
        mainLayout.addWidget(self.messageGroupBox)
        self.setLayout(mainLayout)

        self.iconComboBox.setCurrentIndex(1)
        self.trayIcon.show()

        self.setWindowTitle("Systray")
        self.resize(400, 300)

    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(Window, self).setVisible(visible)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QMessageBox.information(self, "Systray",
                    "The program will keep running in the system tray. To "
                    "terminate the program, choose <b>Quit</b> in the "
                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()

    def setIcon(self, index):
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    def iconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.iconComboBox.setCurrentIndex(
                    (self.iconComboBox.currentIndex() + 1)
                    % self.iconComboBox.count())
        elif reason == QSystemTrayIcon.MiddleClick:
            self.showMessage()

    def showMessage(self):
        icon = QSystemTrayIcon.MessageIcon(
                self.typeComboBox.itemData(self.typeComboBox.currentIndex()))
        self.trayIcon.showMessage(self.titleEdit.text(),
                self.bodyEdit.toPlainText(), icon,
                self.durationSpinBox.value() * 1000)

    def messageClicked(self):
        QMessageBox.information(None, "Systray",
                "Sorry, I already gave what help I could.\nMaybe you should "
                "try asking a human?")

    def createIconGroupBox(self):
        self.iconGroupBox = QGroupBox("Tray Icon")

        self.iconLabel = QLabel("Icon:")

        self.iconComboBox = QComboBox()
        self.iconComboBox.addItem(QIcon(':/images/bad.svg'), "Bad")
        self.iconComboBox.addItem(QIcon(':/images/heart.svg'), "Heart")
        self.iconComboBox.addItem(QIcon(':/images/trash.svg'), "Trash")

        self.showIconCheckBox = QCheckBox("Show icon")
        self.showIconCheckBox.setChecked(True)

        iconLayout = QHBoxLayout()
        iconLayout.addWidget(self.iconLabel)
        iconLayout.addWidget(self.iconComboBox)
        iconLayout.addStretch()
        iconLayout.addWidget(self.showIconCheckBox)
        self.iconGroupBox.setLayout(iconLayout)

    def createMessageGroupBox(self):
        self.messageGroupBox = QGroupBox("Balloon Message")

        typeLabel = QLabel("Type:")

        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem("None", QSystemTrayIcon.NoIcon)
        self.typeComboBox.addItem(self.style().standardIcon(
                QStyle.SP_MessageBoxInformation), "Information",
                QSystemTrayIcon.Information)
        self.typeComboBox.addItem(self.style().standardIcon(
                QStyle.SP_MessageBoxWarning), "Warning",
                QSystemTrayIcon.Warning)
        self.typeComboBox.addItem(self.style().standardIcon(
                QStyle.SP_MessageBoxCritical), "Critical",
                QSystemTrayIcon.Critical)
        self.typeComboBox.setCurrentIndex(1)

        self.durationLabel = QLabel("Duration:")

        self.durationSpinBox = QSpinBox()
        self.durationSpinBox.setRange(5, 60)
        self.durationSpinBox.setSuffix(" s")
        self.durationSpinBox.setValue(15)

        durationWarningLabel = QLabel("(some systems might ignore this "
                "hint)")
        durationWarningLabel.setIndent(10)

        titleLabel = QLabel("Title:")

        self.titleEdit = QLineEdit("Cannot connect to network")

        bodyLabel = QLabel("Body:")

        self.bodyEdit = QTextEdit()
        self.bodyEdit.setPlainText("Don't believe me. Honestly, I don't have "
                "a clue.\nClick this balloon for details.")

        self.showMessageButton = QPushButton("Show Message")
        self.showMessageButton.setDefault(True)

        messageLayout = QGridLayout()
        messageLayout.addWidget(typeLabel, 0, 0)
        messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2)
        messageLayout.addWidget(self.durationLabel, 1, 0)
        messageLayout.addWidget(self.durationSpinBox, 1, 1)
        messageLayout.addWidget(durationWarningLabel, 1, 2, 1, 3)
        messageLayout.addWidget(titleLabel, 2, 0)
        messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4)
        messageLayout.addWidget(bodyLabel, 3, 0)
        messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)
        messageLayout.addWidget(self.showMessageButton, 5, 4)
        messageLayout.setColumnStretch(3, 1)
        messageLayout.setRowStretch(4, 1)
        self.messageGroupBox.setLayout(messageLayout)

    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self,
                triggered=self.hide)

        self.maximizeAction = QAction("Ma&ximize", self,
                triggered=self.showMaximized)

        self.restoreAction = QAction("&Restore", self,
                triggered=self.showNormal)

        self.quitAction = QAction("&Quit", self,
                triggered=qApp.quit)

    def createTrayIcon(self):
         self.trayIconMenu = QMenu(self)
         self.trayIconMenu.addAction(self.minimizeAction)
         self.trayIconMenu.addAction(self.maximizeAction)
         self.trayIconMenu.addAction(self.restoreAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    window.show()
    sys.exit(app.exec_())
