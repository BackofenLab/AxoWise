<template>
    <div class="tool-item">
        <span>Hide labels</span>
        <input id="confirm" v-on:change="check()" type="checkbox" /><label for="confirm"></label>
    </div>
</template>

<script>
export default {
    name: 'ToggleLabel',
    data() {
        return {
          type: 'protein'
        }
    },
    methods: {
      check() {
        if(this.type == 'protein') this.emitter.emit("hideLabels", document.getElementById('confirm').checked);
        else this.emitter.emit("hideTermLabels", document.getElementById('confirm').checked)
      }

    }
}
</script>

<style>
</style>