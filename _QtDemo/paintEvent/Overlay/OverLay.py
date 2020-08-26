# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-19 14:48:53'

"""
NOTE https://stackoverflow.com/questions/48022786/pyqt5-qpainter-overlay-qwidget
"""

import sys

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

# class OverLay(QtWidgets.QWidget):
#     BorderColor     = QColor(0, 0, 0, 255)     
#     BackgroundColor = QColor(255, 165, 0, 180) 
    
#     def __init__(self, *args, **kwargs):
#         QWidget.__init__(self, *args, **kwargs)
#         self.setAttribute(Qt.WA_NoSystemBackground)
#         self.setAttribute(Qt.WA_TransparentForMouseEvents)

#     def paintEvent(self, event):
#         # painter = QPainter(self)
#         # painter.fillRect(self.rect(), QColor(80, 80, 255, 128))
        
#         # NOTE https://stackoverflow.com/questions/51687692/how-to-paint-roundedrect-border-outline-the-same-width-all-around-in-pyqt-pysi
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)   

#         rectPath = QPainterPath()                      
#         height = self.height() - 8                     
#         rectPath.addRoundedRect(QRectF(2, 2, self.width()-4, height), 15, 15)
#         painter.setPen(QPen(self.BorderColor, 2, Qt.SolidLine,
#                                  Qt.RoundCap, Qt.RoundJoin))
#         # painter.setBrush(self.BackgroundColor)
#         # painter.drawPath(rectPath)
#         # painter.setPen(QPen(self.BackgroundColor, 2,
#                                 #  Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

class OverLay(QtWidgets.QWidget):
    BorderColor     = QtGui.QColor(255, 0, 0, 255)     
    BackgroundColor = QtGui.QColor(255, 165, 0, 180) 
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        
        # NOTE https://stackoverflow.com/questions/51687692/how-to-paint-roundedrect-border-outline-the-same-width-all-around-in-pyqt-pysi
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)   

        rectPath = QtGui.QPainterPath()                      
        height = self.height() - 4                 
        rectPath.addRoundedRect(QtCore.QRectF(2, 2, self.width()-4, height), 0, 0)
        painter.setPen(QtGui.QPen(self.BorderColor, 2, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawPath(rectPath)

class Filter(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.m_overlay = None
        self.m_overlayOn = None

    def eventFilter(self, obj, event):
        if not obj.isWidgetType():
            return False
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if not self.m_overlay:
                if obj.parentWidget():
                    self.m_overlay = OverLay(obj.parentWidget())
                    self.m_overlay.setGeometry(obj.geometry())
                else:
                    self.m_overlay = OverLay(obj)
                    self.m_overlay.setGeometry(QtCore.QRect(0,0,obj.width(),obj.height()))

            self.m_overlayOn = obj
            self.m_overlay.show()
        elif event.type() == QtCore.QEvent.Resize:
            if self.m_overlay and self.m_overlayOn == obj:
                self.m_overlay.setGeometry(obj.geometry())
        return False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Filter()
    # window = QtWidgets.QWidget()
    lay = QtWidgets.QHBoxLayout(window)
    for text in ( "Foo", "Bar", "Baz "):
        button = QtWidgets.QPushButton(text)
        lay.addWidget(button)
        button.installEventFilter(window)
        button.clicked.connect(lambda:sys.stdout.write("%s\n" % text))
    window.setMinimumSize(300, 250)
    window.show()
    sys.exit(app.exec_())