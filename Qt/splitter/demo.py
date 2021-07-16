import sys
from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()
                
        self.initUI()
            
    def initUI(self):
        
        hbox = QtWidgets.QHBoxLayout(self)
            
        topleft = QtWidgets.QFrame()
        topleft.setFrameShape(QtWidgets.QFrame.StyledPanel)
        bottom = QtWidgets.QFrame()
        bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
            
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        textedit = QtWidgets.QTextEdit()
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([100,200])
            
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
            
        hbox.addWidget(splitter2)
            
        self.setLayout(hbox)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('windowsvista'))
            
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter demo')
        self.show()
		
def main():
   app = QtWidgets.QApplication(sys.argv)
   ex = Example()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()