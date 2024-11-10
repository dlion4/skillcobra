const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');

module.exports = {
  target: 'web',
  context: path.join(__dirname, '../'),

  entry: {
    project: path.resolve(__dirname, '../skillcobra/static/js/project'),
    vendors: path.resolve(__dirname, '../skillcobra/static/js/vendors'),
    main: path.resolve(__dirname, '../main'),
  },
  output: {
    path: path.resolve(
      __dirname,
      '../skillcobra/static/webpack_bundles/',
    ),
    publicPath: '/static/webpack_bundles/',
    filename: 'js/[name]-[fullhash].js',
    chunkFilename: 'js/[name]-[hash].js',
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(path.join(__dirname, '../')),
      filename: 'webpack-stats.json',
    }),
    new MiniCssExtractPlugin({ filename: 'css/[name].[contenthash].css' }),
    new webpack.HotModuleReplacementPlugin(),
  ],
  module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      {
        test: /\.tsx?$/,  // Handle both .ts and .tsx files
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',  // First use Babel to transpile TypeScript files
            options: {
              presets: [
                '@babel/preset-env',       // Transpile modern JavaScript
                '@babel/preset-react',     // Enable JSX syntax for React
                '@babel/preset-typescript' // Enable TypeScript support
              ],
              plugins: [
                'react-hot-loader/babel',  // Add React Hot Loader plugin for HMR
              ],
            },
          },
          'ts-loader',  // After Babel, use ts-loader to process TypeScript
        ],
      },
      {
        test: /\.jsx$/,  // Handle JavaScript files (for React JS files)
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',       // Transpile modern JS to ES5
              '@babel/preset-react',     // Enable JSX syntax for React
            ],
            plugins: [
              'react-hot-loader/babel',  // Add React Hot Loader for JS
            ],
          },
        },
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['postcss-preset-env', 'autoprefixer', 'pixrem'],
              },
            },
          },
          'sass-loader',
        ],
      },
    ],
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.ts', '.tsx', '.js', ".jsx", ".json"],
    alias: {
      '@': path.resolve(__dirname, '../src'),
    },
  },
  stats: {
    assets: true,
    modules: true,
    chunks: true,
    chunkModules: true,
    chunkOrigins: true,
    hash: true,
  },
};
