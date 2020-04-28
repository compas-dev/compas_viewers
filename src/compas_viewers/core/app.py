import sys

from functools import partial

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from compas_viewers.core import ColorButton
from compas_viewers.core import Slider
from compas_viewers.core import TextEdit

from compas_traits import *

__all__ = ['App']


class MainWindow(QtWidgets.QMainWindow):

    def sizeHint(self):
        return QtCore.QSize(1440, 900)


class App(QtWidgets.QApplication):
    """"""

    def __init__(self, settings=None, ui=None, style=None):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.settings = settings or {}
        self.ui = ui or {}
        if style:
            self.setStyleSheet(style)

    def setup(self):
        self.main = MainWindow()
        self.main.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.main.setCentralWidget(self.view)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.center()

    def center(self):
        w = 1440
        h = 900
        self.main.resize(w, h)
        desktop = self.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - w)
        y = 0.5 * (rect.height() - h)
        self.main.setGeometry(x, y, w, h)

    def init(self):
        # self.main.setUnifiedTitleAndToolBarOnMac(True)
        self.init_statusbar()
        # self.init_menubar()
        self.init_toolbar()
        self.init_sidebar()
        self.init_console()

    def show(self):
        self.main.show()
        self.main.raise_()
        self.start()

    def start(self):
        sys.exit(self.exec_())

    # ==========================================================================
    # init
    # ==========================================================================

    def init_statusbar(self):
        self.statusbar = self.main.statusBar()
        self.statusbar.setContentsMargins(0, 0, 0, 0)
        self.statusbar.showMessage('Ready')

    def init_menubar(self):
        if 'menubar' not in self.ui:
            return
        if not self.ui['menubar']:
            return
        self.menubar = self.main.menuBar()
        self.menubar.setContentsMargins(0, 0, 0, 0)
        self.add_menubar_items(self.ui['menubar'], self.menubar, 0)

    def init_toolbar(self):
        if 'toolbar' not in self.ui:
            return
        if not self.ui['toolbar']:
            return
        self.toolbar = self.main.addToolBar('Tools')
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName('Tools')
        self.toolbar.setIconSize(QtCore.QSize(24, 24))
        self.toolbar.setContentsMargins(0, 0, 0, 0)
        self.add_toolbar_items(self.ui['toolbar'], self.toolbar)

    # make this resizable
    # rename this to controls
    # add true sidebar
    def init_sidebar(self):
        if 'sidebar' not in self.ui:
            return
        if not self.ui['sidebar']:
            return
        self.sidebar = QtWidgets.QDockWidget()
        self.sidebar.setObjectName('Sidebar')
        self.sidebar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.sidebar.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.sidebar.setFixedWidth(240)
        self.sidebar.setTitleBarWidget(QtWidgets.QWidget())
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.main.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.sidebar)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)
        self.sidebar.setWidget(widget)
        self.add_sidebar_items(self.ui['sidebar'], layout)
        layout.addStretch()

    # make this into something that can be toggled
    def init_console(self):
        if 'console' not in self.ui:
            return
        self.console = QtWidgets.QDockWidget()
        self.console.setObjectName('Console')
        self.console.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.console.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.console.setFixedHeight(128)
        self.console.setTitleBarWidget(QtWidgets.QWidget())
        self.console.setContentsMargins(0, 0, 0, 0)
        self.main.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.console)
        editor = QtWidgets.QPlainTextEdit()
        editor.setReadOnly(True)
        self.console.setWidget(editor)

    # ==========================================================================
    # add multiple
    # ==========================================================================

    def add_menubar_items(self, items, parent, level):
        if not items:
            return
        for item in items:
            itype = item.get('type', None)
            if itype == 'separator':
                parent.addSeparator()
                continue
            if itype == 'menu':
                menu = parent.addMenu(item['text'])
                if 'items' in item:
                    self.add_menubar_items(item['items'], menu, level + 1)
                continue
            if itype == 'radio':
                radio = QtWidgets.QActionGroup(self.main, exclusive=True)
                for item in item['items']:
                    action = self.add_action(item, parent)
                    action.setCheckable(True)
                    action.setChecked(item['checked'])
                    radio.addAction(action)
                continue
            self.add_action(item, parent)

    def add_toolbar_items(self, items, parent):
        if not items:
            return
        for item in items:
            itype = item.get('type', None)
            if itype == 'separator':
                parent.addSeparator()
                continue
            self.add_action(item, parent)

    def add_sidebar_items(self, items, parent):
        print(items)
        if not items:
            return
        for item in items:
            if isinstance(item, Group):
                self.add_group(item, parent)
            if isinstance(item, Bool):
                self.add_checkbox(item, parent)
            if isinstance(item, Int) or isinstance(item, Float):
                self.add_slider(item, parent)
            # if itype == 'button':
            #     self.add_button(item, parent)
            #     continue
            # if itype == 'colorbutton':
            #     self.add_colorbutton(item, parent)
            #     continue
            if isinstance(item, String):
                self.add_textedit(item, parent)
            if isinstance(item, Empty):
                parent.addStretch()

    # ==========================================================================
    # add one
    # ==========================================================================

    def add_action(self, item, parent):
        text = item['text']
        if item['action']:
            if hasattr(self.controller, item['action']):
                action = getattr(self.controller, item['action'])
                args = item.get('args', None) or []
                kwargs = item.get('kwargs', None) or {}
                if 'image' in item:
                    icon = QtGui.QIcon(item['image'])
                    return parent.addAction(icon, text, partial(action, *args, **kwargs))
                return parent.addAction(text, partial(action, *args, **kwargs))
            if 'image' in item:
                icon = QtGui.QIcon(item['image'])
                return parent.addAction(icon, text)
        return parent.addAction(text)

    def add_group(self, item, parent):
        group = QtWidgets.QGroupBox(item.Name)
        box = QtWidgets.QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(8)
        group.setContentsMargins(0, 0, 0, 0)
        group.setLayout(box)
        parent.addWidget(group)

        self.add_sidebar_items(item.Children, box)

    def add_slider(self, item, parent):
        slider = Slider(item.Name,
                        item.Attributes.get("text", item.Name),
                        item.Value,
                        item.Min,
                        item.Max,
                        item.Step,
                        item.Attributes.get("scale", 1),
                        getattr(self.controller, item.Attributes.get("slide")),
                        getattr(self.controller, item.Attributes.get("edit")))
        parent.addLayout(slider.layout)
        self.controller.controls[slider.name] = slider

    def add_checkbox(self, item, parent):
        checkbox = QtWidgets.QCheckBox(item.Attributes.get("text", item.Name))
        checkbox.setCheckState(QtCore.Qt.Checked if item.Value else QtCore.Qt.Unchecked)
        if item.Attributes.get("action"):
            checkbox.stateChanged.connect(getattr(self.controller, item.Attributes.get("action")))
        parent.addWidget(checkbox)

    def add_button(self, item, parent):
        pass

    def add_textedit(self, item, parent):
        textedit = TextEdit(item.Attributes.get("text", item.Name),
                            item.Value,
                            getattr(self.controller, item.Attributes.get("edit")))
        parent.addLayout(textedit.layout)

    def add_colorbutton(self, item, parent):
        button = ColorButton(item['text'],
                             color=item['value'],
                             size=item.get('size'),
                             action=getattr(self.controller, item.get('action')))
        parent.addLayout(button.layout)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
