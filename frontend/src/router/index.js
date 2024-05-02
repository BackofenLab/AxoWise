import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import InputScreen from '../components/home/InputScreen.vue'
import ImportScreen from '../components/home/ImportScreen.vue'
import FileScreen from '../components/home/FileScreen.vue'
import ProteinView from '../views/ProteinView.vue'
import TermView from '../views/TermView.vue'
import CitationView from '../views/CitationView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/protein',
    name: 'protein-graph',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: ProteinView,
    meta: { keepAlive: true } // added meta to enable keep-alive
    

  },
  {
    path: '/terms',
    name: 'terms-graph',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: TermView,
    meta: { keepAlive: true } // added meta to enable keep-alive
  },
  {
    path: '/citation',
    name: 'citation-graph',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: CitationView,
    meta: { keepAlive: true } // added meta to enable keep-alive
  },
  {
    path: '/input',
    name: 'input',
    component: InputScreen,
  },
  {
    path: '/import',
    name: 'import',
    component: ImportScreen
  },
  {
    path: '/file',
    name: 'file',
    component: FileScreen
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
