<template>
    <div id="layerpane" class="text" v-show="active_termlayers !== null">
        <div class="nodeattributes">
            <div id="pathway-layers" class="subsection">
                <div class="subsection-header">
                    <span>selected pathways</span>
                </div>
                <div class="subsection-main">
                    <PathwayLayers
                    :active_termlayers='active_termlayers'
                    :hiding_terms='hiding_terms'
                    @hiding_terms_changed = 'hiding_terms = $event'
                    :gephi_data='gephi_data'
                    ></PathwayLayers>
                </div>
            </div>
            <div id="layer-connections" class="subsection">
                <div class="subsection-header">
                    <span>contained proteins</span>
                </div>
                <div class="subsection-main">
                    <LayerProteins
                    :active_termlayers='active_termlayers'
                    :hiding_terms='hiding_terms'
                    :gephi_data='gephi_data'
                    ></LayerProteins>
                </div>
            </div>
            <div id="pathway-connections" class="subsection">
                <div class="subsection-header">
                    <span>intersected pathways</span>
                </div>
                <div class="subsection-main">
                    <EnrichmentConnections
                    :active_termlayers='active_termlayers'
                    ></EnrichmentConnections>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PathwayLayers from '@/components/pane/modules/layer/PathwayLayers.vue'
import LayerProteins from '@/components/pane/modules/layer/LayerProteins.vue'
import EnrichmentConnections from '@/components/pane/modules/layer/EnrichmentConnections.vue'

export default {
    name: 'EnrichmentLayerPane',
    props: ['active_termlayers','gephi_data','node_color_index',],
    emits: ['active_item_changed'],
    components: {
        PathwayLayers,
        LayerProteins,
        EnrichmentConnections
    },
    data() {
        return {
            layer_item: {
                value: null,
                imageSrc: require('@/assets/pane/layer-icon.png')
            },
            terms: null,
            hiding_terms: new Set(),
            colorpalette: {},
            colors: 'rgba(0,0,0,1)',
            term: null,
        }
    },
    watch: {
        active_termlayers: {
            handler(newList) {
            var com = this;

            if (newList == null) {
                return;
            }
            
            com.layer_item.value = newList

            com.$emit('active_item_changed',{ "Pathway layers": com.layer_item})

        },
        deep: true,
    },

    },
    
}
</script>

<style>

    #layer-connections{
        height: 30%;
    }

    #pathway-layers{
        height: 30%;
    }

    #pathway-connections{
        height: 28%;
    }

</style>