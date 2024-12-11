<template>
  <Card class="w-[26rem] !rounded-none order-2"
    :pt="{ body: { class: 'h-full !py-3 !px-0' }, content: { class: 'h-full flex flex-col gap-4' } }">
    <template #content>
      <section :class="`flex relative overflow-hidden transition duration-300 ease-in-out ${containerA.length > 0 ? 'flex-[1_1_50%]' : ''
        }`">
        <Tabs class="flex-1 w-full tab-active-grad" scrollable :value="active_tabA" @update:value="onchangeTabA">
          <TabList :class="`flex-shrink-0 ${dragged_to_container === 'paneContainer1' ? 'opacity-50' : ''}`"
            :pt="{ activeBar: 'tab-activebar-grad' }">
            <draggable id="paneContainer1" class="min-h-[32px] w-full flex cursor-move" v-model="containerA"
              item-key="id" group="shared" :sort="true" :move="checkMove" @end="onDragEnd">
              <template #item="{ element }">
                <Tab v-show="element.view?.includes(mode)" class="!px-2.5 !py-1 rounded" :key="element.value"
                  :value="element.value">
                  {{ element.name }}
                </Tab>
              </template>
            </draggable>

            <h6 v-if="containerA.length === 0"
              class="w-full h-full absolute top-0 left-0 flex items-center justify-center border border-dashed border-slate-400 rounded dark:bg-[#0F182A] bg-white text-slate-400 text-sm text-center">
              Drag and drop tabs
            </h6>
          </TabList>
          <!-- @active_term_changed="active_term = $event" @active_layer_changed="active_layer = $event" -->
          <TabPanelOption v-if="containerA.length > 0" v-model="active_tabA" :gephi_data="gephi_data"
            :active_decoloumn="active_decoloumn" :active_node="active_node" :active_termlayers="active_termlayers"
            :active_background="active_background" :terms="terms" :api="api" :mode="mode" :await_load="await_load"
            :node_index="node_index" />
        </Tabs>
      </section>

      <section :class="`flex relative overflow-hidden transition duration-300 ease-in-out ${containerB.length > 0 ? 'flex-[1_1_50%]' : ''
        }`">
        <Tabs class="flex-1 w-full tab-active-grad" scrollable :value="active_tabB" @update:value="onchangeTabB">
          <TabList :class="`flex-shrink-0 ${dragged_to_container === 'paneContainer2' ? 'opacity-50' : ''}`">
            <draggable id="paneContainer2" class="min-h-[32px] w-full flex cursor-move" v-model="containerB"
              item-key="id" group="shared" :sort="true" :move="checkMove" @end="onDragEnd">
              <template #item="{ element }">
                <Tab v-show="element.view?.includes(mode)" class="!px-2.5 !py-1 rounded" :key="element.value"
                  :value="element.value">
                  {{ element.name }}
                </Tab>
              </template>
            </draggable>

            <h6 v-if="containerB.length === 0"
              class="w-full h-full absolute top-0 left-0 flex items-center justify-center border border-dashed border-slate-400 rounded dark:bg-[#0F182A] bg-white text-slate-400 text-sm text-center">
              Drag and drop tabs
            </h6>
          </TabList>
          <!-- @active_term_changed="active_term = $event" @active_layer_changed="active_layer = $event" -->
          <TabPanelOption v-if="containerB.length > 0" v-model="active_tabB" :gephi_data="gephi_data"
            :active_decoloumn="active_decoloumn" :active_node="active_node" :active_termlayers="active_termlayers"
            :active_background="active_background" :terms="terms" :api="api" :mode="mode" :await_load="await_load"
            :node_index="node_index" />
        </Tabs>
      </section>
    </template>
  </Card>
</template>

<script>
import draggable from "vuedraggable";

export default {
  name: "VerticalPane",
  props: [
    "mode",
    "gephi_data",
    "active_node",
    "active_background",
    "active_termlayers",
    "active_decoloumn",
    "node_index"
  ],
  components: { draggable },
  data() {
    return {
      dcoloumns: this.$store.state.dcoloumns,
      api: {
        subgraph: "api/subgraph/enrichment",
      },
      terms: null,
      terms_list: [],
      await_load: false,
      dragged_to_container: "",
      active_tabA: 'list',
      active_tabB: 'set',
      containerA: [
        { id: 1, name: "Pathways", value: "list", view: ['protein'] },
        { id: 2, name: "List", value: "tlist", view: ['term'] },
        { id: 3, name: "List", value: "clist", view: ['citation'] },
        { id: 4, name: "Enrichment graph", value: "graph", view: ['protein', 'term'] },
        { id: 5, name: "Citation graph", value: "citation", view: ['protein'] },
        { id: 6, name: "Subsets", value: "set", view: ['protein', 'term', 'citation'] },
        { id: 7, name: "Path layers", value: "layers", view: ['protein'] },
        { id: 8, name: "Heatmap", value: "heatmap", view: ['protein'] },
        { id: 9, name: "Diff exp", value: "difexp", view: ['protein'] },
        { id: 10, name: "Communities", value: "communities", view: ['citation'] },
        { id: 11, name: "Summary", value: "summary", view: ['citation'] },
      ],
      containerB: [
      ],
    };
  },
  watch: {
    dcoloumns() {
      // FIXME: remove diffexp based on dcoloumns()
    },
  },
  mounted() {
    var com = this;
    if (com.mode == "protein") {
      com.generatePathways(
        com.gephi_data.nodes[0].species,
        com.gephi_data.nodes.map((node) => node.attributes["Name"])
      );
    }
    // Change active tab based on view
    if (com.mode == "term") {
      com.active_tabA = 'tlist';
    }
    if (com.mode == "citation") {
      com.active_tabA = 'clist';
    }
  },
  methods: {
    onchangeTabA(val) {
      this.active_tabA = val
    },
    onchangeTabB(val) {
      this.active_tab = val
    },
    setActiveTab(container, newIndex = 0) {
      var com = this;
      const items = container === "paneContainer1" ? com.containerA : com.containerB;

      switch (container) {
        case "paneContainer1":
          com.active_tabA = items[newIndex].value;
          break;
        case "paneContainer2":
          com.active_tabB = items[newIndex].value;
          break;

        default:
          break;
      }
    },
    onDragEnd(event) {
      var com = this;
      const { from, to } = event;
      const items = from.id === "paneContainer1" ? com.containerA : com.containerB;
      const active = from.id === "paneContainer1" ? com.active_tabA : com.active_tabB;

      com.dragged_to_container = "";

      // ### This works only if from and to container is different
      if (from.id !== to.id) {
        if (items.some((item) => item.value !== active)) com.setActiveTab(from.id); // ### Sets first item from the dragged container as active

        com.setActiveTab(to.id, event.newIndex); // ### Sets Dragged item as active in new container
      }

      if (from.id === "paneContainer1" && com.containerA.length === 0) {
        com.active_tabA = "";
      } else if (from.id === "paneContainer2" && com.containerB.length === 0) {
        com.active_tabB = "";
      }
    },
    checkMove(evt) {
      const { from, to } = evt;
      this.dragged_to_container = from.id === to.id ? "" : to.id;
    },
    generatePathways(species, genes) {
      var com = this;

      //Adding proteins and species to formdata
      var formData = new FormData();
      formData.append("genes", genes);
      formData.append("species_id", species);
      formData.append(
        "mapping",
        JSON.stringify(com.gephi_data.settings["gene_alias_mapping"])
      );

      this.await_load = true;

      //POST request for generating pathways
      com.sourceToken = this.axios.CancelToken.source();
      com.axios
        .post(com.api.subgraph, formData, {
          cancelToken: com.sourceToken.token,
        })
        .then((response) => {
          com.terms = response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate);
          if (com.terms_list.length == 0)
            this.$store.commit("assign_current_enrichment_terms", com.terms);
          com.terms_list.push(com.terms);
          com.await_load = false;
        });
    },
  },
  created() {
    this.emitter.on("enrichTerms", (terms) => {
      if (terms != null) this.terms = terms;
      else this.terms = this.terms_list[0];
      this.$store.commit("assign_current_enrichment_terms", this.terms);
    });
  },
};
</script>