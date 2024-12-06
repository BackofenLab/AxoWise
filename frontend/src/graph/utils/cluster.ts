import Graph from "graphology";
import Sigma from "sigma";
import { Coordinates } from "sigma/types";
import smallestEnclosingCircle from "smallest-enclosing-circle";

interface Cluster {
  label: string;
  x?: number;
  y?: number;
  r?: number;
  color?: string;
  positions: { x: number; y: number }[];
  viewPositions: { x: number; y: number }[];
  nodes: string[];
}

/*
Generating underlying circles and labels for graph communities by calculation the smallest enclosing circle.
*/
export const generateCluster = (context: string, renderer: Sigma, graph: Graph) => {
  const container = document.getElementById(context) as HTMLElement;
  const clustersData: { label: string; x: number; y: number; r: number }[] = [];

  const nodeClusters: { [key: string]: Cluster } = {};
  graph.forEachNode((node, atts) => {
    if (!nodeClusters[atts.community]) nodeClusters[atts.community] = { label: atts.community, nodes: [], positions: [], viewPositions: [], color: atts.color};
    const cluster = { x: atts.x, y: atts.y }
    const viewportPos = renderer.graphToViewport(cluster as Coordinates);
    nodeClusters[atts.community].viewPositions.push({x: viewportPos.x, y: viewportPos.y});
    nodeClusters[atts.community].positions.push({x: atts.x, y: atts.y});
    nodeClusters[atts.community].nodes.push(node);
  });

  for (const community in nodeClusters) {
    const smallestEnclosingData = smallestEnclosingCircle(nodeClusters[community].positions);
    const smallestEnclosingDataView = smallestEnclosingCircle(nodeClusters[community].viewPositions);
    nodeClusters[community].x = smallestEnclosingData.x;
    nodeClusters[community].y = smallestEnclosingData.y;
    nodeClusters[community].r = smallestEnclosingDataView.r;
  }
  
  const svgLayer = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svgLayer.id = "clustersLayer";
  svgLayer.style.pointerEvents = "none"; 
  svgLayer.style.position = "absolute";
  svgLayer.style.width = "100%";
  svgLayer.style.height = "100%";
  svgLayer.style.top = "0";
  svgLayer.style.left = "0";

  for (const community in nodeClusters) {
    const cluster = nodeClusters[community];
    const viewportPos = renderer.graphToViewport(cluster as Coordinates);
    
    // Create SVG circle element
    const clusterCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    clusterCircle.setAttribute("id", `com-circle-${cluster.label}`);
    clusterCircle.setAttribute("cx", `${viewportPos.x}`);
    clusterCircle.setAttribute("cy", `${viewportPos.y}`);
    clusterCircle.setAttribute("r", `${cluster.r }`);
    clusterCircle.setAttribute("fill", cluster.color || "transparent");
    clusterCircle.setAttribute("opacity", "0.2");
    clusterCircle.setAttribute("stroke", "white");
    clusterCircle.setAttribute("stroke-width", "2");
    clusterCircle.style.display = "none";

    // Create SVG text element for labels
    const clusterLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    const fontSize = Math.max(2, cluster.r );
    clusterLabel.setAttribute("id", `com-${cluster.label}`);
    clusterLabel.setAttribute("x", `${viewportPos.x}`);
    clusterLabel.setAttribute("y", `${viewportPos.y}`);
    clusterLabel.setAttribute("fill", cluster.color || "#000");
    clusterLabel.setAttribute("text-anchor", "middle");
    clusterLabel.setAttribute("alignment-baseline", "middle");
    clusterLabel.setAttribute("opacity", "0.3");
    clusterLabel.style.display = "none";
    clusterLabel.textContent = cluster.label;
    clusterLabel.setAttribute("font-size", `${fontSize}px`);

    clustersData.push({ label: cluster.label, x: viewportPos.x, y: viewportPos.y, r: cluster.r });

    svgLayer.appendChild(clusterCircle);
    svgLayer.appendChild(clusterLabel);
  }

  container.insertBefore(svgLayer, container.getElementsByClassName("sigma-nodes")[0]);   

  //Updating circle and label position on camera ratio.
  renderer.on("afterRender", () => {
    const camera = renderer.getCamera();
    const scalingFactor = camera.getState().ratio;
    clustersData.length = 0;

    for (const community in nodeClusters) {
      const cluster = nodeClusters[community];
      const clusterLabel = document.getElementById(`com-${cluster.label}`) as unknown as SVGTextElement;
      const clusterCircle = document.getElementById(`com-circle-${cluster.label}`) as unknown as SVGCircleElement;
      const viewportPos = renderer.graphToViewport(cluster as Coordinates);
      const fontSize = Math.max(2, cluster.r / scalingFactor );

      clusterLabel.setAttribute("x", `${viewportPos.x}`);
      clusterLabel.setAttribute("y", `${viewportPos.y}`);
      clusterLabel.setAttribute("font-size", `${fontSize}`);
      clusterCircle.setAttribute("cx", `${viewportPos.x}`);
      clusterCircle.setAttribute("cy", `${viewportPos.y}`);
      clusterCircle.setAttribute("r", `${(cluster.r / scalingFactor)}`);

      clustersData.push({ label: cluster.label, x: viewportPos.x, y: viewportPos.y, r: cluster.r / scalingFactor });
    }
  });

  /*
  Attach mouse listener onto cluster layer to track if mouse position isin circle of respective cluster.
  */
  container.addEventListener("mousemove", (event: MouseEvent) => {
    
    const mouseX = event.offsetX;
    const mouseY = event.offsetY;
    

    for (const cluster of clustersData) {
      const dx = mouseX - cluster.x;
      const dy = mouseY - cluster.y;
      const distance = Math.sqrt(dx*dx + dy*dy);
      const clusterCircle = document.getElementById(`com-circle-${cluster.label}`) as unknown as SVGCircleElement;
      const clusterLabel = document.getElementById(`com-${cluster.label}`) as unknown as SVGCircleElement;

      if (distance <= (cluster.r)) {
        clusterCircle.style.display = "block";
        clusterLabel.style.display = "block";
      }else{
        clusterCircle.style.display = "none";
        clusterLabel.style.display = "none";
      }
    }
  });
};
