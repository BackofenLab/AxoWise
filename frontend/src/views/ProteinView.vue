<template>
  <keep-alive>
    <AppBar :gephi_data="gephi_data" :filter_views="filter_views" :mode="mode" @widget_toggled="widget = $event"
      :widget="widget" :view="view">
    </AppBar>
  </keep-alive>
  <keep-alive>
    <PaneSystem :active_node="active_node" @active_node_changed="active_node = $event" :active_term="active_term"
      @active_term_changed="active_term = $event" :active_background="active_background"
      @active_background_changed="active_background = $event" :active_subset="active_subset"
      @active_subset_changed="active_subset = $event" :active_decoloumn="active_decoloumn"
      @active_decoloumn_changed="active_decoloumn = $event" :active_termlayers="active_termlayers"
      @active_termlayers_changed="active_termlayers = $event" @active_layer_changed="active_layer = $event"
      @active_combine_changed="active_combine = $event" :gephi_data="gephi_data" :node_color_index="node_color_index">
    </PaneSystem>
  </keep-alive>
  <main class="h-[calc(100vh-65px)] flex flex-1 overflow-hidden">
    <keep-alive>
      <MainToolBar :mode="mode" :gephi_data="gephi_data" :active_subset="active_subset" :active_term="active_term"
        :ensembl_name_index="ensembl_name_index" :widget="widget"></MainToolBar>
    </keep-alive>

    <keep-alive>
      <VerticalPane :mode="mode" :gephi_data="gephi_data" :active_node="active_node"
        :active_background="active_background" :active_termlayers="active_termlayers"
        :active_decoloumn="active_decoloumn"></VerticalPane>
    </keep-alive>

    <keep-alive>
      <MainVis ref="mainVis" :active_node="active_node" @active_node_changed="active_node = $event"
        :active_term="active_term" @active_term_changed="active_term = $event" :active_termlayers="active_termlayers"
        @active_termlayers_changed="active_termlayers = $event" :active_layer="active_layer"
        @active_layer_changed="active_layer = $event" :active_subset="active_subset"
        @active_subset_changed="active_subset = $event" :subactive_subset="subactive_subset"
        @subactive_subset_changed="subactive_subset = $event" :gephi_data="gephi_data"
        :active_decoloumn="active_decoloumn" :unconnected_nodes="unconnected_nodes" :active_combine="active_combine"
        @active_decoloumn_changed="active_decoloumn = $event" :node_color_index="node_color_index"
        :node_size_index="node_size_index" :edge_color_index="edge_color_index" :node_modul_index="node_modul_index">
      </MainVis>
    </keep-alive>
  </main>
</template>

<script>
// @ is an alias to /src
import MainVis from "@/components/visualization/MainVis.vue";
import PaneSystem from "@/components/pane/PaneSystem.vue";
import VerticalPane from "@/layout/VerticalPane.vue";
import MainToolBar from "@/layout/MainToolBar.vue";
import AppBar from "@/layout/AppBar.vue";

export default {
  name: "ProteinView",
  components: {
    AppBar,
    MainVis,
    PaneSystem,
    MainToolBar,
    VerticalPane,
  },
  data() {
    return {
      gephi_data: this.$store.state.gephi_json.data,
      active_node: null,
      active_term: null,
      active_background: null,
      active_layer: null,
      active_combine: null,
      active_decoloumn: null,
      active_termlayers: null,
      node_color_index: null,
      node_size_index: null,
      edge_color_index: null,
      active_subset: null,
      subactive_subset: null,
      unconnected_nodes: null,
      node_modul_index: null,
      node_cluster_index: null,
      ensembl_name_index: null,
      view: "protein view",
      filter_views: ["term", "citation"],
      widget: true,
      mode: "protein",
    };
  },
  activated() {
    const term = this.$store.state.enrichment;
    const all_terms = this.$store.state.current_enrichment_terms;
    if (term != null) {
      for (var idx in all_terms) {
        var node = all_terms[idx];
        if (node.id == term) {
          this.active_term = node;
        }
      }
      this.$store.commit("assign_active_enrichment", null);
    }
  },
  mounted() {
    var com = this;

    com.ensembl_name_index = {};
    for (var ele of com.gephi_data.nodes) {
      com.ensembl_name_index[ele.attributes["Ensembl ID"]] = ele.attributes["Name"];
    }

    com.node_color_index = {};
    for (var idx in com.gephi_data.nodes) {
      var node = com.gephi_data.nodes[idx];
      com.node_color_index[node.id] = node.color;
    }

    com.node_size_index = {};
    for (var idz in com.gephi_data.nodes) {
      var nodeZ = com.gephi_data.nodes[idz];
      com.node_size_index[nodeZ.id] = nodeZ.size;
    }

    com.edge_color_index = {};
    for (var idy in com.gephi_data.edges) {
      var edge = com.gephi_data.edges[idy];
      com.edge_color_index[edge.id] = edge.color;
    }

    com.node_cluster_index = {};
    for (var idg in com.gephi_data.nodes) {
      var nodeG = com.gephi_data.nodes[idg];
      var modularityClass = nodeG.attributes["Modularity Class"];
      if (!com.node_cluster_index[modularityClass]) com.node_cluster_index[modularityClass] = new Set();
      com.node_cluster_index[modularityClass].add(nodeG.attributes["Name"]);
    }
    this.$store.commit("assign_moduleCluster", com.node_cluster_index);

    const maingraph = new Set(com.gephi_data.subgraph);
    com.unconnected_nodes = com.gephi_data.nodes.filter((item) => !maingraph.has(item.id));

    com.node_modul_index = new Set();
    for (var idm in com.unconnected_nodes) {
      var node_m = com.unconnected_nodes[idm];
      com.node_modul_index.add(node_m.attributes["Modularity Class"]);
    }
    this.$store.commit("assign_moduleIndex", com.node_modul_index);

    this.emitter.on("decoloumn", (state) => {
      com.active_decoloumn = state;
    });
  },
  methods: {},
};
</script>
