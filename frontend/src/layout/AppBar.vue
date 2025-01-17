<template>
  <Toolbar class="h-[58px] !py-1.5 relative !rounded-none dark:!border-0 dark:!bg-[#34343D] z-[1]"
    :pt="{ end: { class: 'flex items-center gap-4' } }">
    <template #start>
      <div class="flex gap-4">
        <Button icon="material-symbols-rounded" aria-label="menu" severity="secondary" @click="toggle_widget(!widget)">
          <span v-if="widget" class="material-symbols-rounded font-variation-ico-filled">widgets</span>
          <span v-if="!widget" class="material-symbols-rounded font-variation-ico-filled">dashboard</span>
        </Button>

        <Button @click="toggle" plain text class="capitalize">
          <span class="material-symbols-rounded">display_settings</span>
          {{ view }}
        </Button>
      </div>
    </template>

    <template #center>
      <Button @click="center" plain text class="capitalize">
        <span class="material-symbols-rounded">fullscreen</span>
        Recenter graph
      </Button>
    </template>

    <template #end>
      <SearchField :data="gephi_data" :mode="mode"></SearchField>

      <keep-alive>
        <NetworkValues :data="gephi_data"></NetworkValues>
      </keep-alive>

      <ThemeSwitcher />
    </template>
  </Toolbar>

  <Popover ref="op">
    <ul class="flex flex-col p-0 m-0 list-none">
      <li v-for="entry in filter_views" :key="entry" v-on:click="swap_view(entry); hide();"
        class="flex items-center gap-2 px-2 py-3 capitalize cursor-pointer hover:bg-emphasis rounded-border">
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

const hide = () => {
  op.value.hide();
};
</script>

<script>
import SearchField from "@/components/appbar/SearchField.vue";
import NetworkValues from "@/components/appbar/NetworkValues.vue";
import { useToast } from "primevue/usetoast";

export default {
  name: "AppBar",
  props: ["gephi_data", "filter_views", "mode", "view", "widget"],
  emits: ["widget_toggled"],
  components: {
    SearchField,
    NetworkValues,
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    center() {
      this.emitter.emit("centerGraph", { check: true, mode: this.mode });
    },
    toggle_widget(event) {
      this.$emit("widget_toggled", event);
    },
    swap_view(entry) {
      if (entry == "protein") {
        this.$router.push("protein");
      }
      if (entry == "term") {
        this.$store.state.term_graph_data
          ? this.$router.push("term")
          : this.toast.add({
            severity: "info",
            detail: "Please generate first a term graph via the enrichment section.",
            life: 4000,
          });
      }
      if (entry == "citation") {
        this.$store.state.citation_graph_data
          ? this.$router.push("citation")
          : this.toast.add({
            severity: "info",
            detail: "Please generate first a citation graph via the citation section.",
            life: 4000,
          });
      }
    },
  },
};
</script>
