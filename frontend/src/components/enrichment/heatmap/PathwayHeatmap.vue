<template>
    <div class="slider" tabindex="0">
        <div v-for="(entry, index) in filt_heatmap" :key="index" class="graph" v-on:click="switch_heatmap(entry)" @mouseover="activeHeatmapIndex = index" @mouseout="activeHeatmapIndex = -1">
            <SnapshotHeatmap :propValue="entry" :index="entry.id"/>
            <div class="graph-options" v-show="activeHeatmapIndex == index" >
                <div class="bookmark-graph" v-on:click.stop="add_graph(entry)" :class="{ checked: favourite_heatmaps.has(entry)}" ref="checkboxStatesHeatmap"></div>
                <img  class="remove-graph" src="@/assets/pathwaybar/cross.png" v-on:click.stop="remove_graph(entry)">
                <div class="graph-name">
                    <input type="text" v-model="entry.label" class="empty" @click.stop />
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import {agnes} from "ml-hclust"
import heatmapDendro from './drawHeatmap';
import SnapshotHeatmap from '@/components/enrichment/heatmap/SnapshotHeatmap.vue'

export default {
    name: 'PathwayHeatmap',
    props: ['favourite_pathways','bookmark_off'],
    components: {
        SnapshotHeatmap
    },
    data() {
        return {
            favourite_heatmaps: new Set(),
            activeHeatmapIndex: -1,
            heatmap_number: 0,
            heatmap_dict: new Set()
        }
    },
    mounted(){
        this.emitter.on("generateHeatmap", () => {
            this.draw_heatmap()
        });
    },
    methods: {
        draw_heatmap(){

            var matrix = this.generateMatrix([...this.favourite_pathways])
            const clusterTree = this.createClusterTree(this.createRowClust(matrix.data),matrix.rowLabels);

            var data = {"matrix": matrix.data, "rowJSON": clusterTree, "colJSON": matrix.colLabels, "rowIndex": matrix.rowIndex}
            this.heatmap_number += 1
            this.heatmap_dict.add({ id: this.heatmap_number, label: `Heatmap ${this.heatmap_number}`, graph: data});

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
        switch_heatmap(entry) {
            heatmapDendro(entry.graph,'#sigma-heatmap', false)
        },
        remove_graph(entry) {
            if (!this.favourite_heatmaps.has(entry)) {
                // Checkbox is checked, add its state to the object
                this.favourite_heatmaps.delete(entry)
            }
            this.heatmap_dict.delete(entry)
            this.$store.commit('remove_snapshotHeatmap', entry.id)
        },
        add_graph(entry){
            if (!this.favourite_heatmaps.has(entry)) {
                // Checkbox is checked, add its state to the object
                this.favourite_heatmaps.add(entry)
            } else {
                // Checkbox is unchecked, remove its state from the object
                this.favourite_heatmaps.delete(entry)
            }
        },
    },
    computed: {
        filt_heatmap() {
            var com = this;
            var filtered = [...com.heatmap_dict];

            if (!com.bookmark_off){
                filtered = filtered.filter(function(heatmap) {
                    return com.favourite_heatmaps.has(heatmap)
                });
            }

            return new Set(filtered);
        }
    }
}
</script>


<style>

#sigma-heatmap{
display: block;
position: absolute;
width: 50%;
height: 100%;
z-index: 2;
cursor: default;
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