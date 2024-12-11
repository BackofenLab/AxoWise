<template>
  <ul class="list-none p-0 m-0 mt-2 flex flex-col divide-y dark:divide-[#343b4c]">
    <li class="flex flex-col gap-2 pb-5 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between gap-2 mb-2">
        Degree value
        <fieldset class="flex gap-1">
          <InputNumber :useGrouping="false" :min="degree_boundary.min" :max="degree_boundary.max"
            :step="degree_boundary.step" v-model="degree_boundary.minValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />-
          <InputNumber :useGrouping="false" :min="degree_boundary.min" :max="degree_boundary.max"
            :step="degree_boundary.step" v-model="degree_boundary.maxValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />
        </fieldset>
      </div>
      <Slider name="degree_boundary" :min="degree_boundary.min" :max="degree_boundary.max" range
        :step="degree_boundary.step" @update:modelValue="sliderChanged($event, 'degree_boundary')"
        :modelValue=[degree_boundary.minValue,degree_boundary.maxValue] />
    </li>

    <li class="flex flex-col gap-2 py-5 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between gap-2 mb-2">
        Betweenness centrality value
        <fieldset class="flex gap-1">
          <InputNumber :useGrouping="false" :min="bc_boundary.min" :max="bc_boundary.max" :step="bc_boundary.step"
            v-model="bc_boundary.minValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />-
          <InputNumber :useGrouping="false" :min="bc_boundary.min" :max="bc_boundary.max" :step="bc_boundary.step"
            v-model="bc_boundary.maxValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />
        </fieldset>
      </div>
      <Slider name="bc_boundary" :min="bc_boundary.min" :max="bc_boundary.max" range :step="bc_boundary.step"
        @update:modelValue="sliderChanged($event, 'bc_boundary')"
        :modelValue=[bc_boundary.minValue,bc_boundary.maxValue] />
    </li>

    <li v-if="mode == 'term'" class="flex flex-col gap-2 py-5 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between gap-2 mb-2">
        padj value (log10)
        <fieldset class="flex gap-1">
          <InputNumber :useGrouping="false" :min="padj_boundary.min" :max="padj_boundary.max" :step="padj_boundary.step"
            v-model="padj_boundary.minValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />-
          <InputNumber :useGrouping="false" :min="padj_boundary.min" :max="padj_boundary.max" :step="padj_boundary.step"
            v-model="padj_boundary.maxValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />
        </fieldset>
      </div>
      <Slider name="padj_boundary" :min="padj_boundary.min" :max="padj_boundary.max" range :step="padj_boundary.step"
        @update:modelValue="sliderChanged($event, 'padj_boundary')"
        :modelValue=[padj_boundary.minValue,padj_boundary.maxValue] />
    </li>

    <li class="flex flex-col gap-2 py-5 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between gap-2 mb-2">
        pagerank value (log10)
        <fieldset class="flex gap-1">
          <InputNumber :useGrouping="false" :min="pr_boundary.min" :max="pr_boundary.max" :step="pr_boundary.step"
            v-model="pr_boundary.minValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />-
          <InputNumber :useGrouping="false" :min="pr_boundary.min" :max="pr_boundary.max" :step="pr_boundary.step"
            v-model="pr_boundary.maxValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />
        </fieldset>
      </div>
      <Slider name="pr_boundary" :min="pr_boundary.min" :max="pr_boundary.max" range :step="pr_boundary.step"
        @update:modelValue="sliderChanged($event, 'pr_boundary')"
        :modelValue=[pr_boundary.minValue,pr_boundary.maxValue] />
    </li>
  </ul>

  <div v-if="mode != 'term' && mode != 'citation'" class="flex justify-between mt-5 font-medium">
    Coloumn section
    <ToggleSwitch class="toggle-xs" v-model="coloumnsCheck" />
  </div>

  <span v-if="!dcoloumns" class="flex justify-center pt-2 text-sm dark:text-[#c3c3c3]">No selectable dcoloumns</span>

  <ul v-if="dcoloumns" v-show="coloumnsCheck"
    class="max-h-[240px] overflow-auto overflow-x-visible list-none mb-4 p-0 m-0 mt-1 px-2.5 flex flex-col divide-y dark:divide-[#343b4c]">
    <li class="flex flex-col gap-2 py-5 dark:text-[#c3c3c3]" v-for="(entry, index) in dcoloumns" :key="index">
      <div class="flex items-center justify-between gap-2 mb-2">
        {{ entry }}
        <fieldset class="flex gap-1">
            <InputNumber :useGrouping="false" :min="dboundaries[entry].min" :max="dboundaries[entry].max"
              :step="dboundaries[entry].step" v-model="dboundaries[entry].minValue" @value-change="searchSubset()"
              inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />-
            <InputNumber :useGrouping="false" :min="dboundaries[entry].min" :max="dboundaries[entry].max"
              :step="dboundaries[entry].step" v-model="dboundaries[entry].maxValue" @value-change="searchSubset()"
            inputClass="w-14 h-7 !px-1.5 !text-xs text-center" />
        </fieldset>
      </div>
      <span class="flex items-center justify-end gap-2 mb-2 text-sm">
        Inverse selection
        <ToggleSwitch :id="'deval-check-' + index" class="toggle-xs" @value-change="change_limits($event, entry);searchSubset();" />
      </span>
      <Slider :name="'deval-slider-' + index" :min="dboundaries[entry].min" :max="dboundaries[entry].max" range
        :step="dboundaries[entry].step" @update:modelValue="devalSliderChanged($event, entry)"
        :modelValue=[dboundaries[entry].minValue,dboundaries[entry].maxValue] />
      </li>
  </ul>

  <Button label="Create subset" severity="secondary" size="small" fluid type="button" class="mt-4 !rounded-lg"
    @click="save_subset()">
  </Button>
</template>

<script>
import { useToast } from "primevue/usetoast";

export default {
  name: "SelectionList",
  props: ["data", "mode", "active_subset", "active_term", "selection_active"],
  // emits: ["selection_active_changed"],
  data() {
    return {
      coloumnsCheck: false,
      degree_boundary: {
        minValue: 0,
        maxValue: 0,
        min: 0,
        max: 0,
        step: 1,
      },
      pr_boundary: {
        minValue: 0,
        maxValue: 0,
        min: 0,
        max: 0,
        step: 0.01,
      },
      bc_boundary: { minValue: 0, maxValue: 0, min: 0, max: 0, step: 1 },
      padj_boundary: {
        minValue: 0,
        maxValue: 0,
        min: 0,
        max: 0,
        step: 0.01,
      },
      dcoloumns: this.$store.state.dcoloumns,
      dboundaries: {},
      nodeCheck: false,
      check: {},
    };
  },
  watch: {
    selection_active() {
      if (this.selection_active) this.searchSubset();
    },
    data() {
      if (this.mode == "term" || this.mode == "citation") this.initialize_all();
    },
  },
  methods: {
    change_limits(value, entry) {
      let com = this;
      com.check[entry] = value;
      com.dboundaries[entry].minValue = com.check[entry] ? 0.001 : com.dboundaries[entry].min;
      com.dboundaries[entry].maxValue = com.check[entry] ? 0 : com.dboundaries[entry].max;
    },
    initialize_de() {
      var com = this;
      var dataForm = com.data;

      for (var column of this.dcoloumns) {
        // _____ this calculation has only to be done once _______
        var subset_de;
        subset_de = dataForm.nodes.map((arrayItem) => {
          return arrayItem.attributes[column];
        });

        // Convert String values to Integers
        var result = subset_de.map(function (x) {
          return parseFloat(x);
        });
        var maxDe = Math.ceil(Math.max(...result));
        var minDe = Math.floor(Math.min(...result));

        this.dboundaries[column] = {
          minValue: minDe,
          maxValue: maxDe,
          min: minDe,
          max: maxDe,
          step: 0.01,
        };
      }
    },
    save_subset() {
      var com = this;
      let genes;
      let count = new Set(com.$store.state.favourite_subsets)?.size || 0;
      if (com.mode == "protein") {
        genes = com.$store.state.active_subset;
      } else if (com.mode == "term") {
        genes = com.$store.state.p_active_subset;
      } else {
        genes = com.$store.state.c_active_subset;
      }

      if (!genes) return;

      this.$store.commit("assign_subset", {
        name: `subset ${count}`,
        genes: genes,
        terms: null,
        view: com.mode,
        abstracts: null,
        status: false,
        information: false,
        actions: false,
        stats: null,
      });
      this.toast.add({ severity: 'success', detail: 'Subset created successfully.', life: 4000 });
    },
    initialize_dg: function () {
      var com = this;

      var dataForm = com.data;

      // initialize values of slider
      var subset_degree;

      subset_degree = dataForm.nodes.map((arrayItem) => {
        return arrayItem.attributes["Degree"];
      });

      // Convert String values to Integers
      var result = subset_degree.map(function (x) {
        return parseInt(x, 10);
      });

      var maxDeg = Math.max(...result); // Need to use spread operator!
      com.degree_boundary["max"] = maxDeg;
      com.degree_boundary["min"] = 0;
      com.degree_boundary["maxValue"] = maxDeg;
      com.degree_boundary["minValue"] = 0;
    },
    initialize_bc() {
      var com = this;

      var dataForm = com.data;

      // _____ this calculation has only to be done once _______
      var subset_bc;
      subset_bc = dataForm.nodes.map((arrayItem) => {
        return arrayItem.attributes["Betweenness Centrality"];
      });

      // Convert String values to Integers
      var result = subset_bc.map(function (x) {
        return parseFloat(x, 10);
      });
      var maxDeg = Math.max(...result) + 10; // Need to use spread operator!
      com.bc_boundary["max"] = maxDeg;
      com.bc_boundary["min"] = 0;
      com.bc_boundary["maxValue"] = maxDeg;
      com.bc_boundary["minValue"] = 0;
    },
    initialize_pagerank() {
      var com = this;

      var dataForm = com.data;

      // _____ this calculation has only to be done once _______
      var subset_pr;
      subset_pr = dataForm.nodes.map((arrayItem) => {
        return arrayItem.attributes["PageRank"];
      });

      // Convert String values to Integers
      var result = subset_pr.map(function (x) {
        return parseFloat(x);
      });
      var minDeg = Math.log10(Math.min(...result)) - 1;
      com.pr_boundary["max"] = 0;
      com.pr_boundary["min"] = minDeg;
      com.pr_boundary["maxValue"] = 0;
      com.pr_boundary["minValue"] = minDeg;
    },
    initialize_padj() {
      var com = this;

      var dataForm = com.data;

      // _____ this calculation has only to be done once _______
      var subset_padj;
      subset_padj = dataForm.nodes.map((arrayItem) => {
        return arrayItem.attributes["FDR"];
      });

      // Convert String values to Integers
      var result = subset_padj.map(function (x) {
        return parseFloat(x);
      });

      var minDeg = Math.log10(Math.min(...result)) - 1; // Need to use spread operator!
      com.padj_boundary["maxValue"] = 0;
      com.padj_boundary["minValue"] = minDeg;
      com.pr_boundary["max"] = 0;
      com.pr_boundary["min"] = minDeg;
    },
    searchSubset() {
      var com = this;

      var dataForm = this.data.nodes;
      // filter hubs
      var finalNodes = [];
      var nodes = [];
      // degree filtering
      for (var element of dataForm) {
        if (
          parseInt(element.attributes["Degree"]) >=
          this.degree_boundary.minValue &&
          parseInt(element.attributes["Degree"]) <=
          this.degree_boundary.maxValue &&
          Math.log10(parseFloat(element.attributes["PageRank"])) >=
          this.pr_boundary.minValue &&
          Math.log10(parseFloat(element.attributes["PageRank"])) <=
          this.pr_boundary.maxValue &&
          parseFloat(element.attributes["Betweenness Centrality"]) >=
          this.bc_boundary.minValue &&
          parseFloat(element.attributes["Betweenness Centrality"]) <=
          this.bc_boundary.maxValue
        ) {
          if (com.mode == "term") {
            if (
              Math.log10(parseFloat(element.attributes["FDR"])) >=
              this.padj_boundary.minValue &&
              Math.log10(parseFloat(element.attributes["FDR"])) <=
              this.padj_boundary.maxValue
            ) {
              nodes.push(element);
            }
          } else if (com.mode == "citation") {
            nodes.push(element);
          } else if (this.dcoloumns) {
            this.nodeCheck = true;
            for (var coloumn of com.dcoloumns) {
              if (
                com.check[coloumn] == false ||
                com.check[coloumn] == undefined
              ) {
                if (
                  parseFloat(element.attributes[coloumn]) <
                  com.dboundaries[coloumn].minValue ||
                  parseFloat(element.attributes[coloumn]) >
                  com.dboundaries[coloumn].maxValue
                ) {
                  this.nodeCheck = false;
                  break;
                }
              } else {
                if (
                  parseFloat(element.attributes[coloumn]) >
                  com.dboundaries[coloumn].minValue &&
                  parseFloat(element.attributes[coloumn]) <
                  com.dboundaries[coloumn].maxValue
                ) {
                  this.nodeCheck = false;
                  break;
                }
              }
            }
            if (this.nodeCheck) nodes.push(element);
          } else {
            nodes.push(element);
          }
        }
      }
      finalNodes = nodes;
      this.emitter.emit("searchSubset", {
        subset: { selection: true, genes: finalNodes },
        mode: this.mode,
      });
    },
    sliderChanged(values, obj) {
      var com = this;
      com[obj]["minValue"] =
        values[0];
      com[obj]["maxValue"] =
        values[1];
      com.searchSubset();
    },
    devalSliderChanged(values, entry) {
      var com = this;
      com.dboundaries[entry]["minValue"] =
        values[0];
      com.dboundaries[entry]["maxValue"] =
        values[1];
      com.searchSubset();
    },
    initialize_all() {
      this.initialize_dg();
      this.initialize_bc();
      this.initialize_pagerank();
      // if (this.dcoloumns && this.mode != "term" && this.mode != "citation")
      //   this.create_de();
      if (this.mode == "term") this.initialize_padj();
      this.searchSubset();
    },
  },
  mounted() {
    this.toast = useToast();
    this.initialize_all();
  },
  created() {
    if (this.dcoloumns) this.initialize_de();
  },
};
</script>
