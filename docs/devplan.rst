===========================
Development Plan for SamsPy
===========================

The primary working code of SamsPy is on branch *master*.
It is currently has a single tag, *v0.0.1*.
The code is considered pre-alpha.

The next target is *v0.0.2*, with the aim of making the package
easier to install for Python users.

For people coming from a UNIX background,
who are familiar with the layout
of executables in ``bin``, libraries in ``lib``, et cetera,
the layout of v0.0.1 makes reasonable sense.
But since SamsPy is composed of Python tools,
and tools to support easy installs in Python are fairly mature
(``venv``, ``pip``),
the users are better served by migrating the package to
the current install tools and their associated package layout.

A number of additional dot-dot releases (e.g., *v0.0.3*, etc.)
may be introduced until the package can be installed via `pip`
from the Python Package Index (PyPI) at ``https://pypi.python.org/pypi``.
At that point, the package is expected to jump to *v0.1.0*,
and new capabilities are planned for addition.


