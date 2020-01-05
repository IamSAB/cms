module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  dev: {
    proxyTable: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    },
  }
}
