Vue.component("d-value", {
    props: ["gephi_json","d_value"],
    data: function() {
        return  {
            selected_d: null,
            dcoloumns: [],
            dcheck: false,
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

            if (!json)return ;//handling null json from backend
            if (!json.dvalues) return ; //handling null json from backend


            com.dcoloumns = com.dcoloumns.concat(json.dvalues);

        },
        "d_value": function(subset){

            // Select default value in d.
            if(!subset){
                document.getElementById("select_d").selectedIndex = 0;
            }
        }
    },
    mounted: function() {
        var com = this;
        
    },
    template: `
        <div v-show="gephi_json != null && dcoloumns.length >= 1" class="toolbar-button">
        <div class="toolbar-theme">
            <v-select id="select_d" v-model="selected_d" :searchable="false" :options="dcoloumns" v-on:input="select_term(selected_d)"></v-select>
            <span class="toolbar-icon">D</span>
            </div>
        </div>
    `
});