<template>
  <div class="tool-item">
    <span>Show all cluster</span>
    <input
      id="switch-modules"
      v-on:change="show_whole()"
      type="checkbox"
    /><label for="switch-modules"></label>
  </div>
</template>

<script>
export default {
  name: "ShowModules",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    show_whole() {
      this.emitter.emit("showCluster", {
        check: document.getElementById("switch-modules").checked,
        mode: this.mode,
      });
    },
  },
};
</script>

<style>
#switch-modules {
  margin-left: 5%;
}
</style>
