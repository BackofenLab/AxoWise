<template>
  <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
    Hide unconnected nodes
    <ToggleSwitch class="toggle-xs" @value-change="show_whole" />
  </li>
</template>

<script>
export default {
  name: "ConnectedGraph",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    show_whole(value) {
      this.emitter.emit("unconnectedGraph", {
        check: value,
        mode: this.mode,
      });
    },
  },
};
</script>
