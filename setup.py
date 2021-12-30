import os
from pathlib import Path
import setuptools
import subprocess

class build_client(setuptools.Command):
  """Build the frontend"""
  description = "install and build frontend"
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    cwd = Path().absolute()
    root = Path(__file__).parent.absolute()
    os.chdir(root / "client")
    subprocess.run(["yarn", "install"], check=True)
    subprocess.run(["yarn", "build:copy"], check=True)
    os.chdir(cwd)

setuptools.setup(
  name="tensorboard_plugin_3d",
  version="0.0.2",
  description="TensorBoard plugin 3D.",
  cmdclass={
    "build_client": build_client
  },
  packages=["tensorboard_plugin_3d"],
  package_data={
    "tensorboard_plugin_3d": ["static/**"],
  },
  entry_points={
    "tensorboard_plugins": [
      "tensorboard_3d = tensorboard_plugin_3d.plugin:TensorboardPlugin3D",
    ],
  },
)
