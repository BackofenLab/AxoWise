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
        }
    },
    watch: {
        "active_term": function(term) {
            var com = this;
            if (term == null) {
                $("#termpane").animate({width: 'hide'}, 350);
                return;
            }

            com.selected_term = term;

            com.links = [];
            for (var idx in term.proteins) {
                var node = sigma_instance.graph.ensemblIdToNode(term.proteins[idx]);
                com.links.push(node);
            }

            // TODO
            $("#termpane").animate({width:'show'}, 350);
        }
    },
    mounted: function() {
        var com = this;

        $("#termpane").find(".returntext").click(() => com.$emit("active-term-changed", null));
        $("#termpane").find(".close").click(() => com.$emit("active-term-changed", null));
    },
    template: `
        <div id="termpane" class="pane">
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
    `
});
