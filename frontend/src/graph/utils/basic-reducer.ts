// basic-reducer.ts
import Graph from "graphology";

interface Edge {
    id: string; 
  }
  
  interface Data {
    label?: string;
    color?: string;
    [key: string]: any;
  }
  
  interface State {
    clickedNode?: String | null;
    clickedNeighbors: Set<String>;
    clickedEnrichment?: Set<String> | null;
    clickedCluster?: Set<String> | null;
  }
  
  export const nodeReducer = (node: String, data: Data, state: State): Data => {
    const res = { ...data };
  
    if (state.clickedNode) {
      res.highlighted = state.clickedNode === node;
      if (!res.highlighted && !state.clickedNeighbors.has(node)) {
        res.label = "";
        res.color = "rgb(60,60,120)";
      }
    } 

    if (state.clickedEnrichment) {
      if (!state.clickedEnrichment.has(res.label)) {
        res.color = "rgb(60,60,120)";
      }else{
        res.color = "rgb(255,255,255)";
      }
    } 

    if (state.clickedCluster) {
      if (state.clickedCluster.has(node)) {
        res.color = "rgb(255,255,255)";
      }else{
        res.color = "rgb(60,60,120)";
      }
    } 
  
    return res;
  };
  
  export const edgeReducer = (graph:Graph, edge: Edge, data: Data, state: State): Data => {
    const res = { ...data };

    const targetNode = state.clickedNode;

    if (targetNode) {
        const isConnected = graph.extremities(edge).every(
            (n) => n === targetNode || graph.areNeighbors(n, targetNode)
        );

        if (!state.clickedNode && !isConnected) {
        } else if (isConnected) {
            res.color = "rgba(20,20,20,0.1)";
        }if(!isConnected){
        }
    }

    return res;
  };
  