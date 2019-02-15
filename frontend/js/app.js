var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            wait: true,
            title: "",
            current_data_node: {},
            data_trees: [
                // name, data, children
            ],
            show: {
                proteins: true,
                pathways: false,
                classes: false
            },
            species: {
                ncbi_id: null,
                kegg_id: null,
                name: null
            },
            protein: {
                id: null,
                name: null
            },
            pathway: {
                id: null,
                name: null  
            },
            protein_list: null,
            threshold: 0.75
        },
        methods: {
            add_data_tree: function(data_tree) {
                var com = this;
                com.data_trees.push(data_tree);
                com.current_data_node = data_tree;
            },
            create_child: function(child) {
                var com = this;
                com.current_data_node.children.push(child);
                com.current_data_node = child;
            }
        }
    });
});
