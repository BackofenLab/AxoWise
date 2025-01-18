<template>
  <ListActionHeader :title="`List of enrichment graph`">
    <Button severity="secondary" rounded size="small" plain v-on:click="bookmark_off = !bookmark_off" class="w-8 h-8"
      v-tooltip.bottom="{ value: bookmark_off ? 'Show only favorites' : 'Show all', pt: { text: '!text-sm' } }">
      <span :class="`material-symbols-rounded text-2xl
          ${bookmark_off ? '' : 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400'}`">
        star
      </span>
    </Button>

    <Button v-if="mode == 'protein'" severity="secondary" label="Generate enrichment" icon="pi pi-plus" size="small"
      :loading="loading_state" v-on:click="get_term_graph()" />
  </ListActionHeader>

  <PathwayGraph :mode="mode" :gephi_data="gephi_data" :filtered_terms="filtered_terms" :bookmark_off="bookmark_off"
    @loading_state_changed="loading_state = $event"></PathwayGraph>
</template>

<script>
import PathwayGraph from "@/components/enrichment/graph/PathwayGraph.vue";
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";

export default {
  name: "PathwayTools",
  props: ["gephi_data", "filtered_terms", "favourite_pathways", "mode"],
  components: {
    PathwayGraph,
    ListActionHeader
  },
  data() {
    return {
      bookmark_off: true,
      loading_state: false,
    };
  },
  methods: {
    get_term_graph() {
      var com = this;

      if (com.loading_state) return;

      com.loading_state = true;
      this.emitter.emit("generateGraph");
    },
  },
};
</script>