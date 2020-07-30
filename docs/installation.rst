.. highlight:: shell

============
Installation
============

From sources
------------

The sources for predictatops can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/JustinGOSSES/predictatops

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/JustinGOSSES/predictatops/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/JustinGOSSES/predictatops
.. _tarball: https://github.com/JustinGOSSES/predictatops/tarball/master

Or instead of setup.py install, I usually use conda environments. The command below changes into the top level predictatops directory, creates a conda environment named predictatops from the environment.yml file and then activates that environment.

.. code-block:: console

    $ cd predictatops 
    $ conda env create -f environment.yml
    $ source activate predictatops


Stable release
--------------
Eh, a stable release doesn't quite exist yet. Enough to work with but not enough to call it stable. It will be pushed to PyPy at some point soon, but has not been pushed there yet. When it does, it will run like this:

If we were to put this on PyPy, you could install predictatops by running this command in your terminal:

.. code-block:: console

    $ pip install predictatops

But it isn't there, so don't try it!

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

