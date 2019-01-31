var NETWORK = null;

Vue.component("visualization", {
    props: ["data", "show", "title", "threshold"],
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
                    }
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
            }
        }
    },
    computed: {
        positioned_data: function() {
            var com = this;
            var data = com.data;
            if (!NETWORK) return;

            NETWORK.setData(data);
            NETWORK.stabilize(50);
            NETWORK.storePositions();
            return data;
        },
        filtered_data: function() {
            var com = this;

            if (!com.positioned_data) return;

            var filtered_nodes = com.positioned_data.nodes.get({
                filter: function(node) {
                    if (node.color == colors.protein) return com.show.proteins;
                    else if (node.color == colors.pathway) return com.show.pathways;
                    else if (node.color == colors.gray) return com.show.classes;
                    return true;
                }
            });

            var filtered_edges = com.positioned_data.edges.get({
                filter: function(edge) {
                    return edge.value / 1000 >= com.threshold;
                }
            });

            return {
                nodes: filtered_nodes,
                edges: filtered_edges
            };
        }
    },
    watch: {
        "filtered_data": function(data) {
            var com = this;
            com.draw(data);
        }
    },
    methods: {
        draw: _.debounce(function(data) {
            if (!NETWORK) return;
            NETWORK.setData(data);

            // Vis.js
            this.stats.nodes = data.nodes.length;
            this.stats.edges = data.edges.length;
        
            if (data.selected_nodes)
                NETWORK.selectNodes(data.selected_nodes);
        }, 100),
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
        // rectangular select
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
            if(!com.data) return;
            var rectangle = com.rectangular_select.rectangle;

            var selected_nodes = [];
            var x_range = com.get_select_range(rectangle.startX, rectangle.w);
            var y_range = com.get_select_range(rectangle.startY, rectangle.h);

            var nodes = com.data.nodes.get();
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
        NETWORK = new vis.Network(container, {
            nodes: new vis.DataSet([]),
            edges: new vis.DataSet([])
        }, com.network_options);

        // rectangular select
        container.oncontextmenu = function() { return false; };
        com.rectangular_select.canvas = NETWORK.canvas.frame.canvas;
        com.rectangular_select.context = com.rectangular_select.canvas.getContext("2d");
    },
    template: `
        <div>
        <div id="visualization"
             class="col-md-12"
             v-on:mousedown="mousedown"
             v-on:mousemove="mousemove"
             v-on:mouseup="mouseup"
        ></div>
        <div id="info" class="col-md-4">
            {{title}}<br/>
            Nodes: {{stats.nodes}}<br/>
            Edges: {{stats.edges}}<br/>
        </div>
        </div>
    `
});