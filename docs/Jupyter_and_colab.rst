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

See the `spleen_segmentation`_ notebook for an example of viewing an image both
with or without a label.

.. _spleen_segmentation: https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/spleen_segmentation_3d.ipynb
