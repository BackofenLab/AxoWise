const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.performance
      .maxEntrypointSize(600000)
      .maxAssetSize(600000)
  }
})
