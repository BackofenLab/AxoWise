/* eslint-disable no-redeclare */
/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */

import * as d3 from "d3";
import { scaleLinear } from "d3-scale";

export default function heatmapDendro(data, parent, snapshot) {
  if (!data || !data.matrix) return;

  const labelsFromTree = (nodes, cluster) =>
    nodes.map((node) => node.data.name);

  const clusterSpace = 50;
  const cellSize = 12;
  const colNumber = data.matrix[0].length;
  const rowNumber = data.matrix.length;
  const width = cellSize * colNumber + clusterSpace;
  const height = cellSize * rowNumber + clusterSpace;

  const rowCluster = d3.cluster().size([height - clusterSpace, clusterSpace]);
  const hierarchyRow = rowCluster(d3.hierarchy(data.rowJSON));
  const rowNodes = hierarchyRow.leaves();
  const linksNodes = hierarchyRow.links();
  const rowLabel = labelsFromTree(rowNodes, rowCluster);
  const colLabel = data.colJSON;

  rowNodes.forEach((node, i) => {
    node.x = cellSize / 2 + cellSize * i;
  });

  hierarchyRow.each((node) => {
    if (node.children) {
      node.x = d3.mean(node.children, (child) => child.x);
      node.y = d3.min(node.children, (child) => child.y) - 5;
    }
  });

  const updatedMatrix = rowLabel.map((label) => {
    const rowIndex = data.rowIndex[label];
    return data.matrix[rowIndex];
  });

  const matrix = [];
  for (let r = 0; r < rowNumber; r++) {
    for (let c = 0; c < colNumber; c++) {
      matrix.push({ row: r + 1, col: c + 1, value: updatedMatrix[r][c] });
    }
  }

  var output = `<?xml version="1.0" encoding="utf-8"?>\n`;
  output += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n';
  output += new XMLSerializer().serializeToString(
    drawHeatmap(parent, matrix, rowLabel, colLabel, linksNodes, snapshot, cellSize, clusterSpace, colNumber, rowNumber, height, width).node()
  );

  return output;
}

function drawHeatmap(
  parent,
  matrix,
  rowLabel,
  colLabel,
  linksNodes,
  snapshot,
  cellSize,
  clusterSpace,
  colNumber,
  rowNumber,
  height,
  width
) {
  let svg;

  if (!snapshot) {
    // Create the SVG element with dimensions matching the parent container
    d3.select(parent).selectAll("svg").remove();
    svg = d3
      .select(parent)
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", `0 0 ${500} ${500}`)
      .call(d3.zoom().on("zoom", (event) => {
        svg.attr("transform", event.transform);
      }))
      .append("g");
  } else {
    clusterSpace = 0;
    const container = document.createElement("div");
    svg = d3
      .select(container)
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", `0 0 ${cellSize * (colNumber + 2)} ${cellSize * (rowNumber + 2)}`);
  }

  const colorScale = scaleLinear()
    .domain([0, 30, 100])
    .range(["white", "orange", "red"]);
  
    
    svg.selectAll("*").remove();

  if (!snapshot) {
    const rowLabels = svg
      .append("g")
      .selectAll(".rowLabelg")
      .data(rowLabel)
      .enter()
      .append("text")
      .text((d) => d)
      .attr("x", 0)
      .attr("y", (d, i) => (i + 1) * cellSize + 1 + clusterSpace)
      .style("text-anchor", "start")
      .attr("transform", `translate(${width + cellSize * 1.5},${cellSize / 1.5})`)
      .attr("class", (d, i) => `rowLabel mono r${i}`);

    const colLabels = svg
      .append("g")
      .selectAll(".colLabelg")
      .data(colLabel)
      .enter()
      .append("text")
      .text((d) => d)
      .attr("x", 0)
      .attr("y", (d, i) => (i + 1) * cellSize + 1)
      .style("text-anchor", "end")
      .attr("transform", `translate(${cellSize / 2},-6) rotate (-90) translate(-${height + cellSize * 2},${clusterSpace})`)
      .attr("class", (d, i) => `colLabel mono c${i}`);

    const rTree = svg
      .append("g")
      .attr("class", "rtree")
      .attr("transform", `translate(10, ${clusterSpace + cellSize})`);

    const rlink = rTree
      .selectAll(".rlink")
      .data(linksNodes)
      .enter()
      .append("path")
      .attr("class", "rlink")
      .attr("d", elbow);
  }

  const heatMap = svg
    .append("g")
    .attr("class", "g3")
    .selectAll(".cellg")
    .data(matrix, (d) => `${d.row}:${d.col}`)
    .enter()
    .append("rect")
    .attr("x", (d) => d.col * cellSize + clusterSpace)
    .attr("y", (d) => d.row * cellSize + clusterSpace)
    .attr("class", (d) => `cell cell-border cr${d.row - 1} cc${d.col - 1}`)
    .attr("width", cellSize)
    .attr("height", cellSize)
    .style("fill", (d) => colorScale(d.value))
    .on("mouseover", function (event, d) {
      d3.select(this).classed("cell-hover", true);
      const mouseX = event.pageX;
      const mouseY = event.pageY;
      d3.select("#d3tooltip")
        .style("left", `${mouseX + 10}px`)
        .style("top", `${mouseY - 10}px`)
        .select("#value")
        .html(
          `Cluster: ${colLabel[d.col - 1]}<br>Pathway: ${rowLabel[d.row - 1]}<br>Value: ${d.value/100}`
        );
      d3.select("#d3tooltip").transition().duration(200).style("opacity", 0.9);
    })
    .on("mouseout", function () {
      d3.select(this).classed("cell-hover", false);
      d3.selectAll(".rowLabel").classed("text-highlight", false);
      d3.selectAll(".colLabel").classed("text-highlight", false);
      d3.select("#d3tooltip").transition().duration(200).style("opacity", 0);
    });

  function elbow(d, i) {
    return `M${d.source.y},${d.source.x}V${d.target.x}H${d.target.y}`;
  }

  const style = svg.append("style").attr("type", "text/css");

  // Define the styles for .rlink and .clink classes within the <style> element
  style.text(`
    .rlink, .clink {
      fill: none;
      stroke: #ccc;
      stroke-width: 1.5px;
    }

    text.mono {
      font-size: 9pt;
      font-family: Consolas, courier;
      fill: #aaa;
    }
  `);

  return svg;
}
