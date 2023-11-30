<template>
    <div class="tool-item">
        <span>Disable module selection</span>
        <input id="module" v-on:change="check()" type="checkbox" /><label for="module"></label>
    </div>
</template>

<script>
export default {
    name: 'ModuleSelection',
    props: ['mode'],
    data() {
        return {
        }
    },
    methods: {
      check() {
        this.emitter.emit("deactivateModules", {mode: this.mode});
      }

    }
}
</script>

<style>
</style>
