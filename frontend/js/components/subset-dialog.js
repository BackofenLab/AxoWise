Vue.component("subset-dialog", {
    props: ["gephi_json", "active_subset", "node2term_index"],
    watch: {
        "active_subset": function(subset) {
            if (subset == null || subset.length < 1) return;

            $("#dialog").dialog("open");
        }
    },
    mounted: function() {
        var com = this;

        var close = function() {
            $("#dialog").dialog("close");
            com.$emit("active-subset-changed", null);
        };

        $("#dialog").dialog({
            autoOpen: false,
            resizable: false,
            height: "auto",
            width: 400,
            maxHeight: 500,
            modal: false,
            buttons: {
                "Close": close,
            },
            close: close
        });
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
        }
    },
    computed: {
        terms: function() {
            var com = this;
            if (com.gephi_json == null || com.active_subset == null) return;

            var all_terms = com.gephi_json.enrichment;
            all_terms.sort(function(t1, t2) {
                var p_t1 = parseFloat(t1.p_value);
                var p_t2 = parseFloat(t2.p_value);
                return p_t1 - p_t2;
            });

            function union(setA, setB) {
                if (!setA && !setB) return new Set();
                if (!setA) return setB;
                if (!setB) return setA;

                var _union = new Set(setA);
                for (var elem of setB) {
                    _union.add(elem);
                }
                return _union;
            }

            var ensembl_ids = com.active_subset.map(protein => protein.attributes["Ensembl ID"]);
            var term_sets = ensembl_ids.map(id => com.node2term_index[id]);
            var contained_terms = term_sets.reduce(union, new Set());

            return contained_terms;
        }
    },
    template: `
        <div id="dialog" title="Protein subset">
            <b>Proteins:</b>
            <p v-for="node in active_subset">
                <a href="#" v-on:click="select_node(node.id)">{{node.label}}</a>
            </p>
            <br/><hr/><br/>
            <b>Functional terms:</b>
            <p v-for="term in terms">
                <a href="#" v-on:click="select_term(term)">{{term.name}}</a>
            </p>
        </div>
    `
});
