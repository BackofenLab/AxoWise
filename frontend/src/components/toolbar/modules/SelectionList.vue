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
  
  <!-- <div class="tool-item">
    <div id="selection_highlight" class="window-menu selection">
      <div id="selection_highlight_header" class="window-header">
        <div class="headertext">
          <span>graph parameter</span>
          <img class="protein_close" src="@/assets/toolbar/cross.png" v-on:click="unactive_proteinlist()" />
        </div>
      </div>
      <div class="selection_list">
        <div class="window-label">degree value</div>
        <div class="menu-items">
          <div id="degree"></div>
          <input type="number" v-bind:min="degree_boundary.min" v-bind:max="degree_boundary.max"
            v-bind:step="degree_boundary.step" v-model="degree_boundary.minValue" v-on:change="searchSubset()"
            v-on:input="
              valueChanged('degree', [
                degree_boundary.minValue,
                degree_boundary.maxValue,
              ])
              " />
          <span class="seperator">-</span>
          <input type="number" v-bind:min="degree_boundary.min" v-bind:max="degree_boundary.max"
            v-bind:step="degree_boundary.step" v-model="degree_boundary.maxValue" v-on:change="searchSubset()"
            v-on:input="
              valueChanged('degree', [
                degree_boundary.minValue,
                degree_boundary.maxValue,
              ])
              " />
        </div>
        <div class="window-label">betweenness centrality value</div>
        <div class="menu-items">
          <div id="betweenes"></div>
          <input type="number" v-bind:min="bc_boundary.min" v-bind:max="bc_boundary.max" v-bind:step="bc_boundary.step"
            v-model="bc_boundary.minValue" v-on:change="searchSubset()" v-on:input="
              valueChanged('betweenes', [
                bc_boundary.minValue,
                bc_boundary.maxValue,
              ])
              " />
          <span class="seperator">-</span>
          <input type="number" v-bind:min="bc_boundary.min" v-bind:max="bc_boundary.max" v-bind:step="bc_boundary.step"
            v-model="bc_boundary.maxValue" v-on:change="searchSubset()" v-on:input="
              valueChanged('betweenes', [
                bc_boundary.minValue,
                bc_boundary.maxValue,
              ])
              " />
        </div>
        <div v-if="mode == 'term'">
          <div class="window-label">padj value (log10)</div>
          <div class="menu-items">
            <div id="padj"></div>
            <input type="number" v-bind:min="padj_boundary.min" v-bind:max="padj_boundary.max"
              v-bind:step="padj_boundary.step" v-model="padj_boundary.minValue" v-on:change="searchSubset()" v-on:input="
                valueChanged('padj', [
                  padj_boundary.minValue,
                  padj_boundary.maxValue,
                ])
                " />
            <span class="seperator">-</span>
            <input type="number" v-bind:min="padj_boundary.min" v-bind:max="padj_boundary.max"
              v-bind:step="padj_boundary.step" v-model="padj_boundary.maxValue" v-on:change="searchSubset()" v-on:input="
                valueChanged('padj', [
                  padj_boundary.minValue,
                  padj_boundary.maxValue,
                ])
                " />
          </div>
        </div>
        <div class="window-label">pagerank value (log10)</div>
        <div class="menu-items">
          <div id="pagerank"></div>
          <input type="number" v-bind:min="pr_boundary.min" v-bind:max="pr_boundary.max" v-bind:step="pr_boundary.step"
            v-model="pr_boundary.minValue" v-on:change="searchSubset()" v-on:input="
              valueChanged('pagerank', [
                pr_boundary.minValue,
                pr_boundary.maxValue,
              ])
              " />
          <span class="seperator">-</span>
          <input type="number" v-bind:min="pr_boundary.min" v-bind:max="pr_boundary.max" v-bind:step="pr_boundary.step"
            v-model="pr_boundary.maxValue" v-on:change="searchSubset()" v-on:input="
              valueChanged('pagerank', [
                pr_boundary.minValue,
                pr_boundary.maxValue,
              ])
              " />
        </div>
      </div>
      <div class="dcoloumn-window" v-if="mode != 'term' && mode != 'citation'">
        <div class="coloumn-padding">
          <div class="class-section" v-on:click="coloumnsCheck = !coloumnsCheck">
            <span>coloumn section</span>
            <img src="@/assets/pane/invisible.png" v-if="!coloumnsCheck" />
            <img src="@/assets/pane/visible.png" v-if="coloumnsCheck" />
          </div>
          <span v-if="!dcoloumns" class="loading-text">no selectable dcoloumns</span>
          <div v-if="dcoloumns" class="slider-section-scroll">
            <div class="d-section-slider" v-show="coloumnsCheck" v-for="(entry, index) in dcoloumns" :key="index">
              <div class="window-label">{{ entry }}</div>
              <div class="menu-items">
                <div class="checkbox-header">
                  <input type="checkbox" :id="'deval-check-' + index" v-on:change="
                    change_limits(
                      'deval-slider-' + index,
                      'deval-check-' + index,
                      entry
                    );
                  searchSubset();
                  " />
                  <label for="edgeCheck"> inverse selection</label>
                </div>
                <div class="body-selection">
                  <div :id="'deval-slider-' + index"></div>
                  <input type="number" v-bind:min="dboundaries[entry].min" v-bind:max="dboundaries[entry].max"
                    v-bind:step="dboundaries[entry].step" v-model="dboundaries[entry].minValue"
                    v-on:change="searchSubset()" v-on:input="
                      valueChanged('deval-slider-' + index, [
                        dboundaries[entry].minValue,
                        dboundaries[entry].maxValue,
                      ])
                      " />
                  <span class="seperator">-</span>
                  <input type="number" v-bind:min="dboundaries[entry].min" v-bind:max="dboundaries[entry].max"
                    v-bind:step="dboundaries[entry].step" v-model="dboundaries[entry].maxValue"
                    v-on:change="searchSubset()" v-on:input="
                      valueChanged('deval-slider-' + index, [
                        dboundaries[entry].minValue,
                        dboundaries[entry].maxValue,
                      ])
                      " />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div> -->
</template>

<script>
// import * as noUiSlider from "nouislider";
// import "@/slider.css";

export default {
  name: "SelectionList",
  props: ["data", "mode", "active_subset", "active_term", "selection_active"],
  // emits: ["selection_active_changed"],
  data() {
    return {
      // once: true,
      // search_data: null,
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
      // formatType: null,
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
    // change_limits(slider_id, check_id, entry) {
    //   let com = this;
    //   let slider = document.getElementById(slider_id);
    //   com.check[entry] = document.getElementById(check_id).checked;

    //   com.check[entry]
    //     ? slider.noUiSlider.set([0, 0])
    //     : slider.noUiSlider.reset();

    //   let currentBorder = slider.noUiSlider.get();
    //   com.dboundaries[entry].minValue = currentBorder[0];
    //   com.dboundaries[entry].maxValue = currentBorder[1];
    // },
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
    },
    // create_de() {
    //   var com = this;
    //   Object.entries(com.dcoloumns).forEach(([index, coloumn]) => {
    //     var slider = document.getElementById("deval-slider-" + index);
    //     noUiSlider.create(slider, {
    //       start: [com.dboundaries[coloumn].min, com.dboundaries[coloumn].max],
    //       connect: true,
    //       range: {
    //         min: com.dboundaries[coloumn].min,
    //         max: com.dboundaries[coloumn].max,
    //       },
    //       step: 0.01,
    //     });

    //     slider.noUiSlider.on("slide", function (values, handle) {
    //       com.dboundaries[coloumn][handle ? "maxValue" : "minValue"] =
    //         values[handle];
    //       com.searchSubset();
    //     });
    //   });
    // },
    // dragElement(elmnt) {
    //   var pos1 = 0,
    //     pos2 = 0,
    //     pos3 = 0,
    //     pos4 = 0;
    //   if (document.getElementById(elmnt.id + "_header")) {
    //     // if present, the header is where you move the DIV from:
    //     document.getElementById(elmnt.id + "_header").onmousedown =
    //       dragMouseDown;
    //   } else {
    //     // otherwise, move the DIV from anywhere inside the DIV:
    //     elmnt.onmousedown = dragMouseDown;
    //   }

    //   function dragMouseDown(e) {
    //     e = e || window.event;
    //     e.preventDefault();
    //     // get the mouse cursor position at startup:
    //     pos3 = e.clientX;
    //     pos4 = e.clientY;
    //     document.onmouseup = closeDragElement;
    //     // call a function whenever the cursor moves:
    //     document.onmousemove = elementDrag;
    //   }

    //   function elementDrag(e) {
    //     e = e || window.event;
    //     e.preventDefault();
    //     // calculate the new cursor position:
    //     pos1 = pos3 - e.clientX;
    //     pos2 = pos4 - e.clientY;
    //     pos3 = e.clientX;
    //     pos4 = e.clientY;
    //     // set the element's new position:
    //     elmnt.style.top = elmnt.offsetTop - pos2 + "px";
    //     elmnt.style.left = elmnt.offsetLeft - pos1 + "px";
    //   }

    //   function closeDragElement() {
    //     // stop moving when mouse button is released:
    //     document.onmouseup = null;
    //     document.onmousemove = null;
    //   }
    // },
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
      // var slider = document.getElementById("degree");
      // if (!slider.noUiSlider) {
      //   noUiSlider.create(slider, {
      //     start: [0, maxDeg],
      //     connect: true,
      //     range: {
      //       min: 0,
      //       max: maxDeg,
      //     },
      //     format: this.formatType,
      //     step: 1,
      //   });

      //   slider.noUiSlider.on("slide", function (values, handle) {
      //     com.degree_boundary[handle ? "maxValue" : "minValue"] =
      //       values[handle];
      //     com.searchSubset();
      //   });
      // } else {
      //   console.log(slider.noUiSlider);
      //   slider.noUiSlider.updateOptions({
      //     start: [0, maxDeg],
      //     range: {
      //       min: 0,
      //       max: maxDeg,
      //     },
      //   });
      // }
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
      // var slider = document.getElementById("betweenes");

      // if (!slider.noUiSlider) {
      //   noUiSlider.create(slider, {
      //     start: [0, maxDeg],
      //     connect: true,
      //     range: {
      //       min: 0,
      //       max: maxDeg,
      //     },
      //     format: this.formatType,
      //     step: 1,
      //   });

      //   slider.noUiSlider.on("slide", function (values, handle) {
      //     com.bc_boundary[handle ? "maxValue" : "minValue"] = values[handle];
      //     com.searchSubset();
      //   });
      // } else {
      //   slider.noUiSlider.updateOptions({
      //     range: {
      //       min: 0,
      //       max: maxDeg,
      //     },
      //   });
      // }
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

      // var slider = document.getElementById("pagerank");
      // if (!slider.noUiSlider) {
      //   noUiSlider.create(slider, {
      //     start: [minDeg, 0],
      //     connect: true,
      //     range: {
      //       min: minDeg,
      //       max: 0,
      //     },
      //     step: 0.01,
      //   });

      //   slider.noUiSlider.on("slide", function (values, handle) {
      //     com.pr_boundary[handle ? "maxValue" : "minValue"] = values[handle];
      //     com.searchSubset();
      //   });
      // } else {
      //   slider.noUiSlider.updateOptions({
      //     range: {
      //       min: minDeg,
      //       max: 0,
      //     },
      //   });
      // }
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
      // var slider = document.getElementById("padj");
      // if (!slider.noUiSlider) {
      //   noUiSlider.create(slider, {
      //     start: [minDeg, 0],
      //     connect: true,
      //     range: {
      //       min: minDeg,
      //       max: 0,
      //     },
      //     step: 0.01,
      //   });

      //   slider.noUiSlider.on("slide", function (values, handle) {
      //     com.padj_boundary[handle ? "maxValue" : "minValue"] = values[handle];
      //     com.searchSubset();
      //   });
      // } else {
      //   slider.noUiSlider.updateOptions({
      //     range: {
      //       min: minDeg,
      //       max: 0,
      //     },
      //   });
      // }
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
    // unactive_proteinlist() {
    //   this.$emit("selection_active_changed", false);
    //   // if(this.active_subset) this.emitter.emit("searchSubset", {subset:this.search_data, mode:this.mode});
    // },
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
    // valueChanged(id, value) {
    //   var slider = document.getElementById(id);
    //   slider.noUiSlider.set(value);
    // },
    // term_genes(list) {
    //   var term_genes = new Set(list);
    //   var termlist = this.data.nodes.filter((element) =>
    //     term_genes.has(element.attributes["Name"])
    //   );
    //   return termlist;
    // },
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
    // this.formatType = {
    //   from: function (value) {
    //     return parseInt(value);
    //   },
    //   to: function (value) {
    //     return parseInt(value);
    //   },
    // };

    // this.dragElement(document.getElementById("selection_highlight"));

    this.initialize_all();
  },
  created() {
    if (this.dcoloumns) this.initialize_de();
  },
};
</script>

<!-- <style>
.selection_list {
  position: relative;
  width: 100%;
  height: 100%;
  padding-top: 3%;
  border-radius: 0px 0px 5px 5px;
  backdrop-filter: blur(7.5px);
  overflow-y: scroll;
  overflow-x: hidden;
}

.selection .menu-items {
  display: flex;
  margin: 0;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.5vw;
  justify-content: center;
  background-clip: content-box;
}

.slider-section-scroll .menu-items {
  display: grid;
  grid-template-rows: 1fr 1fr;
  margin: 0;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.5vw;
  justify-content: center;
  background-clip: content-box;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.selection_list::-webkit-scrollbar,
.slider-section-scroll::-webkit-scrollbar {
  display: none;
}

.selection .window-label {
  color: white;
  white-space: nowrap;
  overflow-x: hidden;
  /* Hide overflow content */
  text-overflow: ellipsis;
  margin: 0 0.5vw 0 0.5vw;
  width: auto;
}

.selection input[type="number"] {
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

.selection input[type="range"] {
  appearance: none;
  outline: none;
  width: 10vw;
  height: 0.3vw;
  border-radius: 5px;
  background-color: #ccc;
}

.selection input[type="range"]::-webkit-slider-thumb {
  background: #fafafa;
  appearance: none;
  box-shadow: 1px 2px 26px 1px #bdbdbd;
  width: 0.8vw;
  height: 0.8vw;
  border-radius: 50%;
}

.seperator {
  font-size: 0.5vw;
  margin: 0 0.1vw 0 0.1vw;
  align-self: center;
  justify-content: center;
}

.dcoloumn-window {
  width: 100%;
  height: 100%;
  padding: 0.7vw;
  overflow: hidden;
}

.class-section {
  height: 1.2vw;
  width: 100%;
  display: flex;
  font-size: 0.7vw;
  background: #d9d9d9;
}

.class-section img {
  width: 0.7vw;
  position: absolute;
  justify-content: center;
  align-self: center;
  right: 1.1vw;
}

.class-section span {
  width: 100%;
  align-self: center;
  text-align-last: center;
}

.d-section-slider {
  padding: 4% 5% 0 5%;
}

.noUi-target {
  margin: 0.5vw 0.9vw 0.5vw 0;
  width: 8.5vw;
}

.coloumn-padding {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  border: solid 0.01vw rgba(255, 255, 255, 0.3);
}

.slider-section-scroll {
  height: 100%;
  width: 100%;
  overflow-y: scroll;
}

.body-selection {
  padding-left: 0.5rem;
  display: -webkit-flex;
}

.checkbox-header {
  padding: 0.5rem 0 0 0.3rem;
  font-size: 0.6vw;
}

.checkbox-header input[type="checkbox"] {
  accent-color: green;
}
</style> -->
