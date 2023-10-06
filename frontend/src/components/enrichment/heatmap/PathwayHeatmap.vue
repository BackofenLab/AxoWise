<template>
    <div id="pathways-heatmaps" v-on:click="draw_heatmap()">
    </div>
</template>

<script>

import {agnes} from "ml-hclust"
import heatmapDendro from './drawHeatmap';

export default {
    name: 'PathwayHeatmap',
    props: ['favourite_pathways'],
    components: {
    },
    data() {
        return {
        }
    },

    methods: {
        draw_heatmap(){

            var matrix = this.generateMatrix([...this.favourite_pathways])
            const clusterTree = this.createClusterTree(this.createRowClust(matrix.data),matrix.rowLabels);

            var data = {"matrix": matrix.data, "rowJSON": clusterTree, "colJSON": matrix.colLabels, "rowIndex": matrix.rowIndex}

            heatmapDendro(data, "#sigma-heatmap")
        },
        generateMatrix(terms){
            const { node_cluster_index, node_modul_index } = this.$store.state,
                matrix = [], rowLabelToIndex = {};

            for (const term of terms) {
                const matrixRow = [];
                for (const clusterKey of Object.keys(node_cluster_index)) {
                    if (!node_modul_index.has(clusterKey)) {
                        matrixRow.push(this.calcPercentageHeatmap(term, node_cluster_index[clusterKey]));
                    }
                }
                rowLabelToIndex[term.name] = matrix.length;
                matrix.push(matrixRow);
            }

            var adjustedMatrix = this.removeColoumns(matrix, Object.keys(node_cluster_index).filter(key => !node_modul_index.has(key)) )

            return {"data": adjustedMatrix.matrix,
                "rowLabels": Object.keys(rowLabelToIndex),
                "colLabels":adjustedMatrix.colLabels,
                "rowIndex": rowLabelToIndex}
        },

        removeColoumns(matrix, colLabels){
            var hasValues = matrix.reduce((r, a) => a.map((value, i) => r[i] || value), []),
                newMatrix = matrix.map(a => a.filter((_, i) => hasValues[i])),
                newcolLabels = colLabels.filter((_, i) => hasValues[i]);

            return {"matrix": newMatrix, "colLabels": newcolLabels}

        },
        createRowClust(matrix) {
            return agnes(matrix, { method: 'upgma',});
        },

        calcPercentageHeatmap(term, cluster) {
            var includedProteins = 0
            for (var protein of term.proteins){
                if(cluster.has(protein)) includedProteins += 1
            }
            return (includedProteins / term.proteins.length)*100
        },

        createClusterTree(linkage, rowLabels) {
            if (linkage.size === 1) {
                return { name: [rowLabels[linkage.index]] };
            } else {
                const leftTree = this.createClusterTree(linkage.children[0], rowLabels),
                      rightTree = this.createClusterTree(linkage.children[1], rowLabels),
                      nodeName = rowLabels[linkage.index] || 'node_'+ linkage.index;
                return {
                    name: [nodeName],
                    children: [
                        leftTree,
                        rightTree
                    ]
                };
            }
        },
    }
}
</script>


<style>

#sigma-heatmap{
position: absolute;
width: 50%;
height: 50%;
z-index: 2;
}

#pathways-heatmaps {
    position: fixed;
    top: 0;
    left: 50%;
    width: 30px;
    height: 30px;
    background: blue;
    z-index: 999;
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
    opacity:0;
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
    stroke          : #333;
    stroke-dasharray: 4px;
    stroke-opacity  : 0.5;
    fill            : transparent;
}

rect.cell-border {
    stroke: #eee;
    stroke-width:0.3px;   
}

rect.cell-selected {
    stroke: rgb(51,102,153);
    stroke-width:0.5px;   
}

rect.cell-hover {
    stroke: #F00;
    stroke-width:0.3px;   
}

</style>