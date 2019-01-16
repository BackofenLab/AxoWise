
var network = null;

var colors = {
    protein: "#52b6e5",
    pathway: "#f2b500",
    white: "#ffffff",
    black: "#000000",
    gray: "#c6c6c6"
};

function generate_legend(legend){
    var html = "<div><ul class=\"legend\">";

    for (var name in legend) {
        var color = legend[name];
        html += "<li><span style=\"background-color: " + color + ";\"></span> " + name + "</li>";
    }

    html += "</ul></div>";

    var visualization = $("#visualization");
    $(html).insertBefore(visualization);
}

function visualize_visjs_data(data) {
    if (network) {
        network.setData(data);
        network.stabilize(50);
        if (data.selected_nodes)
            network.selectNodes(data.selected_nodes);
    }
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

            edges.update({
                from: protein.id,
                to: other.id,
                label: (association.combined / 1000).toString(),
                color: colors.protein
            })
        }

        for (var j = 0; j < row.pathways.length; j++) {
            var pathway = row.pathways[j];

            nodes.update({
                id: pathway.id,
                label: pathway.name,
                title: get_tooltip(pathway.description),
                color: colors.pathway
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

        if (association)
            edges.update({
                from: protein1.id,
                to: protein2.id,
                label: (association.combined / 1000).toString(),
                color: colors.protein
            })

        for (var j = 0; j < pathways.length; j++) {
            var pathway = pathways[j];

            nodes.update({
                id: pathway.id,
                label: pathway.name,
                title: get_tooltip(pathway.description),
                color: colors.pathway
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
        color: colors.pathway
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

    // threshold slider
    $("#threshold-slider").slider({
        min: 0,
        max: 1,
        step: 0.01,
        value: 0.75,
        slide: function (event, ui) {
            $("#threshold-value").text(ui.value);
        },
        create: function () {
            $("#threshold-value").text($("#threshold-slider").slider("value"));
        }
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
            hideEdgesOnDrag: true
        },
        nodes: {
            shape: "dot"
        },
        edges: {
            color: {inherit: true},
            smooth: false,
            font: {
                size: 12
            },
        },
        layout: {
            improvedLayout: true
        }
    };
    
    network = new vis.Network(container, {
        nodes: new vis.DataSet([]),
        edges: new vis.DataSet([])
    }, options);

});
