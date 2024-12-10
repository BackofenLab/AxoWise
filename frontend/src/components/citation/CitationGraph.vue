<template>
  <EmptyState v-if="citation_graphs.size == 0" message="There is no generated citation graph.">
  </EmptyState>

  <section v-if="citation_graphs.size != 0" class="grid grid-cols-2 gap-2.5 pt-3">
    <Card v-for="(entry, index) in filt_graphs" :class="`group relative overflow-hidden border ${active_citation_id === entry.id
      ? 'border-primary-600 !bg-primary-600/25'
      : 'dark:!bg-slate-300/25 !bg-slate-300/10 border-transparent'
      }`" :key="index" :pt="{
        header: { class: 'h-26 relative rounded-md mt-[6px] mx-[6px] overflow-hidden' },
        body: { class: '!p-0 !gap-0' },
        footer: { class: 'flex gap-2 px-2 pb-2' },
        title: { class: 'relative' },
      }">
      <template #header>
        <SnapshotCitation :propValue="entry" :index="entry.id" />

        <div
          class="w-full h-full flex justify-between absolute top-0 left-0 p-1.5 bg-slate-800/50 opacity-0 duration-300 group-hover:opacity-100 z-[1]">
          <Button class="w-7 h-7" severity="secondary" rounded size="small" plain @click.stop="add_graph(entry)">
            <span :class="`material-symbols-rounded ${favourite_graphs.has(entry.id)
              ? 'text-base font-variation-ico-filled text-yellow-500 hover:text-yellow-400'
              : 'text-xl hover:text-yellow-600'
              }`">
              star
            </span>
          </Button>

          <Button class="w-7 h-7" severity="danger" rounded size="small" plain @click.stop="remove_graph(entry)">
            <span class="text-xl text-white material-symbols-rounded"> close </span>
          </Button>
        </div>
      </template>

      <template #title>
        <h6 :class="`w-full h-full absolute top-0 left-0 flex items-center gap-2 py-2 px-2 text-sm font-medium cursor-text z-[1]
          ${focus_citation_id === entry.id ? '!hidden' : ''}`" v-on:click="setFocus(entry.id, index)">
          <span class="line-clamp-1">{{ entry.label }}</span> <span
            class="flex-shrink-0 text-lg material-symbols-rounded dark:text-slate-200"> edit </span>
        </h6>
        <input ref="citationInputs" type="text" v-model="entry.label"
          :class="`w-full bg-transparent py-2 px-2 text-sm font-medium ${focus_citation_id === entry.id ? '' : 'opacity-0'}`"
          @click.stop @blur="clearFocus" />
      </template>

      <template #footer>
        <Button class="flex-1 h-8" severity="secondary" size="small" plain @click="switch_graph(entry)">
          View <span class="text-xl material-symbols-rounded"> arrow_circle_right </span>
        </Button>
      </template>
    </Card>
  </section>
</template>

<script>
import SnapshotCitation from "@/components/citation/SnapshotCitation.vue";
import EmptyState from "@/components/verticalpane/EmptyState.vue";
import { nextTick } from "vue";

export default {
  name: "CitationGraphs",
  props: ["citation_graphs", "favourite_graphs", "bookmark_off", "mode"],
  emits: ["favourite_graph_changed"],
  components: {
    SnapshotCitation,
    EmptyState
  },
  data() {
    return {
      focus_citation_id: null,
      active_citation_id: null
    };
  },
  methods: {
    setFocus(id, index) {
      this.focus_citation_id = id;
      nextTick(() => {
        // Focus the input if focus_citation_id matches the current id
        const input = this.$refs.citationInputs[index];
        if (input) {
          input.focus();
        }
      });
    },
    clearFocus() {
      this.focus_citation_id = null;
    },
    switch_graph(entry) {
      this.$store.commit("assign_citation_graph", {
        id: entry.id,
        graph: entry.graph,
      });
      this.$router.push("citation");
    },
    remove_graph(entry) {
      if (!this.favourite_graphs.has(entry.id)) {
        // Checkbox is checked, add its state to the object
        this.favourite_graphs.delete(entry.id);
      }
      this.citation_graphs.delete(entry);
      this.$store.commit("remove_snapshotCitation", entry.id);
      this.$store.commit("remove_citation_graph", entry);
      if (
        ![...this.citation_graphs].some(
          (e) => e.id == this.$store.state.citation_graph_data.id
        )
      ) {
        this.$store.commit("assign_citation_graph", null);
      }
    },
    add_graph(entry) {
      if (!this.favourite_graphs.has(entry.id)) {
        this.favourite_graphs.add(entry.id);
      } else {
        this.favourite_graphs.delete(entry.id);
      }
    },
  },
  computed: {
    filt_graphs() {
      var com = this;
      var filtered = [...com.citation_graphs];

      if (!com.bookmark_off) {
        filtered = filtered.filter(function (abstract) {
          return com.favourite_graphs.has(abstract.id);
        });
      }

      return new Set(filtered);
    },
  },
};
</script>