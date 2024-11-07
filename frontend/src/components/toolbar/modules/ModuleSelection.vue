<template>
  <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
    Disable module ModuleSelection
    <ToggleSwitch class="toggle-xs" @value-change="check" />
  </li>
</template>

<script>
export default {
  name: "ModuleSelection",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    check() {
      this.emitter.emit("deactivateModules", { mode: this.mode });
    },
  },
};
</script>
