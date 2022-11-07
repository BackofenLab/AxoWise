Vue.component("subset-dialog", {
    props: ["gephi_json", "active_subset", "func_enrichment", "func_json","reset_term", "active_node", "active_term"],
    data: function() {
        return {
            contained_terms: null,
            used_subset: [],
            pane_check: false,
            contained_edges: [],
            subset_ids: [],
            proteins_expand: false,
            edges_expand: false,
            export_edges: [],
            export_option: ['Nodes', 'Edges'],
            selected_export: null,
        }
    },
    watch: {
        "active_subset": function(subset) {
            var com = this;

            if(com.active_node || com.func_enrichment == null)return;

            com.contained_edges = [];
            com.export_edges = [];
            com.subset_ids = [];

            if (subset == null || subset.length < 1){
                if(com.active_term == null){
                old_sub = com.used_subset.pop();
                com.$emit("reset-term-changed", old_sub);
                }
                $("#subsminimize").hide();
                return;
            }

            if (com.active_subset == null) return;
            com.used_subset.push(subset);
            com.$emit("func-json-changed", subset);

            var id_dict = {};
            for (getID in subset){
                id_dict[subset[getID].id] = subset[getID].label;
                com.subset_ids.push(subset[getID].id);
            }
            var subset_proteins = new Set(com.subset_ids);
            for (var idx in com.gephi_json.edges) {
                var edge = com.gephi_json.edges[idx];
                if(subset_proteins.has(edge.source) && subset_proteins.has(edge.target)){
                    if(edge.source != null && edge.target != null){
                        com.export_edges.push(edge);
                        com.contained_edges.push({
                            
                            "source": [edge.source, id_dict[edge.source]],
                            "target": [edge.target, id_dict[edge.target]]
                        
                        });
                    }
                }
            }

            $("#subsminimize").show();

        }
    },
    mounted: function() {
        var com = this;

        $("#subsminimize").find("#dropdown-btn-min").click(() => com.hide_panel());
        $("#subsminimize").find("#dropdown-btn-close").click(() => com.$emit("active-subset-changed", null));
    },
    methods: {
        select_node: function(id) {
            var com = this;
            // $("#dialog").dialog("close");
            com.$emit("active-node-changed", id);
        },
        select_term: function(term) {
            var com = this;
            // $("#dialog").dialog("close");
            com.$emit("active-term-changed", term);
        },
        hide_panel: function() {
            var com = this;
            if(com.pane_check == false){
                $("#subsminimize").find("#dropdown-btn-min").css({'transform': 'rotate(90deg)'});
                $("#subspane").hide();
            }else{
                $("#subsminimize").find("#dropdown-btn-min").css({'transform': 'rotate(0deg)'});
                $("#subspane").show();
            }
            com.pane_check = !com.pane_check;
        },
        copyclipboard: function(){
            com = this;

            textToCopy = [];
            for(link of com.active_subset) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        export_all: function(exports){
            com = this;

            //export nodes as csv
            csvNodeData = com.active_subset
            nodes_csv = 'Ensembl,Name,Modularity,Degree\n';

            csvNodeData.forEach(function(row) {
                nodes_csv += row.attributes['Ensembl ID'] + ", " + row.attributes['Name'] + ", " + row.attributes['Modularity Class'] + "," + row.attributes['Degree'];
                nodes_csv += "\n";  
            });

            //export edges as csv
            csvEdgesData = com.export_edges
            edges_csv = 'Source,Target\n';

            csvEdgesData.forEach(function(row) {
                edges_csv += row.source + " , " + row.target;
                edges_csv += "\n";  
            });

            var hiddenElement = document.createElement('a');
            hiddenElement.target = '_blank';
            if(exports == 'Nodes'){
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(nodes_csv);
            }else if (exports == 'Edges'){
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(edges_csv);
            }
            hiddenElement.download = exports+'.csv';  
            hiddenElement.click();


        },
        expand_proteins: function() {
            var com = this;
            com.edges_expand = !com.edges_expand;
            if(com.edges_expand == false){
                $("#link").hide();
            }else{
                $("#link").show();
            }
            
        },
        expand_assoc: function() {
            var com = this;
            com.proteins_expand = !com.proteins_expand;
            if(com.proteins_expand == false){
                $("#edges").hide();
            }else{
                $("#edges").show();
            }
            
        },
        
    },
    template: `
    <div id="subsminimize" class="minimize">
        <div class="min-button">
            <button id="dropdown-btn-min"></button>
            <button id="dropdown-btn-close"></button>
            </div>
        <div id="subspane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="active_subset !== null" class="nodeattributes">
                <div class="p">
                <b>Proteins:</b>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
                </div>
                    <div class="link" id="link">
                        <ul>
                            <li v-for="node in active_subset">
                                <a href="#" v-on:click="select_node(node.id)">{{node.label}}</a>
                            </li>
                        </ul>
                    </div>
                <div class="p2">
                <b>Associations:</b>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_assoc()" id="expand-btn">Expand</button>
                </div>
                    <div class="link" id="edges">
                        <ul>
                            <li v-for="edge in contained_edges">
                                <div class="edge">
                                <a href="#" v-on:click="select_node(edge.source[0])">{{edge.source[1]}}</a>
                                <a href="#" v-on:click="select_node(edge.target[0])">{{edge.target[1]}}</a>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <select v-model="selected_export">
                    <option disabled value="">Select Export</option>
                    <option v-for="exports in export_option">{{exports}}</option>
                    </select>
                    <button id="export-all-btn" v-on:click="export_all(selected_export)">Export</button>
                </div>
            </div>
        </div>
    </div>
    `
});
