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
  margin: 0.5vw 0 0 0;
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
</style>
