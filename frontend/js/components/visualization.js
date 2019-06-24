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

Vue.component("visualization", {
    props: ["gephi_json", "active_node", "active_term"],
    data: function() {
        return {}
    },
    watch: {
        "gephi_json": function(json) {
            sigma_instance.graph.clear();
            sigma_instance.graph.read(json);
            sigma_instance.refresh();
        },
        "active_term": function(term) {
            if (term == null) return;

            var proteins = term.proteins;

            sigma_instance.graph.nodes().forEach(function (n) {
                var ensembl_id = n.attributes["Ensembl ID"];
                if (proteins.indexOf(ensembl_id) >= 0) {
                    n.color = "rgb(255, 0, 0)"; // red
                }
                else {
                    n.color = "rgb(255, 255, 255)"; // white
                }
            });

            sigma_instance.graph.edges().forEach(function (e) {
                var source_ensembl_id = sigma_instance.graph.getNodeFromIndex(e.source).attributes["Ensembl ID"];
                var target_ensembl_id = sigma_instance.graph.getNodeFromIndex(e.target).attributes["Ensembl ID"];

                var source_present = proteins.indexOf(source_ensembl_id) >= 0;
                var target_present = proteins.indexOf(target_ensembl_id) >= 0;
                if (source_present && !target_present || !source_present && target_present) {
                    e.color = "rgba(255, 125, 125, 0.2)"; // pink
                }
                else if(source_present && target_present) {
                    e.color = "rgba(255, 0, 0, 0.2)"; // red
                }
                else {
                    e.color = "rgba(255, 255, 255, 0.2)"; // white
                }
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
        // Rectangular select callbacks
        mousedown: function(e) {
            var com = this;
            if (e.button == 2) {
                var selectedNodes = e.ctrlKey ? NETWORK.getSelectedNodes() : null;
                com.backup_surface();
                var that = this;
                var rectangle = com.rectangular_select.rectangle;
                rectangle.startX = e.pageX - $(com.container)[0].offsetLeft;
                rectangle.startY = e.pageY - $(com.container)[0].offsetTop;
                com.rectangular_select.active = true;
                $(com.container)[0].style.cursor = "crosshair";
            }
        },
        mousemove: function(e) {
            var com = this;
            if (com.rectangular_select.active) {
                var context = com.rectangular_select.context;
                var rectangle = com.rectangular_select.rectangle;
                com.restore_surface();
                rectangle.w = (e.pageX - $(com.container)[0].offsetLeft) - rectangle.startX;
                rectangle.h = (e.pageY - $(com.container)[0].offsetTop) - rectangle.startY ;
                context.setLineDash([5]);
                context.strokeStyle = "rgb(82,182,229)";
                context.strokeRect(rectangle.startX, rectangle.startY, rectangle.w, rectangle.h);
                context.setLineDash([]);
                context.fillStyle = "rgba(82,182,229,0.2)";
                context.fillRect(rectangle.startX, rectangle.startY, rectangle.w, rectangle.h);
            }
        },
        mouseup: function(e) {
            var com = this;
            if (e.button == 2) {
                com.restore_surface();
                com.rectangular_select.active = false;

                $(com.container)[0].style.cursor = "default";
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
            if(!com.current_data_node.data) return;
            var rectangle = com.rectangular_select.rectangle;

            var selected_nodes = [];
            var x_range = com.get_select_range(rectangle.startX, rectangle.w);
            var y_range = com.get_select_range(rectangle.startY, rectangle.h);

            var nodes = com.current_data_node.data.nodes_protein.get();
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
        },
        get_select_range: function(start, length) {
            return length > 0 ? {start: start, end: start + length} : {start: start + length, end: start};
        },

        normal_node: function() {
            var com = this;

            sigma_instance.graph.edges().forEach(function (a) {
                a.hidden = false;
            });

            sigma_instance.graph.nodes().forEach(function (a) {
                a.hidden = false;
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
                maxNodeSize: 10
            }
        });

        sigma_instance.active = false;
        neighbors = {};
        sigma_instance.detail = false;

        sigma_instance.bind("clickNode", function (node) {
            com.$emit("active-node-changed", node.data.node.id);
        });
        // com.search = new Search(com.form.find("#search"));

        // rectangular select
        // container.oncontextmenu = function() { return false; };
        // com.rectangular_select.canvas = NETWORK.canvas.frame.canvas;
        // com.rectangular_select.context = com.rectangular_select.canvas.getContext("2d");
    },
    template: `
    <div class="sigma-parent">
        <div class="sigma-expand" id="sigma-canvas"></div>
    </div>
    `
});