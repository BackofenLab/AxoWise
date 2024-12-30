<template>
  <div :class="`group/parent flex h-full relative animate__animated animate__faster z-[1]
      ${stacked === 'left' ? 'order-2' : 'order-4'}
      ${is_minimized ? 'w-0 animate__fadeOutDown' : 'animate__fadeInUp'}`">

    <div :class="`flex flex-col gap-2 absolute top-2 p-1 z-[1] opacity-0 duration-300 group-hover/parent:opacity-100
          ${stacked === 'left' ? 'left-full rounded-tr-lg rounded-br-lg' : 'right-full rounded-tl-lg rounded-bl-lg'}`">
      <Button class="w-5 h-5 !p-1.5" type="button" size="small" severity="warn" rounded
        v-tooltip.bottom="'Minimize pane'" @click="minimizePane">
        <span class="material-symbols-rounded !text-lg"> keep_off </span>
      </Button>
      <Button v-if="!is_minimized" class="w-5 h-5 !p-1.5" type="button" size="small" severity="success" rounded
        v-tooltip.bottom="'Stack pane right'" @click="changePanePosition">
        <span class="material-symbols-rounded !text-lg">
          {{ stacked === "left" ? "arrow_right_alt" : "arrow_left_alt" }}
        </span>
      </Button>
    </div>
    <Card class="w-[26rem] !rounded-none"
      :pt="{ body: { class: 'h-full !py-3 !px-0' }, content: { class: 'h-full flex flex-col gap-4' } }">
      <template #content>
        <section :class="`flex relative overflow-hidden transition duration-300 ease-in-out ${containerA.length > 0 ? 'flex-[1_1_47%]' : ''
          }`">
          <Tabs class="flex-1 w-full tab-active-grad" scrollable :value="active_tabA" @update:value="onchangeTabA">
            <TabList :class="`flex-shrink-0 ${dragged_to_container === 'paneContainer1' ? 'opacity-50' : ''}`"
              :pt="{ activeBar: 'tab-activebar-grad' }">
              <!-- <draggable id="paneContainer1" class="min-h-[32px] w-full flex cursor-move" v-model="containerA"
              item-key="id" group="shared" :sort="true" :move="checkMove" @end="onDragEnd"> -->
              <!-- <template #item="{ element }"> -->
              <Tab v-for="(element) in containerA" v-show="element.view?.includes(mode)" class="!px-2.5 !py-1 rounded"
                :key="element.value" :value="element.value">
                {{ element.name }}
              </Tab>
              <!-- </template> -->
              <!-- </draggable>  -->

              <!-- <h6 v-if="containerA.length === 0"
              class="w-full h-full absolute top-0 left-0 flex items-center justify-center border border-dashed border-slate-400 rounded dark:bg-[#0F182A] bg-white text-slate-400 text-sm text-center">
              Drag and drop tabs
            </h6> -->
            </TabList>
            <!-- @active_term_changed="active_term = $event" @active_layer_changed="active_layer = $event" -->
            <TabPanels class="h-[calc(100%-34px)] flex flex-col !p-0 !px-3 overflow-auto" v-if="containerA.length > 0">
              <TabPanel class="flex-1" value="list" v-if="mode === 'protein'">
                <PathwayList :gephi_data="gephi_data" :terms="terms" :await_load="await_load"
                  :favourite_pathways="favourite_pathways" @favourite_pathways_changed="favourite_pathways = $event"
                  @filtered_terms_changed="filtered_terms = $event"></PathwayList>
              </TabPanel>

              <TabPanel class="flex-1" value="graph" v-if="mode !== 'citation'">
                <PathwayTools :gephi_data="gephi_data" :filtered_terms="filtered_terms"
                  :favourite_pathways="favourite_pathways" :mode="mode">
                </PathwayTools>
              </TabPanel>

              <TabPanel class="flex-1" value="citation" v-if="mode === 'protein'">
                <CitationMenu :active_node="active_node" :active_background="active_background"></CitationMenu>
              </TabPanel>

              <TabPanel v-if="mode === 'term'" class="flex-1" value="tlist">
                <PathwayGraphList :term_data="gephi_data" :mode="mode"></PathwayGraphList>
              </TabPanel>

              <TabPanel v-if="mode === 'citation'" class="flex-1" value="clist">
                <CitationList :citation_data="gephi_data"></CitationList>
              </TabPanel>

              <TabPanel v-if="mode === 'citation'" class="flex-1" value="communities">
                <CitationCommunities :citation_data="gephi_data" :await_community="await_community">
                </CitationCommunities>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </section>

        <section :class="`flex relative overflow-hidden transition duration-300 ease-in-out ${containerB.length > 0 ? 'flex-[1_1_53%]' : ''
          }`">
          <Tabs class="flex-1 w-full tab-active-grad" scrollable :value="active_tabB" @update:value="onchangeTabB">
            <TabList :class="`flex-shrink-0 ${dragged_to_container === 'paneContainer2' ? 'opacity-50' : ''}`">
              <!-- <draggable id="paneContainer2" class="min-h-[32px] w-full flex cursor-move" v-model="containerB"
              item-key="id" group="shared" :sort="true" :move="checkMove" @end="onDragEnd"> -->
              <!-- <template #item="{ element }"> -->
              <Tab v-for="(element) in containerB" v-show="element.view?.includes(mode)" class="!px-2.5 !py-1 rounded"
                :key="element.value" :value="element.value">
                {{ element.name }}
              </Tab>
              <!-- </template> -->
              <!-- </draggable> -->

              <!-- <h6 v-if="containerB.length === 0"
              class="w-full h-full absolute top-0 left-0 flex items-center justify-center border border-dashed border-slate-400 rounded dark:bg-[#0F182A] bg-white text-slate-400 text-sm text-center">
              Drag and drop tabs
            </h6> -->
            </TabList>
            <!-- @active_term_changed="active_term = $event" @active_layer_changed="active_layer = $event" -->

            <TabPanels class="h-[calc(100%-34px)] flex flex-col !p-0 !px-3 overflow-auto" v-if="containerB.length > 0">
              <TabPanel class="flex-1" value="set">
                <PathwaySet :gephi_data="gephi_data" :api="api" :mode="mode"></PathwaySet>
              </TabPanel>

              <TabPanel class="flex-1" value="layers" v-if="mode === 'protein'">
                <PathwayLayers :active_termlayers="active_termlayers" :gephi_data="gephi_data" />
              </TabPanel>

              <TabPanel class="flex-1" value="heatmap" v-if="mode === 'protein'">
                <HeatmapTool :mode="mode" :gephi_data="gephi_data" :filtered_terms="filtered_terms"
                  :favourite_pathways="favourite_pathways">
                </HeatmapTool>
              </TabPanel>

              <TabPanel class="flex-1" value="difexp" v-if="dcoloumns && mode === 'protein'">
                <DifExpMenu :active_decoloumn="active_decoloumn" :gephi_data="gephi_data" />
              </TabPanel>

              <TabPanel v-if="mode === 'citation'" class="flex-1" value="summary">
                <CitationSummary :citation_data="gephi_data" :node_index="node_index" :await_community="await_community"
                  @await_community_changed="await_community = $event">
                </CitationSummary>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </section>
      </template>
    </Card>
  </div>
  <Button v-show="is_minimized" type="button" severity="contrast" rounded
    :class="`!absolute z-[9] bottom-9 left-20 !border-2 !border-primary-500`" @click="minimizePane">
    <span class="material-symbols-rounded"> tv_options_input_settings </span>
    Customization
  </Button>
</template>

<script>
// import draggable from "vuedraggable";
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
  components: {
    // draggable,
  },
  data() {
    return {
      favourite_pathways: [],
      filtered_terms: [],
      await_community: false,
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
        { id: 4, name: "Enrichment graph", value: "graph", view: ['protein', 'term'] },
        { id: 5, name: "Citation graph", value: "citation", view: ['protein'] },
        { id: 2, name: "List", value: "tlist", view: ['term'] },
        { id: 3, name: "List", value: "clist", view: ['citation'] },
        { id: 10, name: "Communities", value: "communities", view: ['citation'] },
      ],
      containerB: [
        { id: 6, name: "Subsets", value: "set", view: ['protein', 'term', 'citation'] },
        { id: 7, name: "Path layers", value: "layers", view: ['protein'] },
        { id: 8, name: "Heatmap", value: "heatmap", view: ['protein'] },
        { id: 9, name: "Diff exp", value: "difexp", view: ['protein'] },
        { id: 11, name: "Summary", value: "summary", view: ['citation'] },
      ],
      is_minimized: false,
      stacked: "left",
      initial_drag_btn_position: { top: window.innerHeight - 80, left: 100 },
    };
  },
  watch: {
    dcoloumns() {
      // FIXME: remove diffexp tab based on dcoloumns()
    },
    favourite_pathways: {
      handler(newList) {
        this.emitter.emit("updateFavouriteList", newList);
      },
      deep: true,
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
    minimizePane(e) {
      e.stopPropagation();
      this.is_minimized = !this.is_minimized;
    },
    changePanePosition() {
      this.stacked = this.stacked === "left" ? "right" : "left";
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