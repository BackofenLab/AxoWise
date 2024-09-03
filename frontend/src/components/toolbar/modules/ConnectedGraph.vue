<template>
  <div class="tool-item">
    <span>Hide unconnected nodes</span>
    <input id="switch" v-on:change="show_whole()" type="checkbox" /><label
      for="switch"
    ></label>
  </div>
</template>

<script>
export default {
  name: "ConnectedGraph",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    show_whole() {
      this.emitter.emit("unconnectedGraph", {
        check: document.getElementById("switch").checked,
        mode: this.mode,
      });
    },
  },
};
</script>

<style>
#switch {
  margin-left: 5%;
}
</style>
