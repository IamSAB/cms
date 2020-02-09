module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                timeout: 6000,
                secure: false,
                changeOrigin: true
            }
        }
    },
    configureWebpack: {
        devtool: 'source-map'
    }
}
