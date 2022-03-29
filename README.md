TensorBoardPlugin3D - 3D Tensor Visualization
===============================================

[![PyPI](https://img.shields.io/pypi/v/tensorboard-plugin-3d.svg)](https://pypi.python.org/pypi/tensorboard-plugin-3d)
[![Build and Test](https://github.com/KitwareMedical/tensorboard-plugin-3d/actions/workflows/python-test.yml/badge.svg)](https://github.com/KitwareMedical/tensorboard-plugin-3d/actions/workflows/python-test.yml)
[![DOI](https://zenodo.org/badge/423910165.svg)](https://zenodo.org/badge/latestdoi/423910165)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet_segmentation_3d_ignite.ipynb)

Introduction
------------

TensorBoardPlugin3D is an open-source TensorBoard plugin that supports
visualizing 3D output within the TensorBoard application, JupyterLab, and
Google Colab.

Installation
------------

Install the [PyPI package](https://pypi.python.org/pypi/tensorboard-plugin-3d):

```sh
pip install tensorboard-plugin-3d
```

MONAI Notebook Examples
-----------------
The Spleen Segmentation 3D tutorial shows how to integrate MONAI into an existing PyTorch medical DL program and demonstrates using TensorBoardPlugin3D to view an image with a label to show the input data (shown in the first image) or to compare the model output with the input. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/spleen_segmentation_3d.ipynb)

Get started with a quick view of the output data with the cached notebook. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/cached_spleen_segmentation_3d.ipynb)
![Spleen Image with Label](https://github.com/KitwareMedical/tensorboard-plugin-3d/blob/main/docs/images/spleen_with_label.png?raw=true)
![Spleen Output](https://github.com/KitwareMedical/tensorboard-plugin-3d/blob/main/docs/images/label_with_output.gif?raw=true)

The UNet Segmentation 3D Ignite notebook provides a simple, fast-running notebook with demo data. If you're looking for a quick way to get started and see the plugin in action this is a great place to start. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/unet_segmentation_3d_ignite.ipynb)
![UNet Output](https://github.com/KitwareMedical/tensorboard-plugin-3d/blob/main/docs/images/unet.gif?raw=true)

The BRATS Segmentation 3D notebook demonstrates brain tumor 3D segmentation with MONAI. The tutorial shows how to construct a training workflow of multi-labels segmentation task. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/brats_segmentation_3d.ipynb)

Get started with a quick view of the output data with the cached notebook. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KitwareMedical/tensorboard-plugin-3d/blob/main/demo/notebook/cached_brats_segmentation_3d.ipynb)

Documentation
-------------

See the [documentation](https://tensorboardplugin3d.readthedocs.io/en/latest/)
for a guide on getting started.
