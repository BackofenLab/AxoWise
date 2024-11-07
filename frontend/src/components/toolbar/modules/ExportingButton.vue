<template>
  <Button severity="secondary" type="button" label="Export proteins as .csv" icon="pi pi-download" iconPos="right"
    class="!w-full !justify-between !rounded-lg" @click="toggle" />
  <Popover class="w-[12rem]" ref="op" :pt="{ content: { class: 'px-1 flex flex-col gap-1' } }">
    <Button text plain severity="secondary" type="button" label="White / .png" class="!justify-start !py-1"
      @click="take_screen('white', 'png')" />
    <Button text plain severity="secondary" type="button" label="Black / .png" class="!justify-start !py-1"
      @click="take_screen('black', 'png')" />
    <Button text plain severity="secondary" type="button" label="White / .svg" class="!justify-start !py-1"
      @click="take_screen('white', 'svg')" />
    <Button text plain severity="secondary" type="button" label="Black / .svg" class="!justify-start !py-1"
      @click="take_screen('black', 'svg')" />

  </Popover>
</template>

<script setup>
import { ref } from "vue";

const op = ref();

const toggle = (event) => {
  op.value.toggle(event);
};
</script>

<script>
export default {
  name: "ExportingButton",
  props: ["mode"],
  data() {
    return {};
  },
  methods: {
    take_screen(color, format) {
      this.emitter.emit("exportGraph", {
        params: { color, format },
        mode: this.mode,
      });
    },
  },
};
</script>
