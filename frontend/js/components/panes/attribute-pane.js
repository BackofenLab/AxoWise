Vue.component("attribute-pane", {
    props: ["active_node"],
    data: function() {
        return {
            selected_node: null,
            links: [],
            pane_check: false,
            proteins_expand: false
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
        },
        normal_node: function() {
            var com = this;

            $("#attrminimize").hide();
        },
        hide_panel: function() {
            var com = this;
            if(com.pane_check == false){
                $("#attrminimize").find("#dropdown-btn-min").css({'transform': 'rotate(90deg)'});
                $("#attributepane").hide();
            }else{
                $("#attrminimize").find("#dropdown-btn-min").css({'transform': 'rotate(0deg)'});
                $("#attributepane").show();
            }
            com.pane_check = !com.pane_check;
        },
        expand_proteins: function() {
            var com = this;
            com.proteins_expand = !com.proteins_expand;
            if(com.proteins_expand == false){
                $("#link").hide();
            }else{
                $("#link").show();
            }
            
        },
        copyclipboard: function(){
            com = this;

            textToCopy = [];
            for(link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
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
            for (var id in neighbors) {
                var neighbor = sigma_instance.graph.getNodeFromIndex(id);
                com.links.push({
                    id: neighbor.id,
                    label: neighbor.label
                })
            }
            $("#attrminimize").show();
        }
    },
    mounted: function() {
        var com = this;

        $("#attrminimize").find("#dropdown-btn-min").click(() => com.hide_panel());
        $("#attrminimize").find("#dropdown-btn-close").click(() => com.select_node(null));
    },
    template: `
    <div id="attrminimize" class="minimize">
        <div class="min-button">
        <button id="dropdown-btn-min"></button>
        <button id="dropdown-btn-close"></button>
        </div>
        <div id="attributepane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="selected_node !== null" class="nodeattributes">
                    <div class="name">
                        <span>{{selected_node.attributes['Name']}}</span>
                    </div>
                    <div class="data">
                        <div v-for="(value, key, index) in selected_node.attributes">
                            <span><strong>{{key}}: </strong>{{value}}</span><br/><br/>
                        <div/>
                    </div>
                    <div class="p">
                    <span>Connections:</span>
                    <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                    <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
                    </div>
                    <div class="link" id="link">
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
