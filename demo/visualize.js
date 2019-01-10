
var network = null;

var colors = {
    protein: "#52b6e5", queried_protein: "#00a5f2",
    pathway: "#f2b500",
    white: "#ffffff",
    black: "#000000"
};

function visualize_visjs_data(data) {
    if (network) {
        network.setData(data);
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

    for (var i = 0; i < subgraph.length; i++) {
        var row = subgraph[i];

        nodes.update({
            id: row.protein.id,
            label: row.protein.name,
            title: get_tooltip(row.protein.description),
            color: colors.queried_protein
        });

        nodes.update({
            id: row.other.id,
            label: row.other.name,
            title: get_tooltip(row.other.description),
            color: colors.protein
        });

        edges.update({
            from: row.protein.id,
            to: row.other.id,
            label: (row.association.combined / 1000).toString(),
            color: colors.protein
        })

        for (var j = 0; j < row.pathways.length; j++) {
            var pathway = row.pathways[j];

            nodes.update({
                id: pathway.id,
                label: pathway.name,
                title: get_tooltip(pathway.description),
                color: colors.pathway,
                level: 3
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
        edges: edges
    }
}

function pathway_subgraph_to_visjs_data(subgraph) {
    var nodes = new vis.DataSet();
    var edges = new vis.DataSet();

    for (var i = 0; i < subgraph.length; i++) {
        var row = subgraph[i];


    }
}

$(document).ready(function (){
    // create a network
    var container = document.getElementById("visualization");

    var options = {
        physics: false,
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
        }
    };
    
    network = new vis.Network(container, {
        nodes: new vis.DataSet([]),
        edges: new vis.DataSet([])
    }, options);

});
