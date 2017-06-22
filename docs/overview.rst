==================
Overview of SamsPy
==================

*SamsPy* is envisioned as a collection of simple aerospace models (SAMS)
in Python (PY).

The initial models provided deal with idealized multistage rocket performance.
Effects of gravity and planetary atmosphere are not included.

SamsPy is written in Python 3.  Package requirements for Linux (Ubuntu 12.04)
and Mac OS X (via MacPorts) are given at the bottom of this write-up.  (See
"Requirements" below.)

Example
=======

Note: this version of the overview was written for SamsPy v0.0.1,
and does not reflect the re-arrangement of the source files.
It needs to be modified for version v0.0.2.

Examples of user input are provided in the *share* subdirectory as YAML files.

  * *propellants.yaml* is a selection of possible propellant combinations.
    Information is provided about liquid densities, ratios of oxidizer to fuel,
    specific impulse, etc.

  * *protolv.yaml* is a three-stage prototype launch vehicle with a small payload.

These files can be used as input to the *lvbasic.py* command, a launch vehicle
basic analysis tool.  To use, the SamsPy library modules need to be available
to the command.  The simplest way to do this is to set the PYTHONPATH
environment variable.  For example, assume that SAMSPYROOT represents the top
of the SamsPy source tree::

  $ export PYTHONPATH=${SAMSPYROOT}/lib

Then if executed from there::

  $ cmds/lvbasic.py share/protolv.yaml share/propellants.yaml

The result should be a listing of propellant and performance data for
each stage, along with the delta V (velocity change) achievable from
the specified vehicle.

Testing and Static Analysis
===========================

SamsPy utilizes the Python 3 unittest package to help ensure code quality.
Additionally, it depends on the "nose" framework to drive the tests.
To run tests from top of the SamsPy code tree::

  $ ( cd tests; ./runtests.sh )

A modest amount of static checking has been performed using "pylint".  On
some platforms, pylint for Python 3 has some difficulties in installation.
For the moment, checking was done using "pylint" for Python 2.

Requirements
============

The SamsPy run-time environment requires certain prequisite Python 3
packages.  Below are the packages, with their names on Ubuntu 12.04.
(These names should apply to other Ubuntu and Debian systems as well.)

  * python3 - Python 3 interactive high-level programming language
  * python3-yaml -- YAML parser and emitter for Python3
  * python3-nose -- test framework for Python unittest

On Linux, SamsPy was tested on Ubuntu 12.04.4. The Python 3 version is 3.2.3.

For Mac OS X systems, these packages can be installed using MacPorts.
The corresponding names for Python 3.2 are: python32, py32-yaml, py32-nose

Documetation
============

Like much of the current package, documentation is sparse.  However, pages
are currently crafted in the format of "reStructuredText" and can be
converted to reasonable HTML.  No CSS file is yet provided for it.
