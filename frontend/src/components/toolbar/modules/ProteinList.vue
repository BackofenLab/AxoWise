<template>
  <h6 class="mb-2 text-sm text-slate-300">
    To find multiple nodes separate each node in a new line.
  </h6>
  <Textarea v-model="raw_text" rows="4" fluid autofocus placeholder="Search by gene..." class="text-center"/>
  <Button label="Apply & Create subset" severity="secondary" size="small" fluid type="button" class="mt-2.5 !rounded-lg"
    @click="highlight(raw_text)">
  </Button>
</template>

<script>
import { useToast } from "primevue/usetoast";
export default {
  name: "ProteinList",
  props: ["gephi_data", "mode"],
  data() {
    return {
      raw_text: "",
    };
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    highlight(proteins) {
      var com = this;
      const protein_names = new Set(proteins.toUpperCase().split("\n"));
      const subset = [];
      com.gephi_data.nodes.forEach((node) => {
        if (protein_names.has(node.attributes["Name"].toUpperCase())) {
          subset.push(node);
        }
      });
      com.emitter.emit("searchSubset", { subset: subset, mode: this.mode });
      com.save_subset(subset);
    },
    save_subset(subset) {
      var com = this;
      let genes = subset;
      let count = new Set(com.$store.state.favourite_subsets)?.size || 0;

      if (!genes) return;

      this.$store.commit("assign_subset", {
        name: `subset ${count}`,
        genes: genes,
        terms: null,
        view: com.mode,
        abstracts: null,
        status: false,
        information: false,
        actions: false,
        stats: null,
      });
      this.toast.add({ severity: 'success', detail: 'Subset created successfully.', life: 4000 });
    },
  },
};
</script>