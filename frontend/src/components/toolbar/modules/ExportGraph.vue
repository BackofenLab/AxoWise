<template>
  <Button text plain severity="secondary" type="button" label="Export graph as .js" class="!justify-start !py-1"
    @click="export_graph" />
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
