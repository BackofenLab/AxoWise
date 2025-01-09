<template>
  <Listbox v-if="intersectingDicts?.length" optionLabel="" :options="intersectingDicts" :pt="{
    listContainer: { class: 'order-2' },
    list: { class: '!p-0' },
    emptyMessage: { class: '!flex !justify-center !items-center !text-sm !text-slate-500 dark:!text-slate-300' },
    option: {
      class:
        '!px-0 !py-1 !text-slate-500 dark:!text-slate-300 leading-tight transition-all duration-300 ease-in-out',
    },
  }" listStyle="max-height:100%" class="h-full flex flex-col !p-0 !bg-transparent !border-0" :tabindex="0"
    emptyMessage="No nodes available.">

    <template #footer>
      <header class="sticky -top-2 bg-[var(--card-bg)] items-center gap-2 z-[1] order-1">
        <!-- sorting -->
        <div
          class="grid grid-cols-2 py-1 bg-[var(--card-bg)] shadow-[0_10px_30px_-18px_#34343D] dark:shadow-[0_10px_30px_-18px_#ffffff] z-[1]">

          <a class="text-sm">
            Pathway
          </a>

          <a class="text-sm">
            Pathway
          </a>
        </div>
      </header>
    </template>
    <!-- options -->
    <template #option="slotProps">
      <div :class="`grid items-center w-full grid-cols-2 gap-2`">
        <span class="text-xs line-clamp-2">{{ slotProps.option?.[0]?.name }}</span>

        <span class="text-xs line-clamp-2">{{ slotProps.option?.[1]?.name }}</span>
      </div>
    </template>
  </Listbox>

  <!-- <div id="pathway-layer-connect" class="connect">
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
  </div> -->
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

<!-- <style>
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
</style> -->
