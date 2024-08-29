import { defineConfig } from "vite";
import eslintPlugin from "vite-plugin-eslint";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), eslintPlugin()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
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
