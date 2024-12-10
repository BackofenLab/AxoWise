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

  <EmptyState v-if="terms?.length == 0" message="There is no generated terms.">
  </EmptyState>

  <Listbox v-if="terms !== null && !await_load" v-model="selected_pathway" optionLabel="name" :options="filt_terms" :pt="{
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

          <InputGroupAddon>
            <Button @click="toggle" icon="pi pi-list" text plain />
          </InputGroupAddon>
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
        <span class="col-span-8">{{ slotProps.option.name }}</span>

        <span class="col-span-3 text-right">{{ slotProps.option.fdr_rate.toExponential(2) }}</span>

        <span v-on:click.stop="add_enrichment(slotProps.option)" :class="`material-symbols-rounded text-slate-600 cursor-pointer 
          ${favourite_tab.has(slotProps.option)
            ? 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400'
            : 'hover:text-yellow-600'
          }`">
          star
        </span>
      </div>
    </template>
  </Listbox>

  <Popover ref="op" class="w-[13rem]" :pt="{ content: { class: '!flex !flex-col' } }">
    <Button class="!w-full !justify-start !gap-3" @click="bookmark_off = !bookmark_off" icon="material-symbols-rounded"
      text plain>
      <span :class="`material-symbols-rounded 
          ${!bookmark_off ? 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400' : ''}`">
        star
      </span>
      {{ bookmark_off ? "Show only favorites" : "Show all" }}
    </Button>
    <Button class="!w-full !justify-start !gap-3" @click="export_enrichment" icon="material-symbols-rounded" text plain>
      <span class="material-symbols-rounded">download</span>
      Export terms as csv
    </Button>
  </Popover>
</template>

<script setup>
import { ref } from "vue";

const op = ref();

const toggle = (event) => {
  op.value.toggle(event);
};
</script>

<script>
import EmptyState from "@/components/verticalpane/EmptyState.vue";
export default {
  name: "PathwayList",
  props: [
    "gephi_data",
    "terms",
    "await_load",
    "filtered_terms",
    "favourite_pathways",
  ],
  components: {
    EmptyState
  },
  emits: ["favourite_pathways_changed", "filtered_terms_changed"],
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
    this.emitter.on("bookmarkPathway", (value) => {
      this.add_enrichment(value);
    });
    this.emitter.on("visualizeLayer", () => {
      this.visualize_layers();
    });
    this.favourite_tab = new Set(this.favourite_pathways);
  },
  watch: {
    terms() {
      this.filter_options(this.terms);
      this.init_categories();
    },
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
      var filtered = com.terms;

      if (com.selected_categories?.length) {
        // If category is selected, filter by category
        filtered = filtered.filter(function (term) {
          return com.selected_categories.some(el => el.label === term.category);
        });
      }

      if (com.search_raw !== "") {
        // If search term is not empty, filter by search term
        var regex = new RegExp(com.regex, "i");
        filtered = filtered.filter(function (term) {
          return regex.test(term.name);
        });
      }

      if (com.sort_alph == "asc") {
        filtered.sort(function (t1, t2) {
          return t1.name.toLowerCase() > t2.name.toLowerCase()
            ? 1
            : t1.name.toLowerCase() === t2.name.toLowerCase()
              ? 0
              : -1;
        });
      } else if (com.sort_alph == "dsc") {
        filtered.sort(function (t1, t2) {
          return t2.name.toLowerCase() > t1.name.toLowerCase()
            ? 1
            : t1.name.toLowerCase() === t2.name.toLowerCase()
              ? 0
              : -1;
        });
      }

      if (com.sort_fdr == "asc") {
        filtered.sort((t1, t2) => t2.fdr_rate - t1.fdr_rate);
      } else if (com.sort_fdr == "dsc") {
        filtered.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate);
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
    init_categories() {
      for (let element of this.filter_terms) {
        let checkCategory = element.label;
        if (
          checkCategory !== "GOCC" &&
          checkCategory !== "GOMF" &&
          checkCategory !== "GOBP"
        ) {
          this.selected_categories.push({ label: checkCategory });
        }
      }
    },
    filter_options(terms) {
      var com = this;
      com.filter_terms = [];
      var remove_duplicates = [...new Set(terms?.map((term) => term.category))];
      remove_duplicates.forEach((term) => {
        com.filter_terms.push({ label: term });
      });
    },
    select_term(term) {
      var com = this;
      com.emitter.emit("searchEnrichment", term);
    },
    add_enrichment(enrichment) {
      if (!this.favourite_tab.has(enrichment)) {
        // Checkbox is checked, add its state to the object
        this.favourite_tab.add(enrichment);
      } else {
        // Checkbox is unchecked, remove its state from the object
        this.favourite_tab.delete(enrichment);
      }
      this.$emit("favourite_pathways_changed", this.favourite_tab);
    },
    visualize_layers() {
      var com = this;
      com.emitter.emit("hideTermLayer", {
        main: com.favourite_tab,
        hide: new Set(),
      });
    },
    export_enrichment() {
      var com = this;

      //export terms as csv
      var csvTermsData = com.filt_terms;

      var terms_csv = "category\tfdr_rate\tname\tgenes\n";

      csvTermsData.forEach(function (row) {
        terms_csv +=
          row["category"] +
          "\t" +
          row["fdr_rate"] +
          '\t"' +
          row["name"] +
          '"\t"' +
          row["symbols"] +
          '"';
        terms_csv += "\n";
      });

      //Create html element to hidden download csv file
      var hiddenElement = document.createElement("a");
      hiddenElement.target = "_blank";
      hiddenElement.href =
        "data:text/csv;charset=utf-8," + encodeURI(terms_csv);
      hiddenElement.download = "Terms.csv";
      hiddenElement.click();
    },
  },
};
</script>