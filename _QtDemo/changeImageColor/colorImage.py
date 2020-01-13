import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

dir_path = os.path.dirname(os.path.realpath(__file__))

class Ui_MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindows,self).__init__()
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Change color PNG Test")
        self.setStyleSheet("background-color:white;")
        self.resize(350, 350)

        self.DMX_Color = QtGui.QColor('#ff0000')
        self.button_DMX = QtWidgets.QPushButton(self.central_widget)
        self.button_DMX.move(100, 100)
        path_image = os.path.join(dir_path, "animtool.png").replace("\\", "/")
        self.image = QtGui.QImage(path_image)

        self.button_DMX.clicked.connect(self.processButton_DMX)
        self.change_image()

    def change_image(self, color=QtGui.QColor("white")):
        for x in range(self.image.width()):
            for y in range(self.image.height()):
                pcolor = self.image.pixelColor(x, y)
                if pcolor.alpha() > 0:
                    n_color = QtGui.QColor(color)
                    n_color.setAlpha(pcolor.alpha())
                    self.image.setPixelColor(x, y, n_color)
        self.button_DMX.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(self.image)))
        self.button_DMX.setIconSize(self.image.size())
        self.button_DMX.setFixedSize(self.image.size())        

    @QtCore.pyqtSlot()
    def processButton_DMX(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.white, self)
        if color.isValid():
            self.change_image(color)

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindows()
    MainWindow.show()

    rc = app.exec_()
    sys.exit(rc)


if __name__ == "__main__":
     main()