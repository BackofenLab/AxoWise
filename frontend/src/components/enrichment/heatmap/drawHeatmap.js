/* eslint-disable no-redeclare */
/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */

import * as d3 from "d3";
import {scaleLinear} from "d3-scale";

export default function heatmapDendro (data, parent) {

        if (!data || !data.matrix)
            return;

        var svg = d3.select(parent)
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%");

        var margin = {top: 10, right: 0, bottom: 10, left: 0},
        height = 150 - margin.top - margin.bottom;

        var labelsFromTree = function (nodes, cluster) {
            var labels = [];

            for (var n in nodes) {
                    labels.push(nodes[n].data.name);
            }
            return labels;
        };

        var clusterSpace = 100, // size of the cluster tree
            cellSize = 12,
            colNumber = data.matrix[0].length,
            rowNumber = data.matrix.length,
            width = cellSize * colNumber + clusterSpace, // - margin.left - margin.right,
            height = cellSize * rowNumber + clusterSpace, // - margin.top - margin.bottom,
            rowCluster = d3.cluster()
            .size([height - clusterSpace, clusterSpace]),
            hierarchyRow = rowCluster(d3.hierarchy(data.rowJSON)),
            rowNodes = hierarchyRow.leaves(), 
            rowLabel = labelsFromTree(rowNodes, rowCluster),
            colLabel = data.colJSON;

        for (var e in rowNodes) rowNodes[e].x = cellSize/2 + cellSize * e;

        hierarchyRow.each(function(node) {
            if (node.children) {
                // Calculate the average position of child nodes
                node.x = d3.mean(node.children, function(child) {
                return child.x;
                });
                node.y = d3.min(node.children, function(child) {
                return child.y;
                }) - 5;
            }
        });

        // Create a new matrix with the updated order
        var updatedMatrix = [];
        for (var label of rowLabel) {
        var rowIndex = data.rowIndex[label];
        updatedMatrix.push(data.matrix[rowIndex]);
        }

        var matrix = [];
        for (var r = 0; r < rowNumber; r++) {
            for (var c = 0; c < colNumber; c++) {
                matrix.push({row: r + 1, col: c + 1, value: updatedMatrix[r][c]});
            }
        }

        var colorScale = scaleLinear()
        .domain([0, 30, 100])
        .range(["white", "orange", "red"]);

        svg.selectAll("*").remove();


        var rowLabels = svg.append("g")
            .selectAll(".rowLabelg")
            .data(rowLabel)
            .enter()
            .append("text")
            .text(function (d) {
                return d;
            })
            .attr("x", 0)
            .attr("y", function (d, i) {
                return (i + 1) * cellSize + 1 + clusterSpace;
            })
            .style("text-anchor", "start")
            .attr("transform", "translate(" + (width + cellSize) + "," + cellSize / 1.5 + ")")
            .attr("class", function (d, i) {
                return "rowLabel mono r" + i;
            });

        var colLabels = svg.append("g")
            .selectAll(".colLabelg")
            .data(colLabel)
            .enter()
            .append("text")
            .text(function (d) {
                return d;
            })
            .attr("x", 0)
            .attr("y", function (d, i) {
                return (i + 1) * cellSize + 1;
            })
            .style("text-anchor", "end")
            .attr("transform", "translate(" + cellSize / 2 + ",-6) rotate (-90)  translate( -" + (height + cellSize * 2) + "," + clusterSpace + ")")
            .attr("class", function (d, i) {
                return "colLabel mono c" + i;
            });

        var heatMap = svg.append("g").attr("class", "g3")
            .selectAll(".cellg")
            .data(matrix, function (d) {
                return d.row + ":" + d.col;
            })
            .enter()
            .append("rect")
            .attr("x", function (d) {
                return d.col * cellSize + clusterSpace;
            })
            .attr("y", function (d) {
                return d.row * cellSize + clusterSpace;
            })
            .attr("class", function (d) {
                return "cell cell-border cr" + (d.row - 1) + " cc" + (d.col - 1);
            })
            .attr("width", cellSize)
            .attr("height", cellSize)
            .style("fill", function (d) {
                return colorScale(d.value);
            })
            .on("mouseover", function (event,d) {
                d3.select(this).classed("cell-hover", true);
                //Update the tooltip position and value
                d3.select("#d3tooltip")
                    .style("left", (d3.pointer(event)[0] + 10) + "px")
                    .style("top", (d3.pointer(event)[1] - 10) + "px")
                    .select("#value")
                    .html(
                        "Cell type: " + colLabel[d.col - 1] + "<br>Sample name: " + rowLabel[d.row - 1]
                        + "<br>Value: " + d.value
                        );
                //Show the tooltip
                d3.select("#d3tooltip").transition()
                    .duration(200)
                    .style("opacity", .9);
            })
            .on("mouseout", function () {
                d3.select(this).classed("cell-hover", false);
                d3.selectAll(".rowLabel").classed("text-highlight", false);
                d3.selectAll(".colLabel").classed("text-highlight", false);
                d3.select("#d3tooltip").transition()
                    .duration(200)
                    .style("opacity", 0);
            })
            ;

//tree for rows
        var rTree = svg.append("g").attr("class", "rtree").attr("transform", "translate (10, " + (clusterSpace + cellSize) + ")");
        var rlink = rTree.selectAll(".rlink")
            .data(hierarchyRow.links())
            .enter().append("path")
            .attr("class", "rlink")
            .attr("d", elbow);

        function elbow(d, i) {
            return "M" + d.source.y + "," + d.source.x
                + "V" + d.target.x + "H" + d.target.y;
        }

        var style = svg.append("style")
        .attr("type", "text/css");
    
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

        
        // var output = '<?xml version="1.0" encoding="utf-8"?>\n';
        // output += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n';
        // output += new XMLSerializer().serializeToString(svg.node());

    // /**
    //  * Utilities
    //  */
    // function createBlob(data) {
    //     return new Blob(
    //       [data],
    //       {type: 'image/svg+xml;charset=utf-8'}
    //     );
    //   }
    
    // function download(string, filename) {

    // // Creating blob href
    // var blob = createBlob(string);

    // // Anchor
    // var o = {};
    // o.anchor = document.createElement('a');
    // o.anchor.setAttribute('href', URL.createObjectURL(blob));
    // o.anchor.setAttribute('download', filename);

    // // Click event
    // var event = document.createEvent('MouseEvent');
    // event.initMouseEvent('click', true, false, window, 0, 0, 0 ,0, 0,
    //     false, false, false, false, 0, null);

    // URL.revokeObjectURL(blob);

    // o.anchor.dispatchEvent(event);
    // delete o.anchor;
    // }

    // download(output, "test.svg");

    }