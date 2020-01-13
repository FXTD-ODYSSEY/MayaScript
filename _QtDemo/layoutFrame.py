import sys
from itertools import product

from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWidget

# NOTE https://stackoverflow.com/questions/41483034/pyqt5-layout-with-frames

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        self.layoutUI()

    def layoutUI(self):
        self.setStyleSheet("background-color: brown;")

        self.principalLayout = QHBoxLayout(self)

        self.rightFrame = QFrame(self)
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.rightFrame)
        self.gridLayout = QGridLayout()

        btns = {(0, 0): "start", (0, 2): "Stop",
                (1, 0): "Speed-", (1, 1): "1", (1, 2): "Speed+",
                (2, 0): "Pieces", (2, 1): "0", (2, 2): "Clear",
                (3, 0): "Length", (3, 1): "0", (3, 2): "Clear",
                (4, 1): "Manual",
                (5, 0): "Cut", (5, 1): "Feed", (5, 2): "Clear"}
        for pos, name in btns.items():
            x, y = pos
            btn = QPushButton(self.rightFrame)
            btn.setText(name)
            self.gridLayout.addWidget(btn, x, y)

        self.verticalLayout.addLayout(self.gridLayout)
        self.principalLayout.addWidget(self.rightFrame)

        self.verticalLayoutR = QVBoxLayout()
        self.verticalLayoutR.setSpacing(0)
        self.exitFrame = QFrame(self)
        self.exitFrame.setStyleSheet("background-color: red;")
        self.exitFrame.setFrameShape(QFrame.StyledPanel)
        self.exitFrame.setFrameShadow(QFrame.Raised)
        self.exitverticalLayout = QVBoxLayout(self.exitFrame)
        self.exitBtn = QPushButton("Exit", self.exitFrame)
        self.exitverticalLayout.addWidget(self.exitBtn)
        self.verticalLayoutR.addWidget(self.exitFrame)

        self.numpadFrame = QFrame(self)
        self.numpadFrame.setStyleSheet("background-color: yellow;")
        self.numpadFrame.setFrameShape(QFrame.StyledPanel)
        self.numpadFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.numpadFrame)
        spacerItem = QSpacerItem(2, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QVBoxLayout()
        spacerItem1 = QSpacerItem(20, 57, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)

        x = (0, 1, 2)

        coords = list(product(x, x))
        coords.append((3, 1))

        for coord in coords:
            x, y = coord
            button = QPushButton(self.numpadFrame)
            button.setFixedSize(60, 60)
            button.setText(str(x + 3 * y + 1))
            button.setStyleSheet("background-color: white;")
            self.gridLayout.addWidget(button, x, y)
        button.setText("0")

        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem3 = QSpacerItem(2, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)

        self.verticalLayoutR.addWidget(self.numpadFrame)

        self.adminFrame = QFrame(self)
        self.adminFrame.setStyleSheet("background-color: blue;")
        self.adminFrame.setFrameShape(QFrame.StyledPanel)
        self.adminFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.adminFrame)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.adminBtn = QPushButton("Admin", self.adminFrame)
        self.horizontalLayout.addWidget(self.adminBtn)
        self.verticalLayoutR.addWidget(self.adminFrame)
        self.principalLayout.addLayout(self.verticalLayoutR)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())