<template>
  <div class="container">
    <router-view v-slot="{ Component }">
    <keep-alive exclude="HomeView">
      <component :is="Component" />
    </keep-alive>
  </router-view>
  
  </div>
</template>

<script>
import TermView from '@/views/TermView.vue'
import ProteinView from '@/views/ProteinView.vue'
import HomeView from '@/views/HomeView.vue'

export default {
  name: 'App',
  components: {
    TermView,
    ProteinView,
    HomeView
  }
}
</script>



<style>
.container {
  font-family: 'Roboto Mono', monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
	display: flex;
  overflow: hidden;
	min-height: 100vh;
	align-items: center;
	justify-content: center;
}

nav {
  padding: 30px;
  display: inline-grid;
text-align: center;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
