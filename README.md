TensorboardPlugin3D - 3D Tensor Visualization
===============================================

[![PyPI](https://img.shields.io/pypi/v/tensorboard-plugin-3d.svg)](https://pypi.python.org/pypi/tensorboard-plugin-3d)
[![DOI](https://zenodo.org/badge/423910165.svg)](https://zenodo.org/badge/latestdoi/423910165)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet_segmentation_3d_ignite.ipynb)

Introduction
------------

TensorboardPlugin3D is an open-source Tensorboard plugin that supports
visualizing 3D output within the Tensorboard application, JupyterLab, and
Google Colab.

Installation
------------

Install the [PyPI package](https://pypi.python.org/pypi/tensorboard-plugin-3d):

```sh
pip install tensorboard-plugin-3d
```

Monai Notebook Examples
-----------------
The Spleen Segmentation 3D tutorial shows how to integrate MONAI into an existing PyTorch medical DL program and demonstrates using TensorboardPlugin3D to view either an image with a label (shown above) or just an image, using the model output. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/spleen_segmentation_3d.ipynb)
![Spleen Image with Label](https://github.com/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/spleen_with_label.png)
![Spleen Output](https://github.com/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/spleen_output.png)

The UNet Segmentation 3D Ignite notebook provides a simple, fast-running notebook with demo data. If you're looking for a quick way to get started and see the plugin in action this is a great place to start. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet_segmentation_3d_ignite.ipynb)
![UNet Output](https://github.com/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet.gif)

Documentation
-------------

See the [documentation](https://tensorboardplugin3d.readthedocs.io/en/latest/)
for a guide on getting started.
