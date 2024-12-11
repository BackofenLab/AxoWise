import { createApp } from "vue";
import mitt from "mitt";
import App from "./App.vue";
import router from "./router";
import "vue-select/dist/vue-select.css";
import "./style.css";
import "primeicons/primeicons.css";
import vSelect from "vue-select";
import axios from "axios";
import VueAxios from "vue-axios";
import PrimeVue from "primevue/config";
import { store } from "./store";
import StyleClass from "primevue/styleclass";
import ThemeSwitcher from "./components/ThemeSwitcher.vue";
import AppState from "./plugins/appState.js";
import { definePreset } from "@primevue/themes";
import Aura from "@primevue/themes/aura";
import "animate.css";
import ToastService from "primevue/toastservice";

// Create a reactive object to serve as the EventBus
const emitter = mitt();

const app = createApp(App);
app.use(router);
app.use(store);
app.use(VueAxios, axios);
app.use(PrimeVue, {
  theme: {
    preset: definePreset(Aura, {
      semantic: {
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
        colorScheme: {
          light: {
            primary: {
              color: "{primary.500}",
              contrastColor: "#ffffff",
              hoverColor: "{primary.600}",
              activeColor: "{primary.700}",
            },
            highlight: {
              background: "{primary.50}",
              focusBackground: "{primary.100}",
              color: "{primary.700}",
              focusColor: "{primary.800}",
            },
          },
          dark: {
            primary: {
              color: "{primary.400}",
              contrastColor: "{surface.900}",
              hoverColor: "{primary.300}",
              activeColor: "{primary.200}",
            },
            surface: {
              0: "#ffffff",
              50: "#f8fafc",
              100: "#f1f5f9",
              200: "#e2e8f0",
              300: "#cbd5e1",
              400: "#94a3b8",
              500: "#64748b",
              600: "#475569",
              700: "#334155",
              800: "#1e293b",
              900: "#0f172a",
              950: "#020617",
            },
            highlight: {
              background: "color-mix(in srgb, {primary.400}, transparent 84%)",
              focusBackground: "color-mix(in srgb, {primary.400}, transparent 76%)",
              color: "rgba(255,255,255,.87)",
              focusColor: "rgba(255,255,255,.87)",
            },
          },
        },
      },
    }),
    options: {
      prefix: "p",
      darkModeSelector: ".p-dark", // use "system" for auto selection from system
      lightModeSelector: ".p-light",
      cssLayer: false,
    },
  },
});
app.component("v-select", vSelect);
app.config.globalProperties.emitter = emitter;
app.directive("styleclass", StyleClass); // StyleClass manages css classes declaratively to during enter/leave animations or just to toggle classes on an element
app.use(AppState);
app.use(ToastService);
app.component("ThemeSwitcher", ThemeSwitcher);
app.mount("#app");

export { emitter };
