
var colors = {
    protein: "rgb(82,182,229)",
    pathway: "rgb(242,181,0)",
    white: "rgb(255,255,255)",
    black: "rgb(0,0,0)",
    gray: "rgb(198,198,198)"
};

function json_to_visjs_data(data) {
    var nodes_protein = new vis.DataSet();
    var nodes_pathway = new vis.DataSet();
    var nodes_class = new vis.DataSet();
    var edges = new vis.DataSet();

    var nodes = data.nodes;
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        // Protein
        if (node.type == 0) {
            nodes_protein.update({
                id: node.id,
                label: node.label,
                x: node.x,
                y: node.y,
                title: get_tooltip(node.id, node.description),
                color: {
                    background: colors.protein,
                    border: colors.protein,
                    highlight: "#FFFF00"
                }
            });
        }
        // Pathway
        else if (node.type == 1) {
            nodes_pathway.update({
                id: node.id,
                label: node.label,
                x: node.x,
                y: node.y,
                title: get_tooltip(node.id, node.description),
                color: {
                    background: colors.pathway,
                    border: colors.pathway,
                    highlight: "#FFFF00"
                },
                shape: "square"
            });
        }
        // Class
        else if (node.type == 2) {
            // TODO
        }
    }

    var links = data.links;
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        edges.update([
            {
                from: link.source,
                to: link.target,
                color: colors.pathway
            }
        ]);
    }

    return {
        nodes_protein: nodes_protein,
        nodes_pathway: nodes_pathway,
        nodes_class: nodes_class,
        edges: edges
    }
}

function make_graph_layout(data) {
    // TODO
}

function remove_disconnected_nodes(nodes, allowed_nodes, edges) {
    var node_degree = {};
    var allowed_ids = allowed_nodes.map((node) => (node.id));
    var filtered_nodes = [];
    for (var i = 0; i < edges.length; i++) {
        var edge = edges[i];
        var from = edge.from;
        var to = edge.to;
        if (!allowed_ids.includes(from)) continue;
        node_degree[from] = node_degree[from] ? (node_degree[from] + 1) : 1;
        node_degree[to] = node_degree[to] ? (node_degree[to] + 1) : 1;
    }
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        if (node_degree[node.id] > 0) filtered_nodes.push(node);
    }
    return filtered_nodes;
}

function generate_legend(legend){
    var container = $("#legend");

    var html = "Score:<br/>";
    html += "0.0 <div id=\"grad\"></div> 1.0<br/>";

    html += "<ul class=\"legend-entry\">";

    for (var name in legend) {
        var color = legend[name];
        html += "<li><span style=\"background-color: " + color + ";\"></span> " + name + "</li>";
    }

    html += "</ul>";

    container.html(html);
}

function get_edge_color(score) {

    function color_to_string(color) {
        return "rgb(" + color.r + "," + color.g + "," + color.b + ")";
    }

    function weight_average_colors(c1, c2, w) {
        return {
            r: Math.floor((1 - w) * c1.r + w * c2.r),
            g: Math.floor((1 - w) * c1.g + w * c2.g),
            b: Math.floor((1 - w) * c1.b + w * c2.b)
        }
    }

    var high = {r: 255, g: 0, b: 0};
    var medium = {r: 0, g: 255, b: 0};
    var low = {r: 0, g: 0, b: 255};

    var color = null;

    if (score <=0) {
        color = color_to_string(low);
    }
    else if (score > 0 && score <= 500) {
        var w = score / 500;
        color = weight_average_colors(low, medium, w);
    }
    else if (score > 500 && score <= 1000) {
        var w = (score - 500) / 500;
        color = weight_average_colors(medium, high, w);
    }
    else {
        color = high;
    }

    return color_to_string(color);
}

function get_tooltip(id, text) {
    var div = document.createElement("div");
    div.style.width = "500px";

    var html = "<b>" + id + "</b>";
    html += "<br/><br/>";
    html += text;

    div.innerHTML = html;
    div.style.wordWrap = "break-word";
    div.style.whiteSpace = "pre-wrap";
    return div;
}

$(document).ready(function (){
    // generate legend
    generate_legend({
        "Protein": colors.protein,
        "Pathway": colors.pathway,
        "Class": colors.gray
    });

    // progress bar
    $("#progressbar").progressbar({
        value: 0
    });
});
