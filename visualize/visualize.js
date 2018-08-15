
var w = 400,
    h = 400,
    fill = d3.scale.category20();

var vis = d3.select("#chart")
            .append("svg:svg")
            .attr("width", w)
            .attr("height", h);

d3.json("subgraph.json", function(json) {
    console.log(json);

    var force = d3.layout.force()
                         .charge(-120)
                         .linkDistance(30)
                         .nodes(json.nodes)
                         .links(json.links)
                         .size([w, h])
                         .start();

    var link = vis.selectAll("line.link")
                  .data(json.links)
                  .enter().append("svg:line")
                  .attr("class", "link")
                  .style("stroke-width", 10);

    var node = vis.selectAll("circle.node")
                  .data(json.nodes)
                  .enter().append("svg:circle")
                  .attr("class", "node")
                  .attr("r", 10)
                  // .style("fill", function(d) { return fill(d.group); })
                  .call(force.drag);

    node.append("svg:title")
        .text(function(d) { return d.preferred_name; });

    force.on("tick", function() {
        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
    });
});
