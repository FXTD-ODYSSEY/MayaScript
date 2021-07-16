from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from math import sqrt

# NOTE https://stackoverflow.com/questions/55642436/change-scrollhanddrag-form-left-click-to-middle-click-pyqt5

class Point(QGraphicsItem):
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.rectF = QRectF(0, 0, 30, 30)
        self.x=x
        self.y=y
        self._brush = QBrush(Qt.black)

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    def boundingRect(self):
        return self.rectF

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, self._brush)

    def hoverMoveEvent(self, event):
        point = event.pos().toPoint()
        print(point)
        QGraphicsItem.hoverMoveEvent(self, event)


class PhotoViewer(QGraphicsView):
    photoClicked = pyqtSignal(QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.area = float()
        self.setPoints()

    def setItems(self):
            self.data = {'x': [-2414943.8686, -2417160.6592, -2417160.6592, -2417856.1783, -2417054.7618, -2416009.9966, -2416012.5232, -2418160.8952, -2418160.8952, -2416012.5232, -2417094.7694, -2417094.7694], 'y': [10454269.7008,
     10454147.2672, 10454147.2672, 10453285.2456, 10452556.8132, 10453240.2808, 10455255.8752, 10455183.1912, 10455183.1912, 10455255.8752, 10456212.5959, 10456212.5959]}
            maxX = max(self.data['x'])
            minX = min(self.data['x'])
            maxY = max(self.data['y'])
            minY = min(self.data['y'])
            distance = sqrt((maxX-minX)**2+(maxY-minY)**2)

            self.area = QRectF(minX, minY, distance, distance)
            for i,x in enumerate(self.data['x']):
                x = self.data['x'][i]
                y = self.data['y'][i]
                p = Point(x,y)
                p.setPos(x,y)
                self._scene.addItem(p)
            self.setScene(self._scene)



    def fitInView(self, scale=True):
        rect = QRectF(self.area)
        if not rect.isNull():
            self.setSceneRect(rect)

            unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
            self.scale(factor, factor)
            self._zoom = 0

    def setPoints(self):
        self._zoom = 0
        self.setItems()
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.fitInView()

    def wheelEvent(self, event):
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0


    def mousePressEvent(self, event):

        if event.button() == Qt.MidButton:
            self.viewport().setCursor(Qt.ClosedHandCursor)  
            self.original_event = event
            handmade_event = QMouseEvent(QEvent.MouseButtonPress,QPointF(event.pos()),Qt.LeftButton,event.buttons(),Qt.KeyboardModifiers())
            self.mousePressEvent(handmade_event)
            #Im Sure I have to do something here.

        super(PhotoViewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton:
            #for changing back to Qt.OpenHandCursor
            self.viewport().setCursor(Qt.OpenHandCursor)
            handmade_event = QMouseEvent(QEvent.MouseButtonRelease,QPointF(event.pos()),Qt.LeftButton,event.buttons(),Qt.KeyboardModifiers())
            self.mouseReleaseEvent(handmade_event)
        super(PhotoViewer, self).mouseReleaseEvent(event)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        # 'Load image' button
        self.btnLoad = QToolButton(self)
        self.btnLoad.setText('Load Points')
        self.btnLoad.clicked.connect(self.loadPoints)

        VBlayout = QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QHBoxLayout()
        HBlayout.setAlignment(Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)

        VBlayout.addLayout(HBlayout)

    def loadPoints(self):
        self.viewer.setPoints()




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())