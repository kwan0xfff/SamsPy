README for SamsPy
=================

*SamsPy* is a collection of simple aerospace models in Python.
(Anyway, that's the plan.)

It has been developed on Linux (Ubuntu 12.04) and Mac OS X (Mavericks)
using Python 3 and the corresponding YAML and Nose packages.

More details are given in the file ``docs/overview.rst``.
An initial example is given in ``docs/examples/lvbasic.rst``.
This example deals with simple modeling of a prototype launch vehicle.

The ``cmds`` directory includes a couple of executable commands.
``lvbasic.py`` executes the simple launch vehicle modeling described above.
``sto.py`` computes performance characteristics for utilizing a
super-synchronous transfer orbit to eventually reach geostationery orbit.

