Vue.component("subset-dialog", {
    props: ["gephi_json", "active_subset", "node2term_index", "func_enrichment", "func_json","reset_term"],
    data: function() {
        return {
            contained_terms: null,
            used_subset: [],
        }
    },
    watch: {
        "active_subset": function(subset) {
            var com = this;
            if (subset == null || subset.length < 1){
                old_sub = com.used_subset.pop();
                com.$emit("reset-term-changed", old_sub);
                $("#subsminimize").animate({width:'hide'}, 350);
                return;
            }
            var com = this;
            if (com.func_enrichment == null || com.active_subset == null) return;
            com.used_subset.push(subset);
            com.$emit("func-json-changed", subset);

            $("#subsminimize").animate({width:'show'}, 350);

        }
    },
    mounted: function() {
        var com = this;

        $("#subsminimize").find("#dropdown-btn-max").click(() => com.hide_panel(true));
        $("#subsminimize").find("#dropdown-btn-min").click(() => com.hide_panel(false));
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
        hide_panel: function(check) {
            if (check == true){
                $("#subspane").animate({width: 'show'}, 350);
            }
            if (check == false){
                $("#subspane").animate({width: 'hide'}, 350);
            }
        }
    },
    template: `
    <div id="subsminimize" class="minimize">
        <button id="dropdown-btn-max">Maximize</button>
        <button id="dropdown-btn-min">Minimize</button>
        <button id="dropdown-btn-close">Close</button>
        <div id="subspane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div v-if="active_subset !== null" class="nodeattributes">
                <b>Proteins:</b>
                <p v-for="node in active_subset">
                    <a href="#" v-on:click="select_node(node.id)">{{node.label}}</a>
                </p>
                <br/><hr/><br/>
                </div>
            </div>
        </div>
    </div>
    `
});
