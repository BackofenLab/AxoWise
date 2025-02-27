<template>
  <ul class="list-none p-0 m-0 flex flex-col divide-y dark:divide-[#343b4c]">
    <li class="flex flex-col gap-2 px-2.5 pb-3 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between -mx-2.5 gap-2 mb-2 text-sm">
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

    <li class="flex flex-col gap-2 px-2.5 py-3 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between -mx-2.5 gap-2 mb-2 text-sm">
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
        @update:modelValue="sliderChanged($event, 'bc_boundary')" :modelValue=[bc_boundary.minValue,bc_boundary.maxValue] />
    </li>

    <li class="flex flex-col gap-2 px-2.5 py-3 dark:text-[#c3c3c3]">
      <div class="flex items-center justify-between -mx-2.5 gap-2 mb-2 text-sm">
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
        @update:modelValue="sliderChanged($event, 'pr_boundary')" :modelValue=[pr_boundary.minValue,pr_boundary.maxValue] />
    </li>

    <template v-if="dcoloumns && mode != 'term' && mode != 'citation'">
      <li class="flex flex-col gap-2 px-2.5 py-3 dark:text-[#c3c3c3]" v-for="(entry, index) in dcoloumns" :key="index">
        <div class="flex items-center justify-between -mx-2.5 gap-2 mb-2">
          <span class="text-sm">{{ entry }}</span>
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
          <ToggleSwitch :id="'deval-check-' + index" class="toggle-xs"
            @value-change="change_limits($event, entry); searchSubset();" />
        </span>
        <Slider :name="'deval-slider-' + index" :min="dboundaries[entry].min" :max="dboundaries[entry].max" range
          :step="dboundaries[entry].step" @update:modelValue="devalSliderChanged($event, entry)"
          :modelValue=[dboundaries[entry].minValue,dboundaries[entry].maxValue] />
      </li>
    </template>
  </ul>
</template>

<script>
export default {
  name: "PathwayLinks",
  props: ["active_term", "mode"],
  data() {
    return {
      parameter_data: null,
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
      dcoloumns: this.$store.state.dcoloumns,
      dboundaries: {},
      nodeCheck: false,
      formatType: null,
      check: {},
    };
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
      var dataForm = com.parameter_data;

      for (var coloumn of this.dcoloumns) {
        // _____ this calculation has only to be done once _______
        var subset_de;
        subset_de = dataForm.map((arrayItem) => {
          return arrayItem.attributes[coloumn];
        });

        // Convert String values to Integers
        var result = subset_de.map(function (x) {
          return parseFloat(x);
        });
        var maxDe = Math.ceil(Math.max(...result));
        var minDe = Math.floor(Math.min(...result));

        this.dboundaries[coloumn] = {
          minValue: minDe,
          maxValue: maxDe,
          min: minDe,
          max: maxDe,
          step: 0.01,
        };
      }
    },
    initialize_dg: function () {
      var com = this;

      var dataForm = com.parameter_data;

      // initialize values of slider
      var subset_degree;

      subset_degree = dataForm.map((arrayItem) => {
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

      var dataForm = com.parameter_data;

      // _____ this calculation has only to be done once _______
      var subset_bc;
      subset_bc = dataForm.map((arrayItem) => {
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

      var dataForm = com.parameter_data;

      // _____ this calculation has only to be done once _______
      var subset_pr;
      subset_pr = dataForm.map((arrayItem) => {
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
    searchSubset() {
      var com = this;

      var dataForm = com.parameter_data;
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
      this.emitter.emit("filterPathway", {
        subset: finalNodes.map((element) => {
          return element.attributes["Name"];
        }),
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
    term_genes(list) {
      var term_genes = new Set(list);
      var termlist = this.$store.state.gephi_json.data.nodes.filter((element) =>
        term_genes.has(element.attributes["Name"])
      );
      return termlist;
    },
    load_data() {
      this.parameter_data = this.term_genes(this.active_term.symbols);
    },
  },
  mounted() {
    this.initialize_dg();
    this.initialize_bc();
    this.initialize_pagerank();
    this.searchSubset();
  },
  created() {
    this.load_data();
    if (this.dcoloumns) this.initialize_de();
  },
};
</script>