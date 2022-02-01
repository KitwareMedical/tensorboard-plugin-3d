==============================
JupyterLab and Colab Notebooks
==============================

Installation
------------
To install the TensorboardPlugin3D python package inside the notebook:

    .. code-block::

        !pip install tensorboard_plugin_3d

Usage
-----
The plugin currently looks at the first image available in the log directory
and visualizes it. If two images are available the second image is assumed to
be a label. Each image or image/label pair should be written to its own log
directory. The directory to be used can then be set and visualized with the
tensorboard widget within either JupyterLab or Colab.

    .. code-block::

        tb_dir = os.path.join(root_dir, logdir_to_use)
        %load_ext tensorboard
        %tensorboard --logdir=$tb_dir

.. image:: images/spleen_with_label.png
   :alt: Spleen with Label

See the `spleen_segmentation`_ notebook for an example of viewing both the
input data and output model from real world data, or the `unet_segmentation`_
for a faster demonstration using sample data.

.. _spleen_segmentation: https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/spleen_segmentation_3d.ipynb
.. _unet_segmentation: https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet_segmentation_3d_ignite.ipynb

.. image:: images/unet.gif
   :alt: UNet Demo
