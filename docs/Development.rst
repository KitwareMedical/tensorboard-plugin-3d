===========
Development
===========

Getting started
---------------
Node.js and Yarn are required for building and developing the client.

    - Install `Node.js`_
    - Install `Yarn`_ package manager

.. _Node.js: https://nodejs.org/en/download/
.. _Yarn: https://yarnpkg.com/getting-started/install

Clone the repository:

    .. code-block::

        git clone git@github.com:KitwareMedical/tensorboard-plugin-3d.git

In a virtualenv with TensorBoard installed, run:

    .. code-block::

        python setup.py develop


Changes to the client
---------------------
If you have made changes to the client you will need to run the following
command to update the static html file:

    .. code-block::

        python setup.py build_client develop

This will install and build the frontend and link the plugin into your
virtualenv.


Starting TensorBoard
---------------------
Run the following, pointing to the log directory you would like to use:

    .. code-block::

        tensorboard --logdir ~/path/to/logdir

Open TensorBoard to see the tensorboard plugin 3D tab.


Uninstall
---------
Run the following:

    .. code-block::

        python setup.py develop --uninstall

to unlink the plugin from your virtualenv, after which you can also delete the
``tensorboard_plugin_3d.egg-info/`` directory that the original ``setup.py``
invocation created.
