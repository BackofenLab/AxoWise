
var NETWORK = null;
var NETWORK_DATA_ALL = null;
var NETWORK_DATA_CURRENT = null;

var colors = {
    protein: "rgb(82,182,229)",
    pathway: "rgb(242,181,0)",
    white: "rgb(255,255,255)",
    black: "rgb(0,0,0)",
    gray: "rgb(198,198,198)"
};

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

function visualize_visjs_data(data) {
    if (!NETWORK) return;

    data = APP.filter_nodes(data);
    NETWORK_DATA_CURRENT = data;

    NETWORK.setData(data);

    // Vis.js
    APP.visualization.num_nodes = data.nodes.length;
    APP.visualization.num_edges = data.edges.length;

    NETWORK.stabilize(50);

    if (data.selected_nodes)
        NETWORK.selectNodes(data.selected_nodes);
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
            title: get_tooltip(protein.id, protein.description),
            color: colors.protein
        });

        if (other) {
            nodes.update({
                id: other.id,
                label: other.name,
                title: get_tooltip(other.id, other.description),
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
                title: get_tooltip(pathway.id, pathway.description),
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
            title: get_tooltip(protein1.id, protein1.description),
            color: colors.protein
        });

        nodes.update({
            id: protein2.id,
            label: protein2.name,
            title: get_tooltip(protein2.id, protein2.description),
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
                title: get_tooltip(pathway.id, pathway.description),
                color: colors.pathway,
                shape: "square"
            });

            edges.update(
                {
                    from: protein1.id,
                    to: pathway.id,
                    color: colors.pathway
                }
            );
            edges.update(
                {
                    from: protein2.id,
                    to: pathway.id,
                    color: colors.pathway
                }
            );
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

    for (var i = 0; i < subgraph.classes.length; i++) {
        var klass = subgraph.classes[i];

        nodes.update({
            id: klass.name,
            label: klass.name,
            color: colors.gray
        });
    }

    for (var i = 0; i < subgraph.associations.length; i++) {
        var association = subgraph.associations[i];
        var protein1 = association.protein1;
        var combined_score = association.combined_score;
        var protein2 = association.protein2;

        nodes.update({
            id: protein1.id,
            label: protein1.name,
            title: get_tooltip(protein1.id, protein1.description),
            color: colors.protein
        });

        nodes.update({
            id: protein2.id,
            label: protein2.name,
            title: get_tooltip(protein2.id, protein2.description),
            color: colors.protein
        });

        if (combined_score) {
            var edge_color = get_edge_color(combined_score);
            edges.update({
                from: protein1.id,
                to: protein2.id,
                value: combined_score,
                title: (combined_score / 1000).toString(),
                color: {
                    color: edge_color, highlight: edge_color
                }
            });
        }
    }

    return {
        nodes: nodes,
        edges: edges
    }
}

// rectangular select
function backup_surface() {
    var canvas = APP.rectangular_select.canvas;
    var context = APP.rectangular_select.context;
    APP.rectangular_select.surface_backup = context.getImageData(0, 0, canvas.width, canvas.height);
}

function restore_surface() {
    var context = APP.rectangular_select.context;
    var surface = APP.rectangular_select.surface_backup;
    context.putImageData(surface, 0, 0);
}

function select_nodes_rectangular() {
    if(!NETWORK_DATA_CURRENT) return;
    var rectangle = APP.rectangular_select.rectangle;

    var selected_nodes = [];
    var x_range = get_select_range(rectangle.startX, rectangle.w);
    var y_range = get_select_range(rectangle.startY, rectangle.h);

    var nodes = NETWORK_DATA_CURRENT.nodes.get();
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        var node_position = NETWORK.getPositions([node.id]);
        if (!node_position[node.id]) continue;

        var node_XY = NETWORK.canvasToDOM({x: node_position[node.id].x, y: node_position[node.id].y});
        if (x_range.start <= node_XY.x && node_XY.x <= x_range.end && y_range.start <= node_XY.y && node_XY.y <= y_range.end) {
            selected_nodes.push(node.id);
        }
    }
    NETWORK.selectNodes(selected_nodes);
}

function get_select_range(start, length) {
    return length > 0 ? {start: start, end: start + length} : {start: start + length, end: start};
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

    // reduce graph button
    $("#reduce-graph-btn").click(() => {
        if (!NETWORK || !NETWORK_DATA_CURRENT) return;

        var selected = NETWORK.getSelection();

        var nodes = NETWORK_DATA_CURRENT.nodes.get({
            filter: function (node) {
                return (selected.nodes.indexOf(node.id) >= 0);
            }
        });

        var edges = NETWORK_DATA_CURRENT.edges.get({
            filter: function (edge) {
                return (selected.edges.indexOf(edge.id) >= 0);
            }
        });

        visualize_visjs_data({
            nodes: new vis.DataSet(nodes),
            edges: new vis.DataSet(edges)
        }, true);
    });

    // reset graph button
    $("#undo-graph-btn").click(() => {
        if (!NETWORK || !NETWORK_DATA_ALL) return;

        visualize_visjs_data(NETWORK_DATA_ALL, false);
    });

    // filters
    $("input[type=\"checkbox\"]").checkboxradio({
        icon: false
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
    
    NETWORK = new vis.Network(container, {
        nodes: new vis.DataSet([]),
        edges: new vis.DataSet([])
    }, options);


    // rectangular select
    container.oncontextmenu = function() { return false; };
    APP.rectangular_select.canvas = NETWORK.canvas.frame.canvas;
    APP.rectangular_select.context = APP.rectangular_select.canvas.getContext("2d");

    $(container).on("mousemove", function(e) {
        if (APP.rectangular_select.active) {
            var context = APP.rectangular_select.context;
            var rectangle = APP.rectangular_select.rectangle;
            restore_surface();
            rectangle.w = (e.pageX - this.offsetLeft) - rectangle.startX;
            rectangle.h = (e.pageY - this.offsetTop) - rectangle.startY ;

            context.setLineDash([5]);
            context.strokeStyle = "rgb(82,182,229)";
            context.strokeRect(rectangle.startX, rectangle.startY, rectangle.w, rectangle.h);
            context.setLineDash([]);
            context.fillStyle = "rgba(82,182,229,0.2)";
            context.fillRect(rectangle.startX, rectangle.startY, rectangle.w, rectangle.h);
        }
    });

    $(container).on("mousedown", function(e) {
        if (e.button == 2) {
            selectedNodes = e.ctrlKey ? network.getSelectedNodes() : null;
            backup_surface();
            var that = this;
            var rectangle = APP.rectangular_select.rectangle;
            rectangle.startX = e.pageX - this.offsetLeft;
            rectangle.startY = e.pageY - this.offsetTop;
            APP.rectangular_select.active = true;
            $(container)[0].style.cursor = "crosshair";
        }
    });

    $(container).on("mouseup", function(e) {
        if (e.button == 2) {
            restore_surface();
            APP.rectangular_select.active = false;

            $(container)[0].style.cursor = "default";
            select_nodes_rectangular();
        }
    });
});
