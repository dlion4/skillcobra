const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

module.exports = merge(commonConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    port: 3000,
    hot: true,
    liveReload: false,
    historyApiFallback: true,
    proxy: [
      {
        context: ['/'],
        target: 'http://127.0.0.1:8002',
        secure: false, // Set to false if using HTTP
        changeOrigin: true, // Adjust the origin to match the target (Django server
      },
    ],
    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: true,
      },
    },
    hot: true, // Enable Hot Module Replacement (HMR)
    liveReload: false, // Disable live reload (we want HMR, not full reloads)
    historyApiFallback: true, // Useful for single-page apps with React Router
  },
});
