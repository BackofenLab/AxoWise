<template>
  <Card class="w-[26rem] !rounded-none"
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
                <Tab class="!px-2.5 !py-1 rounded" :key="element.value" :value="element.value">
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
            :active_background="active_background" :terms="terms" :api="api" :mode="mode" :await_load="await_load" />
        </Tabs>
      </section>

      <section :class="`flex relative overflow-hidden transition duration-300 ease-in-out ${containerB.length > 0 ? 'flex-[1_1_50%]' : ''
        }`">
        <Tabs class="flex-1 w-full tab-active-grad" scrollable :value="active_tabB" @update:value="onchangeTabB">
          <TabList :class="`flex-shrink-0 ${dragged_to_container === 'paneContainer2' ? 'opacity-50' : ''}`">
            <draggable id="paneContainer2" class="min-h-[32px] w-full flex cursor-move" v-model="containerB"
              item-key="id" group="shared" :sort="true" :move="checkMove" @end="onDragEnd">
              <template #item="{ element }">
                <Tab class="!px-2.5 !py-1 rounded" :key="element.value" :value="element.value">
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
            :active_background="active_background" :terms="terms" :api="api" :mode="mode" :await_load="await_load" />
        </Tabs>
      </section>
    </template>
  </Card>
  <!-- <div id="vertical-pane">
    <div class="upper-block">
      <div class="tab-system">
        <ul>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab1 === 'set' }"
            v-on:click="active_function_tab1 = 'set'"
          >
            <a href="#">subsets</a>
          </li>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab1 === 'layers' }"
            v-on:click="active_function_tab1 = 'layers'"
          >
            <a href="#">path layers</a>
          </li>
          <li
            class="tab"
            v-if="dcoloumns"
            :class="{ tabSelected: active_function_tab1 === 'difexp' }"
            v-on:click="active_function_tab1 = 'difexp'"
          >
            <a href="#">dif exp</a>
          </li>
        </ul>
      </div>
      <PathwayMenu
        v-show="active_function_tab1 == 'set'"
        :gephi_data="gephi_data"
        :sorted="'top'"
        :mode="mode"
        :active_function="active_function_tab1"
        @active_term_changed="active_term = $event"
        @active_layer_changed="active_layer = $event"
      ></PathwayMenu>

      <PathwayLayers
        v-show="active_function_tab1 == 'layers'"
        :active_termlayers="active_termlayers"
        :gephi_data="gephi_data"
      ></PathwayLayers>

      <DifExpMenu
        v-show="active_function_tab1 == 'difexp'"
        :active_decoloumn="active_decoloumn"
        :gephi_data="gephi_data"
      ></DifExpMenu>
    </div>
    <div class="lower-block">
      <div class="tab-system">
        <ul>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'list' }"
            v-on:click="active_function_tab2 = 'list'"
          >
            <a href="#">pathways</a>
          </li>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'graph' }"
            v-on:click="active_function_tab2 = 'graph'"
          >
            <a href="#">enrichment</a>
          </li>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'heatmap' }"
            v-on:click="active_function_tab2 = 'heatmap'"
          >
            <a href="#">heatmap</a>
          </li>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'citation' }"
            v-on:click="active_function_tab2 = 'citation'"
          >
            <a href="#">citation</a>
          </li>
        </ul>
      </div>
      <PathwayMenu
        v-show="
          active_function_tab2 === 'list' ||
          active_function_tab2 === 'graph' ||
          active_function_tab2 === 'heatmap'
        "
        :sorted="'bottom'"
        :gephi_data="gephi_data"
        :active_function="active_function_tab2"
        @active_term_changed="active_term = $event"
        @active_layer_changed="active_layer = $event"
      ></PathwayMenu>
      <CitationMenu
        v-show="active_function_tab2 === 'citation'"
        :sorted="'bottom'"
        :active_function="active_function_tab2"
        :active_node="active_node"
        :active_background="active_background"
      ></CitationMenu>
    </div>
  </div> -->
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
  ],
  components: { draggable },
  data() {
    return {
      dcoloumns: this.$store.state.dcoloumns,
      // active_function_tab1: "set",
      // active_function_tab2: "list",
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
        { id: 1, name: "Pathways", value: "list" },
        { id: 2, name: "Enrichment", value: "graph" },
        { id: 3, name: "Heatmap", value: "heatmap" },
        { id: 4, name: "Citation", value: "citation" },
        { id: 5, name: "Subsets", value: "set" },
        { id: 6, name: "Path layers", value: "layers" },
        { id: 7, name: "Dif exp", value: "difexp" }
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
    // FIXME: Need condition according to mode?
    com.generatePathways(
      com.gephi_data.nodes[0].species,
      com.gephi_data.nodes.map((node) => node.attributes["Name"])
    );
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
    // abort_enrichment() {
    //   this.sourceToken.cancel("Request canceled");
    //   this.await_load = false;
    // },
    // dragElement(elmnt, val) {
    //   var pos1 = 0,
    //     pos2 = 0,
    //     pos3 = 0,
    //     pos4 = 0;
    //   if (document.getElementById(elmnt.id + "_header")) {
    //     // if present, the header is where you move the DIV from:
    //     document.getElementById(elmnt.id + "_header").onmousedown =
    //       dragMouseDown;
    //   } else {
    //     // otherwise, move the DIV from anywhere inside the DIV:
    //     elmnt.onmousedown = dragMouseDown;
    //   }

    //   function dragMouseDown(e) {
    //     e = e || window.event;
    //     e.preventDefault();
    //     // get the mouse cursor position at startup:
    //     pos3 = e.clientX;
    //     pos4 = e.clientY;
    //     document.onmouseup = closeDragElement;
    //     // call a function whenever the cursor moves:
    //     document.onmousemove = elementDrag;
    //   }

    //   function elementDrag(e) {
    //     if (!val) return;
    //     e = e || window.event;
    //     e.preventDefault();
    //     // calculate the new cursor position:
    //     pos1 = pos3 - e.clientX;
    //     pos2 = pos4 - e.clientY;
    //     pos3 = e.clientX;
    //     pos4 = e.clientY;
    //     // set the element's new position:
    //     elmnt.style.top = elmnt.offsetTop - pos2 + "px";
    //     elmnt.style.left = elmnt.offsetLeft - pos1 + "px";
    //   }

    //   function closeDragElement() {
    //     // stop moving when mouse button is released:
    //     document.onmouseup = null;
    //     document.onmousemove = null;
    //   }
    // },
    // resetElement(elmnt) {
    //   // set the element's new position:
    //   elmnt.style.top = null;
    //   elmnt.style.left = null;
    //   document.getElementById(elmnt.id + "_header").onmousedown = null;
    // },
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

<!-- <style>
#vertical-pane {
  left: 1%;
  top: 1.5%;
  height: 100%;
  width: 24vw;
  padding: 0.5rem;
  -webkit-backdrop-filter: blur(7.5px);
  border: 1px solid #e0e0e0;
  background-color: rgba(107, 107, 107, 0.5);
  box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.1);
  overflow: auto;
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  z-index: 9999;
  resize: horizontal;
}

.upper-block {
  height: 45%;
  top: 0%;
  position: relative;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
  border-style: solid;
  border-width: 1px;
  border-color: white;
  margin-top: 2%;
  overflow: hidden;
}

.lower-block {
  margin-top: 2%;
  height: 48%;
  position: relative;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
  border-style: solid;
  border-width: 1px;
  border-color: white;
}

ul {
  display: inline-block;
  width: 100%;
  list-style-type: none;
}

.tab-system a {
  font-size: 0.8vw;
  font-family: "ABeeZee", sans-serif;
  text-decoration: none;
  color: white;
}

.tab-system {
  flex-direction: column;
}

.tab {
  float: left;
  display: flex;
  height: 10%;
  padding: 0 3% 1% 3%;
  border-right: 0.1vw solid white;
  overflow: hidden;
}

.tab,
.tab a {
  transition: all 0.25s;
}

.tab a {
  display: inline-block;
}

.tab a:first-child {
  padding: 1%;
  white-space: nowrap;
}

.tab:hover {
  background: rgba(222, 222, 222, 0.71);
}

.tabSelected {
  position: relative;
}
.tabSelected:before {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 90%;
  transform: translateX(-50%);
  border-bottom: 0.15vw solid #e6eaf5;
}
</style> -->
