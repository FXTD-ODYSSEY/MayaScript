# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:50:25'

"""
设置自定义的键盘触发事件
通过传入的 event.modifiers 还可以配合 辅助按键来触发不同的点击事件
"""
import sys
from functools import partial
from Qt import QtCore, QtGui, QtWidgets

# NOTE replaceWidget ----------------------------------------------------------------------------

def replaceWidget(src,dst):
    u"""replaceWidget 替换组件
    
    Parameters
    ----------
    src : QWidget
        源组件
    dst : QWidget
        目标组件
    
    Returns
    -------
    QWidget
        [description]
    """
    updateWidgetState(src,dst)
    layout = src.parent().layout()
    layout,index = getTargetLayoutIndex(layout,src)
    if not layout:
        print (u"没有找到 %s 的 Layout，替换失败" % src)
        return src

    layout.insertWidget(index,dst)
    src.setParent(None)
    
    return dst

def updateWidgetState(src,dst):
    u"""updateWidgetState 同步组件状态
    
    Parameters
    ----------
    src : QWidget
        源组件
    dst : QWidget
        目标组件
    """
    if src.acceptDrops()           : dst.setAcceptDrops(src.acceptDrops())
    if src.accessibleDescription() : dst.setAccessibleDescription(src.accessibleDescription())
    if src.backgroundRole()        : dst.setBackgroundRole(src.backgroundRole())
    if src.baseSize()              : dst.setBaseSize(src.baseSize())
    if src.contentsMargins()       : dst.setContentsMargins(src.contentsMargins())
    if src.contextMenuPolicy()     : dst.setContextMenuPolicy(src.contextMenuPolicy())
    if src.cursor()                : dst.setCursor(src.cursor())
    if src.focusPolicy()           : dst.setFocusPolicy(src.focusPolicy())
    if src.focusProxy()            : dst.setFocusProxy(src.focusProxy())
    if src.font()                  : dst.setFont(src.font())
    if src.foregroundRole()        : dst.setForegroundRole(src.foregroundRole())
    if src.geometry()              : dst.setGeometry(src.geometry())
    if src.inputMethodHints()      : dst.setInputMethodHints(src.inputMethodHints())
    if src.layout()                : dst.setLayout(src.layout())
    if src.layoutDirection()       : dst.setLayoutDirection(src.layoutDirection())
    if src.locale()                : dst.setLocale(src.locale())
    if src.mask()                  : dst.setMask(src.mask())
    if src.maximumSize()           : dst.setMaximumSize(src.maximumSize())
    if src.minimumSize()           : dst.setMinimumSize(src.minimumSize())
    if src.hasMouseTracking ()     : dst.setMouseTracking(src.hasMouseTracking ())
    if src.palette()               : dst.setPalette(src.palette())
    if src.parent()                : dst.setParent(src.parent())
    if src.sizeIncrement()         : dst.setSizeIncrement(src.sizeIncrement())
    if src.sizePolicy()            : dst.setSizePolicy(src.sizePolicy())
    if src.statusTip()             : dst.setStatusTip(src.statusTip())
    if src.style()                 : dst.setStyle(src.style())
    if src.toolTip()               : dst.setToolTip(src.toolTip())
    if src.updatesEnabled()        : dst.setUpdatesEnabled(src.updatesEnabled())
    if src.whatsThis()             : dst.setWhatsThis(src.whatsThis())
    if src.windowFilePath()        : dst.setWindowFilePath(src.windowFilePath())
    if src.windowFlags()           : dst.setWindowFlags(src.windowFlags())
    if src.windowIcon()            : dst.setWindowIcon(src.windowIcon())
    if src.windowIconText()        : dst.setWindowIconText(src.windowIconText())
    if src.windowModality()        : dst.setWindowModality(src.windowModality())
    if src.windowOpacity()         : dst.setWindowOpacity(src.windowOpacity())
    if src.windowRole()            : dst.setWindowRole(src.windowRole())
    if src.windowState()           : dst.setWindowState(src.windowState())


def getTargetLayoutIndex(layout,target):
    u"""getTargetLayoutIndex 获取目标 Layout 和 序号
    
    Parameters
    ----------
    layout : QLayout 
        通过 QLayout 递归遍历下属的组件
    target : QWidget
        要查询的组件
    
    Returns
    -------
    layout : QLayout
        查询组件所在的 Layout
    i : int
        查询组件所在的 Layout 的序号
    """
    count = layout.count()
    for i in range(count):
        item = layout.itemAt(i).widget()
        if item == target:
            return layout,i
    else:
        for child in layout.children():
            layout,i = getTargetLayoutIndex(child,target)
            if layout:
                return layout,i
        return [None,None]
        
class ICompleterComboBox( QtWidgets.QComboBox ):
    def __init__( self,  parent = None):
        super( ICompleterComboBox, self ).__init__( parent )

        self.setFocusPolicy( QtCore.Qt.StrongFocus )
        self.setEditable( True )
        self.completer = QtWidgets.QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QtWidgets.QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QtCore.QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( QtCore.Qt.CaseInsensitive )
        self.pFilterModel.setSourceModel( QtGui.QStandardItemModel() )

        self.completer.setPopup( self.view() )

        self.setCompleter( self.completer )

        edit = self.lineEdit()
        # NOTE 取消按 Enter 生成新 item 的功能
        edit.returnPressed.disconnect()
        edit.textEdited[unicode].connect( self.pFilterModel.setFilterFixedString )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def clear(self):
        self.pFilterModel.setSourceModel( QtGui.QStandardItemModel() )
        super(ICompleterComboBox,self).clear()

    def addItems(self,texts):
        super(ICompleterComboBox,self).addItems(texts)
        for text in texts:
            self.addItem(text)

    def addItem(self,*args):
        super(ICompleterComboBox,self).addItem(*args)
        if len(args) == 2:
            _,text = args
        else:
            text = args[0]
        
        model = self.pFilterModel.sourceModel()
        
        item = QtGui.QStandardItem(text)
        model.setItem(model.rowCount(), item)

        if self.completer.model() != self.pFilterModel:
            self.completer.setModel(self.pFilterModel)


    def setModel( self, model ):
        super(ICompleterComboBox, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ICompleterComboBox, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)

class IMouseClickSignal(QtCore.QObject):
    """IMouseClickSignal 监听鼠标点击信号
    """
    
    # NOTE 点击事件
    LClicked   = QtCore.Signal(QtCore.QEvent)
    DLClicked  = QtCore.Signal(QtCore.QEvent)
    MClicked   = QtCore.Signal(QtCore.QEvent)
    DMClicked  = QtCore.Signal(QtCore.QEvent)
    RClicked   = QtCore.Signal(QtCore.QEvent)
    DRClicked  = QtCore.Signal(QtCore.QEvent)
    X1Clicked  = QtCore.Signal(QtCore.QEvent)
    DX1Clicked = QtCore.Signal(QtCore.QEvent)
    X2Clicked  = QtCore.Signal(QtCore.QEvent)
    DX2Clicked = QtCore.Signal(QtCore.QEvent)

    # NOTE 松开事件
    LReleased  = QtCore.Signal(QtCore.QEvent)
    MReleased  = QtCore.Signal(QtCore.QEvent)
    RReleased  = QtCore.Signal(QtCore.QEvent)
    X1Released = QtCore.Signal(QtCore.QEvent)
    X2Released = QtCore.Signal(QtCore.QEvent)

    def __init__(self,widget):
        super(IMouseClickSignal,self).__init__()
        self.setParent(widget)

        self.releaseSingal = {
            QtCore.Qt.LeftButton:self.LReleased.emit,
            QtCore.Qt.MidButton:self.MReleased.emit,
            QtCore.Qt.RightButton:self.RReleased.emit,
            QtCore.Qt.XButton1:self.X1Released.emit,
            QtCore.Qt.XButton2:self.X2Released.emit,
        }
        
        self.clickSingal = {
            QtCore.Qt.LeftButton:self.LClicked.emit,
            QtCore.Qt.MidButton:self.MClicked.emit,
            QtCore.Qt.RightButton:self.RClicked.emit,
            QtCore.Qt.XButton1:self.X1Clicked.emit,
            QtCore.Qt.XButton2:self.X2Clicked.emit,
        }

        self.DbClickSingal = {
            QtCore.Qt.LeftButton:self.DLClicked.emit,
            QtCore.Qt.MidButton:self.DMClicked.emit,
            QtCore.Qt.RightButton:self.DRClicked.emit,
            QtCore.Qt.XButton1:self.DX1Clicked.emit,
            QtCore.Qt.XButton2:self.DX2Clicked.emit,
        }

        widget.installEventFilter(self)

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.clickSingal.get(event.button())(event)
        elif event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
            self.DbClickSingal.get(event.button())(event)
        elif event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            self.releaseSingal.get(event.button())(event)
        return False
