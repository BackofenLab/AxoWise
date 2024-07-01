<template>
  <div class="tool-item">
    <span>Hide labels</span>
    <input id="confirm" v-on:change="check()" type="checkbox" /><label
      for="confirm"
    ></label>
  </div>
</template>

<script>
export default {
  name: "ToggleLabel",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    check() {
      this.emitter.emit("hideLabels", {
        check: document.getElementById("confirm").checked,
        mode: this.mode,
      });
    },
  },
};
</script>

<style></style>
