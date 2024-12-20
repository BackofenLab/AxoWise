import { defineStore } from 'pinia';

export const useVisualizationStore = defineStore('visualization', {
  state: () => ({
    usedRenderer: undefined,
    clickedNode: undefined,
    clickedNeighbors: undefined,
    clickedEnrichment: undefined,
    clickedCluster: undefined,
  }),
  actions: {
    setClickedNode(node, graph) {
      if (node) {
        this.clickedNode = node;
        this.clickedNeighbors = new Set(graph.neighbors(node));
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
    setClickedCluster(cluster, graph) {
      this.clickedCluster = new Set()
      graph.forEachNode((node, atts) => {
        if (atts.community == cluster) this.clickedCluster.add(node)
      });
      this.usedRenderer.refresh({ skipIndexation: true });
    },
    setRenderer(renderer) {
      this.usedRenderer = renderer
    },
  },
});
