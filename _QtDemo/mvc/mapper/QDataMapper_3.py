# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 15:04:06'

"""
https://stackoverflow.com/questions/59896135
"""

import os
import sys
MODULE = os.path.join(__file__,"..","..","..","_vendor","Qt")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *

from enum import Enum


class State(Enum):

    foo = 1
    bar = 2
    baz = 3


class StateEdit(QComboBox):

    def __init__(self, parent=None):
        super(StateEdit, self).__init__(parent)
        self.addItems(State._member_names_)

    def state(self):
        print("getter state")
        text = self.currentText()
        return State[text] if text else None

    def setState(self, value):
        print("setter state",value)
        if value is None:
            index = -1
        else:
            index = self.findText(value.name, Qt.MatchExactly)
        self.setCurrentIndex(index)

    state = Property(State, state, setState, user=True)


class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self._name_edit = QLineEdit()
        self._state_edit = StateEdit()
        self._state_button = QPushButton('Change State')

        self._content = QWidget()
        self.setCentralWidget(self._content)

        self._form = QFormLayout()
        self._content.setLayout(self._form)

        self._form.addRow('Name', self._name_edit)
        self._form.addRow('State', self._state_edit)
        self._form.addRow('Action', self._state_button)

        self._state_button.released.connect(self._on_state_button_clicked)

        self._model = QStandardItemModel()
        name_item = QStandardItem()
        state_item = QStandardItem()
        name_item.setText('My Name')
        state_item.setText('')
        state_item.setData(State.bar)
        self._model.appendRow([name_item, state_item])

        self._mapper = QDataWidgetMapper()
        self._mapper.setModel(self._model)
        self._mapper.addMapping(self._name_edit, 0)
        self._mapper.addMapping(self._state_edit, 1, 'state')
        self._mapper.toFirst()

    def _on_state_button_clicked(self):
        self._state_edit.state = State.baz

    def data(self):
        return {
            'name': self._name_edit.text(),
            'state': self._state_edit.state,
        }



if __name__ == "__main__":
    import sys
    from pprint import pprint

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()
    pprint(win.data())