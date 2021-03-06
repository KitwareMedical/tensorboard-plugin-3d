===========
Development
===========

Getting started
---------------
`Fork`_ the repository into your user's namespace on GitHub.

.. _Fork: https://docs.github.com/en/get-started/quickstart/fork-a-repo

Node.js and Yarn are required for building and developing the client.

    - Install `Node.js`_
    - Install `Yarn`_ package manager

.. _Node.js: https://nodejs.org/en/download/
.. _Yarn: https://yarnpkg.com/getting-started/install

Clone the repository:

    .. code-block::

        git clone git@github.com:KitwareMedical/tensorboard-plugin-3d.git
        cd tensorboard-plugin-3d

Prepare the plugin:

    .. code-block::

        npm install
        npm install commitizen

In a virtualenv with TensorBoard installed, run:

    .. code-block::

        python setup.py build_client develop

This will install and build the frontend and link the plugin into your
virtualenv.

Changes to the client
---------------------
If you have made changes to the client you will need to re-run the setup python
script and the build_client command to re-build the client and update the
static file.

    .. code-block::

        python setup.py build_client develop

In order to test the changes you've made run the following, pointing to the log
directory you would like to use:

    .. code-block::

        tensorboard --logdir ~/path/to/logdir

Open TensorBoard to see the tensorboard plugin 3D tab.

Add changed files and commit them with commitizen. Follow the prompts provided.

    .. code-block::

        git add file1 file2
        cz commit
        git push

The pre-commit hooks will enforce the commitizen formatting.

Uninstall
---------
Run the following:

    .. code-block::

        python setup.py develop --uninstall

to unlink the plugin from your virtualenv, after which you can also delete the
``tensorboard_plugin_3d.egg-info/`` directory that the original ``setup.py``
invocation created.
