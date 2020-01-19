# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-19 15:01:52'

"""
NOTE https://stackoverflow.com/questions/55989245/filling-a-drawn-path-using-qpainterpath-in-pyqt5
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setGeometry(300, 300, 250, 150)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.pixmapItem = (
            QtWidgets.QGraphicsPixmapItem()
        )  # check if everytime you open a new image the old image is still an item
        self.scene().addItem(self.pixmapItem)
        self._path_item = None

    def initial_path(self):
        self._path = QtGui.QPainterPath()
        pen = QtGui.QPen(
            QtGui.QColor("green"), 4, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        )
        self._path_item = self.scene().addPath(self._path, pen)

    @QtCore.pyqtSlot()
    def setImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "select Image", "", "Image Files (*.png *.jpg *jpg *.bmp)"
        )
        if filename:
            self.pixmapItem.setPixmap(QtGui.QPixmap(filename))

    def mousePressEvent(self, event):
        start = event.pos()
        if (
            not self.pixmapItem.pixmap().isNull()
            and event.buttons() & QtCore.Qt.LeftButton
        ):
            self.initial_path()
            self._path.moveTo(self.mapToScene(start))
            self._path_item.setPath(self._path)
        super(GraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (
            not self.pixmapItem.pixmap().isNull()
            and event.buttons() & QtCore.Qt.LeftButton
            and self._path_item is not None
        ):
            self._path.lineTo(self.mapToScene(event.pos()))
            self._path_item.setPath(self._path)
        super(GraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        end = event.pos()
        if (
            not self.pixmapItem.pixmap().isNull()
            and self._path_item is not None
        ):
            self._path.lineTo(self.mapToScene(end))
            self._path.closeSubpath()
            self._path_item.setPath(self._path)
            self._path_item.setBrush(QtGui.QBrush(QtGui.QColor("red")))
            self._path_item.setFlag(
                QtWidgets.QGraphicsItem.ItemIsSelectable, True
            )
            self._path_item = None
        super(GraphicsView, self).mouseReleaseEvent(event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = GraphicsView()
    w.setImage()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())