<template>
  <h6 class="mb-2 text-sm text-slate-300">
    To find multiple nodes separate each node with comma (<span class="leading-[0] text-primary-400 text-4xl">,</span>)
  </h6>
  <Textarea v-model="raw_text" rows="4" fluid autofocus placeholder="Search by gene..." />
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
      // This regex is not user friendly instead use ','
      // const protein_names = new Set(proteins.toUpperCase().split("\n"));
      const protein_names = new Set(proteins.toUpperCase().split(",").map(item => item.trim()));
      const subset = [];
      com.gephi_data.nodes.forEach((node) => {
        if (protein_names.has(node.attributes["Name"].toUpperCase())) {
          subset.push(node);
        }
      });
      com.save_subset();
      com.emitter.emit("searchSubset", { subset: subset, mode: this.mode });
    },
    save_subset() {
      var com = this;
      let genes;
      let count = new Set(com.$store.state.favourite_subsets)?.size || 0;
      if (com.mode == "protein") {
        genes = com.$store.state.active_subset;
      } else if (com.mode == "term") {
        genes = com.$store.state.p_active_subset;
      } else {
        genes = com.$store.state.c_active_subset;
      }

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