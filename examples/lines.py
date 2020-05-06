import random

from math import radians

from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_transform_numpy
from compas.utilities import rgb_to_hex
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Rotation

from compas_viewers.multimeshviewer import MultiMeshViewer
from compas_viewers.multimeshviewer import MeshObject


viewer = MultiMeshViewer()
# make 10 random meshes
# with random position and orientation
for i in range(10):

    line = Line(
        Point(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)),
        Point(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10))
    )

    # this is not ideal and should be handled behind the screens
    viewer.add(line, settings = {'color': rgb_to_hex((210, 210, 210))})

viewer.update()
viewer.show()
