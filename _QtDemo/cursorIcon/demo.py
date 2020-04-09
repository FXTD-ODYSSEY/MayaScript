# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 09:24:27'

"""
https://stackoverflow.com/questions/55455881/is-there-a-way-to-create-a-custom-animated-gif-qcursor
"""

from PySide2 import QtCore, QtGui, QtWidgets

class ManagerCursor(QtCore.QObject):
    def __init__(self, parent=None):
        super(ManagerCursor, self).__init__(parent)
        self._movie = None
        self._widget = None
        self._last_cursor = None

    def setMovie(self, movie):
        if isinstance(self._movie, QtGui.QMovie):
            if not self._movie != QtGui.QMovie.NotRunning:
                self._movie.stop()
            del self._movie
        self._movie = movie
        self._movie.frameChanged.connect(self.on_frameChanged)
        self._movie.started.connect(self.on_started)
        self._movie.finished.connect(self.restore_cursor)

    def setWidget(self, widget):
        self._widget = widget

    @QtCore.Slot()
    def on_started(self):
        if self._widget is not None:
            self._last_cursor = self._widget.cursor()

    @QtCore.Slot()
    def restore_cursor(self):
        if self._widget is not None:
            if self._last_cursor is not None:
                self._widget.setCursor(self._last_cursor)
        self._last_cursor = None

    @QtCore.Slot()
    def start(self):
        if self._movie is not None:
            self._movie.start()

    @QtCore.Slot()
    def stop(self):
        if self._movie is not None:
            self._movie.stop()
            self.restore_cursor()

    @QtCore.Slot()
    def on_frameChanged(self):
        pixmap = self._movie.currentPixmap()
        cursor = QtGui.QCursor(pixmap)
        if self._widget is not None:
            if self._last_cursor is None:
                self._last_cursor = self._widget.cursor()
            self._widget.setCursor(cursor)


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        start_btn = QtWidgets.QPushButton("start", clicked=self.on_start)
        stop_btn = QtWidgets.QPushButton("stop", clicked=self.on_stop)

        self._manager = ManagerCursor(self)
        movie = QtGui.QMovie("loading-icon.gif")
        self._manager.setMovie(movie)
        self._manager.setWidget(self)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(start_btn)
        lay.addWidget(stop_btn)
        lay.addStretch()

    @QtCore.Slot()
    def on_start(self):
        self._manager.start()

    @QtCore.Slot()
    def on_stop(self):
        self._manager.stop()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())