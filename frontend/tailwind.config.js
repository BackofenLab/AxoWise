/** @type {import('tailwindcss').Config} */

import tailwindcssPrimeUI from "tailwindcss-primeui";

export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: ["selector", '[class="p-dark"]'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0fdfa",
          100: "#ccfbf1",
          200: "#99f6e4",
          300: "#5eead4",
          400: "#2dd4bf",
          500: "#14b8a6",
          600: "#0d9488",
          700: "#0f766e",
          800: "#115e59",
          900: "#134e4a",
          950: "#042f2e",
        },
      },
      fontVariationSettings: {
        "ico-filled": '"FILL" 1, "wght" 700, "GRAD" 0, "opsz" 48', // set Material icon as filled
      },
    },
  },
  // eslint-disable-next-line no-undef
  plugins: [
    tailwindcssPrimeUI,
    //### Include ico-filled in hover prefix
    function ({ addUtilities, theme, e }) {
      const fontVariationSettings = theme("fontVariationSettings");
      const newUtilities = Object.entries(fontVariationSettings).map(([key, value]) => ({
        [`.${e(`font-variation-${key}`)}`]: {
          fontVariationSettings: value,
          transition: "font-variation-settings 0.3s ease",
        },
      }));
      addUtilities(newUtilities, ["hover", "group-hover"]);
    },
  ],
};
