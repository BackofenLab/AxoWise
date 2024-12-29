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

  <EmptyState v-if="citation_data?.nodes?.length == 0" message="There is no generated abstracts.">
  </EmptyState>

  <Listbox v-if="citation_data?.nodes?.length != 0 && !await_load" v-model="selected_citation" optionLabel="id"
    :options="filt_abstracts" :pt="{
      header: { class: 'sticky top-0 flex-1 !px-0 bg-[var(--card-bg)] z-[1] order-1' },
      listContainer: { class: 'order-3' },
      list: { class: '!p-0' },
      emptyMessage: { class: '!flex !justify-center !items-center !text-sm !text-slate-500 dark:!text-slate-300' },
      option: {
        class:
          '!px-0 !py-1 !text-slate-500 dark:!text-slate-300 leading-tight transition-all duration-300 ease-in-out',
      },
    }" listStyle="max-height:100%" class="h-full flex flex-col !p-0 !bg-transparent !border-0"
    @update:modelValue="select_abstract" :tabindex="0" emptyMessage="No abstracts available.">

    <template #footer>
      <header class="sticky top-0 bg-[var(--card-bg)] pt-3 items-center gap-2 z-[1] order-1">
        <!-- filter -->
        <IconField class="w-full">
          <InputText v-model="search_raw" placeholder="Search abstracts" class="w-full" />
          <InputIcon class="z-10 pi pi-search" />
        </IconField>

        <!-- sorting -->
        <div
          class="grid grid-cols-12 items-center gap-2 py-2 bg-[var(--card-bg)] shadow-[0_10px_30px_-18px_#34343D] dark:shadow-[0_10px_30px_-18px_#ffffff] z-[1]">
          <a class="flex items-center justify-start col-span-4 gap-1 cursor-pointer" v-on:click="
            sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
          sort_pr = '';
          sort_cb = '';
          sort_y = '';
          ">
            Pubmed ID

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_alph ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_alph ? "swap_vert" : sort_alph === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center col-span-3 gap-1 cursor-pointer" v-on:click="
            sort_cb = sort_cb === 'asc' ? 'dsc' : 'asc';
          sort_pr = '';
          sort_alph = '';
          sort_y = '';
          ">
            Citation

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_cb ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_cb ? "swap_vert" : sort_cb === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center col-span-2 gap-1 cursor-pointer" v-on:click="
            sort_y = sort_y === 'asc' ? 'dsc' : 'asc';
          sort_pr = '';
          sort_cb = '';
          sort_alph = '';
          ">
            Year

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_y ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_y ? "swap_vert" : sort_y === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center col-span-3 gap-1 cursor-pointer" v-on:click="
            sort_pr = sort_pr === 'asc' ? 'dsc' : 'asc';
          sort_alph = '';
          sort_cb = '';
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
        <span class="col-span-4">{{ slotProps.option.id }}</span>

        <span class="col-span-3">{{ slotProps.option.attributes["Citation"] }}</span>

        <span class="col-span-2">{{ slotProps.option.attributes["Year"] }}</span>

        <span class="col-span-3 text-center">{{ Math.log10(
          parseFloat(slotProps.option.attributes["PageRank"])
        ).toFixed(2) }}</span>
      </div>
    </template>
  </Listbox>
</template>

<script>
import EmptyState from "@/components/verticalpane/EmptyState.vue";
export default {
  name: "CitationList",
  props: ["citation_data", "active_node"],
  data() {
    return {
      search_raw: "",
      await_load: false,
      sort_alph: "",
      sort_pr: "asc", // active filter on start
      sort_cb: "",
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
    filt_abstracts() {
      var com = this;
      var filtered = com.citation_data.nodes;

      if (com.search_raw !== "") {
        // If search term is not empty, filter by search term
        var regex = new RegExp(com.regex, "i");
        filtered = filtered.filter(function (abstract) {
          return (
            regex.test(abstract.attributes["Title"]) ||
            regex.test(abstract.attributes["Ensembl ID"])
          );
        });
      }

      if (com.sort_alph == "asc") {
        filtered.sort((t1, t2) => t2.id - t1.id);
      } else if (com.sort_alph == "dsc") {
        filtered.sort((t1, t2) => t1.id - t2.id);
      }

      if (com.sort_cb == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["Citation"] - t1.attributes["Citation"]
        );
      } else if (com.sort_cb == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["Citation"] - t2.attributes["Citation"]
        );
      }

      if (com.sort_y == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["Year"] - t1.attributes["Year"]
        );
      } else if (com.sort_y == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["Year"] - t2.attributes["Year"]
        );
      }

      if (com.sort_pr == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["PageRank"] - t1.attributes["PageRank"]
        );
      } else if (com.sort_pr == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["PageRank"] - t2.attributes["PageRank"]
        );
      }
      return filtered;
      // return new Set(filtered);
    },
  },
  methods: {
    select_abstract(abstract) {
      var com = this;
      com.emitter.emit("searchNode", { node: abstract, mode: "citation" });
    },
  },
};
</script>