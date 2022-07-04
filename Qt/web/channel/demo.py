
import sys
from PySide2.QtCore import pyqtSlot
from PySide2.QtWidgets import QApplication
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
 
html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>        
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
    var backend;
    new QWebChannel(qt.webChannelTransport, function (channel) {
        backend = channel.objects.backend;
    });
    document.getElementById("header").addEventListener("click", function(){
        backend.foo();
    });
    </script>
</head>
<body> <h2 id="header">Header.</h2> </body>
</html>
'''
 
class HelloWorldHtmlApp(QWebEngineView):
 
    def __init__(self):
        super().__init__()
 
        # setup a page with my html
        my_page = QWebEnginePage(self)
        my_page.setHtml(html)
        self.setPage(my_page)
 
        # setup channel
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self)
        self.page().setWebChannel(self.channel)
        self.show()
 
    @pyqtSlot()
    def foo(self):
        print('bar')
 
 
view = HelloWorldHtmlApp()

