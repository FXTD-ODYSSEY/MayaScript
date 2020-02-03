import os
import sys

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine



# Create an instance of the application
# QApplication MUST be declared in global scope to avoid segmentation fault
app = QApplication(sys.argv)

# Create QML engine
engine = QQmlApplicationEngine()

# Load the qml file into the engine
engine.load(QUrl(r"D:\Users\82047\Desktop\repo\MayaScript\_QtDemo\qml\demo\example.qml"))

print engine.rootObjects()

app.exec_()