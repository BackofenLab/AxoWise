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
    props: ['term_data',],
    emits: [],
    data() {
        return {
            links: null,
            expand_stats: false
        }
    },
    watch: {
        active_fdr() {
            var com = this;
            
            if (com.fdr_active == null) {
                return;
            }

        }
    },
    methods: {
    }
}
</script>

<style>

</style>