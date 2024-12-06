import Graph from "graphology";

// basic-reducer.ts
interface Node {
    id: string; 
  }

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
    hoveredNode?: String | null;
    hoveredNeighbors?: Set<String> | null;
  }
  
  export const nodeReducer = (node: String, data: Data, state: State): Data => {
    const res = { ...data };
  
    if (state.clickedNode) {
      res.highlighted = state.clickedNode === node;
      if (!res.highlighted && !state.clickedNeighbors.has(node)) {
        res.label = "";
        res.color = "rgb(100,100,100)";
      }
    } 
    if (!state.clickedNode && state.hoveredNeighbors && !state.hoveredNeighbors.has(node) && state.hoveredNode !== node) {
      res.label = "";
      res.color = "rgb(100,100,100)";
    }
  
    return res;
  };
  
  export const edgeReducer = (graph:Graph, edge: Edge, data: Data, state: State): Data => {
    const res = { ...data };

    const targetNode = state.hoveredNode || state.clickedNode;

    if (targetNode) {
        const isConnected = graph.extremities(edge).every(
            (n) => n === targetNode || graph.areNeighbors(n, targetNode)
        );

        if (state.hoveredNode && !state.clickedNode && !isConnected) {
        } else if (isConnected) {
            res.color = "rgba(20,20,20,0.1)";
        }if(!isConnected){
        }
    }

    return res;
  };
  