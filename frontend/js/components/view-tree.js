Vue.component("tree-node", {
    props: ["node"],
    methods: {
        select: function(node) {
            var com = this;
            com.$emit("data-node-changed", node);
        }
    },
    template:
        `
        <li data-jstree='{"icon": "glyphicon glyphicon-th", "opened": true}'>
            <span v-on:click="select(node);">{{ node.name }}</span>

            <ul v-if="node.children && node.children.length">
                <tree-node v-for="child in node.children"
                           v-bind:node="child"
                           v-on:data-node-changed="select($event)"
                >
                </tree-node>
            </ul>
        </li>
        `
});

Vue.component("view-tree", {
    props: ["data_trees"],
    mounted: function() {
        var tree = $("#view-tree");
        //tree.jstree();
    },
    methods: {
        select: function(node) {
            var com = this;
            com.$emit("data-node-changed", node);
        }
    },
    template:
        `
        <div id="view-tree" class="col-md-2">
        <ul>
            <tree-node v-for="tree in data_trees"
                       v-bind:node="tree"
                       v-on:data-node-changed="select($event)">
            </tree-node>
        </ul>
        </div>
        `
});