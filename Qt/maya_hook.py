import inspect
from Qt import QtWidgets,QtGui,QtCore

class EventHander(QtCore.QObject):
    
    handled = QtCore.Signal(QtCore.QObject,QtCore.QEvent)
    
    def __init__(self):
        super(EventHander,self).__init__()
        self.app = QtWidgets.QApplication.instance()
        self.install()
        
    def install(self):
        self.app.installEventFilter(self)
        
    def uninstall(self):
        self.app.removeEventFilter(self)

    # def __del__(self):
    #     self.uninstall()
    #     super(EventHander,self).__del__()

    def eventFilter(self, reciever, event):
        self.handled.emit(reciever,event)
        return super(EventHander,self).eventFilter(reciever, event)
    
handler = EventHander()

def hook(reciever,event):
    event_type = event.type()
    # if event_type == QtCore.QEvent.MouseButtonPress or event_type == QtCore.QEvent.MetaCall:

    if event_type == QtCore.QEvent.MouseButtonPress:
        handler.uninstall()
        import pdb
        pdb.set_trace()
        print(reciever.objectName(),reciever)
        # print(reciever,type(event))
        # if isinstance(reciever,QtCore.QObject):
        # if isinstance(reciever,QtWidgets.QPushButton):
            
            # meta = reciever.metaObject()
            # method_list = []
            # for i in range(meta.methodCount()):
            #     method = meta.method(i)
            #     if method.methodType() == QtCore.QMetaMethod.Slot:
            #         method_list.append(method.methodSignature())
                
            # print(reciever,method_list)



handler.handled.connect(hook)

import sys

def hook(frame, event, arg):
    if event == 'call':
        code = frame.f_code
        if code.co_filename.
        startswith('<') and code.co_filename.endswith('>'):
            print(code.co_filename,frame.f_lineno)

sys.setprofile(hook)
# sys.setprofile(None)



# handler.uninstall()

# print(dir(handler))

# ['AncestorMode', 'AutomaticVisibility', 'ExcludeTransients', 'FullScreen', 'Hidden', 'IncludeTransients', 'Maximized', 'Minimized', 'Offscreen', 'OpenGLSurface', 'RasterGLSurface', 'RasterSurface', 'SurfaceClass', 'SurfaceType', 'Visibility', 'Window', 'Windowed', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'accessibleRoot', 'activeChanged', 'alert', 'baseSize', 'blockSignals', 'childEvent', 'children', 'close', 'connect', 'connectNotify', 'contentOrientation', 'contentOrientationChanged', 'create', 'cursor', 'customEvent', 'deleteLater', 'destroy', 'destroyed', 'devicePixelRatio', 'disconnect', 'disconnectNotify', 'dumpObjectInfo', 'dumpObjectTree', 'dynamicPropertyNames', 'emit', 'event', 'eventFilter', 'exposeEvent', 'filePath', 'findChild', 'findChildren', 'flags', 'focusInEvent', 'focusObject', 'focusObjectChanged', 'focusOutEvent', 'format', 'frameGeometry', 'frameMargins', 'framePosition', 'fromWinId', 'geometry', 'height', 'heightChanged', 'hide', 'hideEvent', 'icon', 'inherits', 'installEventFilter', 'isActive', 'isAncestorOf', 'isExposed', 'isModal', 'isSignalConnected', 'isTopLevel', 'isVisible', 'isWidgetType', 'isWindowType', 'keyPressEvent', 'keyReleaseEvent', 'killTimer', 'lower', 'm_type', 'mapFromGlobal', 'mapToGlobal', 'mask', 'maximumHeight', 'maximumHeightChanged', 'maximumSize', 'maximumWidth', 'maximumWidthChanged', 'metaObject', 'minimumHeight', 'minimumHeightChanged', 'minimumSize', 'minimumWidth', 'minimumWidthChanged', 'modality', 'modalityChanged', 'mouseDoubleClickEvent', 'mouseMoveEvent', 'mousePressEvent', 'mouseReleaseEvent', 'moveEvent', 'moveToThread', 'objectName', 'objectNameChanged', 'opacity', 'opacityChanged', 'parent', 'position', 'property', 'raise', 'receivers', 'registerUserData', 'removeEventFilter', 'reportContentOrientationChange', 'requestActivate', 'requestUpdate', 'requestedFormat', 'resize', 'resizeEvent', 'screen', 'screenChanged', 'sender', 'senderSignalIndex', 'setBaseSize', 'setCursor', 'setFilePath', 'setFlags', 'setFormat', 'setFramePosition', 'setGeometry', 'setHeight', 'setIcon', 'setKeyboardGrabEnabled', 'setMask', 'setMaximumHeight', 'setMaximumSize', 'setMaximumWidth', 'setMinimumHeight', 'setMinimumSize', 'setMinimumWidth', 'setModality', 'setMouseGrabEnabled', 'setObjectName', 'setOpacity', 'setParent', 'setPosition', 'setProperty', 'setScreen', 'setSizeIncrement', 'setSurfaceType', 'setTitle', 'setTransientParent', 'setVisibility', 'setVisible', 'setWidth', 'setWindowState', 'setX', 'setY', 'show', 'showEvent', 'showFullScreen', 'showMaximized', 'showMinimized', 'showNormal', 'signalsBlocked', 'size', 'sizeIncrement', 'startTimer', 'staticMetaObject', 'supportsOpenGL', 'surfaceClass', 'surfaceHandle', 'surfaceType', 'tabletEvent', 'thread', 'timerEvent', 'title', 'touchEvent', 'tr', 'transientParent', 'type', 'unsetCursor', 'visibility', 'visibilityChanged', 'visibleChanged', 'wheelEvent', 'width', 'widthChanged', 'winId', 'windowState', 'windowStateChanged', 'windowTitleChanged', 'x', 'xChanged', 'y', 'yChanged']

