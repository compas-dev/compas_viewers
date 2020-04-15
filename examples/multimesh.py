import random

from math import radians

from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_transform_numpy
from compas.utilities import rgb_to_hex
from compas.geometry import Translation
from compas.geometry import Rotation

from compas_viewers.multimeshviewer import MultiMeshViewer
from compas_viewers.multimeshviewer import MeshObject


viewer = MultiMeshViewer()
# make 10 random meshes
# with random position and orientation
for i in range(10):
    T = Translation([random.randint(0, 10), random.randint(0, 10), random.randint(0, 5)])
    R = Rotation.from_axis_and_angle([0, 0, 1.0], radians(random.randint(0, 180)))
    X = T * R
    box = Box.from_width_height_depth(random.randint(1, 3), random.randint(1, 3), random.randint(1, 3))
    mesh = Mesh.from_shape(box)
    mesh_transform_numpy(mesh, X)

    # this is not ideal and should be handled behind the screens
    # meshes.append(MeshObject(mesh, color=rgb_to_hex((210, 210, 210))))
    viewer.add(mesh, settings = {'color': rgb_to_hex((210, 210, 210))})

viewer.update()
viewer.show()
