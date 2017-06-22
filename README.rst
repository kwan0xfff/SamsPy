SamsPy: Simple Aerospace ModelS in Python
=========================================

Version: 0.0.2

*SamsPy* is a collection of simple aerospace models in Python.
(Anyway, that's the plan.)

It has been developed on Linux (Ubuntu 12.04, now 16.04)
and Mac OS X (Mavericks, now Sierra)
using Python 3 and the corresponding YAML and Nose packages.

More details are given in the file ``docs/overview.rst``.
An initial example is given in ``docs/examples/lvbasic.rst``.
This example deals with simple modeling of a prototype launch vehicle.
(Note: these were written for SamsPy v0.0.1.)

A major goal of version 0.0.2 has been to make SamsPy installable
by ``pip``, the standard Python package installation program.
As a result, there has been significant re-arrangement of the
Python source files between v0.0.1 and v0.0.2.

The ``cmds`` directory includes a couple of executable commands.
``lvbasic.py`` executes the simple launch vehicle modeling described above.
``sto.py`` computes performance characteristics for utilizing a
super-synchronous transfer orbit to eventually reach geostationery orbit.

Notes for version 0.0.2
-----------------------

``lvbasic`` is now installed by ``pip`` as an executable command.
When so installed, and example YAML files are copied into
the current directory, typical execution of the command looks something like ::

    lvbasic vehicle.yaml propellants.yaml

The example files can be found under ``site-packages/samspy/share`` or
on Github at: ``https://github.com/kwan0xfff/SamsPy``.
(Early versions have the files under ``share``;
later ones under ``samspy/share``.)
