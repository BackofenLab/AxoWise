var NETWORK = null;

Vue.component("visualization", {
    props: ["current_data_node", "show", "title", "threshold"],
    data: function() {
        return {
            container: null,
            stats: {
                nodes: 0,
                edges: 0,
            },
            network_options: {
                physics: {
                    enabled: false,
                    barnesHut: {
                        springConstant: 0.001,
                        avoidOverlap: 0.2,
                    },
                    stabilization: false
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
            },
            rectangular_select: {
                canvas: null,
                context: null,
                rectangle: {},
                active: false,
                surface_backup: null
            },
            filtered_data: {
                nodes: new vis.DataSet(),
                edges: new vis.DataSet(),
            },
            scale: 1,
            view_position: {
                x: 0, y:0
            }
        }
    },
    watch: {
        "current_data_node": function() {
            var com = this;
            var data = com.current_data_node.data;
            if (!NETWORK || !data) return;

            if (!data.nodes || data.nodes.get().length <= 0)
               return;

            var has_x = "x" in data.nodes.get()[0];
            var has_y = "y" in data.nodes.get()[0];
            if (has_x && has_y) {
                com.filtered_data = data;
                return;
            }

            NETWORK.setData(data);
            NETWORK.stabilize(50);
        },
        "threshold": _.debounce(function() {
            var com = this;
            com.filtered_data = com.filter_data(com.current_data_node.data);
        }, 100),
        "show.proteins": function() {
            var com = this;
            com.filtered_data = com.filter_data(com.current_data_node.data);
        },
        "show.pathways": function() {
            var com = this;
            com.filtered_data = com.filter_data(com.current_data_node.data);
        },
        "show.classes": function() {
            var com = this;
            com.filtered_data = com.filter_data(com.current_data_node.data);
        },
        "filtered_data": function() {
            var com = this;
            NETWORK.setData(com.filtered_data);
            NETWORK.moveTo({
                position: com.view_position,
                scale: com.scale
            });

            com.stats.nodes = com.filtered_data.nodes.length;
            com.stats.edges = com.filtered_data.edges.length;
        },
    },
    methods: {
        filter_data: function(data) {
            var com = this;
            if (!data) return;

            var filtered_nodes = data.nodes.get({
                filter: function(node) {
                    if (node.color.background == colors.protein) return com.show.proteins;
                    else if (node.color.background == colors.pathway) return com.show.pathways;
                    else if (node.color.background == colors.gray) return com.show.classes;
                    return true;
                }
            });

            var filtered_edges = data.edges.get({
                filter: function(edge) {
                    return edge.value / 1000 >= com.threshold;
                }
            });

            return {
                nodes: filtered_nodes,
                edges: filtered_edges
            }
        },
        // Vis.js event handlers
        stabilization_progress: function(e) { // For some reason the event 'stabilized' is not triggered
            var com = this;

            if (e.iterations < e.total)
                return;

            NETWORK.storePositions();
            com.filtered_data = com.filter_data(com.current_data_node.data);
        },
        drag_end: function(e) {
            var com = this;
            com.view_position = NETWORK.getViewPosition();
            NETWORK.storePositions();

            // If node(s) was/were dragged, its/their position(s) has to be remembered
            var dragged_nodes = e.nodes;
            if (dragged_nodes.length <= 0) return;

            var dragged_positions = NETWORK.getPositions(dragged_nodes);
            com.data.nodes.forEach(function (node) {
                if (node.id in dragged_positions) {
                    node.x = dragged_positions[node.id].x;
                    node.y = dragged_positions[node.id].y;
                    com.data.nodes.update(node);
                }
            });
        },
        release: function(e) {
            NETWORK.storePositions();
        },
        zoom: _.debounce(function(e) {
            var com = this;
            com.scale = e.scale;
        }, 100),
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

            var nodes = com.current_data_node.data.nodes.get();
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
        }
    },
    mounted: function() {
        var com = this;
        var container = document.getElementById("visualization");
        com.container = container;

        // create a network
        NETWORK = new vis.Network(container, com.filtered_data, com.network_options);
        NETWORK.on("stabilizationProgress", com.stabilization_progress);
        NETWORK.on("zoom", com.zoom);
        NETWORK.on("dragEnd", com.drag_end);
        NETWORK.on("release", com.release);

        // rectangular select
        container.oncontextmenu = function() { return false; };
        com.rectangular_select.canvas = NETWORK.canvas.frame.canvas;
        com.rectangular_select.context = com.rectangular_select.canvas.getContext("2d");
    },
    template: `
        <div>
        <div id="visualization"
             class="col-md-10"
             v-on:mousedown="mousedown"
             v-on:mousemove="mousemove"
             v-on:mouseup="mouseup"
        ></div>
        <!--<div id="info" class="col-md-1">
            {{title}}<br/>
            Nodes: {{stats.nodes}}<br/>
            Edges: {{stats.edges}}<br/>
        </div>-->
        </div>
    `
});