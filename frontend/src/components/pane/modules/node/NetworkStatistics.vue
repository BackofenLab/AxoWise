<template>
  <div id="statistics">
    <div class="network-results" tabindex="0" @keydown="handleKeyDown">
      <table>
        <tbody>
          <tr
            v-for="(key, entry, index) in statistics"
            :key="index"
            class="option"
          >
            <td>
              <div class="statistics-attr">
                <a href="#">{{ entry }}</a>
              </div>
            </td>
            <td>
              <a class="statistics-val">{{ key }}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
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

<style>
#statistics {
  width: 100%;
  height: 100%;
  font-family: "ABeeZee", sans-serif;
  padding: 1.3vw;
}

.pane_values {
  position: absolute;
  left: 68.5%;
}

.statistics-attr {
  display: flex;
  height: 1vw;
  width: 80%;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
  margin-left: 2%;
}

.statistics-attr a {
  cursor: default;
  color: white;
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

#statistics .network-results {
  overflow: scroll;
}

.network-results::-webkit-scrollbar {
  display: none;
}

.statistics-val {
  left: 90.6%;
}

.network-results table {
  display: flex;
  width: 100%;
}

:focus {
  outline: 0 !important;
}

.network-results table tbody {
  width: 100%;
}
.network-results td:first-child {
  width: 50%;
  font-size: 0.6vw;
  align-self: center;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
}
.network-results td:last-child {
  font-size: 0.5vw;
  margin-bottom: 1%;
  color: white;
  width: 50%;
  align-self: center;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
}
</style>
