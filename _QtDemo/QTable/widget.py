# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-14 11:20:40'

"""
# NOTE https://stackoverflow.com/questions/47139958/pyqt-how-to-insert-a-widget-in-a-qtableview
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    tab = QTableView()
    sti = QStandardItemModel()
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    tab.setModel(sti)
    # tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tab.setIndexWidget(sti.index(0, 3), QPushButton("button"))
    tab.show()
    sys.exit(app.exec_())