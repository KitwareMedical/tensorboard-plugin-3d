=================
Quick start guide
=================

Installation
------------
To install the TensorBoardPlugin3D python package:

.. code-block::

    $ pip install tensorboard_plugin_3d

Usage
-----
You will need to have TensorBoard `installed`_ in order to use this plugin.
Information on getting started is available `here`_.

.. _installed: https://www.tensorflow.org/install
.. _here: https://www.tensorflow.org/tensorboard/get_started

Standalone Appplication
#######################

Select the log directory that contains your 3D image data and run:

.. code-block::

    $ tensorboard --logdir ~/path/to/logdir

If you'd like to test the plugin with some sample data you can set the `logdir`
path to the test data:

.. code-block::

    $ tensorboard --logdir ~/path/to/logdir/test/data

Open TensorBoard and select the ``TensorBoard 3D`` tab.

Notebooks
#########

We have a few notebooks available that allow you to quickly see the plugin in
action:

- **UNet Segmentation 3D** - Use randomly generated data to quickly train a dataset and view the output.

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet_segmentation_3d_ignite.ipynb
        :alt: Open in Colab

- **Cached Spleen Segmentation 3D** - Used cached data from the spleen_segmentation_3d notebook and view the output in TensorBoard.

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/cached_spleen_segmentation_3d.ipynb
        :alt: Open in Colab

- **Cached Brats Segmentation 3D** - Use cached data from the brats_segmentation_3d notebook and view the output in TensorBoard.

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/cached_brats_segmentation_3d.ipynb
        :alt: Open in colab
