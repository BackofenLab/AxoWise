import { defineConfig } from "vite";
import eslintPlugin from "vite-plugin-eslint";
import vue from "@vitejs/plugin-vue";
import { PrimeVueResolver } from "@primevue/auto-import-resolver";
import { fileURLToPath, URL } from "node:url";
import Components from "unplugin-vue-components/vite";
// import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    eslintPlugin(),
    Components({
      resolvers: [PrimeVueResolver()],
    }),
  ],
  resolve: {
    alias: {
      // "@": path.resolve(__dirname, "./src"),
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: { chunkSizeWarningLimit: 1600 },
  server: {
    proxy: {
      "^/api": {
        target: "http://127.0.0.1:5000/",
        ws: true,
        changeOrigin: true,
      },
    },
    port: 8080,
  },
});
