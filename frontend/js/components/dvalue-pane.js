Vue.component("dvalue-pane", {
    props: ["d_value"],
    data: function() {
        return {
            selected_term: null,
            links: []
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
        }
    },
    watch: {
        "d_value": function(term) {
            var com = this;
            if (term == null) {
                $("#dvaluepane").animate({width: 'hide'}, 350);
                return;
            }

            var proteins = term[0][0];
            com.selected_term = proteins; 
            com.links = [];
            sigma_instance.graph.nodes().forEach(e => {
                if(proteins[e.attributes['Name']] > 0){
                    var node = sigma_instance.graph.ensemblIdToNode(e.attributes['Ensembl ID']);
                    com.links.push(node);  
                }
            });

            // TODO
            $("#dvaluepane").animate({width:'show'}, 350);
        }
    },
    mounted: function() {
        var com = this;

        $("#dvaluepane").find(".returntext").click(() => com.$emit("d_value-changed", null));
        $("#dvaluepane").find(".close").click(() => com.$emit("d_value-changed", null));
    },
    template: `
        <div id="dvaluepane" class="pane">
            <div class="text">
                <div title="Close" class="left-close returntext">
                    <div class="c cf">
                        <span>Return to the full network</span>
                    </div>
                </div>
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="selected_term !== null" class="nodeattributes">
                    <div class="name">
                        <span>Positive D-Value</span>
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
    `
});
