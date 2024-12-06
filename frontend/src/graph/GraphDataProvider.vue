<template>
    <div>
        <slot :graph="graph"></slot>
    </div>
</template>

<script>
    import { ref } from "vue";
    import { Graph } from "graphology";
    import louvain from 'graphology-communities-louvain';
    import {circlepack} from 'graphology-layout';
    import {largestConnectedComponent} from 'graphology-components';
    import betweennessCentrality from 'graphology-metrics/centrality/betweenness';
    import pagerank from 'graphology-metrics/centrality/pagerank';
    import chroma from "chroma-js";

    export default {
    name: "GraphDataProvider",
    props:["backend_data"],
    data(){
        return{
            graph: null
        }
    },

    methods: {

        initializeGraph(graph, data) {
        /* Creates graphology.js graph of given data and assign respective attributes.(size, color, pagerank, bc, community)
           Applying Mike Bostocks circle pack layout to graph data and louvain community detection.
           Input: data dict{ nodes: List[], edges: List[]}
           Return: initializeGraph: function(), graph: graphObject
        */

            const nodes = data.nodes;
            const edges = data.edges;

            for (const node of nodes) {
                graph.addNode(node.ENSEMBL_PROTEIN, { label: node.SYMBOL, borderColor: "rgb(50,50,50)",});
            }

            for (const edge of edges) {
                graph.addEdgeWithKey(
                    `${edge.source}+${edge.target}`,
                    edge.source,
                    edge.target,
                    {
                    color: "rgba(10,10,10,0.2)",
                    opacity: 0.1,
                    size: 0.1,
                    }
                );
            }
            this.generateGraphLayout(graph);
            this.generateGraphStatistics(graph);
            this.generateGraphColor(graph);
            // this.generateSubgraph(graph);

            graph.forEachNode((node) => {
                const size = graph.degree(node);
                graph.setNodeAttribute(node, "size", 2 + (300 * size/graph.size));
            });
            
        },

        generateGraphLayout(graph){
        /* Generates x,y positions for graph nodes by Mike Bostock circle pack algorithm based on degree and community.
           Aswell as generation of graph modularity by louvain method.
           Input: graph: graphObject
        */

            louvain.assign(graph);
            circlepack.assign(graph, { hierarchyAttributes: ['degree', 'community'] });
        },

        generateGraphStatistics(graph){
        /* Generates graph statistics for graph nodes.
           Input: graph: graphObject
        */

            betweennessCentrality.assign(graph);
            pagerank.assign(graph);
        },

        generateSubgraph(graph){
        /* Filters the highest connected component and hides all unconnected nodes.
           Input: graph: graphObject
        */
            const largest = new Set(largestConnectedComponent(graph));

            graph.forEachNode((node) => {
                !largest.has(node) 
                    ? graph.setNodeAttribute(node, 'hidden', true)
                    : graph.removeNodeAttribute(node, 'hidden');
            });
        },

        generateGraphColor(graph){
        /* Creates colorpalette with chroma.js and assign each node their respective color (community).
           Input: graph: graphObject
        */

            const communities = new Set();

            graph.forEachNode((node, attr) => {
                communities.add(attr.community)
            });

            const colorScale = chroma.scale('Set1').mode('lch').colors(communities.size);

            const communityColors = Object.fromEntries(
              [...communities].map((id, idx) => [id, colorScale[idx]])
            );

            graph.forEachNode((node, attr) => {
              const community = attr.community
              graph.setNodeAttribute(node, 'color', communityColors[community]);
            });
        },

        saveGraph(graph){
        /* Export graph as serialized JSON object into localStorage.
        */
            const serializedGraph = JSON.stringify(graph.export());
            localStorage.setItem("graph", serializedGraph);
        },

        loadGraph(graph){
        /* Import graph as serialized JSON object from localStorage.
        */
            const savedGraph = localStorage.getItem("graph");
            if (savedGraph) {
                const importedData = JSON.parse(savedGraph);
                graph.import(importedData);
            } 
        },
    },
    mounted(){
        this.graph = ref(new Graph());
        this.initializeGraph(this.graph, this.backend_data)
    },
    };
</script>