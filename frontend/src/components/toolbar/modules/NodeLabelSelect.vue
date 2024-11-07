<template>
  <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
    Reset labels
    <Button label="yes" size="small" severity="secondary" @click="reset_labels"></Button>
  </li>
</template>

<script>
export default {
  name: "NodeLabelSelect",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    reset_labels() {
      this.emitter.emit("resetSelect", { mode: this.mode });
    },
  },
};
</script>