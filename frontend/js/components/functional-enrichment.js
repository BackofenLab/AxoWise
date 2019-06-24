Vue.component("functional-enrichment", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
            terms: []
        }
    },
    methods: {
        select_term: function(term) {
            var com = this;
            com.$emit("active-term-changed", term);
        }
    },
    watch: {
        "gephi_json": function(json) {
            var com = this;
            if (!json.enrichment) return;

            com.terms = [];
            for (var idx in json.enrichment) {
                com.terms.push(json.enrichment[idx]);
            }

            com.terms.sort(function(t1, t2) {
                var p_t1 = parseFloat(t1.p_value);
                var p_t2 = parseFloat(t2.p_value);
                return p_t1 - p_t2;
            });
        },
    },
    template: `
        <div id="enrichment" class="cf">
            <h2>Functional enrichment:</h2>
            <div class="results">
                <i v-if="message.length > 0">{{message}}</i>
                <div v-for="entry in terms">
                    <a href="#" v-on:click="select_term(entry)">{{entry.name}}</a>
                </div>
                <div v-if="terms.length == 0">
                    <i>No terms available.</i>
                </div>
            </div>
        </div>
    `
});