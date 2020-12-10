
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
    props: ["gephi_json", "active_node", "active_term", "active_subset", "node_color_index", "edge_color_index", "dark_theme_root","edge_thick"],
    data: function() {
        return {
            rectangular_select: {
                canvas: null,
                context: null,
                rectangle: {},
                active: false,
                surface_backup: null
            },
            container: null,
            darkThemeOn: false,
            edge_opacity: 0.2
        }
    },
    watch: {
        "gephi_json": function(json) {
            var com = this;
            this.edge_opacity = json.edge_thick;
            sigma_instance.graph.clear();
            sigma_instance.graph.read(com.gephi_json);
            com.edit_opacity();
            sigma_instance.refresh();
        },
        "active_subset": function(subset, old_subset) {
            var com = this;

            if (subset == null) {
                com.reset();
                return;
            }

            if (old_subset != null) com.reset();

            var proteins = new Set(subset.map(node => node.attributes["Ensembl ID"]));

            sigma_instance.graph.nodes().forEach(function (n) {
                if (!proteins.has(n.attributes["Ensembl ID"])) n.hidden = true;
            });

            sigma_instance.refresh();
        },
        "active_term": function(term) {
            var com = this;

            if (term == null) {
                if (com.active_node == null) com.reset();
                return;
            }

            if (com.active_node != null) com.$emit("active-node-changed", null);

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
                if (source_present && !target_present || !source_present && target_present) e.color = "rgba(255, 125, 125, "+ this.edge_opacity +")"; // pink
                else if(source_present && target_present) e.color = "rgba(255, 0, 0, "+ this.edge_opacity +")"; // red
                else e.color = "rgba(255, 255, 255, "+ this.edge_opacity +")"; // white
            });

            sigma_instance.refresh();
        },
        "active_node": function(id) {
            var com = this;

            if (id == null) {
                if (com.active_term == null) com.reset();
                return;
            }

            if (com.active_term != null) com.$emit("active-term-changed", null);

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
        },
        "dark_theme_root": function (){
            if (this.dark_theme_root) {
                this.change_renderer('#FFF');}
            else{
                this.change_renderer('#000')
            }
        }
    },
    methods: {
        reset: function() {
            var com = this;

            sigma_instance.graph.edges().forEach(function(e) {
                var s = sigma_instance.graph.getNodeFromIndex(e.source);
                var t = sigma_instance.graph.getNodeFromIndex(e.target);
                s.color = com.node_color_index[e.source]; s.hidden = false;
                t.color = com.node_color_index[e.target]; t.hidden = false;
                e.color = com.edge_color_index[e.id]; e.hidden = false;
            });
            com.edit_opacity();
            sigma_instance.refresh();
        },
        // Rectangular select
        mousedown: function(e) {
            var com = this;
            if (e.button == 2) {
                // var selectedNodes = e.ctrlKey ? NETWORK.getSelectedNodes() : null;
                com.backup_surface();
                var that = this;
                var rectangle = com.rectangular_select.rectangle;
                rectangle.startX = e.pageX - com.container.offsetLeft;
                rectangle.startY = e.pageY - com.container.offsetTop;
                com.rectangular_select.active = true;
                com.container.style.cursor = "crosshair";
            }
        },
        mousemove: function(e) {
            var com = this;
            if (com.rectangular_select.active) {
                var context = com.rectangular_select.context;
                var rectangle = com.rectangular_select.rectangle;
                com.restore_surface();
                rectangle.w = (e.pageX - com.container.offsetLeft) - rectangle.startX;
                rectangle.h = (e.pageY - com.container.offsetTop) - rectangle.startY ;
                context.setLineDash([5]);
                context.strokeStyle = "rgb(82,182,229)";
                context.strokeRect(rectangle.startX, rectangle.startY, rectangle.w, rectangle.h);
                context.setLineDash([]);
                context.fillStyle = "rgba(82,182,229,"+ this.edge_opacity +")";
                context.fillRect(rectangle.startX, rectangle.startY, rectangle.w, rectangle.h);
            }
        },
        mouseup: function(e) {
            var com = this;
            if (e.button == 2) {
                com.restore_surface();
                com.rectangular_select.active = false;

                com.container.style.cursor = "default";
                com.select_nodes_rectangular();
            }
        },
        backup_surface: function() {
            var com = this;
            var canvas = com.rectangular_select.canvas;
            var context = com.rectangular_select.context;
            com.rectangular_select.surface_backup = context.getImageData(0, 0, canvas.width, canvas.height);
        },
        restore_surface: function() {
            var com = this;
            var context = com.rectangular_select.context;
            var surface = com.rectangular_select.surface_backup;
            context.putImageData(surface, 0, 0);
        },
        select_nodes_rectangular: function() {
            var com = this;
            var rectangle = com.rectangular_select.rectangle;

            var selected_nodes = [];
            var x_range = com.get_select_range(rectangle.startX, rectangle.w);
            var y_range = com.get_select_range(rectangle.startY, rectangle.h);

            var nodes = sigma_instance.graph.nodes();
            for (var i in nodes) {
                var node = nodes[i];
                if (node.hidden) continue;

                var node_XY = {
                    x: node["renderer1:x"],
                    y: node["renderer1:y"]
                };

                if (x_range.start <= node_XY.x && node_XY.x <= x_range.end && y_range.start <= node_XY.y && node_XY.y <= y_range.end) {
                    selected_nodes.push(node);
                }
            }
            if (selected_nodes.length > 0) com.$emit("active-subset-changed", selected_nodes);
        },
        get_select_range: function(start, length) {
            return length > 0 ? {start: start, end: start + length} : {start: start + length, end: start};
        },
        change_renderer:function(textcolor){
            for (i in sigma_instance.renderers){
                sigma_instance.renderers[i].clear();
                sigma_instance.killRenderer(i);
            }
            sigma_instance.addRenderer({
            container: "sigma-canvas",
            type: "canvas",
            camera: sigma_instance.addCamera(),
            settings: {
                defaultLabelColor: textcolor,
                hideEdgesOnMove: true,
                maxEdgeSize: 0.3,
                minEdgeSize: 0.3,
                minNodeSize: 1,
                maxNodeSize: 20,
                labelThreshold: 5
            }
        });
            sigma_instance.refresh();
        },
        edit_opacity: function() {
            var com = this;
             sigma_instance.graph.edges().forEach(function (e) {
                e.color = e.color.replace(/[\d\.]+\)$/g, com.edge_opacity+')');
            });
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
                maxNodeSize: 20,
                labelThreshold: 5
            }
        });

        sigma_instance.active = false;
        neighbors = {};
        sigma_instance.detail = false;

        sigma_instance.bind("clickNode", function (node) {
            com.$emit("active-node-changed", node.data.node.id);
        });

        // Rectangular select
        com.rectangular_select.canvas = $(".sigma-mouse")[0];
        com.container = $(".sigma-parent")[0];
        com.rectangular_select.canvas.oncontextmenu = function() { return false; };
        com.rectangular_select.canvas.onmousedown = com.mousedown;
        com.rectangular_select.canvas.onmousemove = com.mousemove;
        com.rectangular_select.canvas.onmouseup = com.mouseup;
        com.rectangular_select.context = com.rectangular_select.canvas.getContext("2d");

        this.eventHub.$on('edge-update', data => {
             this.edge_opacity = data;
             this.edit_opacity();
        });
    },
    template: `
    <div class="sigma-parent">
        <div class="sigma-expand"  v-bind:class="[dark_theme_root ? 'black-theme' : 'white-theme']" id="sigma-canvas"></div>
    </div>
    `
});