<template>
  <Button label="Find your node" icon="pi pi-search" severity="secondary" class="w-[180px] dark:!bg-[#020617]"
    :pt="{ label: { class: 'mr-auto' } }" @click="show_search = !show_search" />

  <Dialog v-model:visible="show_search" position="topright" :minY="60" :minX="60" :closable="true" :pt="{
    root: { class: 'w-[22rem] !mt-[60px] !ml-[60px] !mr-[7rem]' },
    headerActions: { class: '!hidden' },
    header: { class: '!p-3 order-1 cursor-move' },
    content: { class: 'order-2 !px-0' },
    footer: {
      class: 'order-3 !p-3 border-t border-slate-200 dark:border-slate-100/30',
    },
  }">
    <template #header>
      <IconField class="w-full !mt-[10px]">
        <InputIcon class="z-10 pi pi-search" />
        <InputText v-model="search_raw" placeholder="Find your node" class="w-full"
          v-on:keyup.enter="select_node(filt_search[0])" autofocus />
      </IconField>
    </template>

    <h6 v-if="search_raw.length >= 2 && filt_search.length === 0" class="text-center text-slate-300">No available
      options</h6>

    <ul class="divide-y border-slate-200 dark:divide-slate-100/10"
      v-if="search_raw.length >= 2 && filt_search.length > 0">
      <li
        class="flex !justify-between items-center px-4 hover:dark:bg-slate-100/10 hover:bg-slate-100 hover:!text-primary-400"
        v-for="(entry, index) in filt_search" :key="index">
        <a class="flex-1 py-2.5" href="#" v-on:click="select_node(entry)">{{ entry.label }}</a>
        <Divider layout="vertical" />
        <a :id="'results-' + index" href="" v-on:click="google_search(entry.attributes['Name'], index)" target="_blank">
          <img :alt="entry.label" src="@/assets/toolbar/google-logo.png" class="w-4" />
        </a>
      </li>
    </ul>

    <template #footer>
      <span class="flex items-center text-sm gap-1.5 text-slate-400">
        <span
          class="h-[20px] flex items-center font-semibold text-sm px-1 bg-slate-100 rounded text-slate-500 leading-none">
          esc
        </span>
        to close
      </span>
    </template>
  </Dialog>
</template>

<script>
export default {
  name: "SearchField",
  props: ["data", "mode"],
  data() {
    return {
      show_search: false,
      search_raw: "",
    };
  },
  methods: {
    select_node(node) {
      if (node) this.emitter.emit("searchNode", { node: node, mode: this.mode });
    },
    google_search(protein, index) {
      document.getElementById("results-" + index).setAttribute("href", "https://www.google.com/search?q=" + protein);
    },
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    },
    filt_search() {
      var com = this;
      var matches = [];

      if (com.search_raw.length >= 2) {
        var regex = new RegExp(com.regex, "i");
        matches = com.data.nodes.filter(function (node) {
          return regex.test(node.label) || regex.test(node.attributes.Alias);
        });
      }
      return matches;
    },
  },
};
</script>