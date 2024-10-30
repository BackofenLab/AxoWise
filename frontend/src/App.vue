<template>
  <div class="container" id="container">
    <PersistentWindow />
    <DocumentWindow />
    <router-view v-slot="{ Component }">
      <keep-alive exclude="HomeView">
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script>
import TermView from "@/views/TermView.vue";
import CitationView from "@/views/CitationView.vue";
import ProteinView from "@/views/ProteinView.vue";
import HomeView from "@/views/HomeView.vue";
import PersistentWindow from "@/components/PersistentWindow.vue";
import DocumentWindow from "@/components/DocumentWindow.vue";

export default {
  name: "App",
  components: {
    TermView,
    ProteinView,
    HomeView,
    CitationView,
    PersistentWindow,
    DocumentWindow,
  },
};
</script>
