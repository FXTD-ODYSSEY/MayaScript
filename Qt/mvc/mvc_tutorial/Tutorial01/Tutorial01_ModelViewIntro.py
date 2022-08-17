# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-01 22:47:23'

"""

"""
import os
DIR = os.path.dirname(__file__)

import sys
MODULE = os.path.join(DIR,"..","..","..","..","_vendor","Qt")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *



class PaletteListModel(QAbstractListModel):
    
    def __init__(self, colors = [], parent = None):
        QAbstractListModel.__init__(self, parent)
        self.__colors = colors



    def headerData(self, section, orientation, role):
        
        if role == Qt.DisplayRole:
            
            if orientation == Qt.Horizontal:
                return"Palette"
            else:
                return "Color %s" % section

    def rowCount(self, parent):
        return len(self.__colors)


    def data(self, index, role):
        
        
        if role == Qt.EditRole:
            return self.__colors[index.row()].name()
        
        
        if role == Qt.ToolTipRole:
            return "Hex code: " + self.__colors[index.row()].name()
        

        if role == Qt.DecorationRole:
            
            row = index.row()
            value = self.__colors[row]
            
            pixmap = QPixmap(26, 26)
            pixmap.fill(value)
            
            icon = QIcon(pixmap)
            
            return icon

              
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__colors[row]
            
            return value.name() + "asdas"



    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
        
        
    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            
            row = index.row()
            color = QColor(value)
            
            if color.isValid():
                self.__colors[row] = color
                self.dataChanged.emit(index, index)
                return True
        return False


    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#
    def insertRows(self, position, rows, parent = QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            self.__colors.insert(position, QColor("#000000"))
        
        self.endInsertRows()
        
        return True


    
    def removeRows(self, position, rows, parent = QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)
             
        self.endRemoveRows()
        return True






if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle("plastique")

    

    #ALL OF OUR VIEWS
    listView = QListView()
    listView.show()

    treeView = QTreeView()
    treeView.show()

    comboBox = QComboBox()
    comboBox.show()

    tableView = QTableView()
    tableView.show()

    red   = QColor(255,0,0)
    green = QColor(0,255,0)
    blue  = QColor(0,0,255)

    rowCount = 4
    columnCount = 6

    model = PaletteListModel([red, green, blue])
    model.insertRows(0, 1)
    
    listView.setModel(model)
    comboBox.setModel(model)
    tableView.setModel(model)
    treeView.setModel(model)

    button = QPushButton("change")
    def changeOrder():
        pass
    button.clicked.connect(changeOrder)

    button.show()
    
    sys.exit(app.exec_())