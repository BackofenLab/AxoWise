Vue.component("tree-node", {
    props: ["node"],
    template:
        `
        <li data-jstree='{"icon": "glyphicon glyphicon-leaf", "opened": true}'>
            <span>{{ node.name }}</span>

            <ul v-if="node.children && node.children.length">
                <tree-node v-for="child in node.children"
                           v-bind:node="child"
                >
                </tree-node>
            </ul>
        </li>
        `
});

Vue.component("view-tree", {
    data: function () {
        return {
            trees: [
                {
                    name: "Chemokine signaling pathway",
                    children: [
                        {
                            name: "Chemokine signaling pathway #2"
                        }
                    ]
                },
                {
                    name: "CCR5",
                    children: [
                        {
                            name: "CCR5 #2"
                        }
                    ]
                }
            ]
        }
    },
    mounted: function() {
        var tree = $("#view-tree");
        tree.jstree();
    },
    template:
        `
        <div id="view-tree" class="col-md-2">
        <ul>
            <tree-node v-for="tree in trees" v-bind:node="tree"></tree-node>
        </ul>
        </div>
        `
});