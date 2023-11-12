<template>
    <div class="tool-item">
        <span>Disable module selection</span>
        <input id="module" v-on:change="check()" type="checkbox" /><label for="module"></label>
    </div>
</template>

<script>
export default {
    name: 'ModuleSelection',
    data() {
        return {
          type: 'protein'
        }
    },
    methods: {
      check() {
        if(this.type == 'protein') this.emitter.emit("deactivateModules");
      }

    }
}
</script>

<style>
</style>
