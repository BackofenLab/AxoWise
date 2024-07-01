<template>
  <div id="pathway-layer-connect" class="connect">
    <div class="sorting">
      <a class="enrichment_filter">pathway</a>
      <a class="cluster_filter">pathway</a>
    </div>

    <div class="network-results" tabindex="0" @keydown="handleKeyDown">
      <table>
        <tbody>
          <tr v-for="entry in intersectingDicts" :key="entry" class="option">
            <td>
              <div class="statistics-attr">
                <a href="#">{{ entry[0].name }}</a>
              </div>
            </td>
            <td>
              <a class="statistics-val">{{ entry[1].name }}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "EnrichmentConnections",
  props: ["active_termlayers", "gephi_data"],
  components: {},
  data() {
    return {
      intersectingDicts: null,
    };
  },
  watch: {
    active_termlayers: {
      handler(newList) {
        var com = this;

        if (newList == null) {
          return;
        }

        // Find intersecting dictionaries
        com.intersectingDicts = this.findIntersectingDictionaries(
          com.active_termlayers.main
        );
      },
      deep: true,
    },
  },
  methods: {
    findIntersectingDictionaries(mySet) {
      const result = [];
      const arr = Array.from(mySet);
      for (let i = 0; i < arr.length; i++) {
        for (let j = i + 1; j < arr.length; j++) {
          const dict1 = arr[i];
          const dict2 = arr[j];
          if (this.intersectingElements(dict1.symbols, dict2.symbols)) {
            result.push([dict1, dict2]);
          }
        }
      }
      return result;
    },

    // Helper function to check if arrays have intersecting elements
    intersectingElements(arr1, arr2) {
      for (let i = 0; i < arr1.length; i++) {
        if (arr2.includes(arr1[i])) {
          return true;
        }
      }
      return false;
    },
  },
};
</script>

<style>
#pathway-layer-connect {
  width: 100%;
  height: 100%;
  font-family: "ABeeZee", sans-serif;
  padding: 1.3vw 1.3vw 1vw 1.3vw;
}

#pathway-layer-connect .pane_values {
  position: absolute;
  left: 50.5%;
}
#pathway-layer-connect .statistics-val {
  left: 50.6%;
}
#pathway-layer-connect .statistics-attr a {
  align-self: center;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
}
#pathway-layer-connect .network-results td:first-child {
  margin-left: 0.5%;
  font-size: 0.7vw;
  margin-bottom: 1%;
  color: white;
  width: 50%;
  align-self: center;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
}
#pathway-layer-connect .network-results td:last-child {
  font-size: 0.7vw;
  margin-bottom: 1%;
  color: white;
  width: 50%;
  align-self: center;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
}
</style>
