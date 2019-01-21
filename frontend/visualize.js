
var network = null;
var current_data = null;

var colors = {
    protein: "rgb(82,182,229)",
    pathway: "rgb(242,181,0)",
    white: "rgb(255,255,255)",
    black: "rgb(0,0,0)",
    gray: "rgb(198,198,198)"
};

function generate_legend(legend){
    var container = $("#legend-container");

    var html = "<ul class=\"legend\">";

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

function visualize_visjs_data(data, reducing) {
    if (!network) return;

    network.setData(data);
    network.stabilize(50);

    if (!reducing)
        current_data = data;

    if (data.selected_nodes)
        network.selectNodes(data.selected_nodes);
}

function get_tooltip(text) {
    var div = document.createElement("div");
    div.style.width = "500px";
    div.innerHTML = text;
    div.style.wordWrap = "break-word";
    div.style.whiteSpace = "pre-wrap";
    return div;
}

function protein_subgraph_to_visjs_data(subgraph) {
    var nodes = new vis.DataSet();
    var edges = new vis.DataSet();
    var selected_nodes = [];
    if (subgraph.length >=1)
        selected_nodes.push(subgraph[0].protein.id);

    for (var i = 0; i < subgraph.length; i++) {
        var row = subgraph[i];
        var protein = row.protein;
        var other = row.other;
        var association = row.association;

        nodes.update({
            id: protein.id,
            label: protein.name,
            title: get_tooltip(protein.description),
            color: colors.protein
        });

        if (other) {
            nodes.update({
                id: other.id,
                label: other.name,
                title: get_tooltip(other.description),
                color: colors.protein
            });

            var edge_color = get_edge_color(association.combined);
            edges.update({
                from: protein.id,
                to: other.id,
                value: association.combined,
                title: (association.combined / 1000).toString(),
                color: {
                    color: edge_color, highlight: edge_color
                }
            });
        }

        for (var j = 0; j < row.pathways.length; j++) {
            var pathway = row.pathways[j];

            nodes.update({
                id: pathway.id,
                label: pathway.name,
                title: get_tooltip(pathway.description),
                color: colors.pathway,
                shape: "square"
            });

            edges.update([
                // {
                //     from: row.protein.id,
                //     to: pathway.id,
                //     color: colors.pathway
                // },
                {
                    from: row.other.id,
                    to: pathway.id,
                    color: colors.pathway
                }
            ]);
        }
    }

    return {
        nodes: nodes,
        edges: edges,
        selected_nodes: selected_nodes
    }
}

function protein_list_subgraph_to_visjs_data(subgraph) {
    var nodes = new vis.DataSet();
    var edges = new vis.DataSet();

    for (var i = 0; i < subgraph.length; i++) {
        var row = subgraph[i];
        var protein1 = row.protein1;
        var protein2 = row.protein2;
        var association = row.association;
        var pathways = row.pathways;

        nodes.update({
            id: protein1.id,
            label: protein1.name,
            title: get_tooltip(protein1.description),
            color: colors.protein
        });

        nodes.update({
            id: protein2.id,
            label: protein2.name,
            title: get_tooltip(protein2.description),
            color: colors.protein
        });

        if (association) {
            var edge_color = get_edge_color(association.combined);
            edges.update({
                from: protein1.id,
                to: protein2.id,
                value: association.combined,
                title: (association.combined / 1000).toString(),
                color: {
                    color: edge_color, highlight: edge_color
                }
            });
        }

        for (var j = 0; j < pathways.length; j++) {
            var pathway = pathways[j];

            nodes.update({
                id: pathway.id,
                label: pathway.name,
                title: get_tooltip(pathway.description),
                color: colors.pathway,
                shape: "square"
            });

            edges.update([
                {
                    from: protein1.id,
                    to: pathway.id,
                    color: colors.pathway
                },
                {
                    from: protein2.id,
                    to: pathway.id,
                    color: colors.pathway
                }
            ]);
        }
    }

    return {
        nodes: nodes,
        edges: edges
    }
}

function pathway_subgraph_to_visjs_data(subgraph) {
    var nodes = new vis.DataSet();
    var edges = new vis.DataSet();

    var pathway = subgraph.pathway;

    nodes.update({
        id: pathway.id,
        label: pathway.name,
        title: get_tooltip(pathway.description),
        color: colors.pathway,
        shape: "square"
    });

    for (var i = 0; i < subgraph.classes.length; i++) {
        var klass = subgraph.classes[i];

        nodes.update({
            id: klass.name,
            label: klass.name,
            color: colors.gray
        });

        edges.update({
            from: pathway.id,
            to: klass.name
        });
    }

    for (var i = 0; i < subgraph.proteins.length; i++) {
        var protein = subgraph.proteins[i];

        nodes.update({
            id: protein.id,
            label: protein.name,
            title: get_tooltip(protein.description),
            color: colors.protein
        });

        edges.update({
            from: protein.id,
            to: pathway.id
        });
    }

    return {
        nodes: nodes,
        edges: edges
    }
}

$(document).ready(function (){
    // generate legend
    generate_legend({
        "Protein": colors.protein,
        "Pathway": colors.pathway,
        "Class": colors.gray
    });

    // reduce graph button
    $("#reduce-graph-btn").click(() => {
        if (!network || !current_data) return;

        selected = network.getSelection();

        var nodes = current_data.nodes.get({
            filter: function (node) {
                return (selected.nodes.indexOf(node.id) >= 0);
            }
        });

        var edges = current_data.edges.get({
            filter: function (edge) {
                return (selected.edges.indexOf(edge.id) >= 0);
            }
        });

        visualize_visjs_data({
            nodes: nodes,
            edges: edges
        }, true);
    });

    // reset graph button
    $("#reset-graph-btn").click(() => {
        if (!network || !current_data) return;

        visualize_visjs_data(current_data, false);
    });

    // create a network
    var container = document.getElementById("visualization");

    var options = {
        physics: {
            enabled: false,
            barnesHut: {
                springConstant: 0.001,
                avoidOverlap: 0.2,
            }
        },
        interaction: {
            hideEdgesOnDrag: true,
            multiselect: true,
            navigationButtons: true
        },
        nodes: {
            shape: "dot"
        },
        edges: {
            color: {
                color: colors.gray
            },
            smooth: false,
            font: {
                size: 12
            },
            scaling: {
                min: 1,
                max: 3
            }
        },
        layout: {
            randomSeed: 42,
            improvedLayout: false
        }
    };
    
    network = new vis.Network(container, {
        nodes: new vis.DataSet([]),
        edges: new vis.DataSet([])
    }, options);

});
