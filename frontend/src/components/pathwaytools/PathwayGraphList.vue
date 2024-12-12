<template>
  <EmptyState v-if="term_data == null" message="There is no generated terms.">
  </EmptyState>

  <Listbox v-if="term_data !== null" v-model="selected_pathway" optionLabel="name" :options="filt_terms" :pt="{
    header: { class: 'sticky top-0 flex-1 !px-0 bg-[var(--card-bg)] z-[1] order-1' },
    listContainer: { class: 'order-3' },
    list: { class: '!p-0' },
    emptyMessage: { class: '!flex !justify-center !items-center !text-sm !text-slate-500 dark:!text-slate-300' },
    option: {
      class:
        '!px-0 !py-1.5 !text-slate-500 dark:!text-slate-300 leading-tight transition-all duration-300 ease-in-out',
    },
  }" listStyle="max-height:100%" class="h-full flex flex-col !p-0 !bg-transparent !border-0"
    @update:modelValue="select_term" :tabindex="0" emptyMessage="No terms available.">

    <template #footer>
      <header class="sticky top-0 bg-[var(--card-bg)] pt-3 items-center gap-2 z-[1] order-1">
        <!-- filter -->
        <InputGroup>
          <InputGroupAddon class="!px-3">
            <MultiSelect v-model="selected_categories" optionLabel="label" placeholder="Filter" showClear
              resetFilterOnClear filterPlaceholder="Search categories" filter class="!w-60 !p-0 !border-0"
              emptyMessage="No categories available" emptyFilterMessage="No categories available"
              :selectedItemsLabel="`${selected_categories?.length} categories`" :options="filter_terms"
              :maxSelectedLabels="1" :pt="{
                clearIcon: { class: '!w-3.5 !h-3.5 !absolute !right-5 rounded-full z-[1]' },
                overlay: { class: '!w-[18rem]' },
                label: { class: 'max-w-[100px] !py-0 !px-0 text-[15px] !line-clamp-1' },
                dropdown: { class: '!w-auto ml-6' },
                optionLabel: { class: 'whitespace-normal' }
              }" />
          </InputGroupAddon>

          <IconField class="w-full">
            <InputText v-model="search_raw" placeholder="Search pathway" class="w-full" />
            <InputIcon class="z-10 pi pi-search" />
          </IconField>
        </InputGroup>

        <!-- sorting -->
        <div
          class="grid grid-cols-12 items-center gap-2 py-2 bg-[var(--card-bg)] shadow-[0_10px_30px_-18px_#34343D] dark:shadow-[0_10px_30px_-18px_#ffffff] z-[1]">
          <a class="flex items-center justify-start col-span-9 gap-1 text-right cursor-pointer" v-on:click="
            sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
          sort_fdr = '';
          ">
            Functional enrichment pathways ({{ filt_terms.length }})

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_alph ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_alph ? "swap_vert" : sort_alph === "asc" ? "south" : "north" }}
            </span>
          </a>

          <a class="flex items-center justify-end col-span-3 gap-1 text-right cursor-pointer" v-on:click="
            sort_fdr = sort_fdr === 'asc' ? 'dsc' : 'asc';
          sort_alph = '';
          ">
            Fdr rate

            <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_fdr ? 'text-primary-500' : 'text-slate-600'}`">
              {{ !sort_fdr ? "swap_vert" : sort_fdr === "asc" ? "south" : "north" }}
            </span>
          </a>
        </div>
      </header>
    </template>
    <!-- options -->
    <template #option="slotProps">
      <div :class="`grid items-center w-full grid-cols-12 gap-2 ${slotProps.selected ? '!text-primary-400' : ''}`">
        <span class="col-span-8">{{ slotProps.option?.attributes?.["Name"] }}</span>

        <span class="col-span-3 text-right">{{ slotProps.option?.attributes?.["FDR"]?.toExponential(2) }}</span>

      </div>
    </template>
  </Listbox>
</template>

<script>
import EmptyState from "@/components/verticalpane/EmptyState.vue";
export default {
  name: "PathwayGraphList",
  props: ["term_data", "mode"],
  components: {
    EmptyState
  },
  data() {
    return {
      search_raw: "",
      sort_fdr: "",
      sort_alph: "",
      selected_categories: [],
      filter_terms: [],
      bookmark_off: true,
      favourite_tab: new Set(),
      selected_pathway: "",
    };
  },
  mounted() {
    this.filter_options(this.term_data.nodes);
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_terms() {
      var com = this;
      var filtered = com.term_data.nodes;

      if (com.selected_categories?.length) {
        // If category is set, filter by category
        filtered = filtered.filter(function (term) {
          return com.selected_categories.some(el => el.label === term.attributes["Category"]);
        });
      }

      if (com.search_raw !== "") {
        // If search term is not empty, filter by search term
        var regex = new RegExp(com.regex, "i");
        filtered = filtered.filter(function (term) {
          return regex.test(term.attributes["Name"]);
        });
      }

      if (com.sort_alph == "asc") {
        filtered.sort(function (t1, t2) {
          return t1.attributes["Name"].toLowerCase() >
            t2.attributes["Name"].toLowerCase()
            ? 1
            : t1.attributes["Name"].toLowerCase() ===
              t2.attributes["Name"].toLowerCase()
              ? 0
              : -1;
        });
      } else if (com.sort_alph == "dsc") {
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

      if (com.sort_fdr == "asc") {
        filtered.sort((t1, t2) => t2.attributes["FDR"] - t1.attributes["FDR"]);
      } else if (com.sort_fdr == "dsc") {
        filtered.sort((t1, t2) => t1.attributes["FDR"] - t2.attributes["FDR"]);
      }

      if (!com.bookmark_off) {
        filtered = filtered.filter(function (term) {
          return com.favourite_tab.has(term);
        });
      }

      this.$emit("filtered_terms_changed", filtered);

      return filtered;
      // return new Set(filtered);
    },
  },
  methods: {
    filter_options(terms) {
      var com = this;
      com.filter_terms = [];
      var remove_duplicates = [
        ...new Set(terms.map((term) => term.attributes["Category"])),
      ];
      remove_duplicates.forEach((term) => {
        com.filter_terms.push({ label: term });
      });
    },
    select_term(term) {
      var com = this;
      com.emitter.emit("searchNode", { node: term, mode: this.mode });
    },
  },
};
</script>
