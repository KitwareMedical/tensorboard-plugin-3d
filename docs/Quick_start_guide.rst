=================
Quick start guide
=================

Installation
------------
To install the TensorboardPlugin3D python package:

.. code-block::

    $ pip install tensorboard_plugin_3d

Usage
-----
You will need to have Tensorboard `installed`_ in order to use this plugin. 
Information on getting started is available `here`_.

.. _installed: https://www.tensorflow.org/install
.. _here: https://www.tensorflow.org/tensorboard/get_started

Select the log directory that contains your 3D image data and run:

.. code-block::

    $ tensorboard --logdir ~/path/to/logdir

If you'd like to test the plugin with some sample data you can set the `logdir`
path to the test data:

.. code-block::

    $ tensorboard --logdir ~/path/to/logdir/test/data

Open Tensorboard and select the ``Tensorboard 3D`` tab.
