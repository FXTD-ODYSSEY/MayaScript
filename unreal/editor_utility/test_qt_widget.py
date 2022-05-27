from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
from Qt.QtTest import QTest
from dayu_widgets.qt import application


class SuperButton(QtWidgets.QPushButton):
    def mousePressEvent(self, event):
        print("press")
        return super(SuperButton, self).mousePressEvent(event)


class SuperListWidget(QtWidgets.QListWidget):
    def wheelEvent(self, event):
        print("wheelEvent")
        # print(event.angleDelta())
        # print(event.pixelDelta())
        # print(event.orientation())
        # print(event.buttons()== QtCore.Qt.NoButton)
        # print(event.modifiers() == QtCore.Qt.NoModifier)
        return super(SuperListWidget, self).wheelEvent(event)


class SuperWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SuperWindow, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.button = SuperButton()
        self.button.setText("hello")
        self.button.clicked.connect(lambda: print("hello world"))
        layout.addWidget(self.button)

        list_widget = SuperListWidget()
        for i in range(20):
            list_widget.addItem("item {0}".format(i))
        layout.addWidget(list_widget)
        self.list_widget = list_widget

        button = QtWidgets.QPushButton()
        button.setText("simulate click")
        button.clicked.connect(self.simulate_click)
        layout.addWidget(button)

    def simulate_click(self):
        print("simulate_click")
        screen_pos = QtGui.QCursor.pos()
        screen_pos -= QtCore.QPoint(0, 30)
        QtGui.QCursor.setPos(screen_pos)

        local_pos = self.list_widget.mapFromGlobal(screen_pos)
        event = QtGui.QWheelEvent(
            local_pos,
            # QtCore.QPointF(local_pos),
            # QtCore.QPointF(screen_pos),
            # QtCore.QPoint(0, -120),
            # QtCore.QPoint(0, 0),
            -120,
            QtCore.Qt.NoButton,
            QtCore.Qt.NoModifier,
            QtCore.Qt.Vertical,
        )
        # self.list_widget.wheelEvent(event)
        QtWidgets.QApplication.postEvent(self.list_widget, event)

    def mousePressEvent(self, event):
        # widget = QtWidgets.QApplication.widgetAt(QtGui.QCursor.pos())
        # print(widget.text())
        # print(event.localPos())
        # print(QtGui.QCursor.pos())
        return super(SuperWindow, self).mousePressEvent(event)


def main():
    with application():
        window = SuperWindow()
        window.show()


if __name__ == "__main__":
    main()
