const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const InlineChunkHtmlPlugin = require('inline-chunk-html-plugin')
const CopyPlugin = require('copy-webpack-plugin')
const WebPackBar = require('webpackbar')

const entry = path.resolve(__dirname, 'node_modules', 'itk-vtk-viewer', 'src', 'index.js')
const vtkRules = require('vtk.js/Utilities/config/dependency.js').webpack.core
  .rules
const cssRules = require('vtk.js/Utilities/config/dependency.js').webpack.css
  .rules
const itkConfig = path.resolve(__dirname, 'node_modules', 'itk-vtk-viewer', 'src', 'itkConfig.js')

const fallback = {
  path: false,
  url: false,
  module: false,
  fs: false,
  stream: require.resolve('stream-browserify'),
  crypto: false,
}

const moduleConfigRules = [
  {
    test: /\.(js|jsx)$/i,
    loader: 'babel-loader',
    options: {
      presets: ['@babel/preset-env','@babel/preset-react','babel-preset-mobx'],
    },
  },
  {
    test: /\.worker.js$/,
    use: [{ loader: 'worker-loader', options: { inline: 'no-fallback' } }],
  },
  {
    test: /\.(png|jpe?g|gif)$/i,
    type: 'asset',
    parser: { dataUrlCondition: { maxSize: 128 * 1024 } },
  }, // 128kb
  { test: /\.svg$/, type: 'asset/source' },
].concat(vtkRules, cssRules)

const isDev = process.env.NODE_ENV !== 'production'
const __parent = path.resolve(__dirname, '..')

module.exports = {
  mode: isDev ? 'development' : 'production',
  entry: ['regenerator-runtime/runtime.js', './src/index.js'],
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'index.js',
    publicPath: '',
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      '../itkConfig.js': itkConfig,
      '../../itkConfig.js': itkConfig,
    },
    fallback,
  },
  module: {
    rules: moduleConfigRules.concat([
      {
        test: entry,
        loader: 'expose-loader',
        options: { exposes: 'itkVtkViewer' },
      },
    ]),
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: path.join(
            __dirname,
            'node_modules',
            'itk-vtk-viewer',
            'dist',
            'itk',
          ),
          to: path.join(__parent, 'tensorboard_plugin_3d', 'static', 'itk'),
        },
      ],
    }),
    new HtmlWebpackPlugin({
      inject: true,
      scriptLoading: 'blocking',
      template: 'index.html'
    }),
    !isDev ? new InlineChunkHtmlPlugin(HtmlWebpackPlugin, [/.*/]) : undefined,
    new WebPackBar(),
  ].filter(Boolean)
}