<template>
    <div id="modules-parent" class="modules-position">
        <div id="modules">
            <div v-for="(value, key) in modules" :key="key" >
                <template v-if="key !== 'rgb(255,255,153)'">
                    <a href="#">
                        <div class="rectangle" v-bind:style="{background: key}" v-on:click="select_module(value, key)"></div>
                    </a>
                </template>
                <template v-if="key == 'rgb(255,255,153)'">
                    <a href="#">
                        <div id="unconnected_group" class="rectangle" v-bind:style="{background: key}" v-on:click="select_module(value, key)"></div>
                    </a>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ModularityClass',
    props: ['gephi_data', 'active_subset', 'type', 'term_data'],
    emits: [],
    data() {
        return {
            modules: null,
            saved_dict: {}
        }
    },
    methods: {
        select_module(subset, key) {
            var com = this;

            if (key in com.saved_dict && Object.getOwnPropertyNames(com.saved_dict).length > 1) {
                delete com.saved_dict[key];
            } else {
                com.saved_dict[key] = com.modules[key];
            }

            const multiple_clusters = Object.values(com.saved_dict).flat();

            this.$emit('active_subset_changed', multiple_clusters)
        },
        show_unconnectedGraphModule(state) {

            const module = document.getElementById('unconnected_group')
            if(state == 'Whole Graph') {
                module.style.display = 'flex'
            }
            else module.style.display = 'none'
            
        }
    },
    watch: {
        active_subset(subset) {
            if(!subset) this.saved_dict={};
        },
        term_data(){
            var com = this;

            com.modules = {};
            if(!com.term_data) return; //handling null json from backend
            var nodes = com.term_data.nodes; 
            for (var idx in nodes) {
                var node = nodes[idx];
                if (!(node.color in com.modules)) com.modules[node.color] = [];
                com.modules[node.color].push(node);
            }

        }
    },
    mounted() {
        var com = this;

        com.modules = {};
        var nodes = null;
        if(com.type == 'protein'){
            if(!com.gephi_data) return; //handling null json from backend
            nodes = com.gephi_data.nodes; 
            
        }
        else {
            if(!com.term_data) return; //handling null json from backend
            nodes = com.term_data.nodes; 
        }
        for (var idx in nodes) {
            var node = nodes[idx];
            if (!(node.color in com.modules)) com.modules[node.color] = [];
            com.modules[node.color].push(node);
        }

        this.emitter.on("unconnectedGraph", state => {
            this.show_unconnectedGraphModule(state)
        });

        this.emitter.on("unconnectedTermGraph", state => {
            this.show_unconnectedGraphModule(state)
        });
    }
}
</script>

<style>
#modules-parent {
    margin: 0 10px 0 10px;
}

#unconnected_group {
  display: none;
}
</style>