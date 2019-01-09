
// // create an array with nodes
// var nodes = new vis.DataSet([
// {id: 1, label: 'Node 1'},
// {id: 2, label: 'Node 2'},
// {id: 3, label: 'Node 3'},
// {id: 4, label: 'Node 4'},
// {id: 5, label: 'Node 5'}
// ]);

// // create an array with edges
// var edges = new vis.DataSet([
// {from: 1, to: 3},
// {from: 1, to: 2},
// {from: 2, to: 4},
// {from: 2, to: 5},
// {from: 3, to: 3}
// ]);

var network = null;

function visualize_visjs_data(data) {
    if (network) {
        network.setData(data);
    }
}

function protein_subgraph_to_visjs_data(subgraph) {
    var nodes = new vis.DataSet();
    var edges = new vis.DataSet();

    for (var i = 0; i < subgraph.length; i++) {
        row = subgraph[i];

        nodes.update({
            id: row.protein.id,
            label: row.protein.name
        })

        nodes.update({
            id: row.other.id,
            label: row.other.name
        })

        edges.update({
            from: row.protein.id,
            to: row.other.id
        })
    }

    return {
        nodes: nodes,
        edges: edges
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
            smooth: false
        },
    };
    
    network = new vis.Network(container, {
        nodes: new vis.DataSet([]),
        edges: new vis.DataSet([])
    }, options);

});
