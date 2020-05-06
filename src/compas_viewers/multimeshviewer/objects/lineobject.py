from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView


__all__ = ['LineView', 'LineObject']


class LineObject(PrimitiveObject):

    def __init__(self, scene, primitive, name=None, visible=True, settings={}, **kwargs):
        super(LineObject,self).__init__(scene, primitive, **kwargs)
        self.view = LineView(primitive)

class LineView(PrimitiveView):

    def __init__(self, primitive):
        self._primitive = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.primitive = primitive

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return [0, 1]

    @property
    def faces(self):
        return []

    @property
    def edges(self):
        return [[0, 1]]

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, line):
        self._primitive = line
        xyz = [list(line.start), list(line.end)]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
