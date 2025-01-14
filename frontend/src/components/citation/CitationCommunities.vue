<template>
  <div v-if="await_load" class="flex flex-col items-center justify-center h-full gap-3">
    <h6 class="flex items-center gap-2 dark:text-slate-300">Fetching data
      <span class="relative flex">
        <span class="absolute inline-flex w-full h-full rounded-full opacity-75 animate-ping bg-primary-500"></span>
        <span
          class="material-symbols-rounded text-primary-500 animate animate-[spin_1s_ease-in-out_infinite]">scatter_plot</span>
      </span>
    </h6>
  </div>

  <EmptyState v-if="citation_data?.community_scores?.length == 0" message="There is no generated communities.">
  </EmptyState>

  <Listbox v-if="citation_data?.community_scores?.length != 0 && !await_load" v-model="selected_citation"
    optionLabel="name" :options="filt_communities" :pt="{
      listContainer: { class: 'order-2' },
      list: { class: '!p-0' },
      emptyMessage: { class: '!flex !justify-center !items-center !text-sm !text-slate-500 dark:!text-slate-300' },
      option: {
        class:
          '!px-0 !py-1 !text-slate-500 dark:!text-slate-300 leading-tight transition-all duration-300 ease-in-out',
      },
    }" :virtualScrollerOptions="{ itemSize: 28 }" listStyle="max-height:100%" class="h-full flex flex-col !p-0 !bg-transparent !border-0"
    @update:modelValue="select_community" :tabindex="0" emptyMessage="No communities available.">

    <template #footer>
      <header class="sticky top-0 bg-[var(--card-bg)] pt-3 items-center gap-2 z-[1] order-1">
        <!-- filter -->
        <InputGroup>
          <IconField class="w-full">
            <InputText v-model="search_raw" placeholder="Search abstracts" class="w-full" />
            <InputIcon class="z-10 pi pi-search" />
          </IconField>
          <InputGroupAddon>
            <Button class="w-8 h-8" icon="material-symbols-rounded" size="small" :loading="await_community" text plain
              rounded v-tooltip.bottom="'Top nodes'" @click="top_nodes(5)">
              <span class="material-symbols-rounded !text-lg">hub</span>
            </Button>
          </InputGroupAddon>
        </InputGroup>

        <!-- sorting -->
        <div
          class="grid grid-cols-12 items-center gap-2 py-2 bg-[var(--card-bg)] shadow-[0_10px_30px_-18px_#34343D] dark:shadow-[0_10px_30px_-18px_#ffffff] z-[1]">
          <a class="flex items-center justify-start col-span-6 gap-1 cursor-pointer" v-on:click="
            sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
          sort_pr = '';
          sort_y = '';
          ">
            Communities

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_alph ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_alph ? "swap_vert" : sort_alph === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center col-span-3 gap-1 cursor-pointer" v-on:click="
            sort_y = sort_y === 'asc' ? 'dsc' : 'asc';
          sort_pr = '';
          sort_alph = '';
          ">
            Nodes

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_y ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_y ? "swap_vert" : sort_y === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center col-span-3 gap-1 cursor-pointer" v-on:click="
            sort_pr = sort_pr === 'asc' ? 'dsc' : 'asc';
          sort_alph = '';
          sort_y = '';
          ">
            Page Rank

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_pr ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_pr ? "swap_vert" : sort_pr === "asc" ? "south" : "north" }}
            </span>
          </a>
        </div>
      </header>
    </template>
    <!-- options -->
    <template #option="slotProps">
      <div :class="`grid items-center w-full grid-cols-12 gap-2 ${slotProps.selected ? '!text-primary-400' : ''}`">
        <span class="col-span-6 line-clamp-1">Community {{ slotProps.option.modularity_class }}</span>

        <span class="col-span-3 line-clamp-1">{{ slotProps.option.nodes.length }}</span>

        <span class="col-span-3 text-center line-clamp-1">{{ Math.log10(
          parseFloat(slotProps.option.cumulative_pagerank)
        ).toFixed(2) }}</span>
      </div>
    </template>
  </Listbox>
</template>

<script>
import EmptyState from "@/components/verticalpane/EmptyState.vue";
export default {
  name: "CitationCommunities",
  props: ["citation_data", "await_community"],
  data() {
    return {
      search_raw: "",
      await_load: false,
      sort_alph: "",
      sort_pr: "asc", //active filter on start
      sort_y: "",
      selected_citation: "",
    };
  },
  components: {
    EmptyState
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_communities() {
      var com = this;
      var filtered = Object.values(com.citation_data?.community_scores || {});
      console.log('00',filtered)
      if (com.search_raw !== "") {
        // If search term is not empty, filter by search term
        var regex = new RegExp(com.regex, "i");
        filtered = filtered.filter(function (abstract) {
          return regex.test(abstract.nodes.join(" "));
        });
      }

      if (com.sort_alph == "asc") {
        filtered.sort((t1, t2) => t2.modularity_class - t1.modularity_class);
      } else if (com.sort_alph == "dsc") {
        filtered.sort((t1, t2) => t1.modularity_class - t2.modularity_class);
      }

      if (com.sort_y == "asc") {
        filtered.sort((t1, t2) => t2.nodes.length - t1.nodes.length);
      } else if (com.sort_y == "dsc") {
        filtered.sort((t1, t2) => t1.nodes.length - t2.nodes.length);
      }

      if (com.sort_pr == "asc") {
        filtered.sort(
          (t1, t2) => t2.cumulative_pagerank - t1.cumulative_pagerank
        );
      } else if (com.sort_pr == "dsc") {
        filtered.sort(
          (t1, t2) => t1.cumulative_pagerank - t2.cumulative_pagerank
        );
      }
      return filtered;
      // return new Set(filtered);
    },
  },
  methods: {
    select_community(community_nodes) {
      var com = this;
      var abstract_names = new Set(community_nodes.nodes);

      const subset = [];
      com.citation_data.nodes.forEach((node) => {
        if (abstract_names.has(node.attributes["Name"].toUpperCase())) {
          subset.push(node);
        }
      });
      com.emitter.emit("searchSubset", { subset: subset, mode: "citation" });
    },
    top_communities(count) {
      var com = this;
      var filtered = Object.values(com.citation_data.community_scores);
      return filtered
        .sort((t1, t2) => t2.cumulative_pagerank - t1.cumulative_pagerank)
        .slice(0, count);
    },
    top_nodes(count) {
      var com = this;
      var sorted_communities = com.top_communities(count);
      var top_nodes = [];

      for (var community of sorted_communities) {
        var abstract_names = new Set(community.nodes);
        var subset = [];

        com.citation_data.nodes.forEach((node) => {
          if (abstract_names.has(node.attributes["Name"].toUpperCase())) {
            subset.push(node);
          }
        });

        var highestPageRankNode = com.getHighestPageRankElements(subset);
        if (highestPageRankNode) {
          top_nodes.push(highestPageRankNode);
        }
      }

      var flatList = top_nodes.flat();
      com.emitter.emit("searchSubset", { subset: flatList, mode: "citation" });
    },

    getHighestPageRankElements(list) {
      if (list.length === 0) return null;

      if (list.length === 1) return [list[0]];

      list.sort((a, b) => b.pagerank - a.pagerank);
      return [list[0], list[1]];
    },
  },
};
</script>