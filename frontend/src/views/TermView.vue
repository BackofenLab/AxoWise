<template>
  <keep-alive>
    <AppBar :gephi_data="term_data" :filter_views="filter_views" :mode="mode" @widget_toggled="widget = $event"
      :widget="widget" :view="view">
    </AppBar>
  </keep-alive>
  <keep-alive>
    <TermPaneSystem :gephi_data="term_data" :active_node="active_node" @active_node_changed="active_node = $event"
      :active_subset="active_subset" @active_subset_changed="active_subset = $event"
      @active_layer_changed="active_layer = $event" @active_combine_changed="active_combine = $event"
      :node_color_index="node_color_index"></TermPaneSystem>
  </keep-alive>
  <main class="h-[calc(100vh-65px)] flex flex-1">
    <keep-alive>
      <MainToolBar :mode="mode" :gephi_data="term_data" :active_subset="active_subset" :active_term="null"
        :ensembl_name_index="null" :widget="widget"></MainToolBar>
    </keep-alive>
    <keep-alive>
      <!-- <VerticalPane :mode="mode" :gephi_data="term_data" :active_node="null" :active_background="null"
        :active_termlayers="null" :active_decoloumn="null"></VerticalPane> -->
    </keep-alive>
    <keep-alive>
      <TermVis ref="termVis" :active_node="active_node" @active_node_changed="active_node = $event"
        :active_fdr="active_fdr" @active_fdr_changed="active_fdr = $event" :active_subset="active_subset"
        @active_subset_changed="active_subset = $event" :active_layer="active_layer"
        @active_layer_changed="active_layer = $event" :subactive_subset="subactive_subset" :term_data="term_data"
        :active_combine="active_combine" :centering_active="centering_active" :node_color_index="node_color_index"
        :edge_color_index="edge_color_index" :node_size_index="node_size_index" :node_modul_index="node_modul_index"
        :unconnected_nodes="unconnected_nodes"></TermVis>
    </keep-alive>
  </main>
  <!-- <keep-alive>
    <div class="term-view">
      <ExportScreen :mode="mode" :filter_views="filter_views"></ExportScreen>
      <TermVis
        ref="termVis"
        :active_node="active_node"
        @active_node_changed="active_node = $event"
        :active_fdr="active_fdr"
        @active_fdr_changed="active_fdr = $event"
        :active_subset="active_subset"
        @active_subset_changed="active_subset = $event"
        :active_layer="active_layer"
        @active_layer_changed="active_layer = $event"
        :subactive_subset="subactive_subset"
        :term_data="term_data"
        :active_combine="active_combine"
        :centering_active="centering_active"
        :node_color_index="node_color_index"
        :edge_color_index="edge_color_index"
        :node_size_index="node_size_index"
        :node_modul_index="node_modul_index"
        :unconnected_nodes="unconnected_nodes"
      ></TermVis>
      <VerticalPanePathway :term_data="term_data"></VerticalPanePathway>
      <TermToolBar
        :data="term_data"
        :active_subset="active_subset"
      ></TermToolBar>
      <NetworkValues :data="term_data"></NetworkValues>
      <div id="view" class="filter-section">
        <div
          id="pathway-filter"
          class="pre-full"
          v-on:click="handling_filter_menu()"
          :class="{ full: view_filtering == true }"
        >
          <span>{{ view }}</span>
        </div>
        <div id="list-filter-categories" v-show="view_filtering == true">
          <div
            class="element"
            v-for="entry in filter_views"
            :key="entry"
            v-on:click="swap_view(entry)"
          >
            <a>{{ entry + " view" }} </a>
          </div>
        </div>
      </div>
      <TermPaneSystem
        :gephi_data="term_data"
        :active_node="active_node"
        @active_node_changed="active_node = $event"
        :active_subset="active_subset"
        @active_subset_changed="active_subset = $event"
        @active_layer_changed="active_layer = $event"
        @active_combine_changed="active_combine = $event"
        :node_color_index="node_color_index"
      ></TermPaneSystem>
    </div>
  </keep-alive> -->
</template>

<script>
import AppBar from "@/layout/AppBar.vue";
import MainToolBar from "@/layout/MainToolBar.vue";
// import VerticalPane from "@/layout/VerticalPane.vue";
import TermPaneSystem from "@/components/pane/TermPaneSystem.vue";
import TermVis from "@/components/visualization/TermVis.vue";
// import NetworkValues from "../components/interface/NetworkValues.vue";
// import TermToolBar from "../components/toolbar/TermToolBar.vue";
// import VerticalPanePathway from "@/components/verticalpane/VerticalPanePathway.vue";
// import ExportScreen from "@/components/toolbar/modules/ExportScreen.vue";

export default {
  name: "TermView",
  components: {
    AppBar,
    MainToolBar,
    // VerticalPane,
    TermPaneSystem,
    TermVis,
    // NetworkValues,
    // TermToolBar,
    // VerticalPanePathway,
    // ExportScreen,
  },
  data() {
    return {
      term_data: this.$store.state.term_graph_data.graph,
      active_node: null,
      active_layer: null,
      active_fdr: null,
      active_subset: null,
      subactive_subset: null,
      active_combine: null,
      node_color_index: null,
      edge_color_index: null,
      node_size_index: null,
      centering_active: null,
      unconnected_nodes: null,
      view: "term view",
      // view_filtering: false,
      widget: true,
      mode: "term",
      filter_views: ["protein", "citation"],
    };
  },
  watch: {
    term_data() {
      const com = this;

      com.node_color_index = {};
      for (var idx in com.term_data.nodes) {
        var node = com.term_data.nodes[idx];
        com.node_color_index[node.id] = node.color;
      }

      com.node_size_index = {};
      for (var idz in com.term_data.nodes) {
        var nodeZ = com.term_data.nodes[idz];
        com.node_size_index[nodeZ.id] = nodeZ.size;
      }

      com.edge_color_index = {};
      for (var idy in com.term_data.edges) {
        var edge = com.term_data.edges[idy];
        com.edge_color_index[edge.id] = edge.color;
      }

      com.node_cluster_index = {};
      for (var idg in com.term_data.nodes) {
        var nodeG = com.term_data.nodes[idg];
        var modularityClass = nodeG.attributes["Modularity Class"];
        if (!com.node_cluster_index[modularityClass])
          com.node_cluster_index[modularityClass] = new Set();
        com.node_cluster_index[modularityClass].add(nodeG.attributes["Name"]);
      }
      this.$store.commit("assign_moduleCluster_term", com.node_cluster_index);

      com.node_modul_index = new Set();
      for (var idm in com.unconnected_nodes) {
        var node_m = com.unconnected_nodes[idm];
        com.node_modul_index.add(node_m.attributes["Modularity Class"]);
      }
      this.$store.commit("assign_moduleIndex_term", com.node_modul_index);

      const maingraph = new Set(com.term_data.subgraph);
      com.unconnected_nodes = com.term_data.nodes.filter(
        (item) => !maingraph.has(item.id)
      );
    },
  },
  activated() {
    this.change_graph();
  },
  mounted() {
    const com = this;

    com.active_subset = null;

    com.node_color_index = {};
    for (var idx in com.term_data.nodes) {
      var node = com.term_data.nodes[idx];
      com.node_color_index[node.id] = node.color;
    }

    com.node_size_index = {};
    for (var idz in com.term_data.nodes) {
      var nodeZ = com.term_data.nodes[idz];
      com.node_size_index[nodeZ.id] = nodeZ.size;
    }

    com.edge_color_index = {};
    for (var idy in com.term_data.edges) {
      var edge = com.term_data.edges[idy];
      com.edge_color_index[edge.id] = edge.color;
    }

    com.node_cluster_index = {};
    for (var idg in com.term_data.nodes) {
      var nodeG = com.term_data.nodes[idg];
      var modularityClass = nodeG.attributes["Modularity Class"];
      if (!com.node_cluster_index[modularityClass])
        com.node_cluster_index[modularityClass] = new Set();
      com.node_cluster_index[modularityClass].add(nodeG.attributes["Name"]);
    }
    this.$store.commit("assign_moduleCluster_term", com.node_cluster_index);

    com.node_modul_index = new Set();
    for (var idm in com.unconnected_nodes) {
      var node_m = com.unconnected_nodes[idm];
      com.node_modul_index.add(node_m.attributes["Modularity Class"]);
    }
    this.$store.commit("assign_moduleIndex_term", com.node_modul_index);

    const maingraph = new Set(com.term_data.subgraph);
    com.unconnected_nodes = com.term_data.nodes.filter(
      (item) => !maingraph.has(item.id)
    );

    this.emitter.on("graphChanged", () => {
      this.change_graph();
    });
  },
  methods: {
    change_graph() {
      this.term_data = this.$store.state.term_graph_data.graph;

      const term_node = this.$store.state.active_node_enrichment;
      if (term_node != null) {
        for (var idx in this.term_data.nodes) {
          var node = this.term_data.nodes[idx];
          if (node.attributes["Ensembl ID"] == term_node.id) {
            this.active_node = this.term_data.nodes[idx];
          }
        }
        this.$store.commit("assign_active_enrichment_node", null);
      }
    },
    // handling_filter_menu() {
    //   var com = this;
    //   if (!com.view_filtering) {
    //     com.view_filtering = true;

    //     // Add the event listener
    //     document.addEventListener("mouseup", com.handleMouseUp);
    //   } else {
    //     com.view_filtering = false;
    //     document.removeEventListener("mouseup", com.handleMouseUp);
    //   }
    // },
    // handleMouseUp(e) {
    //   var com = this;

    //   var container = document.getElementById("list-filter-categories");
    //   var container_button = document.getElementById("pathway-filter");
    //   if (
    //     !container.contains(e.target) &&
    //     !container_button.contains(e.target)
    //   ) {
    //     com.view_filtering = false;

    //     // Remove the event listener
    //     document.removeEventListener("mouseup", com.handleMouseUp);
    //   }
    // },
    // swap_view(entry) {
    //   if (entry == "protein") {
    //     this.$router.push("protein");
    //   }
    //   if (entry == "citation") {
    //     this.$store.state.citation_graph_data
    //       ? this.$router.push("citation")
    //       : alert(
    //         "Please generate first a citation graph via the citation section on protein view."
    //       );
    //   }
    // },
  },
};
</script>

<!-- <style>
.term-view {
  background-color: #0a1308;
  display: flex;
}

.term-view .colortype {
  background: #0a1308;
}
</style> -->
