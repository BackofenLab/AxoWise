Vue.component("attribute-pane", {
    props: ["active_node"],
    data: function() {
        return {
            selected_node: null,
            links: []
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
        },
        normal_node: function() {
            var com = this;

            $("#attrminimize").animate({width: 'hide'}, 350);
        },
        hide_panel: function(check) {
            var com = this;
            if (check == true){
                $("#attributepane").animate({width: 'show'}, 350);
            }
            if (check == false){
                $("#attributepane").animate({width: 'hide'}, 350);
            }
        }
    },
    watch: {
        "active_node": function(id) {
            var com = this;

            if (id == null) {
                com.normal_node();
                return;
            }

            var node = sigma_instance.graph.getNodeFromIndex(id);
            com.selected_node = node;
            var neighbors = {};

            sigma_instance.graph.edges().forEach(function (e) {
                n = {
                    name: e.label,
                    color: e.color
                };
                if (id == e.source || id == e.target)
                    neighbors[id == e.target ? e.source : e.target] = n;
            });

            com.links = [];
            var lis = [];
            for (var id in neighbors) {
                var neighbor = sigma_instance.graph.getNodeFromIndex(id);
                com.links.push({
                    id: neighbor.id,
                    label: neighbor.label
                })
            }
            $("#attrminimize").animate({width:'show'}, 350);
        }
    },
    mounted: function() {
        var com = this;

        $("#attrminimize").find("#dropdown-btn-max").click(() => com.hide_panel(true));
        $("#attrminimize").find("#dropdown-btn-min").click(() => com.hide_panel(false));
        $("#attrminimize").find("#dropdown-btn-close").click(() => com.select_node(null));
    },
    template: `
    <div id="attrminimize" class="minimize">
        <button id="dropdown-btn-max">Maximize</button>
        <button id="dropdown-btn-min">Minimize</button>
        <button id="dropdown-btn-close">Close</button>
        <div id="attributepane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="selected_node !== null" class="nodeattributes">
                    <div class="name">
                        <span>{{selected_node.label}}</span>
                    </div>
                    <div class="data">
                        <div v-for="(value, key, index) in selected_node.attributes">
                            <span><strong>{{key}}: </strong>{{value}}</span><br/><br/>
                        <div/>
                    </div>
                    <div class="p">Connections:</div>
                    <div class="link">
                        <ul>
                        <li class="membership" v-for="link in links">
                            <a href="#" v-on:click="select_node(link.id)">{{link.label}}</a>
                        </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>     
    `
});
