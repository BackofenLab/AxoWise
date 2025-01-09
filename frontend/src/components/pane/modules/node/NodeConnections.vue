<template>
  <p v-if="!filt_links?.length" class="flex items-center justify-center py-1 text-sm text-slate-300">No nodes
  </p>

  <Listbox v-if="filt_links?.length" optionLabel="" :options="filt_links" :pt="{
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
          class="grid grid-cols-12 items-center gap-2 py-2 bg-[var(--card-bg)] shadow-[0_10px_30px_-18px_#34343D] dark:shadow-[0_10px_30px_-18px_#ffffff] z-[1]">

          <a class="flex items-center justify-start col-span-6 gap-1 text-sm cursor-pointer" v-on:click="
            sort_node = sort_node === 'asc' ? 'dsc' : 'asc';
          sort_cluster = '';
          sort_degree = '';
          ">
            Nodes
            <span :class="`material-symbols-rounded text-sm cursor-pointer 
            ${sort_node ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_node ? "swap_vert" : sort_node === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center justify-center col-span-3 gap-1 text-sm text-center cursor-pointer" v-on:click="
            sort_cluster = sort_cluster === 'asc' ? 'dsc' : 'asc';
          sort_node = '';
          sort_degree = '';
          ">
            Cluster
            <span :class="`material-symbols-rounded text-sm cursor-pointer 
            ${sort_cluster ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_cluster ? "swap_vert" : sort_cluster === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center justify-center col-span-3 gap-1 text-sm text-center cursor-pointer" v-on:click="
            sort_degree = sort_degree === 'asc' ? 'dsc' : 'asc';
          sort_cluster = '';
          sort_node = '';
          ">
            Degree
            <span :class="`material-symbols-rounded text-sm cursor-pointer 
            ${sort_degree ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_degree ? "swap_vert" : sort_degree === "asc" ? "south" : "north" }}
            </span>
          </a>
        </div>
      </header>
    </template>
    <!-- options -->
    <template #option="slotProps">
      <div :class="`grid items-center w-full grid-cols-12 gap-2`">
        <span class="col-span-6 text-xs line-clamp-2">{{ slotProps.option?.attributes?.["Name"] }}</span>

        <span class="col-span-3 text-xs text-center">{{ slotProps.option?.attributes?.["Modularity Class"] }}</span>

        <span class="col-span-3 text-xs text-center">{{ slotProps.option?.attributes?.["Degree"] }}</span>
      </div>
    </template>
  </Listbox>

  <!-- <div id="connect" class="connect">
    <div class="sorting">
      <a class="node_filter" v-on:click="
        sort_node = sort_node === 'asc' ? 'dsc' : 'asc';
      sort_cluster = '';
      sort_degree = '';
      ">nodes</a>
      <a class="cluster_filter" v-on:click="
        sort_cluster = sort_cluster === 'asc' ? 'dsc' : 'asc';
      sort_node = '';
      sort_degree = '';
      ">cluster</a>
      <a class="degree_filter" v-on:click="
        sort_degree = sort_degree === 'asc' ? 'dsc' : 'asc';
      sort_cluster = '';
      sort_node = '';
      ">degree</a>
    </div>
    <div class="network-results" tabindex="0" @keydown="handleKeyDown">
      <table>
        <tbody>
          <tr v-for="(entry, index) in filt_links" :key="index" class="option">
            <td>
              <div class="statistics-attr">
                <a href="#">{{ entry.attributes["Name"] }}</a>
              </div>
            </td>
            <td>
              <a class="statistics-val">{{
                entry.attributes["Modularity Class"]
                }}</a>
            </td>
            <td>
              <a class="statistics-val">{{ entry.attributes["Degree"] }}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div> -->
</template>

<script>

export default {
  name: "NodeConnections",
  props: ["active_node", "links"],
  data() {
    return {
      sort_node: "",
      sort_cluster: "",
      sort_degree: "",
    };
  },

  computed: {
    filt_links() {
      var com = this;
      var filtered = com.links;

      if (com.sort_node == "asc") {
        filtered.sort(function (t1, t2) {
          return t1.attributes["Name"].toLowerCase() >
            t2.attributes["Name"].toLowerCase()
            ? 1
            : t1.attributes["Name"].toLowerCase() ===
              t2.attributes["Name"].toLowerCase()
              ? 0
              : -1;
        });
      } else if (com.sort_node == "dsc") {
        filtered.sort(function (t1, t2) {
          return t2.attributes["Name"].toLowerCase() >
            t1.attributes["Name"].toLowerCase()
            ? 1
            : t1.attributes["Name"].toLowerCase() ===
              t2.attributes["Name"].toLowerCase()
              ? 0
              : -1;
        });
      }

      if (com.sort_cluster == "asc") {
        filtered.sort(
          (t1, t2) =>
            t2.attributes["Modularity Class"] -
            t1.attributes["Modularity Class"]
        );
      } else if (com.sort_cluster == "dsc") {
        filtered.sort(
          (t1, t2) =>
            t1.attributes["Modularity Class"] -
            t2.attributes["Modularity Class"]
        );
      }

      if (com.sort_degree == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["Degree"] - t1.attributes["Degree"]
        );
      } else if (com.sort_degree == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["Degree"] - t2.attributes["Degree"]
        );
      }
      return filtered;
      // return new Set(filtered);
    },
  },
};
</script>

<!-- <style>
#connect {
  width: 100%;
  height: 100%;
  font-family: "ABeeZee", sans-serif;
  padding: 1.3vw 1.3vw 1vw 1.3vw;
}

.connect .network-results {
  width: 100%;
  height: 100%;
  overflow: scroll;
}

.connect .sorting {
  font-size: 0.53vw;
  display: flex;
  border-bottom: 1px solid;
  border-color: white;
  cursor: default;
}

:focus {
  outline: 0 !important;
}

.connect td:first-child {
  width: 50%;
  font-size: 0.6vw;
  align-self: center;
  white-space: nowrap;
  overflow: hidden;
  /* Hide overflow content */
  text-overflow: ellipsis;
}

.connect td:nth-child(2) {
  width: 25%;
  font-size: 0.6vw;
  align-self: center;
}

.connect td:last-child {
  font-size: 0.5vw;
  margin-bottom: 1%;
  color: white;
  width: 25%;
  align-self: center;
}

.node_filter {
  width: 50%;
}

.cluster_filter {
  width: 25%;
}

.degree_filter {
  width: 25%;
}
</style> -->
