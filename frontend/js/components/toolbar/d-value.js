Vue.component("d-value", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
            terms: null,
            selected_d: null,
            dcoloumns: ["no selection"],
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
    },
    mounted: function() {
        var com = this;
        
    },
    template: `
        <div v-show="gephi_json != null && dcoloumns.length > 1" class="toolbar-button">
        <div class="toolbar-theme">
            <select v-model="selected_d" v-on:change="select_term(selected_d)">
                <option disabled value="">Please select D Section</option>
                <option v-for="value in dcoloumns">{{value}}</option>
            </select>
            <span class="toolbar-icon">D</span>
            </div>
        </div>
    `
});