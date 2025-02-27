<template>
  <div v-show="active_term !== null">
    <header v-if="active_term !== null" class="flex flex-wrap items-center gap-2">
      <span class="flex items-center gap-1 text-sm font-medium">
        <span v-on:click.stop="bookmark_pathway()" :class="`text-xl material-symbols-rounded text-slate-600 cursor-pointer 
          ${favourite_pathways?.has(active_term)
            ? 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400'
            : 'hover:text-yellow-600'
          }`">
          star
        </span>
        <strong class="font-normal">{{ active_term.clean }}</strong>
      </span>
      <Button class="w-5 h-5 ml-auto" size="small" text plain rounded @click="to_term()">
        <span class="dark:text-white material-symbols-rounded !text-lg">
          open_in_new
        </span>
      </Button>
    </header>

    <Tabs v-model:value="active_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="informations">
            <h3 class="mb-1 text-sm font-medium">
              Informations
            </h3>
            <PathwayStatistics :active_term="active_term"></PathwayStatistics>
          </TabPanel>
          <TabPanel value="statistics" v-if="active_term !== null">
            <h3 class="mb-1 text-sm font-medium">
              Parameter Selection
            </h3>
            <PathwayLinks :active_term="active_term" :mode="mode"></PathwayLinks>
          </TabPanel>
          <TabPanel value="connections">
            <div class="flex items-center justify-between mb-1">
              <h3 class="text-sm font-medium">
                Connections
              </h3>
              <Button class="w-5 h-5" size="small" text plain rounded @click="copyclipboard()">
                <span class="dark:text-white material-symbols-rounded !text-lg"> content_copy </span>
              </Button>
            </div>
            <PathwayConnections :active_term="active_term" :gephi_data="gephi_data"></PathwayConnections>
          </TabPanel>
        </TabPanels>
      </div>

      <footer class="flex items-end !mt-2 !border-t !border-slate-600 py-2">
        <TabList class="" :pt="{
          tabList: { class: '!border-0 !gap-4' },
          activeBar: { class: '!hidden' }
        }">
          <Tab value="informations" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'informations' ? 'font-variation-ico-filled' : ''}`">info</span>
          </Tab>
          <Tab value="statistics" class="!p-0 !border-0" v-if="active_term !== null"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'statistics' ? 'font-variation-ico-filled' : ''}`">tune</span>
          </Tab>
          <Tab value="connections" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-base ${active_section == 'connections' ? 'font-variation-ico-filled' : ''}`">hub</span>
          </Tab>
        </TabList>

        <div class="ml-auto">
          <Button class="w-5 h-5 !mr-1" size="small" text rounded plain @click="expand_collapse_tab()">
            <span :class="`dark:text-white material-symbols-rounded !text-lg`">{{ active_section ? 'expand_circle_up' :
              'expand_circle_down' }}</span>
          </Button>
          <Button class="w-5 h-5" size="small" text rounded plain @click="call_chatbot(mode)">
            <span class="dark:text-white material-symbols-rounded !text-lg">forum</span>
          </Button>
        </div>
      </footer>
    </Tabs>
  </div>
</template>

<script>
import PathwayStatistics from "@/components/pane/modules/pathways/PathwayStatistics.vue";
import PathwayConnections from "@/components/pane/modules/pathways/PathwayConnections.vue";
import PathwayLinks from "@/components/pane/modules/pathways/PathwayLinks.vue";
import { useToast } from "primevue/usetoast";

export default {
  name: "TermPane",
  props: ["active_term", "gephi_data", "mode"],
  emits: [
    "active_item_changed",
    "highlight_subset_changed",
  ],
  components: {
    PathwayStatistics,
    PathwayConnections,
    PathwayLinks,
  },
  data() {
    return {
      active_section: "",
      hide: false,
      term_history: [],
      expand_stats: false,
      expand_proteins: false,
      term_item: {
        value: null,
      },
      favourite_pathways: new Set(),
    };
  },
  watch: {
    active_term() {
      var com = this;
      if (com.active_term == null) {
        return;
      }

      com.term_item.value = com.active_term;
      com.$emit("active_item_changed", { Pathway: com.term_item });
    },
  },
  methods: {
    copyclipboard() {
      this.emitter.emit("copyConnections");
      this.toast.add({ severity: 'success', detail: 'Message copied to clipboard.', life: 4000 });
    },
    expand_collapse_tab() {
      if (this.active_section) {
        this.active_section = null;
      } else {
        this.active_section = 'informations'
      }
    },
    to_term() {
      var com = this;
      if (!com.$store.state.term_graph_data) {
        this.toast.add({ severity: 'error', detail: 'There is no term graph.', life: 4000 });
        return;
      }

      this.$store.commit("assign_active_enrichment_node", com.active_term);
      this.$router.push("term");
    },
    select_node(value) {
      this.emitter.emit("searchNode", { node: value, mode: this.mode });
    },
    bookmark_pathway() {
      this.emitter.emit("bookmarkPathway", this.active_term);
      this.favourite_pathways = this.$store.state.favourite_enrichments;
    },
    show_layer() {
      var com = this;

      var subset_check = !this.hide ? com.active_term.symbols : null;
      this.emitter.emit("hideSubset", {
        subset: subset_check,
        mode: this.mode,
      });
      com.hide = !com.hide;
    },
    call_chatbot(mode) {
      this.emitter.emit("addToChatbot", {
        id: this.active_term.id,
        mode: mode,
        type: "term",
        data: this.active_term,
      });
    },
  },
  mounted() {
    this.toast = useToast();
    this.emitter.on("updateFavouriteList", (value) => {
      this.favourite_pathways = value;
    });
  },
};
</script>