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
import DarkNovaBlueTheme from "./presets/DarkNovaBluetheme.js";
import "animate.css";

// Create a reactive object to serve as the EventBus
const emitter = mitt();

const app = createApp(App);
app.use(router);
app.use(store);
app.use(VueAxios, axios);
app.use(PrimeVue, {
  theme: {
    preset: DarkNovaBlueTheme,
    options: {
      prefix: "p",
      darkModeSelector: ".p-dark", // use "system" for auto selection from system
      cssLayer: false,
    },
  },
});
app.component("v-select", vSelect);
app.config.globalProperties.emitter = emitter;
app.directive("styleclass", StyleClass); // StyleClass manages css classes declaratively to during enter/leave animations or just to toggle classes on an element
app.use(AppState);
app.component("ThemeSwitcher", ThemeSwitcher);
app.mount("#app");

export { emitter };
