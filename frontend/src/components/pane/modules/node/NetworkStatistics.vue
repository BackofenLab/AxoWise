<template>
  <ul class="list-none p-0 m-0 flex flex-col divide-y dark:divide-[#343b4c]">
    <li class="grid grid-cols-2 gap-1.5 py-1 dark:text-[#c3c3c3]" v-for="(key, entry, index) in statistics"
      :key="index">
      <strong class="text-sm font-normal dark:text-slate-400">{{ entry }}</strong>
      <span class="text-sm break-all">{{ key }}</span>
    </li>
  </ul>
</template>

<script>
export default {
  name: "NetworkStatistics",
  props: ["active_node", "mode"],
  data() {
    return {
      statistics: {},
    };
  },
  watch: {
    active_node() {
      var com = this;

      if (com.active_node == null) {
        return;
      }

      let {
        Degree,
        "Ensembl ID": EnsemblID,
        "Betweenness Centrality": BetweenesCentrality,
        "Modularity Class": Cluster,
        PageRank,
        Category,
        FDR,
        Alias,
      } = com.active_node.attributes;
      PageRank = Math.abs(PageRank).toExponential(2);
      FDR = Math.abs(FDR).toExponential(2);
      if (this.mode == "protein")
        com.statistics = {
          Cluster,
          Degree,
          EnsemblID,
          BetweenesCentrality,
          PageRank,
          Alias,
        };
      else
        com.statistics = {
          Cluster,
          Degree,
          EnsemblID,
          Category,
          BetweenesCentrality,
          PageRank,
          FDR,
        };
      if (com.$store.state.dcoloumns != null) {
        com.$store.state.dcoloumns.forEach((dcoloumn) => {
          com.statistics[dcoloumn] = com.active_node.attributes[dcoloumn];
        });
      }
    },
  },
};
</script>