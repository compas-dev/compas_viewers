"""
********************************************************************************
compas_rv2.scene
********************************************************************************

.. currentmodule:: compas_rv2.scene


.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .scene import Scene

from compas.datastructures import Mesh
from compas_viewers.multimeshviewer import MeshObject

from compas.geometry import Line

from compas_viewers.multimeshviewer import LineObject

Scene.register(Mesh, MeshObject)
Scene.register(Line, LineObject)


__all__ = [name for name in dir() if not name.startswith('_')]
