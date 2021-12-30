# tensorboard-plugin-3d

[![PyPI](https://img.shields.io/pypi/v/tensorboard-plugin-3d.svg)](https://pypi.python.org/pypi/tensorboard-plugin-3d)

## Getting started

Copy the directory `tensorboard/examples/plugins/tensorboard_plugin_3d` into a desired folder. In a virtualenv with TensorBoard installed, run:

```
python setup.py develop
```

or if you have changes to the client:

```
python setup.py build_client develop
```

This will install and build the frontend and link the plugin into your virtualenv. Then, just run

```
mkdir /tmp/test
tensorboard --logdir /tmp/test
```

and open TensorBoard to see the tensorboard plugin 3D tab.

To uninstall, you can run

```
python setup.py develop --uninstall
```

to unlink the plugin from your virtualenv, after which you can also delete the `tensorboard_plugin_3d.egg-info/` directory that the original `setup.py` invocation created.
