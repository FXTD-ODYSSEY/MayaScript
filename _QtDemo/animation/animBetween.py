from PyQt5 import QtCore, QtWidgets

# NOTE https://stackoverflow.com/questions/53402046/pyqt5-how-to-update-qlabel-as-an-animation

class NumLabel(QtWidgets.QLabel):
    def number(self):
        try:
            return int(self.text())
        except:
            return 0
    def setNumber(self, number):
        self.setNum(number)
    number = QtCore.pyqtProperty(int, fget=number, fset=setNumber)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = NumLabel(alignment=QtCore.Qt.AlignCenter)
    w.resize(640, 480)
    animation = QtCore.QPropertyAnimation(w, b'number')
    animation.setStartValue(3)
    animation.setEndValue(0)
    animation.setDuration(1000*(abs(animation.endValue() - animation.startValue())))
    animation.start()
    w.show()
    sys.exit(app.exec_())