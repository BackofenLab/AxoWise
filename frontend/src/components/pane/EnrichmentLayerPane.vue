<template>
    <div class="text" v-if="active_termlayers !== null">
        <div class="headertext">
            <span>Term Visualization</span>
        </div>
        <div class="nodeattributes">
            <div class="p">
            <span>Layers:</span>
            </div>
            <div class="link" id="link">
                <ul>
                    <li class="membership" v-for="term in terms" :key="term" >
                        <a href="#" v-on:click="select_enrichment(term)">{{term.name}}</a>
                    </li>
                </ul>
            </div>
            
        </div>
    </div>
</template>

<script>

export default {
    name: 'EnrichmentLayerPane',
    props: ['active_termlayers','gephi_data','node_color_index',],
    emits: ['active_item_changed'],
    data() {
        return {
            layer_item: {
                value: null,
                imageSrc: require('@/assets/pane/layer-icon.png')
            },
            terms: null
        }
    },
    watch: {
        active_termlayers() {
            var com = this;
            
            if (com.active_termlayers == null) {
                return;
            }
            
            com.layer_item.value = com.active_termlayers

            com.terms = com.active_termlayers

            com.$emit('active_item_changed',{ "layers": com.layer_item})
            

        }
    },
    methods: {
        select_enrichment(value){

            this.emitter.emit("searchEnrichment", value);
        }
        
    },
}
</script>

<style>

    .pane-show {
        transform: translateX(326px);
    }

</style>