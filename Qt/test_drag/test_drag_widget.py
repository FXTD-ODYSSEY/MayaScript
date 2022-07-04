from Qt import QtWidgets,QtCore,QtGui

class Tracker(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Tracker, self).__init__(parent)
        self.location = None
        self.label = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setModal(True)
        self.showFullScreen()

    def mouseReleaseEvent(self, e):
        pos = self.mapToGlobal(e.pos())
        self.location = pos.x(), pos.y()
        print("releasing mouse",pos)
        return super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e):
        pos = self.mapToGlobal(e.pos())
        self.label.setText(f"x: {pos.x()}, y: {pos.y()}")
        return super().mouseMoveEvent(e)


def test_emulate_QMouseEvent(qtbot):
    start_pos, end_pos = QtCore.QPoint(300, 300), QtCore.QPoint(400, 300)

    track = Tracker()

    def on_value_changed(value):
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseMove,
            value,
            QtCore.Qt.NoButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        QtCore.QCoreApplication.sendEvent(track, event)

    animation = QtCore.QVariantAnimation(
        startValue=start_pos, endValue=end_pos, duration=5000
    )
    qtbot.mousePress(track, QtCore.Qt.LeftButton, pos=QtCore.QPoint(300, 300))
    animation.valueChanged.connect(on_value_changed)
    with qtbot.waitSignal(animation.finished, timeout=10000):
        animation.start()
    qtbot.mouseRelease(track, QtCore.Qt.LeftButton)
    track.location == (end_pos.x(), end_pos.y())

# if __name__ == "__main__":

#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     window = Tracker()
#     sys.exit(app.exec_())