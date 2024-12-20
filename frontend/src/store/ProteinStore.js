import { defineStore } from 'pinia';

export const useVisualizationStore = defineStore('visualization', {
  state: () => ({
    usedGraph: undefined,
    usedRenderer: undefined,
    clickedNode: undefined,
    clickedNeighbors: undefined,
    clickedEnrichment: undefined,
    clickedCluster: undefined,
  }),
  actions: {
    setClickedNode(node) {
      if (node) {
        this.clickedNode = node;
        this.clickedNeighbors = new Set(this.usedGraph.neighbors(node));
      } else {
        this.clickedNode = undefined;
        this.clickedNeighbors = undefined;
      }
      this.usedRenderer.refresh({ skipIndexation: true });
    },
    setClickedEnrichment(enrichment) {
      if (enrichment) {
        this.clickedEnrichment = new Set(enrichment);
      } else {
        this.clickedEnrichment = undefined;
      }
      this.usedRenderer.refresh({ skipIndexation: true });
    },
    setClickedCluster(cluster) {
      this.clickedCluster = new Set()
      this.usedGraph.forEachNode((node, atts) => {
        if (atts.community == cluster) this.clickedCluster.add(node)
      });
      this.usedRenderer.refresh({ skipIndexation: true });
    },
    setClickedSubset(subset) {
      this.clickedCluster = new Set()
      this.usedGraph.forEachNode((node) => {
        if (subset.has(node)) this.clickedCluster.add(node)
      });
      this.usedRenderer.refresh({ skipIndexation: true });
    },
    setRenderer(renderer) {
      this.usedRenderer = renderer
    },
    setGraph(graph) {
      this.usedGraph = graph
    },
  },
});
