const fs = require('fs-extra')
const path = require('path')

fs.copySync(
  path.resolve(__dirname, 'dist/index.html'),
  path.resolve(__dirname, '../tensorboard_plugin_3d/static/index.html'),
)
