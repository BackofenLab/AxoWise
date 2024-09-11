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
      <li v-on:click="chatbot()">
        <img src="@/assets/toolbar/bote.png" alt="bot Icon" />
      </li>
      <li v-on:click="switch_graph()">
        <img src="@/assets/toolbar/logout.png" alt="3D Icon" />
      </li>
    </ul>
    <MenuWindow
      v-show="tools_active"
      v-on:mouseover="tools_active = true"
      v-on:mouseleave="tools_active = false"
      :tools_active="tools_active"
      :mode="mode"
      @tools_active_changed="tools_active = $event"
    ></MenuWindow>
    <SelectionList
      v-show="selection_active"
      :selection_active="selection_active"
      :data="data"
      :mode="mode"
      :active_subset="active_subset"
      @selection_active_changed="selection_active = $event"
    >
    </SelectionList>
    <ProteinList
      v-show="protein_active"
      :gephi_data="data"
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
  name: "TermToolBar",
  props: ["data", "active_subset"],
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
      mode: "term",
    };
  },
  methods: {
    switch_home() {
      this.$router.push("/").then(() => {
        window.location.reload();
      });
    },
    switch_graph() {
      this.$router.push("protein");
    },
    center() {
      this.emitter.emit("centerGraph", { check: true, mode: this.mode });
    },
    chatbot() {
      this.emitter.emit("openChatbot");
    },
  },
};
</script>

<style></style>
