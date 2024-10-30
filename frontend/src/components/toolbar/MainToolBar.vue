<template>
  <div>
    <ul class="menu-bar" :class="{ full: tools_active == true }">
      <li v-on:click="switch_home()">
        <img src="@/assets/toolbar/home.png" alt="Home Icon" />
      </li>
      <li v-on:click="protein_active = !protein_active">
        <img src="@/assets/toolbar/proteinselect.png" alt="Search Icon" />
      </li>
      <li
        v-on:mouseover="tools_active = true"
        v-on:mouseleave="tools_active = false"
      >
        <img src="@/assets/toolbar/menu-burger.png" alt="Tool Icon" />
      </li>
      <li v-on:click="selection_active = !selection_active">
        <img src="@/assets/toolbar/settings-sliders.png" alt="Graph Icon" />
      </li>
      <li v-on:click="center()">
        <img src="@/assets/toolbar/expand.png" alt="Center Icon" />
      </li>
      <!-- <li v-on:click="threeview()">
        <img src="@/assets/toolbar/3d-icon.png" alt="3D Icon">
      </li> -->
      <li v-on:click="chatbot()">
        <img src="@/assets/toolbar/bote.png" alt="bot Icon" />
      </li>
      <li v-on:click="word()">
        <img src="@/assets/toolbar/word.png" alt="word Icon" />
      </li>
      <li
        v-on:click="hide_labels(label_check)"
        :class="{ crossed: label_check }"
      >
        <div class="label-container">
          <img src="@/assets/toolbar/label.png" alt="label Icon" />
          <span v-if="label_check" class="cross-line"></span>
        </div>
      </li>
    </ul>
    <MenuWindow
      v-show="tools_active"
      v-on:mouseover="tools_active = true"
      v-on:mouseleave="tools_active = false"
      :gephi_data="gephi_data"
      :ensembl_name_index="ensembl_name_index"
      :tools_active="tools_active"
      :mode="mode"
      @tools_active_changed="tools_active = $event"
    ></MenuWindow>
    <SelectionList
      v-show="selection_active"
      :data="gephi_data"
      :selection_active="selection_active"
      :active_subset="active_subset"
      :active_term="active_term"
      :mode="mode"
      @selection_active_changed="selection_active = $event"
    >
    </SelectionList>
    <ProteinList
      v-show="protein_active"
      :gephi_data="gephi_data"
      :mode="mode"
      @protein_active_changed="protein_active = $event"
    >
    </ProteinList>
  </div>
</template>

<script>
import MenuWindow from "@/components/toolbar/windows/MenuWindow.vue";
import ProteinList from "@/components/toolbar/modules/ProteinList.vue";
import SelectionList from "@/components/toolbar/modules/SelectionList.vue";

export default {
  name: "MainToolBar",
  props: [
    "gephi_data",
    "term_data",
    "active_subset",
    "active_term",
    "ensembl_name_index",
  ],
  components: {
    MenuWindow,
    ProteinList,
    SelectionList,
  },
  data() {
    return {
      tools_active: false,
      protein_active: false,
      selection_active: false,
      label_check: true,
      mode: "protein",
    };
  },
  methods: {
    switch_home() {
      this.$router.push("/").then(() => {
        window.location.reload();
      });
    },
    center() {
      this.emitter.emit("centerGraph", { check: true, mode: this.mode });
    },
    threeview() {
      this.emitter.emit("threeView");
    },
    chatbot() {
      this.emitter.emit("openChatbot");
    },
    word() {
      this.emitter.emit("openWord");
    },
    hide_labels(check) {
      this.label_check = !check;
      this.emitter.emit("hideLabels", {
        check: this.label_check,
        mode: this.mode,
      });
    },
  },
};
</script>

<style>
.menu-bar {
  position: relative;
  border-radius: 5px;
  width: 3vw;
  display: inline-block;
  backdrop-filter: blur(7.5px);
  -webkit-backdrop-filter: blur(7.5px);
  align-items: center;
  padding: 5% 0;
  z-index: 99;
  margin: 0.5vw 0 0 0.5vw;
}

.menu-bar li {
  list-style: none;
  color: #0a0a1a;
  font-family: sans-serif;
  font-weight: bold;
  padding: 0.5vw;
  margin: 0 2%;
  position: relative;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.menu-bar li img {
  max-width: none;
  width: 60%;
  filter: invert(100%);
}

.menu-bar li::before {
  content: " ";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: -1;
  transition: 0.2s;
  border-radius: 5px;
}
.menu-bar li:hover::before {
  background: linear-gradient(to bottom, #e8edec, #d2d1d3);
  box-shadow: 0px 3px 20px 0px black;
  transform: scale(1.2);
}
.menu-bar li:hover {
  color: black;
}
.menu-bar li:hover img {
  color: black;
  filter: none;
}
/* Use ::v-deep to apply styles to nested child components */
::v-deep .menu-bar li {
  color: white;
}
::v-deep .menu-bar li:hover {
  color: black;
}
.label-container {
  position: relative;
  display: contents;
  text-align: center;
}

.cross-line {
  position: absolute;
  border-top: 1px solid rgba(255, 255, 255, 0.883); /* Red cross line, adjust thickness/color as needed */
  transform: rotate(-45deg); /* Optional: Diagonal cross */
  width: 60%;
}
</style>
