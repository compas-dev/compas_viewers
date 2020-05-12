from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from compas_viewers.core import App

from compas_viewers.objectviewer import MeshObject
from compas_viewers.objectviewer.view import View
from compas_viewers.objectviewer.controller import Controller

from compas_viewers.objectviewer.settings import SETTINGS
from compas_viewers.objectviewer.ui import UI
from compas_viewers.objectviewer.style import STYLE


__all__ = ['ObjectViewer']


class ObjectTree(QtWidgets.QTreeWidget):

    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(['Objects', 'Properties'])


class Manager(object):

    def __init__(self, parent, app):
        self._items = []
        self.app = app
        self.parent = parent
        self.widget = ObjectTree()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)
        self.parent.setWidget(self.widget)
        self.widget.itemSelectionChanged.connect(self.on_item_selection_changed)

    def set_items(self, nodes):

        sceneitem = QtWidgets.QTreeWidgetItem()
        sceneitem.setText(0, 'scene')
        self.widget.addTopLevelItems([sceneitem])
        sceneitem.setExpanded(True)

        self._items = nodes
        for node in nodes:
            self._add_node_item(node, sceneitem)

    def _add_node_item(self, node, parent):
        nodeitem = QtWidgets.QTreeWidgetItem(parent)
        nodeitem.setText(0, node.__class__.__name__)
        node.widget = nodeitem
        
        for child_node in node.children:
            self._add_node_item(child_node, nodeitem)

    def find_selected_item(self, item):
        index = self.widget.indexFromItem(item)
        trail = []
        while True:
            i = index.row()
            j = index.column()
            if i == -1 and j == -1:
                break
            trail.append((i, j))
            index = index.parent()
        return trail[::-1]

    def on_item_selection_changed(self):
        for item in self.widget.selectedItems():
            trail = self.find_selected_item(item)
            mid = trail[0][0]
            node = self._items[mid]
            if node not in self.app.view.selected:
                self.app.view.selected.add(node)

            # mesh = meshobject.datastructure
            # if len(trail) > 0:
            #     pass
            # if len(trail) > 1:
            #     pass
            # if len(trail) > 2:
            #     if trail[1][0] == 0:
            #         # vertex
            #         key = int(item.text(0))
            #         attr = mesh.vertex_attributes(key)
            #         print("Mesh {}: Vertex {} => {}".format(mid, key, attr))
            #     else:
            #         # edge
            #         key = int(item.text(0))
            #         attr = mesh.edge_attributes(key)
            #         print("Mesh {}: Edge {} => {}".format(mid, key, attr))
        self.app.view.make_buffers()
        self.app.view.updateGL()

class ObjectProperty(QtWidgets.QWidget):
    def start(self):
        self.resize(250, 150)
        self.setWindowTitle('ObjectProperty')
        self.show()

class ObjectViewer(App):
    """"""

    def __init__(self):
        super().__init__(SETTINGS, UI, STYLE)
        self.controller = Controller(self)
        self.view = View(self.controller)
        self.view.camera.events.rotX.connect(self.controller.on_rotX)
        self.view.camera.events.rotZ.connect(self.controller.on_rotZ)
        self.view.camera.events.distance.connect(self.controller.on_distance)

        self.setup()
        self.init()
        self.init_sidebar2()

        self.manager = Manager(self.sidebar2, self)

        self.view.glInit()
        self.view.setup_grid()
        self.view.setup_axes()
        self.view.setFocus()

    def init_sidebar2(self):
        self.sidebar2 = QtWidgets.QDockWidget()
        self.sidebar2.setObjectName('Sidebar')
        self.sidebar2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.sidebar2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.sidebar2.setMinimumWidth(180)
        self.sidebar2.setTitleBarWidget(QtWidgets.QWidget())
        self.sidebar2.setContentsMargins(0, 0, 0, 0)
        self.main.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.sidebar2)

    @property
    def scene(self):
        # TODO: Where is it optimal to put scene ??
        return self.controller.scene

    @scene.setter
    def scene(self, scene):
        self.controller.scene = scene
        # self.controller.center()
        self.update()

    def add(self, mesh, *args, **kwargs):
        self.scene.add(mesh, *args, **kwargs)
        # self._update_items()

    def update(self):
        self.manager.set_items(list(self.controller.scene.traverse(recursive=False)))
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass