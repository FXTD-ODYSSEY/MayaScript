# coding:utf-8
from PySide2 import QtWidgets,QtCore
from PySide2.QtWebKitWidgets import QWebView,QWebSettings

class Browser(QWebView):
    def __init__(self):
        super(Browser,self).__init__()
        self.setWebGL(True)
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)

    def load(self,url):
        self.setUrl(QtCore.QUrl(url))
    
    def adjustTitle(self):
        self.setWindowTitle(self.title())
    
    def setWebGL(self,state=True):
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.WebGLEnabled, state)

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])

    view = Browser()
    # # NOTE 视频无法播放
    # view.load("https://www.bilibili.com/video/av94045683")
    # NOTE 测试 WebGL 是否启动成功
    # view.load("https://get.webgl.org/")
    # view.load("https://blog.l0v0.com/my_work/OPENGL_homework/old_Method/")
    view.load(r"http://editor.l0v0.com/")
    view.show()

    app.exec_()