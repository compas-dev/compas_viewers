from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise


__all__ = ['PrimitiveView', 'PrimitiveObject']


class PrimitiveObject(object):

    def __init__(self, scene, primitive, name=None, visible=True, settings={}, **kwargs):
        self.scene = scene
        self.primitive = primitive
        self.name = name
        self.guid = None
        self.visible = visible
        # self.artist = None
        self.view = PrimitiveView(primitive)
        self._settings = {}
        self._settings.update(settings)


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        return self._settings.update(settings)



class PrimitiveView(object):

    def __init__(self, primitive):
        self._primitive = None
        self.primitive = primitive

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, primitive):
        self._primitive = primitive


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
