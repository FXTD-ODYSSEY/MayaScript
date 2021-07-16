# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 11:28:44'

"""
# NOTE https://stackoverflow.com/questions/9957195/updating-gui-elements-in-multithreaded-pyqt
"""

import sys
import urllib2


from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.Signal(object)

    def __init__(self, url):
        QtCore.QThread.__init__(self)
        self.url = url

    def run(self):
        info = urllib2.urlopen(self.url).info()
        self.data_downloaded.emit('%s\n%s' % (self.url, info))


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_widget = QtWidgets.QListWidget()
        self.button = QtWidgets.QPushButton("Start")
        self.button.clicked.connect(self.start_download)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def start_download(self):
        urls = ['http://google.com', 'http://twitter.com', 'http://yandex.ru',
                'http://stackoverflow.com/', 'http://www.youtube.com/']
        self.threads = []
        for url in urls:
            downloader = DownloadThread(url)
            downloader.data_downloaded.connect(self.on_data_ready)
            self.threads.append(downloader)
            downloader.start()

    def on_data_ready(self, data):
        print data
        self.list_widget.addItem(unicode(data))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())