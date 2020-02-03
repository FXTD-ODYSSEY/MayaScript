from PySide2 import QtCore

class Example(QtCore.QObject):
    def __init__(self):
        super(Example,self).__init__()

    @QtCore.Slot()
    def dup(self):
        beep('dup-class')

    @QtCore.Slot(str)
    def beep(self, text):
        print(text)

@QtCore.Slot()
def dup(self):
    beep('dup-local')

@QtCore.Slot(str)
def beep(text):
    print(text)

if __name__ == '__main__':
    QtCore.QMetaObject.invokeMethod(None, 'dup')
    QtCore.QMetaObject.invokeMethod(None, 'beep', QtCore.Qt.AutoConnection, QtCore.QGenericArgument('text', 'beep-local'))

    print('now some classy trials')
    t = Example()
    QtCore.QMetaObject.invokeMethod(t, 'dup')
    QtCore.QMetaObject.invokeMethod(t, 'beep', QtCore.Qt.AutoConnection, QtCore.QGenericArgument('text', 'beep-class'))
    QtCore.QMetaObject.invokeMethod(t, 'beep', QtCore.Qt.AutoConnection, QtCore.QGenericArgument('self', t), QtCore.QGenericArgument('text', 'beep-class-b'))