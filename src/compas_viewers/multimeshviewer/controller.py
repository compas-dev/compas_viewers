import os

from functools import partial

from PySide2 import QtCore
from PySide2 import QtWidgets

from OpenGL.GL import *    # noqa: F401 F403
from OpenGL.GLU import *   # noqa: F401 F403
from OpenGL.GLUT import *  # noqa: F401 F403

import compas

from compas.geometry import centroid_points
from compas.utilities import hex_to_rgb
from compas.utilities import flatten

from compas_viewers import core

from .scene import Scene


HERE = os.path.dirname(__file__)


__all__ = ['Controller']


get_obj_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select OBJ file',
    dir=compas.DATA,
    filter='OBJ files (*.obj)'
)

get_stl_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select STL file',
    dir=compas.DATA,
    filter='STL files (*.stl)'
)

get_json_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select JSON file',
    dir=compas.DATA,
    filter='JSON files (*.json)'
)

get_ply_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select PLY file',
    dir=compas.DATA,
    filter='PLY files (*.ply)'
)

hex_to_rgb = partial(hex_to_rgb, normalize=True)


def flist(items):
    return list(flatten(items))


class Controller(core.controller.Controller):

    def __init__(self, app):
        super(Controller, self).__init__(app)
        self._scene = Scene()
        self._colors = []

    @property
    def settings(self):
        return self.app.settings

    @property
    def view(self):
        return self.app.view

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        self._scene = scene

    def center(self):
        # perhaps this should be a bestfit_frame
        # and a frame to frame transformation of all points
        # most certainly use numpy transformations
        xyz = [_xyz for o in self.meshes for _xyz in o.datastructure.get_vertices_attributes('xyz')]
        cx, cy, cz = centroid_points(xyz)
        for o in self.meshes:
            for key, attr in o.datastructure.vertices(True):
                attr['x'] -= cx
                attr['y'] -= cy
                attr['z'] -= cz
            o.view.mesh = o.datastructure

    # ==========================================================================
    # Slots
    # ==========================================================================

    def on_rotX(self, rx):
        slider = self.controls['elevation']
        slider.update(rx)

    def on_rotZ(self, rz):
        slider = self.controls['azimuth']
        slider.update(rz)

    def on_distance(self, d):
        slider = self.controls['distance']
        slider.update(d)

    # ==========================================================================
    # commands
    # ==========================================================================

    def select_command(self):
        pass

    # ==========================================================================
    # constructors
    # ==========================================================================

    # def from_obj(self):
    #     filename, _ = get_obj_file()
    #     if filename:
    #         self.mesh = Mesh.from_obj(filename)
    #         # self.center_mesh()
    #         self.view.make_buffers()
    #         self.view.updateGL()

    # def to_obj(self):
    #     self.message('Export to OBJ is under construction...')

    # def from_json(self):
    #     filename, _ = get_json_file()
    #     if filename:
    #         self.mesh = Mesh.from_json(filename)
    #         self.view.make_buffers()
    #         self.view.updateGL()

    # def to_json(self):
    #     self.message('Export to JSON is under construction...')

    # def from_stl(self):
    #     filename, _ = get_stl_file()
    #     if filename:
    #         self.mesh = Mesh.from_stl(filename)
    #         self.view.make_buffers()
    #         self.view.updateGL()

    # def to_stl(self):
    #     self.message('Export to STL is under construction...')

    # def from_ply(self):
    #     filename, _ = get_ply_file()
    #     if filename:
    #         self.mesh = Mesh.from_ply(filename)
    #         self.view.make_buffers()
    #         self.view.updateGL()

    # def to_ply(self):
    #     self.message('Export to STL is under construction...')

    # def from_polyhedron(self, f):
    #     self.mesh = Mesh.from_polyhedron(f)
    #     self.view.make_buffers()
    #     self.view.updateGL()

    # ==========================================================================
    # view
    # ==========================================================================

    def zoom_extents(self):
        self.message('Zoom Extents is under construction...')

    def zoom_in(self):
        self.view.camera.zoom_in()
        self.view.updateGL()

    def zoom_out(self):
        self.view.camera.zoom_out()
        self.view.updateGL()

    def set_view(self, view):
        self.view.current = view
        self.view.updateGL()

    def capture_image(self):
        result = QtWidgets.QFileDialog.getSaveFileName(caption="File name", dir=HERE)
        if not result:
            return
        filepath = result[0]
        root, ext = os.path.splitext(filepath)
        if not ext:
            return
        self.view.capture(filepath, ext[1:])

    # ==========================================================================
    # appearance
    # ==========================================================================

    def slide_size_vertices(self, value):
        self.settings['vertices.size:value'] = value
        self.view.updateGL()

    def edit_size_vertices(self, value):
        self.settings['vertices.size:value'] = value
        self.view.updateGL()

    def slide_width_edges(self, value):
        self.settings['edges.width:value'] = value
        self.view.updateGL()

    def edit_width_edges(self, value):
        self.settings['edges.width:value'] = value
        self.view.updateGL()

    # ==========================================================================
    # visibility
    # ==========================================================================

    def toggle_faces(self, state):
        self.settings['faces.on'] = state == QtCore.Qt.Checked
        self.view.updateGL()

    def toggle_edges(self, state):
        self.settings['edges.on'] = state == QtCore.Qt.Checked
        self.view.updateGL()

    def toggle_vertices(self, state):
        self.settings['vertices.on'] = state == QtCore.Qt.Checked
        self.view.updateGL()

    # ==========================================================================
    # color
    # ==========================================================================

    def change_vertices_color(self, color):
        self.settings['vertices.color'] = color
        self.view.update_vertex_buffer('vertices.color', self.view.array_vertices_color)
        self.view.updateGL()
        self.app.main.activateWindow()

    def change_edges_color(self, color):
        self.settings['edges.color'] = color
        self.view.update_vertex_buffer('edges.color', self.view.array_edges_color)
        self.view.updateGL()
        self.app.main.activateWindow()

    # ==========================================================================
    # camera
    # ==========================================================================

    def slide_azimuth(self, value):
        self.view.camera.rz = float(value)
        self.view.updateGL()

    def edit_azimuth(self, value):
        pass

    def slide_elevation(self, value):
        self.view.camera.rx = float(value)
        self.view.updateGL()

    def edit_elevation(self, value):
        pass

    def slide_distance(self, value):
        self.view.camera.distance = float(value)
        self.view.updateGL()

    def edit_distance(self, value):
        pass

    def slide_fov(self, value):
        self.view.camera.fov = float(value)
        self.view.updateGL()

    def edit_fov(self, value):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
