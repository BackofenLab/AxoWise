Vue.component("fdrvalue", {
    props: ["gephi_json","fdrvalue"],
    data: function() {
        return  {
            dcheck: false,
        }
    },
    methods: {
        select_term: function(term) {
            var com = this;
            com.dcheck = !com.dcheck
            com.$emit("fdrvalue-changed", term);
        }
    },
    watch: {
        "gephi_json": function(json) {
            var com = this;

            if (!json)return ;//handling null json from backend

        },
        "fdrvalue": function(subset){
        }
    },
    mounted: function() {
        var com = this;
        
    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
        <div class="toolbar-theme">
            <button v-on:click= "select_term(dcheck)">Apply</button>
            <span class="toolbar-icon">F</span>
            </div>
        </div>
    `
});