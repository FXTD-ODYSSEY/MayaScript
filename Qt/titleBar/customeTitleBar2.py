import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

# NOTE https://stackoverflow.com/questions/44241612/custom-titlebar-with-frame-in-pyqt5

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout  = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800,400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False


class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("My Own Bar")

        btn_size = 35

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("background-color: red;")

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("background-color: gray;")

        self.btn_max = QPushButton("+")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet("background-color: gray;")

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: black;
            color: white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())