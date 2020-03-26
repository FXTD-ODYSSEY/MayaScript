# coding:utf-8
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEngineSettings as QWebSettings

class Browser(QWebView):
    def __init__(self):
        super(Browser,self).__init__()
        # self.setWebGL(True)
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
    # NOTE 测试 WebGL 是否启动成功
    view.load("https://get.webgl.org/")
    # view.load("https://webglreport.com/?v=2")


    # NOTE 编辑器测试
    # view.load(r"https://threejs.org/editor/")
    # view.load(r"http://editor.l0v0.com/")
    # # NOTE 图片加载尝试
    # view.load(r"file:///D:/Users/82047/Desktop/img/chapter1-intro.mp4_20190928_094236.865.png")
    # view.load("https://blog.l0v0.com/my_work/OPENGL_homework/old_Method/")
    view.show()
    app.exec_()