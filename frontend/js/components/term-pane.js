Vue.component("term-pane", {
    props: ["active_term"],
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
        },
        hide_panel: function(check) {
            var com = this;
            if (check == true){
                $("#termpane").animate({width: 'show'}, 350);
            }
            if (check == false){
                $("#termpane").animate({width: 'hide'}, 350);
            }
        }
    },
    watch: {
        "active_term": function(term) {
            var com = this;
            if (term == null) {
                $("#termminimize").animate({width: 'hide'}, 350);
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
                        <span><strong>p-value: </strong>{{selected_term.p_value}}</span>
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
