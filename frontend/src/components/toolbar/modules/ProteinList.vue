<template>
  <h6 class="mb-2 text-sm text-slate-300">
    To find multiple nodes separate each node with comma (<span class="leading-[0] text-primary-400 text-4xl">,</span>)
  </h6>
  <Textarea v-model="raw_text" rows="4" fluid autofocus placeholder="Search by gene..." />
  <Button label="Apply" severity="secondary" size="small" fluid type="button" class="mt-2.5 !rounded-lg"
    @click="highlight(raw_text)">
  </Button>
</template>

<script>
export default {
  name: "ProteinList",
  props: ["gephi_data", "mode"],
  data() {
    return {
      raw_text: "",
    };
  },
  methods: {
    highlight(proteins) {
      var com = this;
      // This regex is not user friendly instead use ','
      // const protein_names = new Set(proteins.toUpperCase().split("\n"));
      const protein_names = new Set(proteins.toUpperCase().split(",").map(item => item.trim()));
      const subset = [];
      com.gephi_data.nodes.forEach((node) => {
        if (protein_names.has(node.attributes["Name"].toUpperCase())) {
          subset.push(node);
        }
      });

      com.emitter.emit("searchSubset", { subset: subset, mode: this.mode });
    },
  },
};
</script>