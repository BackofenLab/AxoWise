<template>
  <aside class="py-4">
    <!-- <ul class="menu-bar" :class="{ full: tools_active == true }">
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
      <li v-on:click="threeview()">
        <img src="@/assets/toolbar/3d-icon.png" alt="3D Icon">
      </li>
      <li v-on:click="chatbot()">
        <img src="@/assets/toolbar/bote.png" alt="bot Icon" />
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
    </ul> -->

    <nav class="w-[64px] flex flex-col items-center gap-4 overflow-auto">
      <Button icon="material-icons" text plain @click="switch_home">
        <span class="material-icons">home</span>
      </Button>

      <Button icon="material-icons" text plain @click="protein_active = !protein_active">
        <span class="material-icons">hub</span>
      </Button>

      <!-- <Button icon="material-icons" v-on:mouseover="tools_active = true" v-on:mouseleave="tools_active = false"> -->
      <Button icon="material-icons" text plain @click="showWindow">
        <span class="material-icons">tune</span>
      </Button>

      <Button icon="material-icons" text plain @click="selection_active = !selection_active">
        <span class="material-icons">settings_applications</span>
      </Button>

      <Button icon="material-icons" text plain @click="center">
        <span class="material-icons">fullscreen</span>
      </Button>

      <Button icon="material-icons" text plain @click="chatbot">
        <span class="material-icons">chat</span>
      </Button>

      <Button icon="material-icons" text plain @click="hide_labels(label_check)">
        <span v-if="!label_check" class="material-icons">visibility</span>
        <span v-if="label_check" class="material-icons">visibility_off</span>
      </Button>
    </nav>
    <!-- <MenuWindow
      v-show="tools_active"
      v-on:mouseover="tools_active = true"
      v-on:mouseleave="tools_active = false"
      :gephi_data="gephi_data"
      :ensembl_name_index="ensembl_name_index"
      :tools_active="tools_active"
      :mode="mode"
      @tools_active_changed="tools_active = $event"
    ></MenuWindow> -->
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
  </aside>
</template>

<script setup>
import { ref } from "vue";

const windowRef = ref();

const showWindow = (event) => {
  windowRef.value.toggle(event);
};
</script>

<script>
// import MenuWindow from "@/components/toolbar/windows/MenuWindow.vue";
import ProteinList from "@/components/toolbar/modules/ProteinList.vue";
import SelectionList from "@/components/toolbar/modules/SelectionList.vue";

export default {
  name: "MainToolBar",
  props: ["gephi_data", "term_data", "active_subset", "active_term", "ensembl_name_index", "widget"],
  components: {
    // MenuWindow,
    ProteinList,
    SelectionList,
  },
  data() {
    return {
      // tools_active: false,
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
