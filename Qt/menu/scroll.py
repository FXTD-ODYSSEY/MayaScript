# -*- coding: utf-8 -*-
"""
https://www.pythonfixing.com/2021/10/fixed-how-to-have-scrollable-context.html
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-12-04 14:39:02"


from Qt import QtWidgets, QtCore, QtGui
from Qt.QtCompat import isValid

from dayu_widgets.mixin import property_mixin
from dayu_widgets.popup import MPopup
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets import dayu_theme
from functools import partial
import six
import re

@property_mixin
class MMenuSearchBase(object):
    
    
    def search_key_event(self,call,event):
        key = event.key()
        # NOTES: support menu original key event on search bar
        if key in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down,QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
            super(MMenuSearchBase, self).keyPressEvent(event)
        elif key == QtCore.Qt.Key_Tab:
            self.search_bar.setFocus()
        return call(event)
        
    def search(self):
        self.setStyleSheet("QMenu{menu-scrollable: 1;}")
        self.setProperty("search", True)
        self.search_popup = MPopup(self)
        layout = QtWidgets.QVBoxLayout()

        self.search_bar = MLineEdit(self)
        self.search_bar.keyPressEvent = partial(self.search_key_event,self.search_bar.keyPressEvent)
        self.search_bar.setPlaceholderText(self.tr("Search Action..."))
        self.search_bar.textChanged.connect(self.slot_search_change)
        self.search_label = QtWidgets.QLabel(self.tr("Search Action..."))
        self.search_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_bar)
        self.search_popup.setLayout(layout)

        self.aboutToHide.connect(lambda: self.search_bar.setText(""))

    def _set_search(self, value):
        value and self.search()
        
    def _set_search_label(self, value):
        self.property("search") and self.search_label.setText(value)
        
    def _set_search_placeholder(self, value):
        self.property("search") and self.search_bar.setPlaceholderText(value)

    def slot_search_change(self, text):
        search_reg = re.compile(r".*%s.*" % text)
        self._update_search(search_reg)

    def _update_search(self, search_reg, parent_menu=None):
        actions = parent_menu.actions() if parent_menu else self.actions()
        vis_list = []
        for action in actions:
            menu = action.menu()
            if not menu:
                is_match = bool(re.match(search_reg, action.text()))
                action.setVisible(is_match)
                is_match and vis_list.append(action)
            else:
                is_match = bool(re.match(search_reg, menu.title()))
                self._update_search("" if is_match else search_reg, menu)

        if parent_menu:
            parent_menu.menuAction().setVisible(bool(vis_list) or not search_reg)

    def keyPressEvent(self, event):
        print(self.property("search"))
        key = event.key()
        if self.property("search"):
            # NOTES(timmyliang): 26 character trigger search bar
            if 65 <= key <= 90:
                char = chr(key)
                self.search_bar.setText(char)
                self.search_bar.setFocus()
                self.search_bar.selectAll()
                self.search_popup.show()
                width = self.sizeHint().width()
                width = width if width >= 50 else 50
                offset = QtCore.QPoint(width,0)
                self.search_popup.move(self.pos() + offset)
            elif key == QtCore.Qt.Key_Escape:
                self.search_bar.setText("")
                self.search_bar.hide()
        return super(MMenuSearchBase, self).keyPressEvent(event)
    
class ScrollableMenu(MMenuSearchBase,QtWidgets.QMenu):
    deltaY = 0
    dirty = True
    ignoreAutoScroll = False

    def __init__(self, *args, **kwargs):
        maxItemCount = kwargs.pop("maxItemCount", 0)
        super(ScrollableMenu,self).__init__(*args, **kwargs)
        self._maximumHeight = self.maximumHeight()
        self._actionRects = []

        self.scrollTimer = QtCore.QTimer(
            self, interval=50, singleShot=True, timeout=self.checkScroll
        )
        self.scrollTimer.setProperty("defaultInterval", 50)
        self.delayTimer = QtCore.QTimer(self, interval=100, singleShot=True)

        self.setMaxItemCount(maxItemCount)
        self.search()

    @property
    def actionRects(self):
        if self.dirty or not self._actionRects:
            del self._actionRects[:]
            offset = self.offset()
            for action in self.actions():
                geo = super(ScrollableMenu,self).actionGeometry(action)
                if offset:
                    geo.moveTop(geo.y() - offset)
                self._actionRects.append(geo)
            self.dirty = False
        return self._actionRects

    def iterActionRects(self):
        for action, rect in zip(self.actions(), self.actionRects):
            yield action, rect

    def setMaxItemCount(self, count):
        style = self.style()
        opt = QtWidgets.QStyleOptionMenuItem()
        opt.initFrom(self)

        a = QtWidgets.QAction("fake action", self)
        self.initStyleOption(opt, a)
        size = QtCore.QSize()
        fm = self.fontMetrics()
        qfm = opt.fontMetrics
        size.setWidth(
            fm.boundingRect(QtCore.QRect(), QtCore.Qt.TextSingleLine, a.text()).width()
        )
        size.setHeight(max(fm.height(), qfm.height()))
        self.defaultItemHeight = style.sizeFromContents(
            style.CT_MenuItem, opt, size, self
        ).height()

        if not count:
            self.setMaximumHeight(self._maximumHeight)
        else:
            fw = style.pixelMetric(style.PM_MenuPanelWidth, None, self)
            vmargin = style.pixelMetric(style.PM_MenuHMargin, opt, self)
            scrollHeight = self.scrollHeight(style)
            self.setMaximumHeight(
                self.defaultItemHeight * count + (fw + vmargin + scrollHeight) * 2
            )
        self.dirty = True

    def scrollHeight(self, style):
        return style.pixelMetric(style.PM_MenuScrollerHeight, None, self) * 2

    def isScrollable(self):
        return self.height() < super(ScrollableMenu,self).sizeHint().height()

    def checkScroll(self):
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        delta = max(2, int(self.defaultItemHeight * 0.25))
        if self.scrollUpRect.contains(pos):
            delta *= -1
        elif not self.scrollDownRect.contains(pos):
            return
        if self.scrollBy(delta):
            self.scrollTimer.start(self.scrollTimer.property("defaultInterval"))

    def offset(self):
        if self.isScrollable():
            return self.deltaY - self.scrollHeight(self.style())
        return 0

    def translatedActionGeometry(self, action):
        return self.actionRects[self.actions().index(action)]

    def ensureVisible(self, action):
        style = self.style()
        fw = style.pixelMetric(style.PM_MenuPanelWidth, None, self)
        hmargin = style.pixelMetric(style.PM_MenuHMargin, None, self)
        vmargin = style.pixelMetric(style.PM_MenuVMargin, None, self)
        scrollHeight = self.scrollHeight(style)
        extent = fw + hmargin + vmargin + scrollHeight
        r = self.rect().adjusted(0, extent, 0, -extent)
        geo = self.translatedActionGeometry(action)
        if geo.top() < r.top():
            self.scrollBy(-(r.top() - geo.top()))
        elif geo.bottom() > r.bottom():
            self.scrollBy(geo.bottom() - r.bottom())

    def scrollBy(self, step):
        if step < 0:
            newDelta = max(0, self.deltaY + step)
            if newDelta == self.deltaY:
                return False
        elif step > 0:
            newDelta = self.deltaY + step
            style = self.style()
            scrollHeight = self.scrollHeight(style)
            bottom = self.height() - scrollHeight

            for lastAction in reversed(self.actions()):
                if lastAction.isVisible():
                    break
            lastBottom = (
                self.actionGeometry(lastAction).bottom() - newDelta + scrollHeight
            )
            if lastBottom < bottom:
                newDelta -= bottom - lastBottom
            if newDelta == self.deltaY:
                return False

        self.deltaY = newDelta
        self.dirty = True
        self.update()
        return True

    def actionAt(self, pos):
        for action, rect in self.iterActionRects():
            if rect.contains(pos):
                return action

    # class methods reimplementation

    def sizeHint(self):
        hint = super(ScrollableMenu,self).sizeHint()
        if hint.height() > self.maximumHeight():
            hint.setHeight(self.maximumHeight())
        return hint

    def eventFilter(self, source, event):
        if event.type() == event.Show:
            if self.isScrollable() and self.deltaY:
                action = source.menuAction()
                self.ensureVisible(action)
                rect = self.translatedActionGeometry(action)
                delta = rect.topLeft() - self.actionGeometry(action).topLeft()
                source.move(source.pos() + delta)
            return False
        return super(ScrollableMenu,self).eventFilter(source, event)

    def event(self, event):
        if not self.isScrollable():
            return super(ScrollableMenu,self).event(event)
        if event.type() == event.KeyPress and event.key() in (
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
        ):
            res = super(ScrollableMenu,self).event(event)
            action = self.activeAction()
            if action:
                self.ensureVisible(action)
                self.update()
            return res
        elif event.type() in (event.MouseButtonPress, event.MouseButtonDblClick):
            pos = event.pos()
            if self.scrollUpRect.contains(pos) or self.scrollDownRect.contains(pos):
                if event.button() == QtCore.Qt.LeftButton:
                    step = max(2, int(self.defaultItemHeight * 0.25))
                    if self.scrollUpRect.contains(pos):
                        step *= -1
                    self.scrollBy(step)
                    self.scrollTimer.start(200)
                    self.ignoreAutoScroll = True
                return True
        elif event.type() == event.MouseButtonRelease:
            pos = event.pos()
            self.scrollTimer.stop()
            if not (
                self.scrollUpRect.contains(pos) or self.scrollDownRect.contains(pos)
            ):
                action = self.actionAt(pos)
                if action:
                    action.trigger()
                    self.close()
            return True
        return super(ScrollableMenu,self).event(event)

    def timerEvent(self, event):
        if not self.isScrollable():
            # ignore internal timer event for reopening popups
            super(ScrollableMenu,self).timerEvent(event)

    def mouseMoveEvent(self, event):
        if not self.isScrollable():
            super(ScrollableMenu,self).mouseMoveEvent(event)
            return

        pos = event.pos()
        if pos.y() < self.scrollUpRect.bottom() or pos.y() > self.scrollDownRect.top():
            if not self.ignoreAutoScroll and not self.scrollTimer.isActive():
                self.scrollTimer.start(200)
            return
        self.ignoreAutoScroll = False

        oldAction = self.activeAction()
        if not self.rect().contains(pos):
            action = None
        else:
            y = event.y()
            for action, rect in self.iterActionRects():
                if rect.y() <= y <= rect.y() + rect.height():
                    break
            else:
                action = None

        self.setActiveAction(action)
        if action and isValid(action) and not action.isSeparator():

            def ensureVisible():
                self.delayTimer.timeout.disconnect()
                self.ensureVisible(action)

            try:
                self.delayTimer.disconnect()
            except:
                pass
            self.delayTimer.timeout.connect(ensureVisible)
            self.delayTimer.start(150)
        elif oldAction and oldAction.menu() and oldAction.menu().isVisible():

            def closeMenu():
                self.delayTimer.timeout.disconnect()
                oldAction.menu().hide()

            self.delayTimer.timeout.connect(closeMenu)
            self.delayTimer.start(50)
        self.update()

    def wheelEvent(self, event):
        if not self.isScrollable():
            return
        self.delayTimer.stop()
        if event.angleDelta().y() < 0:
            self.scrollBy(self.defaultItemHeight)
        else:
            self.scrollBy(-self.defaultItemHeight)

    def showEvent(self, event):
        if self.isScrollable():
            self.deltaY = 0
            self.dirty = True
            for action in self.actions():
                if action.menu():
                    action.menu().installEventFilter(self)
            self.ignoreAutoScroll = False
        super(ScrollableMenu,self).showEvent(event)

    def hideEvent(self, event):
        for action in self.actions():
            if action.menu():
                action.menu().removeEventFilter(self)
        super(ScrollableMenu,self).hideEvent(event)

    def resizeEvent(self, event):
        super(ScrollableMenu,self).resizeEvent(event)

        style = self.style()
        l, t, r, b = self.getContentsMargins()
        fw = style.pixelMetric(style.PM_MenuPanelWidth, None, self)
        hmargin = style.pixelMetric(style.PM_MenuHMargin, None, self)
        vmargin = style.pixelMetric(style.PM_MenuVMargin, None, self)
        leftMargin = fw + hmargin + l
        topMargin = fw + vmargin + t
        bottomMargin = fw + vmargin + b
        contentWidth = self.width() - (fw + hmargin) * 2 - l - r

        scrollHeight = self.scrollHeight(style)
        self.scrollUpRect = QtCore.QRect(
            leftMargin, topMargin, contentWidth, scrollHeight
        )
        self.scrollDownRect = QtCore.QRect(
            leftMargin,
            self.height() - scrollHeight - bottomMargin,
            contentWidth,
            scrollHeight,
        )

    def paintEvent(self, event):
        if not self.isScrollable():
            super(ScrollableMenu,self).paintEvent(event)
            return

        style = self.style()
        qp = QtGui.QPainter(self)
        rect = self.rect()
        emptyArea = QtGui.QRegion(rect)

        menuOpt = QtWidgets.QStyleOptionMenuItem()
        menuOpt.initFrom(self)
        menuOpt.state = style.State_None
        menuOpt.maxIconWidth = 0
        menuOpt.tabWidth = 0
        style.drawPrimitive(style.PE_PanelMenu, menuOpt, qp, self)

        fw = style.pixelMetric(style.PM_MenuPanelWidth, None, self)

        topEdge = self.scrollUpRect.bottom()
        bottomEdge = self.scrollDownRect.top()
        offset = self.offset()
        qp.save()
        qp.translate(0, -offset)
        # offset translation is required in order to allow correct fade animations
        for action, actionRect in self.iterActionRects():
            actionRect = self.translatedActionGeometry(action)
            if actionRect.bottom() < topEdge:
                continue
            if actionRect.top() > bottomEdge:
                continue

            visible = QtCore.QRect(actionRect)
            if actionRect.bottom() > bottomEdge:
                visible.setBottom(bottomEdge)
            elif actionRect.top() < topEdge:
                visible.setTop(topEdge)
            visible = QtGui.QRegion(visible.translated(0, offset))
            qp.setClipRegion(visible)
            emptyArea -= visible.translated(0, -offset)

            opt = QtWidgets.QStyleOptionMenuItem()
            self.initStyleOption(opt, action)
            opt.rect = actionRect.translated(0, offset)
            style.drawControl(style.CE_MenuItem, opt, qp, self)
        qp.restore()

        cursor = self.mapFromGlobal(QtGui.QCursor.pos())
        upData = (False, self.deltaY > 0, self.scrollUpRect)
        downData = (True, actionRect.bottom() - 2 > bottomEdge, self.scrollDownRect)

        for isDown, enabled, scrollRect in upData, downData:
            qp.setClipRect(scrollRect)

            scrollOpt = QtWidgets.QStyleOptionMenuItem()
            scrollOpt.initFrom(self)
            scrollOpt.state = style.State_None
            scrollOpt.state |= style.State_DownArrow if isDown else style.State_UpArrow
            scrollOpt.checkType = scrollOpt.NotCheckable
            scrollOpt.maxIconWidth = scrollOpt.tabWidth = 0
            scrollOpt.rect = scrollRect
            scrollOpt.menuItemType = scrollOpt.Scroller
            if enabled:
                if scrollRect.contains(cursor):
                    frame = QtWidgets.QStyleOptionMenuItem()
                    frame.initFrom(self)
                    frame.rect = scrollRect
                    frame.state |= style.State_Selected | style.State_Enabled
                    style.drawControl(style.CE_MenuItem, frame, qp, self)

                scrollOpt.state |= style.State_Enabled
                scrollOpt.palette.setCurrentColorGroup(QtGui.QPalette.Active)
            else:
                scrollOpt.palette.setCurrentColorGroup(QtGui.QPalette.Disabled)
            style.drawControl(style.CE_MenuScroller, scrollOpt, qp, self)

        if fw:
            borderReg = QtGui.QRegion()
            borderReg |= QtGui.QRegion(QtCore.QRect(0, 0, fw, self.height()))
            borderReg |= QtGui.QRegion(
                QtCore.QRect(self.width() - fw, 0, fw, self.height())
            )
            borderReg |= QtGui.QRegion(QtCore.QRect(0, 0, self.width(), fw))
            borderReg |= QtGui.QRegion(
                QtCore.QRect(0, self.height() - fw, self.width(), fw)
            )
            qp.setClipRegion(borderReg)
            emptyArea -= borderReg
            frame = QtWidgets.QStyleOptionFrame()
            frame.rect = rect
            frame.palette = self.palette()
            frame.state = QtWidgets.QStyle.State_None
            frame.lineWidth = style.pixelMetric(style.PM_MenuPanelWidth)
            frame.midLineWidth = 0
            style.drawPrimitive(style.PE_FrameMenu, frame, qp, self)

        qp.setClipRegion(emptyArea)
        menuOpt.state = style.State_None
        menuOpt.menuItemType = menuOpt.EmptyArea
        menuOpt.checkType = menuOpt.NotCheckable
        menuOpt.rect = menuOpt.menuRect = rect
        style.drawControl(style.CE_MenuEmptyArea, menuOpt, qp, self)


class Test(QtWidgets.QWidget):
    def __init__(self):
        super(Test,self).__init__()
        self.menu = ScrollableMenu()
        self.menu.setMaxItemCount(10)
        self.menu.addAction("test action")
        for i in range(10):
            self.menu.addAction("Action {}".format(i + 1))
            if i & 1:
                self.menu.addSeparator()
        subMenu = self.menu.addMenu("very long sub menu")
        subMenu.addAction("goodbye")

        self.menu.triggered.connect(self.menuTriggered)

        layout = QtWidgets.QVBoxLayout()
        button = QtWidgets.QPushButton("test")
        button.setMenu(self.menu)
        layout.addWidget(button)
        self.setLayout(layout)
        
    def menuTriggered(self, action):
        print(action.text())

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())


if __name__ == "__main__":
    import sys
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    dayu_theme.apply(app)

    test = Test()
    test.show()
    sys.exit(app.exec_())
