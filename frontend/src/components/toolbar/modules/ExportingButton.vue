<template>
    <div>
      <div class="tool-item">
        <span v-on:click="open_export()">Export proteins as .csv</span>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ExportingButton",
    props: ["mode"],
    data() {
      return {
      };
    },
    methods: {
        open_export() {
        this.emitter.emit("openExportScreen", this.mode);
      },
    },
  };
  </script>
  
  <style scoped>
  </style>
  