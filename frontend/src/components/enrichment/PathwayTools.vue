<template>
  <ListActionHeader :title="`List of enrichment graph`">
    <Button severity="secondary" rounded size="small" plain v-on:click="bookmark_off = !bookmark_off" class="w-8 h-8"
      v-tooltip.bottom="bookmark_off ? 'Show only favorites' : 'Show all'">
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

  <!-- <div id="pathways-graphs">
    <div class="tool-section-graph">
      <div class="coloumn-button">
        <button class="tool-buttons" v-show="tool == 'Termgraph'" v-on:click="get_term_graph()">
          <img class="buttons-img" src="@/assets/plus-1.png" v-if="!loading_state" />
          <div v-if="loading_state" class="loading_button"></div>
        </button>
      </div>
      <div class="coloumn-button">
        <button class="tool-buttons" :class="{ recolor_filter: bookmark_off == false }"
          v-on:click="bookmark_off = !bookmark_off">
          <img class="buttons-img" src="@/assets/star.png" />
        </button>
      </div>
    </div>
    <div class="graph-section">
      <PathwayGraph v-show="tool == 'Termgraph'" :mode="mode" :gephi_data="gephi_data" :filtered_terms="filtered_terms"
        :bookmark_off="bookmark_off" @loading_state_changed="loading_state = $event"></PathwayGraph>
    </div>
  </div> -->
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
      // tool: "Termgraph",
      // favourite_graphs: new Set(),
      bookmark_off: true,
      // tool_selecting: false,
      // tools: [{ id: "Termgraph" }, { id: "Heatmap" }],
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

<!-- <style>
#pathways-graphs {
  width: 100%;
  height: 100%;
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: "ABeeZee", sans-serif;
}

.generate {
  width: 50%;
  cursor: default;
  background: #d9d9d9;
}

.generate .generate-text {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0a0a1a;
  font-size: 0.7vw;
}

.export-heatmap {
  position: absolute;
  cursor: default;
}

.export-heatmap .generate-text {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.95vw;
}

.bookmark-button-graph {
  background: #d9d9d9;
  width: 2.5vw;
  align-content: center;
  justify-content: center;
}

#pathway-tools-filter {
  width: 17.81%;
  height: 11.16%;
  display: flex;
  position: absolute;
  border-radius: 5px;
  align-items: center;
  justify-content: center;
}

#pathway-tools-filter span {
  display: block;
  width: 90%;
  font-size: 0.95vw;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: default;
  text-align: center;
}

#pathway-tools-filter-categories {
  display: flex;
  position: fixed;
  width: 20%;
  height: 30.32%;
  left: -1.5%;
  top: 15%;
  padding: 1% 0% 1% 0%;
  border-radius: 5px;
  border: 1px solid #fff;
  z-index: 1;
  justify-content: center;
  overflow-x: scroll;
  overflow-y: hidden;
  cursor: default;
}

#pathway-tools-filter-categories .element {
  border-radius: 5px;
  background: rgba(217, 217, 217, 0.17);
  display: flex;
  width: 36.88%;
  height: 100%;
  margin: 0% 2% 0% 2%;
  overflow: hidden;
}

#pathway-tools-filter-categories .element:hover {
  background: rgba(217, 217, 217, 0.47);
}

.tool-section-graph {
  display: grid;
  grid-template-columns: 0.5fr 0.5fr 0.7fr 0.7fr 0.7fr 0.7fr;
  padding: 0.5vw 1vw 0.5vw 1vw;
  width: 100%;
  flex-shrink: 0;
  /* Prevents the tool-section-graph from shrinking */
}

.tool-section-term {
  display: inline-flex;
  margin: 1vw 0 1vw 0;
  height: 1vw;
  width: 100%;
  align-items: center;
  justify-content: center;
}

.coloumn-button {
  padding: 0.5vw;
  display: grid;
  row-gap: 1vw;
  z-index: 9999;
}

.tool-buttons {
  min-width: 2rem;
  padding: 0.2vw 0 0.2vw 0;
  border-radius: 0;
  cursor: pointer;
  display: flex;
  font-size: 0.7vw;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  justify-content: center;
  border: 0.05vw solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 6px -3px rgba(255, 255, 255, 0.23);
  transition: transform 0.25s cubic-bezier(0.7, 0.98, 0.86, 0.98),
    box-shadow 0.25s cubic-bezier(0.7, 0.98, 0.86, 0.98);
  background-color: #0a0a1a;
}

.tool-buttons:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 6px -1.5px rgba(255, 255, 255, 0.23);
}

.loading_button {
  position: relative;
  display: flex;
  width: 100%;
  height: 100%;
  text-align: center;
  justify-content: center;
}

.loading_button::after {
  content: "";
  position: absolute;
  width: 12px;
  height: 12px;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;
  border: 4px solid transparent;
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: button-loading-spinner 1s ease infinite;
}

.graph-section {
  flex-grow: 1;
  overflow-y: auto;
  position: relative;
  padding: 0.5vw;
}

.buttons-img {
  width: 0.6vw;
  height: 0.6vw;
  filter: invert(80%);
}
</style> -->
