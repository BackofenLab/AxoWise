<template>
  <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
    Visualize fdr-rate
    <Button label="yes" size="small" severity="secondary" @click="activate_fdr(check);
    check = !check;"></Button>
  </li>
</template>

<script>
export default {
  name: "FDRValue",
  data() {
    return {
      check: true,
    };
  },
  methods: {
    activate_fdr() {
      this.emitter.emit("activateFDR", this.check);
    },
  },
};
</script>
