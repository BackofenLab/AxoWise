import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ProteinView from "../views/ProteinView.vue";
import TermView from "../views/TermView.vue";
import CitationView from "../views/CitationView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/protein",
    name: "protein-graph",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: ProteinView,
    meta: { keepAlive: true }, // added meta to enable keep-alive
  },
  {
    path: "/term",
    name: "terms-graph",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: TermView,
    meta: { keepAlive: true }, // added meta to enable keep-alive
  },
  {
    path: "/citation",
    name: "citation-graph",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: CitationView,
    meta: { keepAlive: true }, // added meta to enable keep-alive
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
