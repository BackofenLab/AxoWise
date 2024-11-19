<template>
  <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
    Show all cluster
    <ToggleSwitch class="toggle-xs" @value-change="show_whole" />
  </li>
</template>

<script>
export default {
  name: "ShowModules",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    show_whole(value) {
      this.emitter.emit("showCluster", {
        check: value,
        mode: this.mode,
      });
    },
  },
};
</script>