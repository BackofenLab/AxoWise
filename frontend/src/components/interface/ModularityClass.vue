<template>
    <div id="modules-parent" class="modules-position">
        <div id="modules">
            <div v-for="(value, key) in modules" :key="key" >
                <a href="#"><div class="rectangle" v-bind:style="{background: key}" v-on:click="select_module(value, key)"></div></a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ModularityClass',
    props: ['gephi_data', 'active_subset'],
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
        }
    },
    watch: {
        active_subset(subset) {
            if(!subset) this.saved_dict={};
        }
    },
    mounted() {
        var com = this;

        com.modules = {};
        if(!com.gephi_data) return; //handling null json from backend

        var nodes = com.gephi_data.nodes;
        for (var idx in nodes) {
            var node = nodes[idx];
            if (!(node.color in com.modules)) com.modules[node.color] = [];
            com.modules[node.color].push(node);
        }
    }
}
</script>

<style>
#modules-parent {
    margin: 0 10px 0 10px;
}
</style>