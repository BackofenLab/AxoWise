<template>
    <div id="term-statistics" class="term-statistics">
      <div class="selection_list">
        <div class="window-label">degree value</div>
        <div class="menu-items">
          <div id="term-degree"></div>
          <input
            type="number"
            v-bind:min="degree_boundary.min"
            v-bind:max="degree_boundary.max"
            v-bind:step="degree_boundary.step"
            v-model="degree_boundary.minValue"
            v-on:change="searchSubset()"
            v-on:input="
              valueChanged('term-degree', [
                degree_boundary.minValue,
                degree_boundary.maxValue,
              ])
            "
          />
          <span class="seperator">-</span>
          <input
            type="number"
            v-bind:min="degree_boundary.min"
            v-bind:max="degree_boundary.max"
            v-bind:step="degree_boundary.step"
            v-model="degree_boundary.maxValue"
            v-on:change="searchSubset()"
            v-on:input="
              valueChanged('term-degree', [
                degree_boundary.minValue,
                degree_boundary.maxValue,
              ])
            "
          />
        </div>
        <div class="window-label">betweenness centrality value</div>
        <div class="menu-items">
          <div id="term-betweenes"></div>
          <input
            type="number"
            v-bind:min="bc_boundary.min"
            v-bind:max="bc_boundary.max"
            v-bind:step="bc_boundary.step"
            v-model="bc_boundary.minValue"
            v-on:change="searchSubset()"
            v-on:input="
              valueChanged('term-betweenes', [
                bc_boundary.minValue,
                bc_boundary.maxValue,
              ])
            "
          />
          <span class="seperator">-</span>
          <input
            type="number"
            v-bind:min="bc_boundary.min"
            v-bind:max="bc_boundary.max"
            v-bind:step="bc_boundary.step"
            v-model="bc_boundary.maxValue"
            v-on:change="searchSubset()"
            v-on:input="
              valueChanged('term-betweenes', [
                bc_boundary.minValue,
                bc_boundary.maxValue,
              ])
            "
          />
        </div>
        <div class="window-label">pagerank value (log10)</div>
        <div class="menu-items">
          <div id="term-pagerank"></div>
          <input
            type="number"
            v-bind:min="pr_boundary.min"
            v-bind:max="pr_boundary.max"
            v-bind:step="pr_boundary.step"
            v-model="pr_boundary.minValue"
            v-on:change="searchSubset()"
            v-on:input="
              valueChanged('term-pagerank', [
                pr_boundary.minValue,
                pr_boundary.maxValue,
              ])
            "
          />
          <span class="seperator">-</span>
          <input
            type="number"
            v-bind:min="pr_boundary.min"
            v-bind:max="pr_boundary.max"
            v-bind:step="pr_boundary.step"
            v-model="pr_boundary.maxValue"
            v-on:change="searchSubset()"
            v-on:input="
              valueChanged('term-pagerank', [
                pr_boundary.minValue,
                pr_boundary.maxValue,
              ])
            "
          />
        </div>
        <div
          v-if="dcoloumns && mode != 'term' && mode != 'citation'"
          class="slider-section-scroll"
        >
          <div v-for="(entry, index) in dcoloumns" :key="index">
            <div class="window-label">{{ entry }}</div>
            <div class="menu-items">
              <div class="checkbox-header">
                <input
                  type="checkbox"
                  :id="'term-deval-check-' + index"
                  v-on:change="
                    change_limits(
                      'term-deval-slider-' + index,
                      'term-deval-check-' + index,
                      entry
                    );
                    searchSubset();
                  "
                />
                <label for="edgeCheck"> inverse selection</label>
              </div>
              <div class="body-selection">
                <div :id="'term-deval-slider-' + index"></div>
                <input
                  type="number"
                  v-bind:min="dboundaries[entry].min"
                  v-bind:max="dboundaries[entry].max"
                  v-bind:step="dboundaries[entry].step"
                  v-model="dboundaries[entry].minValue"
                  v-on:change="searchSubset()"
                  v-on:input="
                    valueChanged('term-deval-slider-' + index, [
                      dboundaries[entry].minValue,
                      dboundaries[entry].maxValue,
                    ])
                  "
                />
                <span class="seperator">-</span>
                <input
                  type="number"
                  v-bind:min="dboundaries[entry].min"
                  v-bind:max="dboundaries[entry].max"
                  v-bind:step="dboundaries[entry].step"
                  v-model="dboundaries[entry].maxValue"
                  v-on:change="searchSubset()"
                  v-on:input="
                    valueChanged('term-deval-slider-' + index, [
                      dboundaries[entry].minValue,
                      dboundaries[entry].maxValue,
                    ])
                  "
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import * as noUiSlider from "nouislider";
  import "@/slider.css";
  
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
          max: Number,
          step: 1,
        },
        pr_boundary: {
          minValue: 0,
          maxValue: 0,
          min: 0,
          max: Number,
          step: 0.01,
        },
        bc_boundary: { minValue: 0, maxValue: 0, min: 0, max: Number, step: 1 },
        dcoloumns: this.$store.state.dcoloumns,
        dboundaries: {},
        nodeCheck: false,
        formatType: null,
        check: {},
      };
    },
    methods: {
      change_limits(slider_id, check_id, entry) {
        let com = this;
        let slider = document.getElementById(slider_id);
        com.check[entry] = document.getElementById(check_id).checked;
  
        com.check[entry]
          ? slider.noUiSlider.set([0, 0])
          : slider.noUiSlider.reset();
  
        let currentBorder = slider.noUiSlider.get();
        com.dboundaries[entry].minValue = currentBorder[0];
        com.dboundaries[entry].maxValue = currentBorder[1];
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
      create_de() {
        var com = this;
  
        Object.entries(com.dcoloumns).forEach(([index, coloumn]) => {
          var slider = document.getElementById("term-deval-slider-" + index);
          noUiSlider.create(slider, {
            start: [com.dboundaries[coloumn].min, com.dboundaries[coloumn].max],
            connect: true,
            range: {
              min: com.dboundaries[coloumn].min,
              max: com.dboundaries[coloumn].max,
            },
            step: 0.01,
          });
  
          slider.noUiSlider.on("slide", function (values, handle) {
            com.dboundaries[coloumn][handle ? "maxValue" : "minValue"] =
              values[handle];
            com.searchSubset();
          });
        });
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
        com.degree_boundary["maxValue"] = maxDeg;
        com.degree_boundary["minValue"] = 0;
  
        var slider = document.getElementById("term-degree");
        noUiSlider.create(slider, {
          start: [0, maxDeg],
          connect: true,
          range: {
            min: 0,
            max: maxDeg,
          },
          format: this.formatType,
          step: 1,
        });
  
        slider.noUiSlider.on("slide", function (values, handle) {
          com.degree_boundary[handle ? "maxValue" : "minValue"] = values[handle];
          com.searchSubset();
        });
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
        com.bc_boundary["maxValue"] = maxDeg;
        com.bc_boundary["minValue"] = 0;
  
        var slider = document.getElementById("term-betweenes");
        noUiSlider.create(slider, {
          start: [0, maxDeg],
          connect: true,
          range: {
            min: 0,
            max: maxDeg,
          },
          format: this.formatType,
          step: 1,
        });
  
        slider.noUiSlider.on("slide", function (values, handle) {
          com.bc_boundary[handle ? "maxValue" : "minValue"] = values[handle];
          com.searchSubset();
        });
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
        com.pr_boundary["maxValue"] = 0;
        com.pr_boundary["minValue"] = minDeg;
  
        this.pr_boundary.min = minDeg;
        this.pr_boundary.max = 0;
        var slider = document.getElementById("term-pagerank");
        noUiSlider.create(slider, {
          start: [minDeg, 0],
          connect: true,
          range: {
            min: minDeg,
            max: 0,
          },
          step: 0.01,
        });
  
        slider.noUiSlider.on("slide", function (values, handle) {
          com.pr_boundary[handle ? "maxValue" : "minValue"] = values[handle];
          com.searchSubset();
        });
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
          subset: finalNodes.map((element) => {return element.attributes["Name"]}),
          mode: this.mode,
        });
      },
      valueChanged(id, value) {
        var slider = document.getElementById(id);
        slider.noUiSlider.set(value);
      },
      term_genes(list) {
        var term_genes = new Set(list);
        var termlist = this.$store.state.gephi_json.data.nodes.filter((element) =>
          term_genes.has(element.attributes["Name"])
        );
        return termlist;
      },
      load_data() {
        console.log("Links")
        this.parameter_data = this.term_genes(this.active_term.symbols)
  
        console.log(this.parameter_data);
      },
    },
    mounted() {
      this.formatType = {
        from: function (value) {
          return parseInt(value);
        },
        to: function (value) {
          return parseInt(value);
        },
      };
  
      this.initialize_dg();
      this.initialize_bc();
      this.initialize_pagerank();
      if (this.dcoloumns && this.mode != "term" && this.mode != "citation") this.create_de();
      this.searchSubset();
    },
    created() {
      this.load_data();
      if (this.dcoloumns) this.initialize_de();
    },
  };
  </script>
  
  <style>
  .term-statistics .menu-items {
    display: flex;
    margin: 0;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 0.5vw;
    justify-content: center;
    background-clip: content-box;
  }
  
  .term-statistics input[type="number"] {
    width: 10%;
    border: none;
    font-family: "ABeeZee", sans-serif;
    font-size: 0.5vw;
    color: white;
    background: none;
    -moz-appearance: textfield;
    -webkit-appearance: textfield;
    appearance: textfield;
    text-align: center;
  }
  
  #term-statistics {
    width: 100%;
    height: 100%;
    font-family: "ABeeZee", sans-serif;
    padding: 0.5vw;
  }
  </style>
  