import setuptools

setuptools.setup(
    name="tensorboard_plugin_3d",
    version="0.0.1",
    description="TensorBoard plugin 3D.",
    packages=["tensorboard_plugin_3d"],
    package_data={
        "tensorboard_plugin_3d": ["client/**"],
    },
    entry_points={
        "tensorboard_plugins": [
            "tensorboard_3d = tensorboard_plugin_3d.plugin:TensorboardPlugin3D",
        ],
    },
)
