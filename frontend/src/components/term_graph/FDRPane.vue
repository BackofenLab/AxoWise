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
            expand_stats: false
        }
    },
    watch: {
        active_fdr() {
            var com = this;
            
            if (com.active_fdr == null) {
                return;
            }

            com.$emit('active_item_changed',{ "fdr": com.active_fdr })

        }
    },
    methods: {
    }
}
</script>

<style>

</style>