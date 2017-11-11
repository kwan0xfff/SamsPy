===============================
SamsPy in a virtual environment
===============================

*SamsPy* can be downloaded from Github or PyPI,
but it is probably most easily installed and used from the 
Python 3 virtual environment.

Setting up the venv
-------------------

On Linux or MacOS, assuming that Python3 is already installed,
the simplest way to set up the enviroment is to go to the desired
parent directory, and run ::

    $ python3 -m venv myvenv

This creates a subdirectory ``myvenv``.

More information on the virtual environment can be found in the
online Python library documentation, for example,

    https://docs.python.org/3/library/venv.html

With the virtual envirnment ``myvenv`` in place,
activate it by ::

    $ . myvenv/bin/activate
    (myvenv) $

At this point, the shell prompt has changed.
(To later leave the virtual environment, use "deactivate".
We'll cover this later.)

The installation of SamsPy is handled by ``pip``.
Running ``pip list``,
you may find that your version of ``pip`` is outdated.
For example ::

    (myvenv) $ pip list
    pip (8.1.1)
    pkg-resources (0.0.0)
    setuptools (20.7.0)
    You are using pip version 8.1.1, however version 9.0.1 is available.
    You should consider upgrading via the 'pip install --upgrade
    pip' command.
    (myvenv) $ 

In this case, as suggested, run the upgrade. ::

    (myvenv) $ pip install --upgrade pip

Install SamsPy
--------------

Use ``pip`` to install SamsPy.
Any dependencies (e.g., `PyYAML`)
will be satisfied during the installation. ::

    (myvenv) $ pip install samspy

First run
---------

SamsPy currently only exposes a single executable command ``lvbasic``,
which computes basic properties of a liquid propellant launch vehicle.
Running it with without arugments shows what arguments are needed.  ::

    (myvenv) $ samspy
    usage: lvbasic [-h] [-v] vehicle propellants
    lvbasic: error: the following arguments are required: vehicle, propellants

Copies of the example vehicle and propellant files are buried deeply
in the envionment of ``myvenv``.
If the working directory has not changed since creation of ``myvenv``,
then these files are found in the site package for SamSpy.
For example, ::

    (myvenv) $ cd myvenv/lib/python3.5  # might be 3.6 or something else
    (myvenv) $ cd site-packages/samspy/share
    (myvenv) $ ls
    propellants.yaml  protolv.yaml

You can now run the ``lvbasic`` command with the input arguments in
the correct order. ::

    (myvenv) $ lvbasic protolv.yaml propellants.yaml
    ...
      Total deltaV (m/s, ft/s)   8414.8755  27607.8592
    ...

Use local data
--------------

To modify the vehicle and propellant properties,
copy the argument files to a new directory, edit them,
and run them there.  For example, ::

    (myvenv) $ mkdir $HOME/samspy
    (myvenv) $ cp protolv.yaml $HOME/samspy/mylv.yaml
    (myvenv) $ cp propellants.yaml $HOME/samspy/propellants.yaml
    (myvenv) $ cd $HOME/samspy

Do the appropriate editing.  And then... ::

    (myvenv) $ lvbasic mylv.yaml propellants.yaml

Leave the venv
--------------

To leave the virtual environment, simply deactivate it from within.  ::

    (myvenv) $ deactivate
    $ 

Note that activating the virtual environment does not invoke a new shell.
Instead, it rewrites environment variables used in Python's execution.
Activating it adds directories to the execution path;
deactivating it restores the original paths.
During the activation, the executing shell remains the same;
that this, the underlying shell process ID remains the same.

