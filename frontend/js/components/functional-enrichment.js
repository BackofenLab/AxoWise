Vue.component("functional-enrichment", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
            terms: [],
            search_raw: ""
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
            if (!json) return ; //handling null json from backend
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
    computed: {
        regex: function() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase());
        },
        filtered_terms: function() {
            var com = this;

            if (com.search_raw == "") return com.terms;

            var regex = com.regex;
            var filtered = com.terms.filter(term => regex.test(term.name.toLowerCase()));
            return filtered;
        }
    },
    template: `
        <div v-show="gephi_json != null" id="enrichment" class="cf">
            <h4>Functional enrichment:</h4>
            <input type="text" value="Search functional terms by name" v-model="search_raw" class="empty"/>
            <div class="results">
                <i v-if="message.length > 0">{{message}}</i>
                <div v-for="entry in filtered_terms">
                    <a href="#" v-on:click="select_term(entry)">{{entry.name}}</a>
                </div>
                <div v-if="terms.length == 0">
                    <i>No terms available.</i>
                </div>
            </div>
        </div>
    `
});