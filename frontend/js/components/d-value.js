Vue.component("d-value", {
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
            com.$emit("d_value-changed", term);
        }
    },
    watch: {
        "gephi_json": function(json) {
            var com = this;
            if (!json) return ; //handling null json from backend
            if (!json.dvalue) return;

            com.terms = [];
            com.terms.push(json.dvalue);

        },
    },
    computed: {
    },
    template: `
        <div v-show="gephi_json != null" class="cf">
            <button v-on:click="select_term([terms[0], 0])" id="d-value">Show D-Value</button>
            <br/><br/>
            <button v-on:click="select_term([terms[0], 1])" id="d-value">Show D-Value2</button>
            <br/><br/>
            <button v-on:click="select_term([terms[0], 2])" id="d-value">Show D-Value3</button>
            <br/><br/>
            <button v-on:click="select_term([terms[0], 3])" id="d-value">Show D-Value4</button>
        </div>
    `
});