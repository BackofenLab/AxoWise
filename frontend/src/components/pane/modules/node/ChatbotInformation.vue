<template>
  <p class="text-sm">
    {{ protein_information }}
  </p>
</template>

<script>
export default {
  name: "ChatbotInformation",
  props: ["active_node"],
  data() {
    return {
      protein_information: "",
    };
  },
  watch: {
    active_node() {
      if (this.active_node == null) return;
      this.protein_information = this.active_node.attributes["Description"];
    },
  },
};
</script>
