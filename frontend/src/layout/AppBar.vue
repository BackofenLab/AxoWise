<template>
  <Toolbar
    class="h-[60px] !py-1.5 relative !rounded-none dark:!border-0 dark:!bg-[#34343D] z-[1]"
    :pt="{ end: { class: 'flex items-center gap-4' } }"
  >
    <template #start>
      <div class="flex gap-4">
        <Button icon="material-icons" aria-label="menu" severity="secondary" @click="toggle_widget(!widget)">
          <span v-if="widget" class="material-icons">widgets</span>
          <span v-if="!widget" class="material-icons">dashboard</span>
        </Button>

        <Button @click="toggle" plain text class="capitalize">
          <span class="material-icons">display_settings</span>
          {{ view }}
        </Button>
      </div>
    </template>

    <template #center><SearchField :data="gephi_data" :mode="mode"></SearchField></template>

    <template #end>
      <keep-alive>
        <NetworkValues :data="gephi_data"></NetworkValues>
      </keep-alive>

      <ThemeSwitcher />
    </template>
  </Toolbar>

  <Popover ref="op">
    <ul class="flex flex-col p-0 m-0 list-none">
      <li
        v-for="entry in filter_views"
        :key="entry"
        v-on:click="swap_view(entry)"
        class="flex items-center gap-2 px-2 py-3 capitalize cursor-pointer hover:bg-emphasis rounded-border"
      >
        {{ entry + " view" }}
      </li>
    </ul>
  </Popover>
</template>

<script setup>
import { ref } from "vue";

const op = ref();

const toggle = (event) => {
  op.value.toggle(event);
};
</script>

<script>
import SearchField from "@/components/interface/SearchField.vue";
import NetworkValues from "../components/interface/NetworkValues.vue";

export default {
  name: "AppBar",
  props: ["isDockActive", "gephi_data", "mode", "view","widget"],
  emits: ["widget_toggled"],
  components: {
    SearchField,
    NetworkValues,
  },
  data() {
    return { filter_views: ["term", "citation"] };
  },
  methods: {
    toggle_widget(event) {
      this.$emit("widget_toggled", event);
    },
    swap_view(entry) {
      // FIXME: Use toast instead of alert
      if (entry == "term") {
        this.$store.state.term_graph_data
          ? this.$router.push("term")
          : alert("Please generate first a term graph via the enrichment section ");
      }
      if (entry == "citation") {
        this.$store.state.citation_graph_data
          ? this.$router.push("citation")
          : alert("Please generate first a citation graph via the citation section ");
      }
    },
  },
  mounted() {},
};
</script>
