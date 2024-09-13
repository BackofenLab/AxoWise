<template>
  <div class="text" v-show="active_term !== null">
    <div class="path_attribute" v-if="active_term !== null">
      <div class="favourite-pane-symbol">
        <label class="custom-checkbox">
          <div
            class="checkbox-image"
            v-on:click="bookmark_pathway()"
            :class="{ checked: favourite_pathways.has(active_term) }"
          ></div>
        </label>
      </div>
      <div class="term">{{ active_term.clean }}</div>
      <div class="colorbar-img" v-on:click="to_term()">
        <img src="@/assets/pane/follow.png" />
      </div>
    </div>

    <!-- <div class="nodeattributes">
            <div id="network" class="subsection">
                <div class="subsection-header">
                    <span>pathway statistics</span>
                </div>
                <div class="subsection-main colortype">

                </div>
            </div>
            <div id="pathway-connections" class="subsection">
                <div class="subsection-header">
                    <span>connections</span>
                    <div id='vis-button'>
                        <img src="@/assets/pane/invisible.png" v-if="!hide" v-on:click="show_layer()">
                        <img src="@/assets/pane/visible.png" v-if="hide" v-on:click="show_layer()">
                        <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()">
                    </div>
                </div>
                <div class="subsection-main colortype">

                </div>
            </div>
        </div> -->

    <div
      :class="{
        'tool-section': !tool_active,
        'tool-section-active': tool_active,
      }"
    >
      <div
        id="informations"
        class="subsection"
        v-show="tool_active && active_section == 'information'"
      >
        <div class="subsection-header">
          <span>information</span>
        </div>
        <div class="subsection-main colortype">
          <PathwayStatistics :active_term="active_term"></PathwayStatistics>
        </div>
      </div>
      <div
        id="network"
        class="subsection"
        v-if="
          tool_active && active_section == 'statistics' && active_term !== null
        "
      >
        <div class="subsection-header">
          <span>parameter selection</span>
        </div>
        <div class="subsection-main colortype">
          <PathwayLinks :active_term="active_term" :mode="mode"></PathwayLinks>
        </div>
      </div>
      <div
        id="connections"
        class="subsection"
        v-show="tool_active && active_section == 'connections'"
      >
        <div class="subsection-header">
          <span>connections</span>
          <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()" />
        </div>
        <div class="subsection-main colortype">
          <PathwayConnections
            :active_term="active_term"
            :gephi_data="gephi_data"
          ></PathwayConnections>
        </div>
      </div>
    </div>

    <div class="nodeattributes">
      <img
        class="icons"
        src="@/assets/toolbar/menu-burger.png"
        v-on:click="change_section('information')"
      />
      <img
        class="icons"
        src="@/assets/toolbar/settings-sliders.png"
        v-on:click="change_section('statistics')"
      />
      <img
        class="icons"
        src="@/assets/toolbar/proteinselect.png"
        v-on:click="change_section('connections')"
      />
      <img
        class="icons"
        src="@/assets/toolbar/bote.png"
        v-on:click="call_chatbot(mode)"
      />
      <!-- <img  class="icons" src="@/assets/toolbar/logout.png" v-on:click="change_section(!tool_active,'routing')"> -->
    </div>
  </div>
</template>

<script>
import PathwayStatistics from "@/components/pane/modules/pathways/PathwayStatistics.vue";
import PathwayConnections from "@/components/pane/modules/pathways/PathwayConnections.vue";
import PathwayLinks from "@/components/pane/modules/pathways/PathwayLinks.vue";

export default {
  name: "TermPane",
  props: ["active_term", "gephi_data", "mode", "tool_active"],
  emits: [
    "active_item_changed",
    "highlight_subset_changed",
    "tool_active_changed",
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
    change_section(val) {
      var com = this;

      if (com.tool_active && com.active_section == val) {
        com.active_section = "";
        com.$emit("tool_active_changed", false);
      } else {
        if (!com.tool_active) {
          com.active_section = val;
          com.$emit("tool_active_changed", true);
        }

        if (com.tool_active && com.active_section != val) {
          com.active_section = val;
          com.$emit("tool_active_changed", true);
        }
      }
    },
    copyclipboard() {
      this.emitter.emit("copyConnections");
    },
    to_term() {
      var com = this;
      if (!com.$store.state.term_graph_data) {
        alert("There is no term graph");
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
      console.log(this.active_term);
      this.emitter.emit("addToChatbot", {
        id: this.active_term.id,
        mode: mode,
        type: "term",
        data: this.active_term,
      });
    },
  },
  mounted() {
    this.emitter.on("updateFavouriteList", (value) => {
      this.favourite_pathways = value;
    });
  },
};
</script>

<style>
.term {
  width: 70%;
  margin-left: 0.3vw;
  font-size: 0.9vw;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.path_attribute {
  display: flex;
  font-family: "ABeeZee", sans-serif;
  align-items: center;
  color: #0a0a1a;
}

#colorbar-pathway {
  position: relative;
  display: flex;
  border-radius: 5px;
  margin-top: 5%;
  width: 70%;
  color: white;
  align-items: center;
  text-align: center;
  justify-content: center;
  transform: translate(13.5%);
  font-family: "ABeeZee", sans-serif;
  font-size: 0.9vw;
  background-color: darkgreen;
  border-radius: 5px 0 0 5px;
}
.colorbar-text {
  width: 100%;
  background-color: darkgreen;
  padding: 2%;
  border-radius: 5px 0 0 5px;
}

#pathway-connections {
  height: 40%;
}

.favourite-pane-symbol {
  height: 100%;
  width: 10%;
  left: 2%;
  justify-content: center;
  text-align: center;
  position: relative;
  display: flex;
}
.favourite-pane-symbol .custom-checkbox {
  position: relative;
  display: inline-block;
  cursor: default;
}

.checked {
  background-color: #ffa500;
}

#vis-button {
  position: absolute;
  width: 50%;
  right: -15%;
  display: -webkit-flex;
  padding: 1%;
  border-radius: 0 5px 5px 0;
  padding: 5% 23% 5% 23%;
}
#vis-button img {
  filter: invert(100%);
  position: relative;
  width: unset;
  right: unset;
  padding: 0%;
}
</style>
