# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-14 16:41:31'

"""
CollapsibleWidget
"""

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

class CollapsibleWidget( object ):
    def __init__(self):
        super( CollapsibleWidget, self ).__init__()
        
    @staticmethod
    def install(btn,container,duration=300,expand_callback=None,collapse_callback=None):
        anim = QtCore.QPropertyAnimation(container, "maximumHeight")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(container.sizeHint().height())
        btn.toggleCollapse = False
        btn.setText(u"▼ %s"%btn.text())
        style = btn.styleSheet()
        if 'font:normal' not in style:
            style = style + 'QPushButton {font:normal}' if "{" in style else style + ';font:normal;'
            btn.setStyleSheet(style)
        
        def toggleFn(btn,anim):
            if btn.toggleCollapse:
                btn.toggleCollapse = False
                anim.setEndValue(container.sizeHint().height())
                anim.setDirection(QtCore.QAbstractAnimation.Forward)
                anim.start()
                btn.setText(u"▼%s"%btn.text()[1:])
                style = btn.styleSheet().replace("font:bold","font:normal")
                btn.setStyleSheet(style)
                if expand_callback:
                    expand_callback()
            else:
                btn.toggleCollapse = True
                anim.setDirection(QtCore.QAbstractAnimation.Backward)
                anim.start()
                btn.setText(u"■%s"%btn.text()[1:])
                style = btn.styleSheet().replace("font:normal","font:bold")
                btn.setStyleSheet(style)
                if collapse_callback:
                    collapse_callback()

        func = partial(toggleFn,btn,anim)
        btn.clicked.connect(func)
        return func,anim

class SpliterWidget( object ):
    def __init__(self):
        super( SpliterWidget, self ).__init__()
        
    @staticmethod
    def install(*args,**kwargs):
        direction= kwargs["direction"] if kwargs.has_key("direction") else QtCore.Qt.Horizontal
        width= kwargs["width"] if kwargs.has_key("width") else 100
        height= kwargs["height"] if kwargs.has_key("height") else 200
        
        splitter = QtWidgets.QSplitter(direction)
        splitter.setSizes([width,height])
        parent = args[0].parent()
        for arg in args:
            if not isinstance(arg,QtWidgets.QWidget):
                raise RuntimeError("Please Add widget")
            splitter.addWidget(arg)

        parent.layout().addWidget(splitter)
        return splitter
