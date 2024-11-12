<template>
  <h6 class="mb-5 text-sm text-slate-300">
    <span
      class="inline-block mr-1 text-xl leading-none align-bottom material-symbols-rounded font-variation-ico-filled">help</span>
    To find multiple nodes separate each node name with comma (<span
      class="leading-[0] text-primary-400 text-4xl">,</span>)
  </h6>
  <Textarea v-model="raw_text" rows="4" cols="45" autofocus placeholder="Search by gene..." />
  <Button label="Apply" severity="secondary" type="button" class="mt-2.5 !rounded-lg" @click="highlight(raw_text)">
  </Button>

  <!-- <div class="hidden tool-item">
    <div id="protein_highlight" class="window-menu">
      <div id="protein_highlight_header" class="window-header">
        <div class="headertext">
          <span>highlight nodes</span>
          <img class="protein_close" src="@/assets/toolbar/cross.png" v-on:click="unactive_proteinlist()" />
        </div>
      </div>
      <div class="keyword-search">
        <div class="window-label">keyword search</div>
        <div class="keyword-searchbar">
          <span v-on:click="search_subset(filt_keyword)">></span>
          <input type="text" v-model="search_raw" class="empty" placeholder="input keyword" />
        </div>
        <div class="keyword-result">
          <div v-for="(entry, index) in filt_keyword" :key="index">
            <a href="#" v-on:click="select_node(entry)" :class="{ in_subset: active_genes.has(entry.label) }">{{
              entry.attributes["Name"] }}</a>
          </div>
        </div>
      </div>
      <div class="highlight-list">
        <div class="window-label">gene search</div>
        <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
        <button v-on:click="highlight(raw_text)" id="highlight_protein" class="colortype">
          apply
        </button>
      </div>
    </div>
  </div> -->
</template>


<script>
// import {QuickScore} from "quick-score";
export default {
  name: "ProteinList",
  props: ["gephi_data", "mode"],
  emits: ["protein_active_changed"],
  data() {
    return {
      search_raw: "",
      raw_text: "",
      active_genes: new Set(),
    };
  },
  methods: {
    // dragElement(elmnt) {
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
    // unactive_proteinlist() {
    //   this.$emit("protein_active_changed", false);
    // },
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

      com.emitter.emit("searchSubset", { subset: subset, mode: this.mode });
    },
    select_node(node) {
      if (node)
        this.emitter.emit("searchNode", { node: node, mode: "protein" });
    },
    search_subset(subset) {
      var com = this;
      com.emitter.emit("searchSubset", { subset: subset, mode: this.mode });
    },
  },
  mounted() {
    // var com = this;
    // this.$nextTick(() => {
    //   com.dragElement(document.getElementById("protein_highlight"));
    // });
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_keyword() {
      var com = this;
      var matches = [];

      if (com.search_raw.length >= 2) {
        com.active_genes = com.$store.state.active_subset
          ? new Set(com.$store.state.active_subset)
          : new Set();
        var regex = new RegExp(com.regex, "i");
        matches = com.gephi_data.nodes.filter(function (node) {
          return (
            regex.test(node.attributes["Description"]) || regex.test(node.label)
          );
        });
      }
      return matches;
    },
  },
};
</script>

<!-- <style>
.window-menu {
  position: fixed;
  display: flex;
  flex-direction: column;
  top: 30%;
  left: 42%;
  width: 16%;
  height: 40%;
  flex-shrink: 0;
  border-style: solid;
  border-width: 1px;
  background: #0a0a1a;
  border-color: white;
  overflow: hidden;
}
.keyword-search {
  margin-top: 2%;
  position: relative;
  width: 100%;
  height: 45%;
}
.highlight-list {
  position: relative;
  width: 100%;
  height: 45%;
}

.window-header {
  width: 100%;
  height: 9.41%;
  position: relative;
  flex-shrink: 0;
  backdrop-filter: blur(7.5px);
  background: #d9d9d9;
  text-align: center;
}

.window-header .headertext {
  color: #0a0a1a;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.window-header .headertext span {
  height: 100%;
  display: flex;
  font-size: 0.9vw;
  align-items: center;
}

.window-header .protein_close {
  right: 3%;
  width: 0.5vw;
  height: 0.5vw;
  position: absolute;
}

.highlight-list textarea {
  margin-top: 3%;
  font-size: 0.9vw;
  width: 100%;
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
  text-align: center;
  border: none;
  padding-top: 5%;
  resize: none;
  outline: none;
  height: 65%;
}

#highlight_protein {
  position: absolute;
  display: block;
  cursor: pointer;
  border: none;
  color: white;
  border-style: solid;
  border-width: 1px;
  background: #0a0a1a;
  border-color: white;
  margin-top: 1%;
  padding: 1%;
  width: 60%;
  margin-left: 50%;
  transform: translate(-50%, 0);
}

.keyword-searchbar {
  margin-top: 0.5vw;
  padding: 0 0 0 0.3vw;
  height: 1.4vw;
  display: flex;
  align-items: center;
  align-content: center;
  justify-content: left;
}

.keyword-searchbar span {
  filter: invert(100%);
}

.keyword-searchbar input[type="text"] {
  margin-left: 0.5vw;
  width: 8vw;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 0.2vw;
  font-size: 0.85vw;
  color: white;
  cursor: default;
  border: none;
  font-family: "ABeeZee", sans-serif;
}

.keyword-searchbar [type="text"]::-webkit-input-placeholder {
  opacity: 70%;
}

.keyword-search .keyword-result {
  margin: 0.2vw 0.5vw 0.5vw 0.5vw;
  padding: 0.3vw;
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 65%;
  overflow: scroll;
}

.keyword-result a {
  font-size: 0.85vw;
  color: white;
  text-decoration: none;
}

.keyword-result .in_subset {
  color: lightgreen;
}
</style> -->
