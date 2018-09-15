var tooltip = d3.select("body")
                     .append("div")
                     .attr("class", "node-tooltip")
                     .style("width", "500px")
                     .style("word-wrap", "break-word")
                     .style("display", "none")
                     .style("position", "absolute")
                     .style("background-color", "#999")
                     .style("color", "#FFFFFF");

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-1000))
    .force("center", d3.forceCenter(width / 2, height / 2));

d3.json("subgraph.json", function(error, graph) {
  if (error) throw error;

  // Edges
  var link = svg.append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(graph.links)
                .enter().append("line")
                .style("transform", "translate(50%, 50%)")
                .attr("stroke-width", 10)
                .attr("stroke", function(d){
                    if ("combined" in d) return "#89c6ff";
                    return "#999";
                });

  link.on("mouseover", function(d) {
    if (!("combined" in d)) return;

    d3.select(this)
      .style("cursor", "pointer")
  });

  link.on("click", function(d){
    tooltip.style("opacity", "1")
            .style("display", "inline")

    channels = [
      "combined",
      "coexpression",
      "experiments",
        "database",
        "textmining",
        "neighborhood",
        "fusion",
        "cooccurence"
    ]

    html = "";
    for (var i = 0; i < channels.length; i++){
      channel = channels[i];
      if (channel in d) html += ("<b>" + channel + "</b>: " + d[channel] / 1000 + "<br/>");
    }

    tooltip.html(html)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY) + "px")
  });

  // link.on("mouseout", function(d){
  //   tooltip.style("display", "none")
  // });

  // Nodes
  var node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(graph.nodes)
                .enter().append("circle")
                .attr("r", 30)
                .attr("fill", function(d) {
                  if (d.type == "protein") return "#89c6ff";
                  else if (d.type == "action") return "#ff8989";
                  else if (d.type == "compound") return "#d1b5ff";
                  else if (d.type == "pathway") return "#ffffb5";
                  else if (d.type == "drug") return "#ccc4a7";
                  else if (d.type == "disease") return "#fdff89";
                  else return "#99ff99";
                 })
                .style("transform", "translate(50%, 50%)")
                .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

  node.on("mouseover", function(d){
    d3.select(this)
      .style("cursor", "pointer")
  });

  node.on("click", function(d){
    tooltip.style("opacity", "1")
                .style("display", "inline")

    html = "";

    if (d.type == "protein") {
      html = "<b>" + d.external_id + "</b><br/>";
      html += d.annotation;
    }
    else if (d.type == "action") {
      html = "score: " + d.score / 1000;
    }
    else if (d.type == "pathway") {
      html = "<b>" + d.id + "</b><br/>";
      html += d.description + "<br/>";
    }

    tooltip.html(html)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY) + "px")
  });

  // node.on("mouseout", function(d){
  //   tooltip.style("display", "none")
  // });

  // Node labels
  var lables = svg.append("g")
                   .attr("class", "labels")
                   .selectAll("circle")
                   .data(graph.nodes)
                   .enter().append("text")
                   .text(function(d) {
                      if (d.type == "protein") return d.preferred_name;
                      else if (d.type == "action") return d.mode;
                      else if (d.type == "pathway" ||
                              d.type == "disease" ||
                              d.type == "compound" ||
                              d.type == "drug") return d.name;
                      return "null";
                    })
                   .style("transform", "translate(50%, 50%)")
                   .style("text-anchor", "middle");

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
            .links(graph.links);

  function ticked() {
      link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

      node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

      lables
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; });
    }
});

function dragstarted(d) {
  if (!d3.event.active)
    simulation.alphaTarget(0.3).restart();

  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active)
    simulation.alphaTarget(0);

  d.fx = null;
  d.fy = null;
}