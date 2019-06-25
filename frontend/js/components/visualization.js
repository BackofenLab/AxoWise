
// Sigma.js

// THIS INSTANCE OF SIGMA IS GLOBAL
var sigma_instance = null;

sigma.classes.graph.addMethod('getNodeFromIndex', function(id) {
    return this.nodesIndex[id];
});

sigma.classes.graph.addMethod('ensemblIdToNode', function(ensembl_id) {
    var nodes = this.nodes();
    for (var idx in nodes) {
        var node = nodes[idx];
        if (node.attributes["Ensembl ID"] === ensembl_id)
            return node;
    }
    return null;
});

// Component
Vue.component("visualization", {
    props: ["gephi_json", "active_node", "active_term"],
    data: function() {
        return {}
    },
    watch: {
        "gephi_json": function(json) {
            var com = this;
            com.reload();
        },
        "active_term": function(term) {
            var com = this;

            if (term == null) {
                com.reload();
                return;
            }

            var proteins = new Set(term.proteins);

            sigma_instance.graph.edges().forEach(function (e) {
                // Nodes
                var source = sigma_instance.graph.getNodeFromIndex(e.source);
                var target = sigma_instance.graph.getNodeFromIndex(e.target);

                // Ensembl IDs
                var source_ensembl_id = source.attributes["Ensembl ID"];
                var target_ensembl_id = target.attributes["Ensembl ID"];

                // Are they present in the functional term?
                var source_present = proteins.has(source_ensembl_id);
                var target_present = proteins.has(target_ensembl_id);

                // Source
                if (source_present) source.color = "rgb(255, 0, 0)"; // red
                else source.color = "rgb(255, 255, 255)"; // white

                // Target
                if (target_present) target.color = "rgb(255, 0, 0)"; // red
                else target.color = "rgb(255, 255, 255)"; // white

                // Edge
                if (source_present && !target_present || !source_present && target_present) e.color = "rgba(255, 125, 125, 0.2)"; // pink
                else if(source_present && target_present) e.color = "rgba(255, 0, 0, 0.2)"; // red
                else e.color = "rgba(255, 255, 255, 0.2)"; // white
            });

            sigma_instance.refresh();
        },
        "active_node": function(id) {
            var com = this;

            if (id == null) {
                com.normal_node();
                return;
            }

            var neighbors = {};
            var node = sigma_instance.graph.getNodeFromIndex(id);

            sigma_instance.graph.edges().forEach(function (e) {
                n = {
                    name: e.label,
                    color: e.color
                };

                if (id == e.source || id == e.target)
                    neighbors[id == e.target ? e.source : e.target] = n;

                e.hidden = false;
            });

            var f = [];

            // Hide all nodes first
            sigma_instance.graph.nodes().forEach(function (n) {
                n.hidden = true;
            });

            // Show only the node and its neighbors
            node.hidden = false;
            for (var id in neighbors) {
                var neighbor = sigma_instance.graph.getNodeFromIndex(id);
                neighbor.hidden = false;
            }

            sigma_instance.refresh();
        }
    },
    methods: {
        normal_node: function() {
            var com = this;

            com.reload();

            sigma_instance.refresh();
        },

        reload: function() {
            // TODO This is expensive to call every time the colors need to be reset
            var com = this;
            sigma_instance.graph.clear();
            sigma_instance.graph.read(com.gephi_json);
            sigma_instance.refresh();
        }
    },
    mounted: function() {
        var com = this;

        sigma_instance= new sigma();
        var camera = sigma_instance.addCamera();

        sigma_instance.addRenderer({
            container: "sigma-canvas",
            type: "canvas",
            camera: camera,
            settings: {
                defaultLabelColor: "#FFF",
                hideEdgesOnMove: true,
                maxEdgeSize: 0.3,
                minEdgeSize: 0.3,
                minNodeSize: 1,
                maxNodeSize: 10
            }
        });

        sigma_instance.active = false;
        neighbors = {};
        sigma_instance.detail = false;

        sigma_instance.bind("clickNode", function (node) {
            com.$emit("active-node-changed", node.data.node.id);
        });
    },
    template: `
    <div class="sigma-parent">
        <div class="sigma-expand" id="sigma-canvas"></div>
    </div>
    `
});