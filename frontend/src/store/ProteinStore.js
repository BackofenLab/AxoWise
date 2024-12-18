import { defineStore } from 'pinia';

export const useVisualizationStore = defineStore('visualization', {
  state: () => ({
    hoveredNode: undefined,
    hoveredNeighbors: undefined,
    clickedNode: undefined,
    clickedNeighbors: undefined,
    clickedEnrichment: undefined,
  }),
  actions: {
    setHoveredNode(node, graph) {
      if (node) {
        this.hoveredNode = node;
        this.hoveredNeighbors = new Set(graph.neighbors(node));
      } else {
        this.hoveredNode = undefined;
        this.hoveredNeighbors = undefined;
      }
    },
    setClickedNode(node, graph) {
      if (node) {
        this.clickedNode = node;
        this.clickedNeighbors = new Set(graph.neighbors(node));
      } else {
        this.clickedNode = undefined;
        this.clickedNeighbors = undefined;
      }
    },
    setClickedEnrichment(enrichment) {
      if (enrichment) {
        this.clickedEnrichment = new Set(enrichment);
      } else {
        this.clickedEnrichment = undefined;
      }
    },
  },
});
