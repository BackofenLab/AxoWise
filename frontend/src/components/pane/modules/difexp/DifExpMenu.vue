<template>
  <ListActionHeader>
    <Select v-model="selected_category" :options="dcoloumns" showClear placeholder="Select dcoloumns" checkmark
      class="flex-1" @update:modelValue="active_categories($event)" />
  </ListActionHeader>

  <EmptyState v-if="active_decoloumn === null" message="There is no active dcoloumn.">
  </EmptyState>

  <div v-if="active_decoloumn !== null" class="pt-2 mt-10 overflow-hidden">
    <div class="px-3 w-[80%] mx-auto relative z-[1]">
      <Slider :min="dboundary.min" :max="dboundary.max" :step="dboundary.step" v-model="dboundary.value"
        @update:modelValue="check_boundary()" />
    </div>
    <svg id="demo1" class="transform translate-x-[10%] translate-y-[-10%]" width="250" height="80"></svg>
  </div>
</template>

<script>
import * as d3 from "d3";
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";
import EmptyState from "@/components/verticalpane/EmptyState.vue";

export default {
  name: "DifExpMenu",
  props: ["active_decoloumn", "gephi_data"],
  components: { ListActionHeader, EmptyState },
  data() {
    return {
      selected_category: null,
      active_section: "",
      dcoloumns: this.$store.state.dcoloumns,
      dboundary: {
        value: 1,
        min: 1,
        max: 10,
        step: 1,
      },
    };
  },
  watch: {
    active_decoloumn() {
      console.log(this.active_decoloumn);
    },
  },
  methods: {
    active_categories(category) {
      if (!category) {
        this.reset_categories();
        return;
      }
      this.emitter.emit("decoloumn", category);
    },
    reset_categories() {
      this.emitter.emit("decoloumn", null);
    },
    change_section(bool, val) {
      var com = this;
      if (com.active_section == val) {
        com.active_section = "";
        com.$emit("tool_active_changed", bool);
      } else {
        if (com.active_section == "") com.$emit("tool_active_changed", bool);
        com.active_section = val;
      }
    },
    draw_legend: function () {
      var com = this;

      var minB = -com.dboundary.value;
      var maxB = com.dboundary.value;
      var listB = [minB, minB / 2, minB / 4, 0, maxB / 4, maxB / 2, maxB];
      var svgWidth = 125;
      var svgHeight = 100;

      document.getElementById("demo1").innerHTML = "";
      var svg = d3
        .select("#demo1")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `0 0 ${svgWidth * 2} ${svgHeight}`);

      var xScale = d3
        .scaleLinear()
        .domain(listB)
        .range([10, 40, 70, 100, 130, 160, 190]);

      var xAxis = d3.axisBottom(xScale).tickValues(listB);

      svg
        .append("g")
        .attr("transform", "translate(0,68)")
        .attr("color", "white")
        .call(xAxis);

      var colorScale = d3
        .scaleLinear()
        .domain([minB, 0, maxB])
        .range(["blue", "white", "red"]);

      var gradient = svg
        .append("defs")
        .append("linearGradient")
        .attr("id", "legendGradient")
        .attr("x1", "0%")
        .attr("x2", "100%");

      gradient
        .append("stop")
        .attr("offset", "0%")
        .attr("stop-color", colorScale(minB));

      gradient
        .append("stop")
        .attr("offset", "50%")
        .attr("stop-color", colorScale(0));

      gradient
        .append("stop")
        .attr("offset", "100%")
        .attr("stop-color", colorScale(maxB));

      // Create the legend bar using the linear gradient
      svg
        .append("rect")
        .attr("x", 10) // Adjust the x-coordinate to center it
        .attr("y", 50) // Adjust the y-coordinate to center it vertically
        .attr("width", 180)
        .attr("height", 15)
        .style("fill", "url(#legendGradient");
    },
    check_boundary: function () {
      var com = this;
      com.draw_legend();
      com.emitter.emit("adjustDE", this.dboundary.value);
    },
  },
  updated() {
    if (this.active_decoloumn != null) {
      this.draw_legend();
      this.emitter.emit("adjustDE", this.dboundary.value);
    }
  },
};
</script>