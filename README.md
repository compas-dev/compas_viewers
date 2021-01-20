# DEPRECATED: COMPAS viewers

THIS PACKAGE IS DEPRECATED IN FAVOUR OF compas_view2

---

Standalone viewers for COMPAS based on PySide2 and PyOpenGL.

The package provides base functionality for making viewers and minimal CAD-style applications.
It also implements this base functionality in the following pre-configured viewers/apps:

* `MeshViewer`: A viewer for individual COMPAS meshes.
* `MultiMeshViewer`: A viewer for multiple mesh objects with a first draft of an object manager for selecting and working with individual mesh objects.

The goal is to provide an environment for testing and prototyping code for 3D applications without restrictions on functionality due to limited availability of Python packages or external libraries (as for example in IronPython), and without the need for integration in CAD software.

**Note that the functionality in this package is under active development and still quite experimental and therefore subject to frequent change.**

## Installation

`compas_viewers` can be installed from source using pip in a Python environment with COMPAS, PySide2, and PyOpenGL.

```bash
conda create -n viewers python=3.7 COMPAS">=0.15.6" PySide2 PyOpenGL --yes
conda activate viewers
pip install path/to/compas_viewers
```

### Windows

Installation of PyOpenGL on Windows is known to be problematic.
The wheels provided by Christophe Gohlke seems to be the most reliable option: <https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl>
Note tha you have to choose the wheel that is compatible with your Python version.

```bash
conda activate viewers
pip install https://www.lfd.uci.edu/~gohlke/pythonlibs/PyOpenGL_accelerate‑3.1.5‑cp37‑cp37m‑win_amd64.whl
```

## Verify installation

To verify your installation, start Python from the command line and run the following:

```python
>>> import compas
>>> import compas_viewers
```

## Getting started

Basic example scripts are availble in the `examples` folder.

## Issue tracker

If you find a bug, please help us solve it by [filing a report](https://github.com/compas-dev/compas_viewers/issues).

## Contributing

Contributions are very welcome and highly appreciated.
Also feature requests or suggestions for future development are helpful.

## License

`compas_viewers` is released under the MIT License.
