Vue.component("modules", {
    props: ["gephi_json"],
    data: function() {
        return {
            modules: {}
        }
    },
    methods: {
        select_module(subset) {
            var com = this;

            com.$emit("active-subset-changed", subset);
        }
    },
    watch: {
        "gephi_json": function() {
            var com = this;

            com.modules = {};

            var nodes = com.gephi_json.nodes;
            for (var idx in nodes) {
                var node = nodes[idx];
                if (!(node.color in com.modules)) com.modules[node.color] = [];
                com.modules[node.color].push(node);
            }
        }
    },
    template: `
        <div id="modules-parent">
            <div id="modules">
                <div v-for="(value, key, index) in modules">
                    <a href="#"><div class="rectangle" v-bind:style="{background: key}" v-on:click="select_module(value)"></div></a>
                </div>
            </div>
        </div>
    `
});