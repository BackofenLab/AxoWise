import { createApp} from 'vue';
import mitt from 'mitt';
import App from './App.vue'
import router from './router'
import 'vue-select/dist/vue-select.css';
import './style.css';
import vSelect from 'vue-select'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { store } from './store'

// Create a reactive object to serve as the EventBus
const emitter = mitt();

const app = createApp(App);
app.use(router)
app.use(store)
app.use(VueAxios, axios)
app.component("v-select", vSelect)
app.config.globalProperties.emitter = emitter
app.mount('#app')

export { emitter };
