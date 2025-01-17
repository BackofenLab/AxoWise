<template>
  <p v-if="!filt_links?.length" class="flex items-center justify-center py-1 text-sm text-slate-300">No proteins
  </p>

  <Listbox v-if="filt_links?.length" optionLabel="" :options="filt_links" :pt="{
    listContainer: { class: 'order-2' },
    list: { class: '!p-0' },
    emptyMessage: { class: '!flex !justify-center !items-center !text-sm !text-slate-500 dark:!text-slate-300' },
    option: {
      class:
        '!px-0 !py-1 !text-slate-500 dark:!text-slate-300 leading-tight transition-all duration-300 ease-in-out',
    },
  }" :virtualScrollerOptions="{ itemSize: 28 }" scrollHeight="4.5rem" listStyle="max-height:100%" class="h-full flex flex-col !p-0 !bg-transparent !border-0" :tabindex="0"
    emptyMessage="No proteins available.">

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
        <span class="col-span-6 text-xs line-clamp-1">{{ slotProps.option?.attributes?.["Name"] }}</span>

        <span class="col-span-3 text-xs text-center line-clamp-1">{{ slotProps.option?.attributes?.["Modularity Class"] }}</span>

        <span class="col-span-3 text-xs text-center line-clamp-1">{{ slotProps.option?.attributes?.["Degree"] }}</span>
      </div>
    </template>
  </Listbox>
</template>

<script>
import { useToast } from "primevue/usetoast";
export default {
  name: "LayerProteins",
  props: ["active_termlayers", "gephi_data"],
  data() {
    return {
      intersectionSet: new Set(),
      hiding_terms: this.$store.state.hiding_pathways,
      sort_node: "",
      sort_cluster: "",
      sort_degree: "",
    };
  },
  watch: {
    active_termlayers: {
      handler(newList) {
        var com = this;

        if (newList == null) {
          return;
        }

        com.hiding_terms = com.$store.state.hiding_pathways;

        com.intersectionSet = new Set();
        var intersectionSet = new Set();

        for (var checkElement of com.active_termlayers.main) {
          if (
            !com.hiding_terms.has(checkElement) &&
            com.active_termlayers.main.size >= 1
          ) {
            intersectionSet = new Set(checkElement.symbols);
            break;
          }
        }

        for (var element of com.active_termlayers.main) {
          if (!com.hiding_terms.has(element)) {
            intersectionSet = new Set(
              element.symbols.filter((value) => intersectionSet.has(value))
            );
          }
        }

        for (var proteins of this.gephi_data.nodes) {
          if (intersectionSet.has(proteins.attributes["Name"])) {
            com.intersectionSet.add(proteins);
          }
        }
      },
      deep: true,
    },
  },
  methods: {
    select_node(value) {
      this.emitter.emit("searchNode", value);
    },
    copyclipboard() {
      var com = this;

      var textToCopy = [];
      for (var link of com.intersectionSet) textToCopy.push(link.label);
      navigator.clipboard.writeText(textToCopy.join("\n"));
      this.toast.add({ severity: 'success', detail: 'Message copied to clipboard.', life: 4000 });
    },
  },
  mounted() {
    this.toast = useToast();
    this.emitter.on("copyLayerConnections", () => {
      this.copyclipboard();
    });
  },
  computed: {
    filt_links() {
      var com = this;
      var filtered = [...com.intersectionSet];

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
