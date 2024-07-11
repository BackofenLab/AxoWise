<template>
  <div class="loading-section">
    <div class="loading-text" v-if="filt_heatmap.size == 0">
      <span>There is no generated heatmap.</span>
    </div>
    <div class="slider" tabindex="0" v-if="filt_heatmap.size != 0">
      <div
        v-for="(entry, index) in filt_heatmap"
        :key="index"
        class="graph"
        v-on:click="switch_heatmap(entry)"
        @mouseover="activeHeatmapIndex = index"
        @mouseout="activeHeatmapIndex = -1"
      >
        <SnapshotHeatmap :propValue="entry" :index="entry.id" />
        <div class="graph-options">
          <div
            class="bookmark-graph"
            v-show="activeHeatmapIndex == index"
            v-on:click.stop="add_graph(entry)"
            :class="{ checked: favourite_heatmaps.has(entry.id) }"
            ref="checkboxStatesHeatmap"
          ></div>
          <img
            class="remove-graph"
            v-show="activeHeatmapIndex == index"
            src="@/assets/pathwaybar/cross.png"
            v-on:click.stop="remove_graph(entry)"
          />
          <div class="graph-name">
            <input
              type="text"
              v-model="entry.label"
              class="empty"
              @click.stop
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { agnes } from "ml-hclust";
import heatmapDendro from "@/components/enrichment/heatmap/drawHeatmap.js";
import SnapshotHeatmap from "@/components/enrichment/heatmap/SnapshotHeatmap.vue";

export default {
  name: "PathwayHeatmap",
  props: ["bookmark_off"],
  components: {
    SnapshotHeatmap,
  },
  data() {
    return {
      favourite_heatmaps: new Set(),
      activeHeatmapIndex: -1,
      heatmap_number: 0,
      heatmap_dict: [],
      heatmap_dict_array: [],
      export_image: null,
    };
  },
  mounted() {
    var com = this;
    if (this.mode != "term") {
      this.emitter.on("generateHeatmap", (pathway_data) => {
        this.draw_heatmap(pathway_data);
      });
      this.emitter.on("exportHeatmap", () => {
        this.export_svg();
      });
    }

    com.heatmap_dict_array = this.$store.state.term_heatmap_dict;
    com.favourite_heatmaps = this.$store.state.favourite_heatmaps_dict;
    if (this.heatmap_dict_array.length != 0) {
      this.heatmap_number = Math.max.apply(
        Math,
        this.heatmap_dict_array.map((item) => item.id)
      );
      this.heatmap_dict = new Set(this.heatmap_dict_array);
    } else {
      this.heatmap_dict = new Set();
    }
    console.log(
      "mounted",
      this.favourite_heatmaps,
      this.$store.state.favourite_heatmaps_dict
    );
  },
  beforeUnmount() {
    this.emitter.off("generateHeatmap");
    this.emitter.off("exportHeatmap");
  },
  methods: {
    draw_heatmap(pathway_data) {
      var matrix = this.generateMatrix([...pathway_data]);
      const clusterTree = this.createClusterTree(
        this.createRowClust(matrix.data),
        matrix.rowLabels
      );

      var data = {
        matrix: matrix.data,
        rowJSON: clusterTree,
        colJSON: matrix.colLabels,
        rowIndex: matrix.rowIndex,
      };
      this.heatmap_number += 1;
      this.$store.commit("assign_new_heatmap_graph", {
        id: this.heatmap_number,
        label: `Heatmap ${this.heatmap_number}`,
        graph: data,
      });
      this.heatmap_dict.add({
        id: this.heatmap_number,
        label: `Heatmap ${this.heatmap_number}`,
        graph: data,
      });
    },
    generateMatrix(terms) {
      const { node_cluster_index, node_modul_index } = this.$store.state,
        matrix = [],
        rowLabelToIndex = {};

      for (const term of terms) {
        const matrixRow = [];
        for (const clusterKey of Object.keys(node_cluster_index)) {
          if (!node_modul_index.has(clusterKey)) {
            matrixRow.push(
              this.calcPercentageHeatmap(term, node_cluster_index[clusterKey])
            );
          }
        }
        rowLabelToIndex[term.name] = matrix.length;
        matrix.push(matrixRow);
      }

      var adjustedMatrix = this.removeColoumns(
        matrix,
        Object.keys(node_cluster_index).filter(
          (key) => !node_modul_index.has(key)
        )
      );

      return {
        data: adjustedMatrix.matrix,
        rowLabels: Object.keys(rowLabelToIndex),
        colLabels: adjustedMatrix.colLabels,
        rowIndex: rowLabelToIndex,
      };
    },

    removeColoumns(matrix, colLabels) {
      var hasValues = matrix.reduce(
          (r, a) => a.map((value, i) => r[i] || value),
          []
        ),
        newMatrix = matrix.map((a) => a.filter((_, i) => hasValues[i])),
        newcolLabels = colLabels.filter((_, i) => hasValues[i]);

      return { matrix: newMatrix, colLabels: newcolLabels };
    },
    createRowClust(matrix) {
      return agnes(matrix, { method: "upgma" });
    },

    calcPercentageHeatmap(term, cluster) {
      var includedProteins = 0;
      for (var protein of term.symbols) {
        if (cluster.has(protein)) includedProteins += 1;
      }
      return (includedProteins / term.symbols.length) * 100;
    },

    createClusterTree(linkage, rowLabels) {
      if (linkage.size === 1) {
        return { name: [rowLabels[linkage.index]] };
      } else {
        const leftTree = this.createClusterTree(linkage.children[0], rowLabels),
          rightTree = this.createClusterTree(linkage.children[1], rowLabels),
          nodeName = rowLabels[linkage.index] || "node_" + linkage.index;
        return {
          name: [nodeName],
          children: [leftTree, rightTree],
        };
      }
    },
    switch_heatmap(entry) {
      this.emitter.emit("heatmapView");
      this.export_image = heatmapDendro(entry.graph, "#sigma-heatmap", false);
      this.draw_legend();
    },
    remove_graph(entry) {
      if (!this.favourite_heatmaps.has(entry)) {
        // Checkbox is checked, add its state to the object
        this.favourite_heatmaps.delete(entry);
      }
      this.heatmap_dict.delete(entry);
      this.$store.commit("update_heatmap_dict", [...this.heatmap_dict]);
      this.$store.commit("assign_favourite_heatmap", this.favourite_heatmaps);
    },
    add_graph(entry) {
      if (!this.favourite_heatmaps.has(entry.id)) {
        this.favourite_heatmaps.add(entry.id);
      } else {
        this.favourite_heatmaps.delete(entry.id);
      }
      this.$store.commit("assign_favourite_heatmap", this.favourite_heatmaps);
      console.log(
        "added",
        this.favourite_heatmaps,
        this.$store.state.favourite_heatmaps_dict
      );
    },
    export_svg() {
      this.download(this.export_image, "heatmap.svg");
    },
    createBlob(data) {
      return new Blob([data], { type: "image/svg+xml;charset=utf-8" });
    },
    download(string, filename) {
      // Creating blob href
      var blob = this.createBlob(string);

      // Anchor
      var o = {};
      o.anchor = document.createElement("a");
      o.anchor.setAttribute("href", URL.createObjectURL(blob));
      o.anchor.setAttribute("download", filename);

      // Click event
      var event = document.createEvent("MouseEvent");
      event.initMouseEvent(
        "click",
        true,
        false,
        window,
        0,
        0,
        0,
        0,
        0,
        false,
        false,
        false,
        false,
        0,
        null
      );

      URL.revokeObjectURL(blob);

      o.anchor.dispatchEvent(event);
      delete o.anchor;
    },
    draw_legend() {
      const colorScale = d3
        .scaleLinear()
        .domain([0, 30, 100])
        .range(["white", "orange", "red"]);

      var listB = [0, 0.5, 1];

      var svgWidth = 320; // Define the SVG width
      var svgHeight = 100; // Define the SVG height

      var svg = d3
        .select("#heatdemo")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `0 0 ${svgWidth * 2.2} ${svgHeight}`)
        .append("g")
        .attr("transform", `translate(${svgWidth / 1.6}, ${svgHeight / 2})`); // Center the SVG content

      var xScale = d3.scaleLinear().domain([0, 1]).range([0, 300]); // Adjust the range to center it

      var xAxis = d3.axisBottom(xScale).tickValues(listB);

      svg.append("g").attr("transform", "translate(0, 5)").call(xAxis);

      svg.selectAll("text").style("fill", "white");

      // Remove the domain (the line along the x-axis)
      svg.select(".domain").remove();

      // Create a linear gradient for the legend bar using the existing colorScale
      var gradient = svg
        .append("defs")
        .append("linearGradient")
        .attr("id", "legendGradient")
        .attr("x1", "0%")
        .attr("x2", "100%");

      gradient
        .append("stop")
        .attr("offset", "0%")
        .attr("stop-color", colorScale(0));

      gradient
        .append("stop")
        .attr("offset", "30%")
        .attr("stop-color", colorScale(30));

      gradient
        .append("stop")
        .attr("offset", "100%")
        .attr("stop-color", colorScale(100));

      // Create the legend bar using the linear gradient
      svg
        .append("rect")
        .attr("x", 0) // Adjust the x-coordinate to center it
        .attr("y", -10) // Adjust the y-coordinate to center it vertically
        .attr("width", 300)
        .attr("height", 15)
        .style("fill", "url(#legendGradient");

      // Optionally, you can add a border to the legend bar
      svg
        .append("rect")
        .attr("x", 0)
        .attr("y", -10)
        .attr("width", 300)
        .attr("height", 15)
        .attr("stroke", "white")
        .attr("stroke-width", 0.5)
        .attr("fill", "none");

      return svg;
    },
  },
  computed: {
    filt_heatmap() {
      var com = this;
      var filtered = [...com.heatmap_dict];

      if (!com.bookmark_off) {
        filtered = filtered.filter(function (heatmap) {
          return com.favourite_heatmaps.has(heatmap.id);
        });
      }

      return new Set(filtered);
    },
  },
};
</script>

<style>
#sigma-heatmap {
  display: block;
  position: absolute;
  cursor: default;
  position: absolute;
  height: 100%;
  width: 75%;
  left: 25%;
  box-sizing: border-box;
  overflow: hidden;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

#d3tooltip {
  position: absolute;
  width: 200px;
  height: auto;
  padding: 10px;
  background-color: #fafafa;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  -webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
  -moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
  pointer-events: none;
  opacity: 0;
  z-index: 999;
}

#d3tooltip.hidden {
  display: none;
}

#d3tooltip p {
  margin: 0;
  font-family: sans-serif;
  font-size: 12px;
  line-height: 20px;
}

rect.selection {
  stroke: #333;
  stroke-dasharray: 4px;
  stroke-opacity: 0.5;
  fill: transparent;
}

rect.cell-border {
  stroke: #eee;
  stroke-width: 0.3px;
}

rect.cell-selected {
  stroke: rgb(51, 102, 153);
  stroke-width: 0.5px;
}

rect.cell-hover {
  stroke: #f00;
  stroke-width: 0.3px;
}

.legend {
  position: absolute;
  bottom: 0;
  padding: 20px;
  align-items: center;
  justify-content: center;
  display: block;
}

#heatdemo {
  position: absolute;
  bottom: 0;
  text-align: center;
  width: 100%;
}
</style>
