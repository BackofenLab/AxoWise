<template>
  <Button severity="secondary" type="button" label="Export graph as .js" icon="pi pi-download" iconPos="right"
  class="!w-full !justify-between !rounded-lg" @click="export_graph" />
</template>

<script>
export default {
  name: "ExportGraph",
  data() {
    return {};
  },
  methods: {
    export_graph() {
      var com = this;

      let dataStr = JSON.stringify(com.$store.state.gephi_json.data);
      let dataUri =
        "data:application/json;charset=utf-8," + encodeURIComponent(dataStr);

      let exportFileDefaultName = "data.json";

      let linkElement = document.createElement("a");
      linkElement.setAttribute("href", dataUri);
      linkElement.setAttribute("download", exportFileDefaultName);
      linkElement.click();
    },
  },
};
</script>
