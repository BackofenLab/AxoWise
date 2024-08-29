import globals from "globals";
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";

export default [
  {
    files: ["src/**/*.{js,mjs,cjs,vue}"], // Only lint files in the src directory
    languageOptions: {
      globals: {
        ...globals.browser,
        sigma: "readonly", // Define sigma as a global variable
        __dirname: "readonly", // Define __dirname as a global variable
      },
    },
  },
  pluginJs.configs.recommended,
  ...pluginVue.configs["flat/essential"],
];
