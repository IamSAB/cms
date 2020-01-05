module.exports = {
    devServer: {
      proxy: {
        '^/api': {
          target: 'localhost:5000',
          changeOrigin: true
        }
      }
    }
  }
