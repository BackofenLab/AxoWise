const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: (config) => {
    config.performance.maxEntrypointSize(600000).maxAssetSize(600000);
  },
  devServer: {
    proxy: {
      "^/api": {
        target: "http://127.0.0.1:5000/",
        ws: true,
        changeOrigin: true,
      },
    },
  },
});
