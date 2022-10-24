Vue.component("term-pane", {
    props: ["active_term", "func_json", "active_layer", "revert_term", "active_subset"],
    data: function() {
        return {
            selected_term: null,
            links: [],
            saved_links: [null],
            counter: null
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
        },
        hide_panel: function(check) {
            var com = this;
            if (check == true){
                $("#termpane").animate({width: 'show'}, 350);
            }
            if (check == false){
                $("#termpane").animate({width: 'hide'}, 350);
            }
        },
        change_level(subset) {
            var com = this;
            com.saved_links.push(subset);
            com.$emit("func-json-changed", subset);
            com.$emit("active-layer-changed", subset);
        },
        change_level_up(subsets) {
            var com = this;
            if(!subsets) return;
            subsets.pop();
            var subset = subsets[subsets.length - 1];
            com.$emit("revert-term-changed", subset);
            com.$emit("active-layer-changed", subset);
        }
    },
    watch: {
        "active_term": function(term) {
            var com = this;
            if(com.active_subset != null) return;  
            if (term == null) {
                $("#termminimize").animate({width: 'hide'}, 350);
                com.$emit("func-json-changed", null);
                return;
            }

            com.selected_term = term;

            com.links = [];
            for (var idx in term.proteins) {
                var node = sigma_instance.graph.ensemblIdToNode(term.proteins[idx]);
                com.links.push(node);
            }

            // TODO
             $("#termminimize").animate({width:'show'}, 350);
        }
    },
    mounted: function() {
        var com = this;

        $("#termminimize").find("#dropdown-btn-max").click(() => com.hide_panel(true));
        $("#termminimize").find("#dropdown-btn-min").click(() => com.hide_panel(false));
        $("#termminimize").find("#dropdown-btn-close").click(() => com.$emit("active-term-changed", null));
    },
    template: `
    <div id="termminimize" class="minimize">
        <button id="dropdown-btn-max">Maximize</button>
        <button id="dropdown-btn-min">Minimize</button>
        <button id="dropdown-btn-close">Close</button>
        <div id="termpane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="selected_term !== null" class="nodeattributes">
                    <div class="name">
                        <span>{{selected_term.name}}</span>
                    </div>
                    <div class="data">
                        <span><strong>ID: </strong>{{selected_term.id}}</span><br/><br/>
                        <span><strong>p-value: </strong>{{selected_term.p_value}}</span><br/><br/>
                        <span><strong>false-discovery-rate: </strong>{{selected_term.fdr_rate}}</span>
                    </div>
                    </br></br>
                    <div>
                    <button id="down_level" v-on:click="change_level(links)">Apply Level</button>
                    <button id="up_level" v-on:click="change_level_up(saved_links)">Revert Level</button>
                    </div>
                    <div class="p">Proteins:</div>
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
