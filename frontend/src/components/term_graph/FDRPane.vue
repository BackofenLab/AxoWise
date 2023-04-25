<template>
    <div class="text" v-if="active_fdr !== null">
        <div class="headertext">
            <span>FDR</span>
        </div>
        <div class="nodeattributes">
        </div>
    </div>
</template>

<script>

export default {
    name: 'FDRPane',
    props: ['term_data','active_fdr'],
    emits: ['active_item_changed'],
    data() {
        return {
            links: null,
            expand_stats: false,
            fdr_item: {
                value: null,
                imageSrc: require('@/assets/pane/fdr-icon.png')
            }
        }
    },
    watch: {
        active_fdr() {
            var com = this;
            
            if (com.active_fdr == null) {
                return;
            }

            com.fdr_item.value = com.active_fdr
            com.$emit('active_item_changed',{ "fdr": com.fdr_item })

        }
    },
    methods: {
    }
}
</script>

<style>

</style>