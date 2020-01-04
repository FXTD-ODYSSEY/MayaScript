# NOTE https://stackoverflow.com/questions/52270391/i-want-to-create-a-color-animation-for-a-button-with-pyqt5
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class BeautifulButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(BeautifulButton, self).__init__(*args, **kwargs)
        effect = QtWidgets.QGraphicsColorizeEffect(self)
        self.setGraphicsEffect(effect)

        self.animation = QtCore.QPropertyAnimation(effect, b"color")

        self.animation.setStartValue(QtGui.QColor(QtCore.Qt.cyan))
        self.animation.setEndValue(QtGui.QColor(255,0,0))

        self.animation.setLoopCount(5)
        self.animation.setDuration(5000)


class Page(QtWidgets.QWidget):
    okClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Page, self).__init__(parent)
        mainlayout = QtWidgets.QVBoxLayout(self)
        self.keypad = QtWidgets.QGroupBox()
        self.search = QtWidgets.QLineEdit()
        self.search.setProperty("last_text", "")
        self.search.setAlignment(QtCore.Qt.AlignCenter)
        self.search.setStyleSheet('font: bold 50pt')
        self.search.setMaxLength(13)
        self.search.setEchoMode(QtWidgets.QLineEdit.Password)
        mainlayout.addWidget(self.search)
        mainlayout.addWidget(self.keypad)
        mainlayout.setContentsMargins(150,150,150,150)

        lay = QtWidgets.QGridLayout(self.keypad)

        virtualkeypad = [
            '7','8','9',
            '4','5','6',
            '1','2','3',
            'BACK','0','OK'
        ]
        positions = [(i, j) for i in range(4) for j in range(3)]

        self.buttons = {}

        for position, name in zip(positions, virtualkeypad):
            if name == "OK":
                btn = BeautifulButton(name)
                btn.setStyleSheet('background-color: none; font: 50pt;')
                btn.setDisabled(True)
            else:
                btn = QtWidgets.QPushButton(name)
                btn.setStyleSheet('background-color: orange; font: bold 50pt;')

            self.buttons[name] = btn
            btn.clicked.connect(partial(self.on_clicked, name))
            btn.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
            lay.addWidget(btn, *position)

    def on_clicked(self, text):
        if text in  map(str, range(0, 10)):
            if len(self.search.text()) == 2:
                self.search.clear()
            self.search.insert(text)
            btn = self.buttons["OK"]
            if len(self.search.text()) == 2:
                btn.setEnabled(True)
                btn.setStyleSheet('background-color: orange; font: bold 50pt;')
                btn.animation.start()
            else:
                btn.setEnabled(False)
                btn.setStyleSheet('background-color: white; font: 50pt;')
                btn.animation.stop()
        elif text == "BACK":
            self.search.backspace()
        elif text == "OK":
            self.okClicked.emit()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.center_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.center_widget)
        self.SearchUI()

    def SearchUI(self):
        page = Page()
        page.okClicked.connect(partial(self.center_widget.setCurrentIndex, 0))
        self.center_widget.addWidget(page)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())