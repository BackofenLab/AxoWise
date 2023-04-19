<template>
    <div class="tool-item">
        <li v-on:click="show_fdr">Show FDR</li>
    </div>
</template>

<script>
export default {
    name: 'FDRValue',
    data() {
        return {
            check: false
        }
    },
    methods: {
        show_fdr() {
            this.emitter.emit("fdrvalue", this.check);
            this.check = !this.check
        }
    },
}
</script>