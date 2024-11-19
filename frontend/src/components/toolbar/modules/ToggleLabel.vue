<template>
  <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
    Hide labels
    <ToggleSwitch class="toggle-xs" @value-change="check" />
  </li>
</template>

<script>
export default {
  name: "ToggleLabel",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    check(value) {
      this.emitter.emit("hideLabels", {
        check: value,
        mode: this.mode,
      });
    },
  },
};
</script>

<style></style>
