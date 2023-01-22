Vue.component("modules", {
    props: ["gephi_json","active_subset"],
    data: function() {
        return {
            modules: {},
            multiple_check: false,
            saved_dict:{}
        }
    },
    updated: function() {
        var element=$('#modules');
        if($(element).html()==''){
        $(element).parent().hide();
        }else{
             $(element).parent().show();
        }
    },
    methods: {
        select_module(subset, key) {
            var com = this;


            if(key in com.saved_dict && Object.keys(com.saved_dict).length >1){
                delete com.saved_dict[key]; 
            }
            else{
                com.saved_dict[key]=com.modules[key]
            }

            var multiple_clusters = [];

            for (const [key,value] of Object.entries(com.saved_dict)) {
                
                multiple_clusters = multiple_clusters.concat(value);

            }

            com.$emit("active-subset-changed", multiple_clusters);

            
        }
    },
    watch: {
        "active_subset": function(subset) {
            var com = this;

            if(!subset) com.saved_dict={};

        },
        "gephi_json": function() {
            var com = this;
            com.modules = {};
            if(!com.gephi_json) return; //handling null json from backend

            var nodes = com.gephi_json.nodes;
            for (var idx in nodes) {
                var node = nodes[idx];
                if (!(node.color in com.modules)) com.modules[node.color] = [];
                com.modules[node.color].push(node);
            }
        }
    },
    template: `
        <div id="modules-parent" class="modules-position">
            <div id="modules">
                <div v-for="(value, key, index) in modules" >
                    <a href="#"><div class="rectangle" v-bind:style="{background: key}" v-on:click="select_module(value, key)"></div></a>
                </div>
            </div>
        </div>
    `
});