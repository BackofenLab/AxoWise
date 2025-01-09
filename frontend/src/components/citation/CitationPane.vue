<template>
  <Dialog :visible="!!active_node" position="topright" :minY="60" :minX="60" :pt="{
    root: { class: 'w-[25rem] !mt-[60px] !ml-[60px]' },
    header: { class: '!py-2.5' },
    title: { class: '!text-base' },
    content: { class: '!max-h-[24rem]' },
  }" :closable="false" @hide="close_pane()">
    <template #header>
      <h3 class="flex items-center gap-2 cursor-pointer hover:text-primary-500"
        v-on:click="google_search(active_node.id)">
        PMID: {{ active_node.id }}
        <span class="text-sm material-symbols-rounded"> open_in_new </span>
      </h3>

      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-8 h-8" size="small" text rounded plain v-tooltip.bottom="'Add to summary'"
          @click="add_abstract(active_node.id)">
          <span class="material-symbols-rounded"> note_add </span>
        </Button>
        <Button class="w-8 h-8 group" icon="material-symbols-rounded" size="small" text plain rounded
          v-tooltip.bottom="'Add to AxoBot'" @click="call_chatbot('citation')">
          <span class="material-symbols-rounded">forum</span>
        </Button>
        <Button class="w-8 h-8" size="small" text rounded plain @click="close_pane()">
          <span class="dark:text-white material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>

    <h5 class="mb-4">
      {{ active_node.attributes["Title"] }}
    </h5>

    <div class="flex justify-between gap-2 mb-3 bg-[var(--card-bg)] z-[2]">
      <span class="flex flex-col items-center">
        {{ active_node.attributes["Year"] }}
        <strong class="text-sm font-normal text-primary-400">Year</strong>
      </span>
      <span class="flex flex-col items-center">
        {{ active_node.attributes["Citation"] }}
        <strong class="text-sm font-normal text-primary-400">Citations</strong>
      </span>
      <span class="flex flex-col items-center">
        {{ active_node.attributes["Degree"] }}
        <strong class="text-sm font-normal text-primary-400">Deg</strong>
      </span>
      <span class="flex flex-col items-center">
        {{ Math.abs(Math.log10(active_node.attributes["PageRank"])).toFixed(2) }}
        <strong class="text-sm font-normal text-primary-400">PR</strong>
      </span>
    </div>

    <Divider />

    <Tabs :value="active_function" @update:value="onChangeTab">
      <div class="h-[10rem] overflow-auto overflow-x-visible">
        <TabPanels class="!p-0 !h-full">
          <TabPanel value="abstract">
            <p class="m-0 whitespace-pre-wrap">
              {{ active_node.attributes["Abstract"] }}
            </p>
          </TabPanel>
          <TabPanel value="summary" class="!h-full">
            <div v-if="await_load" class="flex flex-col items-center justify-center h-full gap-3">
              <h6 class="flex items-center gap-2 dark:text-slate-300">Fetching summary
                <span class="relative flex">
                  <span
                    class="absolute inline-flex w-full h-full rounded-full opacity-75 animate-ping bg-primary-500"></span>
                  <span
                    class="material-symbols-rounded text-primary-500 animate animate-[spin_1s_ease-in-out_infinite]">scatter_plot</span>
                </span>
              </h6>
            </div>
            <p class="m-0 whitespace-pre-wrap" v-if="!await_load">
              {{ summary_dict[active_node.id] }}
            </p>
          </TabPanel>
        </TabPanels>
      </div>

      <footer class="flex items-end !border-t !border-slate-600 pt-2">
        <TabList class="" :pt="{
          tabList: { class: '!border-0 !gap-4' },
          activeBar: { class: '!hidden' }
        }">
          <Tab value="abstract" class="!p-0 !border-0 !flex !items-center !gap-2"><span
              :class="`material-symbols-rounded !text-xl ${active_function == 'abstract' ? 'font-variation-ico-filled' : ''}`">summarize</span>Abstract
          </Tab>
          <Tab value="summary" class="!p-0 !border-0 !flex !items-center !gap-2"><span
              :class="`material-symbols-rounded !text-xl ${active_function == 'summary' ? 'font-variation-ico-filled' : ''}`">description
            </span>Summary
          </Tab>
        </TabList>
      </footer>
    </Tabs>
  </Dialog>
</template>

<script>
import { useToast } from "primevue/usetoast";
export default {
  name: "CitationPane",
  props: ["active_node", "active_subset"],
  emits: ["active_node_changed", "active_subset_changed"],
  data() {
    return {
      active_function: "abstract",
      summary_dict: {},
      api: {
        summary: "api/subgraph/summary",
      },
      await_load: false,
    };
  },
  watch: {
    active_node() {
      this.active_function = "abstract";
      if (this.active_node == null) {
        this.$emit("active_subset_changed", null);
      }
    },
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    google_search(id) {
      window.open(`http://www.ncbi.nlm.nih.gov/pubmed/${id}`, "_blank");
    },
    add_abstract(id) {
      this.emitter.emit("addNodeToSummary", id);
      this.toast.add({ severity: 'success', detail: 'Node added to summary.', life: 4000 });
    },
    close_pane() {
      this.$emit("active_node_changed", null);
      this.$emit("active_subset_changed", null);
    },
    onChangeTab(tab) {
      var com = this;
      com.active_function = tab;
      if (tab == 'summary' && this.active_node) {
        var finalList = [];
        var nodeDict = {};
        if (!com.summary_dict[this.active_node.id]) {
          com.await_load = true;
          var formData = new FormData();
          nodeDict[this.active_node.id] = this.active_node;
          finalList.push(nodeDict);
          formData.append("abstracts", JSON.stringify(finalList));

          //POST request for generating pathways
          com.axios.post(com.api.summary, formData).then((response) => {
            com.summary_dict[this.active_node.id] = response.data;
            com.await_load = false;
          });
        }
      }
    },
    call_chatbot(mode) {
      this.emitter.emit("addToChatbot", {
        id: this.active_node.attributes["Name"],
        mode: mode,
        type: "protein",
        data: this.active_node,
      });
    },
  },
};
</script>
