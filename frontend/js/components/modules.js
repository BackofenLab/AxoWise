Vue.component("modules", {
    props: ["gephi_json"],
    data: function() {
        return {
            modules: {}
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
        select_module(subset) {
            var com = this;

            com.$emit("active-subset-changed", subset);
        }
    },
    watch: {
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
            <div><h4> Groups </h4></div>
            <div id="modules">
                <div v-for="(value, key, index) in modules" >
                    <a href="#"><div class="rectangle" v-bind:style="{background: key}" v-on:click="select_module(value)"></div></a>
                </div>
            </div>
        </div>
    `
});