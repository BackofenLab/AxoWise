<template>
  <ListActionHeader title="List of selected path layers">
    <Button class="flex-shrink-0" severity="primary" label="Add path layers" icon="pi pi-plus" size="small" raised
      v-on:click="call_layers()" />
  </ListActionHeader>

  <ul class="p-0 m-0 list-none">
    <li
      class="w-full h-9 grid grid-cols-12 items-center gap-2 !py-0 !px-0 !font-normal !text-slate-500 dark:!text-slate-300 !leading-tight"
      v-for="entry in terms" :key="entry">
      <label class="col-span-9">{{ entry.name }}</label>
      <span class="w-4 h-4 col-start-11 rounded-full cursor-pointer" id="color_rect" @click="open_picker($event, entry)"
        :style="{ backgroundColor: colorpalette[entry.name] }"></span>
      <Button severity="secondary" rounded size="small" plain class="w-5 h-5" @click="hide_termlayer(entry)"
        v-tooltip.bottom="hiding_terms.has(entry) ? 'Show' : 'Hide'">
        <span class="text-xl material-symbols-rounded">
          {{ hiding_terms.has(entry) ? "visibility_off" : "visibility" }}
        </span>
      </Button>
    </li>
  </ul>

  <Dialog v-model:visible="color_picker" :header="`${active_term?.name || ''}`" position="top" :minY="60" :minX="60"
    :pt="{
      root: { class: 'w-[20rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-sm' },
      content: { class: 'flex' },
    }">
    <Sketch id="color-picker" class="flex-1 !p-0 !bg-transparent !shadow-none" v-model="colors"
      @update:model-value="handleColorChange(active_term)" />
  </Dialog>
</template>

<script>
import { Sketch } from "@ckpack/vue-color";
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";

export default {
  name: "PathwayLayers",
  props: ["active_termlayers", "gephi_data"],
  components: {
    Sketch,
    ListActionHeader,
  },
  data() {
    return {
      terms: null,
      colorpalette: null,
      hiding_terms: this.$store.state.hiding_pathways,
      color_picker: false,
      active_term: null,
      colors: "rgba(0,0,0,1)",
    };
  },
  watch: {
    active_termlayers: {
      handler(newList) {
        var com = this;

        if (newList == null) {
          com.terms = null;
          return;
        }

        com.colorpalette = com.$store.state.colorpalette;
        com.terms = newList.main;
        com.hiding_terms = com.$store.state.hiding_pathways;
      },
      deep: true,
    },
  },
  methods: {
    call_layers() {
      var com = this;
      com.emitter.emit("visualizeLayer");
    },
    handleColorChange(term) {
      var com = this;

      const colorObject = com.colors["rgba"];
      com.colorpalette[
        term.name
      ] = `rgb(${colorObject.r},${colorObject.g},${colorObject.b})`;

      this.$store.commit("assign_colorpalette", com.colorPalette);

      this.emitter.emit("hideTermLayer", {
        main: com.terms,
        hide: com.hiding_terms,
      });
    },
    open_picker(event, term) {
      var com = this;

      console.log("in");
      com.color_picker = true;
      com.active_term = term;
      com.colors = this.colorpalette[term.name];
    },
    hide_termlayer(term) {
      var com = this;
      console.log("in2");

      if (com.hiding_terms.has(term)) com.hiding_terms.delete(term);
      else com.hiding_terms.add(term);

      this.$store.commit("assign_hiding_pathways", com.hiding_terms);
      this.emitter.emit("hideTermLayer", {
        main: com.terms,
        hide: com.hiding_terms,
      });
    },
    select_enrichment(value) {
      this.emitter.emit("searchEnrichment", value);
    },
  },
};
</script>