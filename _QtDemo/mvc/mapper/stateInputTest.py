# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 17:03:48'

"""

"""

import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt import QtGui,QtWidgets,QtCore
from functools import partial
from collections import OrderedDict

def notify(func):
    def wrapper(self,*args,**kwargs):
        res = func(self,*args,**kwargs)
        if hasattr(self,"STATE"):
            self.STATE.emitDataChanged()
        return res
    return wrapper

class NotifyList(list):
    """
    https://stackoverflow.com/questions/13259179/list-callbacks
    """
    __repr__ = list.__repr__

    def __init__(self,val,STATE):
        super(NotifyList, self).__init__(val)
        self.STATE = STATE

    extend = notify(list.extend)
    append = notify(list.append)
    remove = notify(list.remove)
    pop = notify(list.pop)
    __iadd__ = notify(list.__iadd__)
    __imul__ = notify(list.__imul__)

    #Take care to return a new NotifyList if we slice it.
    if sys.version_info[0] < 3:
        __setslice__ = notify(list.__setslice__)
        __delslice__ = notify(list.__delslice__)
        def __getslice__(self,*args):
            return self.__class__(list.__getslice__(self,*args))

    __delitem__ = notify(list.__delitem__)
    
    def __getitem__(self,item):
        if isinstance(item,slice):
            return self.__class__(list.__getitem__(self,item))
        else:
            return list.__getitem__(self,item)

    @notify
    def __setitem__(self,key,value):
        if isinstance(value, dict):
            value = NotifyDict(value,self.STATE)
        elif isinstance(value, list):
            value = NotifyList(value,self.STATE)
        list.__setitem__(self,key,value)
        
class NotifyDict(OrderedDict):
    """
    https://stackoverflow.com/questions/5186520/python-property-change-listener-pattern
    """
    __repr__ = dict.__repr__
    def __init__(self,val,STATE):
        super(NotifyDict, self).__init__(val)
        self.STATE = STATE

    clear = notify(OrderedDict.clear)
    pop = notify(OrderedDict.pop)
    popitem = notify(OrderedDict.popitem)
    setdefault = notify(OrderedDict.setdefault)
    update =  notify(OrderedDict.update)
    __delitem__ = notify(OrderedDict.__delitem__)

    @notify
    def __setitem__(self,key,value):
        if hasattr(self,"STATE"):
            if isinstance(value, dict):
                value = NotifyDict(value,self.STATE)
            elif isinstance(value, list):
                value = NotifyList(value,self.STATE)
        return OrderedDict.__setitem__(self,key,value)

class State(QtGui.QStandardItem):
    # __repr__ = lambda self: "State(%s)" % self.val.__repr__()
    __repr__ = lambda self: self.val.__repr__()
    # __str__ = lambda self:self.val.__str__(),
    
    operator_list = {
        "__add__"       : lambda self,x:self.val.__add__(x),
        "__sub__"       : lambda self,x:self.val.__sub__(x),
        "__mul__"       : lambda self,x:self.val.__mul__(x),
        "__floordiv__"  : lambda self,x:self.val.__floordiv__(x),
        "__truediv__"   : lambda self,x:self.val.__truediv__(x),
        "__mod__"       : lambda self,x:self.val.__mod__(x),
        "__pow__"       : lambda self,x:self.val.__pow__(x),
        "__lshift__"    : lambda self,x:self.val.__lshift__(x),
        "__rshift__"    : lambda self,x:self.val.__rshift__(x),
        "__and__"       : lambda self,x:self.val.__and__(x),
        "__xor__"       : lambda self,x:self.val.__xor__(x),
        "__or__"        : lambda self,x:self.val.__or__(x),

        "__iadd__"      : lambda self,x:self.val.__iadd__(x),
        "__isub__"      : lambda self,x:self.val.__isub__(x),
        "__imul__"      : lambda self,x:self.val.__imul__(x),
        "__idiv__"      : lambda self,x:self.val.__idiv__(x),
        "__ifloordiv__" : lambda self,x:self.val.__ifloordiv__(x),
        "__imod__"      : lambda self,x:self.val.__imod__(x),
        "__ipow__"      : lambda self,x:self.val.__ipow__(x),
        "__ilshift__"   : lambda self,x:self.val.__ilshift__(x),
        "__irshift__"   : lambda self,x:self.val.__irshift__(x),
        "__iand__"      : lambda self,x:self.val.__iand__(x),
        "__ixor__"      : lambda self,x:self.val.__ixor__(x),
        "__ior__"       : lambda self,x:self.val.__ior__(x),
        
        "__neg__"       : lambda self,x:self.val.__neg__(x),
        "__pos__"       : lambda self,x:self.val.__pos__(x),
        "__abs__"       : lambda self,x:self.val.__abs__(x),
        "__invert__"    : lambda self,x:self.val.__invert__(x),
        "__complex__"   : lambda self,x:self.val.__complex__(x),
        "__int__"       : lambda self,x:self.val.__int__(x),
        "__long__"      : lambda self,x:self.val.__long__(x),
        "__float__"     : lambda self,x:self.val.__float__(x),
        "__oct__"       : lambda self,x:self.val.__oct__(x),
        "__hex__"       : lambda self,x:self.val.__hex__(x),
        
        "__lt__"        : lambda self,x:self.val.__lt__(x),
        "__le__"        : lambda self,x:self.val.__le__(x),
        "__eq__"        : lambda self,x:self.val.__eq__(x),
        "__ne__"        : lambda self,x:self.val.__ne__(x),
        "__ge__"        : lambda self,x:self.val.__ge__(x),
        "__gt__"        : lambda self,x:self.val.__gt__(x),
    }
    def __init__(self,val = None):
        super(State,self).__init__()
        self.val = self.retrieve2Notify(val)
        self.val_type = basestring if type(self.val)  is str or type(self.val)  is unicode else type(self.val) 

        self.__override_attr_list = []
        self.overrideMethod(val)

    def __get__(self, instance, owner):
        return self.val() if callable(self.val) else self.val

    def __set__(self, instance, value):
        self.setVal(value)

    def setVal(self,value):
        if type(value) is not self.val_type and not isinstance(value,self.val_type):
            QtWidgets.QMessageBox.warning(QtWidgets.QApplication.activeWindow(),"warning","dynamic change state type not support")
            return
        self.val = self.retrieve2Notify(value)
        self.overrideMethod(value)
        self.emitDataChanged()

    def overrideMethod(self,val):
        """ sync the val operator and method """
        [delattr(self,attr) for attr in self.__override_attr_list if hasattr(self,attr)]
        self.__override_attr_list = [attr for attr in dir(val) if not attr.startswith("_")]
        for attr in self.__override_attr_list:
            setattr(self,attr,getattr(self.val,attr))
        self.overrideOperator(val)

    @classmethod
    def overrideOperator(cls,val):
        for attr in dir(val):
            func = cls.operator_list.get(attr)
            if func is not None:
                setattr(cls,attr,func)

    def retrieve2Notify(self,val,initialize=True):
        """
        遍历所有字典和数组对象，转换为 Notify 对象
        """
        itr = val.items() if type(val) is dict else enumerate(val) if type(val) is list else []
        for k,v in itr:        
            if isinstance(v, dict):
                self.retrieve2Notify(v,initialize=False)
                val[k] = NotifyDict(v,self)
            elif isinstance(v, list):            
                self.retrieve2Notify(v,initialize=False)
                val[k] = NotifyList(v,self)
        
        if initialize:
            if isinstance(val, dict):
                return NotifyDict(val,self)
            elif isinstance(val, list):
                return NotifyList(val,self)
            else:
                return val
    
    def data(self,role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return str(self.val)

    def setData(self,value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.setVal(value)
            return True            
        return False   

def StateHandler(func):
    def wrapper(self,value,*args, **kwargs):
        if callable(value):
            self.STATE_DICT = {} if not hasattr(self,"STATE_DICT") else self.STATE_DICT
            self.STATE_DICT.setdefault(self.STATE,{})
            callback = self.STATE_DICT.get(self.STATE).get(func)
            self.STATE.model.itemChanged.disconnect(callback) if callback else None
                
            callback = partial(lambda value,state:(func(self,value(),*args, **kwargs)),value)
            self.STATE_DICT[self.STATE][func] = callback
            self.STATE.model.itemChanged.connect(callback)

            value = value()
        res = func(self,value,*args,**kwargs)
        return res
    return wrapper

setattr(QtWidgets.QLabel,"setText",StateHandler(QtWidgets.QLabel.setText))
setattr(QtWidgets.QCheckBox,"setText",StateHandler(QtWidgets.QCheckBox.setText))
setattr(QtWidgets.QLineEdit,"setText",StateHandler(QtWidgets.QLineEdit.setText))
setattr(QtWidgets.QCheckBox,"setChecked",StateHandler(QtWidgets.QCheckBox.setChecked))

class WidgetTest(QtWidgets.QWidget):
    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        class StateDescriptor(object):
            _var_dict = {}
            _var_dict['item'] = State(['a'])
            _var_dict['text'] = State('text')
            _var_dict['enable'] = State(True)
            
            locals().update(_var_dict)

            model = QtGui.QStandardItemModel()
            model.appendRow(_var_dict.values())

            def __init__(self):
                super(StateDescriptor, self).__init__()
                widget_list = [QtWidgets.QLineEdit,QtWidgets.QCheckBox,QtWidgets.QLabel]
                for widget in widget_list:
                    setattr(widget,"STATE",self)

        self.state = StateDescriptor()
        

        self.label = QtWidgets.QLabel(self)
        layout.addWidget(self.label)
        self.line2 = QtWidgets.QLineEdit()
        layout.addWidget(self.line2)
        self.label2 = QtWidgets.QLabel(self)
        layout.addWidget(self.label2)
        self.cb = QtWidgets.QCheckBox(self)
        layout.addWidget(self.cb)
        self.line = QtWidgets.QLineEdit()
        layout.addWidget(self.line)
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()
        layout.addWidget(comboBox)

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        listView.setModel(self.state.model)
        comboBox.setModel(self.state.model)
        tableView.setModel(self.state.model)
        treeView.setModel(self.state.model)

        self.label2.setText(lambda:"%s %s" % (self.state.item,self.state.text))
        self.label.setText(lambda:"%s" % (self.state.item))
        self.cb.setText(lambda:self.state.text)
        self.line.setText(lambda:self.state.text)
        self.line2.setText(lambda:self.state.text)
        self.cb.setText(lambda:"%s %s" % (self.state.item,self.state.text))

        self.cb.setChecked(lambda:self.state.enable)
        
        self.line.textChanged.connect(partial(self.changeText,self.line))
        self.line2.textChanged.connect(partial(self.changeText,self.line2))

        self.button = QtWidgets.QPushButton('click')

        self.button.clicked.connect(lambda : [None for self.state.enable in [not self.state.enable]])
        layout.addWidget(self.button)
        
        # print (self.state._var_dict['item'].valueChanged)
        # mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)
    
    def changeText(self,widget,text):
        pos = widget.property("cursorPosition")
        self.state.text = text
        widget.setProperty("cursorPosition",pos) if pos else None

class WidgetTest2(QtWidgets.QWidget):
    def __init__(self):
        super(WidgetTest2, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        class StateDescriptor(object):
            _var_dict = {}
            _var_dict['label_text'] = State('label_text')
            
            locals().update(_var_dict)

            model = QtGui.QStandardItemModel()
            model.appendRow(_var_dict.values())

            def __init__(self):
                super(StateDescriptor, self).__init__()
                widget_list = [QtWidgets.QLineEdit,QtWidgets.QCheckBox,QtWidgets.QLabel]
                for widget in widget_list:
                    setattr(widget,"STATE",self)

        self.state = StateDescriptor()

        self.label = QtWidgets.QLabel(u"test")
        self.label.setText(lambda:self.state.label_text)

        self.line = QtWidgets.QLineEdit()
        self.line.setText(lambda:self.state.label_text)
        self.line.textChanged.connect(partial(self.changeText,self.line))

        layout.addWidget(self.label)
        layout.addWidget(self.line)

    def changeText(self,widget,text):
        pos = widget.property("cursorPosition")
        self.state.label_text = text
        widget.setProperty("cursorPosition",pos) if pos else None

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    spliter = QtWidgets.QSplitter()
    layout = QtWidgets.QHBoxLayout()
    # container.setLayout(layout)

    widget = WidgetTest()
    widget2 = WidgetTest2()

    widget.label2.setText(lambda:widget2.state.label_text)

    spliter.addWidget(widget)
    spliter.addWidget(widget2)

    spliter.show()
    
    sys.exit(app.exec_())

    