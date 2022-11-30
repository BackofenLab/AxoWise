Vue.component("hubs", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
            select_function: ["Whole Graph", "Main Graph"],
            selected_func: null
        }
    },
    methods: {
        get_hubs: function(state) {
            var com = this;

            
            com.$emit("unconnected-graph-changed", [com.gephi_json.subgraph, state]);

        }
    },
    watch: {
        "active_subset": function(subset){

            // Select default value in hubs.
            if(!subset){
                document.getElementById("select_hubs").selectedIndex = 0;
            }
        }
    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
                <v-select id="select_d" v-model="selected_func" :options="select_function" v-on:input="get_hubs(selected_func)"></v-select>
                <span class="toolbar-icon">G</span>
            </div>
        </div>
    `
});