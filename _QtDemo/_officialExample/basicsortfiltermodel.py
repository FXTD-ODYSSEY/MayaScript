# -*- coding: utf-8 -*-
"""
https://doc.qt.io/qtforpython/examples/example_widgets_itemviews_basicfiltermodel.html?highlight=sort
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-06-28 13:23:37'


import sys
from PySide2.QtCore import (QDate, QDateTime, QRegularExpression,
                            QSortFilterProxyModel, QTime, Qt)
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QTreeView, QVBoxLayout, QWidget)


REGULAR_EXPRESSION = 0
WILDCARD = 1
FIXED_STRING = 2


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._proxy_model = QSortFilterProxyModel()
        self._proxy_model.setDynamicSortFilter(True)

        self._source_group_box = QGroupBox("Original Model")
        self._proxy_group_box = QGroupBox("Sorted/Filtered Model")

        self._source_view = QTreeView()
        self._source_view.setRootIsDecorated(False)
        self._source_view.setAlternatingRowColors(True)

        self._proxy_view = QTreeView()
        self._proxy_view.setRootIsDecorated(False)
        self._proxy_view.setAlternatingRowColors(True)
        self._proxy_view.setModel(self._proxy_model)
        self._proxy_view.setSortingEnabled(True)

        self._sort_case_sensitivity_check_box = QCheckBox("Case sensitive sorting")
        self._filter_case_sensitivity_check_box = QCheckBox("Case sensitive filter")

        self._filter_pattern_line_edit = QLineEdit()
        self._filter_pattern_line_edit.setClearButtonEnabled(True)
        self._filter_pattern_label = QLabel("&Filter pattern:")
        self._filter_pattern_label.setBuddy(self._filter_pattern_line_edit)

        self._filter_syntax_combo_box = QComboBox()
        self._filter_syntax_combo_box.addItem("Regular expression",
                                          REGULAR_EXPRESSION)
        self._filter_syntax_combo_box.addItem("Wildcard",
                                          WILDCARD)
        self._filter_syntax_combo_box.addItem("Fixed string",
                                          FIXED_STRING)
        self._filter_syntax_label = QLabel("Filter &syntax:")
        self._filter_syntax_label.setBuddy(self._filter_syntax_combo_box)

        self._filter_column_combo_box = QComboBox()
        self._filter_column_combo_box.addItem("Subject")
        self._filter_column_combo_box.addItem("Sender")
        self._filter_column_combo_box.addItem("Date")
        self._filter_column_label = QLabel("Filter &column:")
        self._filter_column_label.setBuddy(self._filter_column_combo_box)

        self._filter_pattern_line_edit.textChanged.connect(self.filter_reg_exp_changed)
        self._filter_syntax_combo_box.currentIndexChanged.connect(self.filter_reg_exp_changed)
        self._filter_column_combo_box.currentIndexChanged.connect(self.filter_column_changed)
        self._filter_case_sensitivity_check_box.toggled.connect(self.filter_reg_exp_changed)
        self._sort_case_sensitivity_check_box.toggled.connect(self.sort_changed)

        source_layout = QHBoxLayout()
        source_layout.addWidget(self._source_view)
        self._source_group_box.setLayout(source_layout)

        proxy_layout = QGridLayout()
        proxy_layout.addWidget(self._proxy_view, 0, 0, 1, 3)
        proxy_layout.addWidget(self._filter_pattern_label, 1, 0)
        proxy_layout.addWidget(self._filter_pattern_line_edit, 1, 1, 1, 2)
        proxy_layout.addWidget(self._filter_syntax_label, 2, 0)
        proxy_layout.addWidget(self._filter_syntax_combo_box, 2, 1, 1, 2)
        proxy_layout.addWidget(self._filter_column_label, 3, 0)
        proxy_layout.addWidget(self._filter_column_combo_box, 3, 1, 1, 2)
        proxy_layout.addWidget(self._filter_case_sensitivity_check_box, 4, 0, 1, 2)
        proxy_layout.addWidget(self._sort_case_sensitivity_check_box, 4, 2)
        self._proxy_group_box.setLayout(proxy_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._source_group_box)
        main_layout.addWidget(self._proxy_group_box)
        self.setLayout(main_layout)

        self.setWindowTitle("Basic Sort/Filter Model")
        self.resize(500, 450)

        self._proxy_view.sortByColumn(1, Qt.AscendingOrder)
        self._filter_column_combo_box.setCurrentIndex(1)

        self._filter_pattern_line_edit.setText("Andy|Grace")
        self._filter_case_sensitivity_check_box.setChecked(True)
        self._sort_case_sensitivity_check_box.setChecked(True)

    def set_source_model(self, model):
        self._proxy_model.setSourceModel(model)
        self._source_view.setModel(model)

    def filter_reg_exp_changed(self):
        syntax_nr = self._filter_syntax_combo_box.currentData()
        pattern = self._filter_pattern_line_edit.text()
        if syntax_nr == WILDCARD:
            pattern = QRegularExpression.wildcardToRegularExpression(pattern)
        elif syntax_nr == FIXED_STRING:
            pattern = QRegularExpression.escape(pattern)

        reg_exp = QRegularExpression(pattern)
        if not self._filter_case_sensitivity_check_box.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self._proxy_model.setFilterRegularExpression(reg_exp)

    def filter_column_changed(self):
        self._proxy_model.setFilterKeyColumn(self._filter_column_combo_box.currentIndex())

    def sort_changed(self):
        if self._sort_case_sensitivity_check_box.isChecked():
            case_sensitivity = Qt.CaseSensitive
        else:
            case_sensitivity = Qt.CaseInsensitive

        self._proxy_model.setSortCaseSensitivity(case_sensitivity)


def add_mail(model, subject, sender, date):
    model.insertRow(0)
    model.setData(model.index(0, 0), subject)
    model.setData(model.index(0, 1), sender)
    model.setData(model.index(0, 2), date)


def create_mail_model(parent):
    model = QStandardItemModel(0, 3, parent)

    model.setHeaderData(0, Qt.Horizontal, "Subject")
    model.setHeaderData(1, Qt.Horizontal, "Sender")
    model.setHeaderData(2, Qt.Horizontal, "Date")

    add_mail(model, "Happy New Year!", "Grace K. <grace@software-inc.com>",
            QDateTime(QDate(2006, 12, 31), QTime(17, 3)))
    add_mail(model, "Radically new concept", "Grace K. <grace@software-inc.com>",
            QDateTime(QDate(2006, 12, 22), QTime(9, 44)))
    add_mail(model, "Accounts", "pascale@nospam.com",
            QDateTime(QDate(2006, 12, 31), QTime(12, 50)))
    add_mail(model, "Expenses", "Joe Bloggs <joe@bloggs.com>",
            QDateTime(QDate(2006, 12, 25), QTime(11, 39)))
    add_mail(model, "Re: Expenses", "Andy <andy@nospam.com>",
            QDateTime(QDate(2007, 1, 2), QTime(16, 5)))
    add_mail(model, "Re: Accounts", "Joe Bloggs <joe@bloggs.com>",
            QDateTime(QDate(2007, 1, 3), QTime(14, 18)))
    add_mail(model, "Re: Accounts", "Andy <andy@nospam.com>",
            QDateTime(QDate(2007, 1, 3), QTime(14, 26)))
    add_mail(model, "Sports", "Linda Smith <linda.smith@nospam.com>",
            QDateTime(QDate(2007, 1, 5), QTime(11, 33)))
    add_mail(model, "AW: Sports", "Rolf Newschweinstein <rolfn@nospam.com>",
            QDateTime(QDate(2007, 1, 5), QTime(12, 0)))
    add_mail(model, "RE: Sports", "Petra Schmidt <petras@nospam.com>",
            QDateTime(QDate(2007, 1, 5), QTime(12, 1)))

    return model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.set_source_model(create_mail_model(window))
    window.show()
    sys.exit(app.exec_())