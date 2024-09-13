<template>
  <div
    id="menu-tools"
    :class="{
      'pathwaybar-small': pane_hidden === true,
      pathways: pane_hidden === false,
    }"
  >
    <div class="pathwaybar">
      <PathwayList
        v-if="sorted == 'bottom'"
        v-show="active_function === 'list'"
        :gephi_data="gephi_data"
        :terms="terms"
        :await_load="await_load"
        :favourite_pathways="favourite_pathways"
        @favourite_pathways_changed="favourite_pathways = $event"
        @filtered_terms_changed="filtered_terms = $event"
      ></PathwayList>
      <PathwaySet
        v-if="active_function === 'set'"
        :gephi_data="gephi_data"
        :api="api"
        :mode="mode"
      ></PathwaySet>
      <PathwayTools
        v-if="active_function === 'graph'"
        :gephi_data="gephi_data"
        :filtered_terms="filtered_terms"
        :favourite_pathways="favourite_pathways"
      ></PathwayTools>
      <HeatmapTool
        v-if="active_function === 'heatmap'"
        :gephi_data="gephi_data"
        :filtered_terms="filtered_terms"
        :favourite_pathways="favourite_pathways"
      ></HeatmapTool>
    </div>
  </div>
</template>

<script>
import PathwayList from "@/components/enrichment/PathwayList.vue";
import PathwayTools from "@/components/enrichment/PathwayTools.vue";
import HeatmapTool from "@/components/enrichment/HeatmapTool.vue";
import PathwaySet from "@/components/enrichment/PathwaySet.vue";

export default {
  name: "PathwayMenu",
  props: ["gephi_data", "active_term", "active_function", "sorted", "mode"],
  components: {
    PathwayList,
    PathwayTools,
    PathwaySet,
    HeatmapTool,
  },
  data() {
    return {
      api: {
        subgraph: "api/subgraph/enrichment",
      },
      terms: null,
      terms_list: [],
      pane_hidden: false,
      await_load: false,
      favourite_pathways: [],
      filtered_terms: [],
    };
  },
  watch: {
    favourite_pathways: {
      handler(newList) {
        this.emitter.emit("updateFavouriteList", newList);
      },
      deep: true,
    },
    pane_hidden(val) {
      if (val) this.dragElement(document.getElementById("menu-tools"), val);
      else {
        this.resetElement(document.getElementById("menu-tools"));
      }
    },
  },
  mounted() {
    var com = this;
    if (com.sorted == "bottom")
      com.generatePathways(
        com.gephi_data.nodes[0].species,
        com.gephi_data.nodes.map((node) => node.attributes["Name"])
      );
  },
  methods: {
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
    abort_enrichment() {
      this.sourceToken.cancel("Request canceled");
      this.await_load = false;
    },
    dragElement(elmnt, val) {
      var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
      if (document.getElementById(elmnt.id + "_header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "_header").onmousedown =
          dragMouseDown;
      } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
      }

      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }

      function elementDrag(e) {
        if (!val) return;
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = elmnt.offsetTop - pos2 + "px";
        elmnt.style.left = elmnt.offsetLeft - pos1 + "px";
      }

      function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
      }
    },
    resetElement(elmnt) {
      // set the element's new position:
      elmnt.style.top = null;
      elmnt.style.left = null;
      document.getElementById(elmnt.id + "_header").onmousedown = null;
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

<style>
.pathways {
  z-index: 999;
  width: 100%;
  height: 100%;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
}
#menu-tools_header {
  width: 100%;
  height: 9.41%;
  position: absolute;
  flex-shrink: 0;
  border-radius: 5px 5px 0px 0px;
  backdrop-filter: blur(7.5px);
  background: #d9d9d9;
  transition: transform 330ms ease-in-out;
}

#menu-tools_header img {
  position: absolute;
  top: 35%;
  right: 0.7vw;
  width: 0.7vw;
  height: 0.7vw;
  flex-shrink: 0;
  transition: transform 330ms ease-in-out;
}
.pathwaybar {
  width: 100%;
  height: 100%;
  flex-shrink: 0;
}
.pathwaybar-small {
  z-index: 999;
  position: absolute;
  width: 32.83%;
  height: 27.2%;
  top: 70.7%;
  left: 3.515%;
  transition: transform 330ms ease-in-out;
}
.pathwaybar #pathway-bg {
  width: 20%;
  height: 100%;
  margin-left: 30.87%;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
</style>
