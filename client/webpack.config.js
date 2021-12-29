const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const InlineChunkHtmlPlugin = require('inline-chunk-html-plugin')

const isDev = process.env.NODE_ENV !== 'production'

module.exports = {
  mode: isDev ? 'development' : 'production',
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'index.js'
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/i,
        loader: 'babel-loader',
        options: { presets: ['@babel/preset-env','@babel/preset-react'] }
      },
      { test: /\.css$/i, use: ['style-loader', 'css-loader'] },
      { test: /\.(png|jpe?g|gif)$/i, use: ['file-loader'] },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      inject: true,
      scriptLoading: 'blocking',
      template: 'index.html'
    }),
    !isDev ? new InlineChunkHtmlPlugin(HtmlWebpackPlugin, [/.*/]) : undefined
  ].filter(Boolean)
}