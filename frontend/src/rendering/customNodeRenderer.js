/**
 * The default node renderer. It renders the node as a simple disc.
 *
 * @param  {object}                   node     The node object.
 * @param  {CanvasRenderingContext2D} context  The canvas context.
 * @param  {configurable}             settings The settings function.
 */
export default function customNodeRenderer(node, context, settings) {
  var prefix = settings("prefix") || "";

  context.fillStyle = node.color || settings("defaultNodeColor");
  context.stroke();
  context.strokeStyle = "rgb(0, 0, 0)";
  context.beginPath();
  context.arc(
    node[prefix + "x"],
    node[prefix + "y"],
    node[prefix + "size"],
    0,
    Math.PI * 2,
    true
  );

  context.closePath();
  context.fill();
}

export function createCustomNodeSVG(node, settings) {
  /**
   * SVG Element creation.
   *
   * @param  {object}                   node     The node object.
   * @param  {configurable}             settings The settings function.
   */
  var circle = document.createElementNS(settings("xmlns"), "circle");

  // Defining the node's circle
  circle.setAttributeNS(null, "data-node-id", node.id);
  circle.setAttributeNS(null, "class", settings("classPrefix") + "-node");
  circle.setAttributeNS(
    null,
    "fill",
    node.color || settings("defaultNodeColor")
  );

  // Adding stroke properties
  circle.setAttributeNS(null, "stroke", "black"); // Set the stroke color
  circle.setAttributeNS(null, "stroke-width", "1"); // Set the stroke width

  // Returning the DOM Element
  return circle;
}
