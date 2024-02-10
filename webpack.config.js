const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const path = require('path');


module.exports = {
  entry: './main_app/static/js/main.js',
  output: {
    path: path.resolve(__dirname, 'main_app', 'static', 'dist'),
    filename: 'my-first-webpack.bundle.js',
  },
    module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ],
  },
   devServer: {
    static: './main_app/static/dist',
  },
  plugins: [
    new webpack.ProgressPlugin(),
    new HtmlWebpackPlugin({ template: './main_app/templates/index.html' }),
  ],
  stats: {
    children: true,
  },

};