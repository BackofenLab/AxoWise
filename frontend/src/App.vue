<template>
  <AxoChatBot />
  <DocumentWindow />
  <Toast />
  <router-view v-slot="{ Component }">
    <keep-alive exclude="HomeView">
      <component :is="Component" />
    </keep-alive>
  </router-view>
</template>

<script>
import TermView from "@/views/TermView.vue";
import CitationView from "@/views/CitationView.vue";
import ProteinView from "@/views/ProteinView.vue";
import HomeView from "@/views/HomeView.vue";
import AxoChatBot from "@/components/AxoChatBot.vue";
import DocumentWindow from "@/components/DocumentWindow.vue";
import Toast from 'primevue/toast';

export default {
  name: "App",
  components: {
    TermView,
    ProteinView,
    HomeView,
    CitationView,
    AxoChatBot,
    DocumentWindow,
    Toast
  },
};
</script>
