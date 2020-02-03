# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-03 15:40:32'

"""

"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class OverLay(QtWidgets.QWidget):
    """OverLay 红框Debug标记 暂时弃用"""
    BorderColor     = QtGui.QColor(255, 0, 0, 255)     
    BackgroundColor = QtGui.QColor(0, 255, 0, 125) 
    
    def __init__(self, parent):
        super(OverLay,self).__init__()
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setWindowFlags(QtCore.Qt.WindowTransparentForInput | QtCore.Qt.FramelessWindowHint)
        self.setFocusPolicy( QtCore.Qt.NoFocus )
        self.hide()

        # self.setEnabled(False)
        # self.setAutoFillBackground(True)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setParent(parent)
        parent.installEventFilter(self)

    def paintEvent(self, event):
        
        # NOTE https://stackoverflow.com/questions/51687692/how-to-paint-roundedrect-border-outline-the-same-width-all-around-in-pyqt-pysi
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)   

        rectPath = QtGui.QPainterPath()                      
        height = self.height() - 4                     
        rect = QtCore.QRectF(2, 2, self.width()-4, height)
        
        # NOTE 绘制边界颜色
        rectPath.addRoundedRect(rect, 15, 15)
        painter.setPen(QtGui.QPen(self.BorderColor, 2, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawPath(rectPath)

        # NOTE 绘制背景颜色
        painter.setBrush(self.BackgroundColor)
        painter.drawRoundedRect(rect, 15, 15)
    
    def eventFilter(self, obj, event):
        if not obj.isWidgetType():
            return False
        
        if self.isVisible():
            self.setGeometry(obj.rect())
        elif event.type() == QtCore.QEvent.Resize:
            self.setGeometry(obj.rect())

        return False


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    button = QtWidgets.QPushButton("click")
    frame = OverLay(button)
    button.clicked.connect(lambda:frame.setVisible(not frame.isVisible()))
    button.show()

    app.exec_()