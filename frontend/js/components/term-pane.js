Vue.component("term-pane", {
    props: ["active_term", "func_json", "active_layer", "revert_term", "active_subset", "gephi_json"],
    data: function() {
        return {
            selected_term: null,
            links: [],
            saved_links: [null],
            counter: null,
            pane_check: false,
            proteins_expand: false,
            number_asc: "",
            number_prot: "",
            associations: [],
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
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
        },
        hide_panel: function() {
            var com = this;
            if(com.pane_check == false){
                $("#termminimize").find("#dropdown-btn-min").css({'transform': 'rotate(90deg)'});
                $("#termpane").hide();
            }else{
                $("#termminimize").find("#dropdown-btn-min").css({'transform': 'rotate(0deg)'});
                $("#termpane").show();
            }
            com.pane_check = !com.pane_check;
        },
        expand_proteins: function() {
            var com = this;
            com.proteins_expand = !com.proteins_expand;
            if(com.proteins_expand == false){
                $("#linkterm").hide();
            }else{
                $("#linkterm").show();
            }
            
        },
        copyclipboard: function(){
            com = this;

            textToCopy = [];
            for(link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
            },
        updateNumbers: function(){
                com = this;
    
                com.associations = [];

                com.number_prot = com.links.length.toString();
                
                var subset_proteins = new Set(com.selected_term.proteins);
                for (var idx in com.gephi_json.edges) {
                    var edge = com.gephi_json.edges[idx];
                    if(subset_proteins.has(edge.source) && subset_proteins.has(edge.target)){
                        com.associations.push(edge);
                    }
                }

                com.number_asc = com.associations.length.toString();

            }
    },
    watch: {
        "active_term": function(term) {
            var com = this; 
            if (term == null) {
                $("#termminimize").hide();
                com.$emit("func-json-changed", null);
                return;
            }

            com.selected_term = term;

            com.links = [];
            for (var idx in term.proteins) {
                var node = sigma_instance.graph.ensemblIdToNode(term.proteins[idx]);
                com.links.push(node);
            }

            com.updateNumbers();
            // TODO
             $("#termminimize").show();
        }
    },
    mounted: function() {
        var com = this;

        $("#termminimize").find("#dropdown-btn-min").click(() => com.hide_panel());
        $("#termminimize").find("#dropdown-btn-close").click(() => com.$emit("active-term-changed", null));
    },
    template: `
    <div id="termminimize" class="minimize">
        <div class="min-button">
        <button id="dropdown-btn-min"></button>
        <button id="dropdown-btn-close"></button>
        </div>
        <div id="termpane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="selected_term !== null" class="nodeattributes">
                    <div class="name_term">
                    <span>{{selected_term.name}}</span>
                    </div>
                    <div class="change-level-menu">
                    <button id="down_level" v-on:click="change_level(links)">Apply</button>
                    <button id="up_level" v-on:click="change_level_up(saved_links)">Revert</button>
                    </div>
                    <div class="data">
                        <span><strong>ID: </strong>{{selected_term.id}}</span><br/><br/>
                        <span><strong>p-value: </strong>{{selected_term.p_value}}</span><br/><br/>
                        <span><strong>FDR: </strong>{{selected_term.fdr_rate}}</span><br/><br/>
                        <span><strong>Number of Proteins: </strong>{{number_prot}}</span><br/><br/>
                        <span><strong>Number of Associations: </strong>{{number_asc}}</span><br/><br/>
                    </div>
                    <div class="p">
                    <span>Proteins:</span>
                    <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                    <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
                    </div>
                    <div class="link" id="linkterm">
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
