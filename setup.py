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

this_directory = Path(__file__).parent.absolute()
with open(this_directory/'README.md', encoding='utf-8') as f:
  long_description = f.read()

setuptools.setup(
  name="tensorboard_plugin_3d",
  use_scm_version=True,
  setup_requires=['setuptools-scm'],
  description="TensorBoard plugin for 3D visualization",
  long_description=long_description,
  long_description_content_type='text/markdown',
  cmdclass={
    "build_client": build_client
  },
  packages=["tensorboard_plugin_3d"],
  package_data={
    "tensorboard_plugin_3d": [
      "static/**",
      "static/itk/image-io/**",
      "static/itk/mesh-io/**",
      "static/itk/pipeline/**",
      "static/itk/web-workers/**",
      "static/itk/web-workers/bundles/**",
      "static/itk/web-workers/min-bundles/**",
    ],
  },
  entry_points={
    "tensorboard_plugins": [
      "tensorboard_3d = tensorboard_plugin_3d.plugin:TensorBoardPlugin3D",
    ],
  },
  install_requires=["tensorflow"],
  url='https://github.com/KitwareMedical/tensorboard-plugin-3d',
)
