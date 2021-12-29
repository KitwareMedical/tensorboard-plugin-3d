const fs = require('fs')
const path = require('path')

console.log(__dirname)
fs.copyFileSync(
  path.resolve(__dirname, 'dist/index.html'),
  path.resolve(__dirname, '../tensorboard_plugin_3d/static/index.html')
)
