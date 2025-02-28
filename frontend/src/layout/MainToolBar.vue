<template>
  <aside
    :class="`py-4 animate__animated animate__faster order-1 ${widget ? 'animate__fadeInDown' : 'w-0 animate__fadeOutUp'}`">
    <nav class="w-[64px] flex flex-col items-center gap-4 overflow-auto">
      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Home'" @click="switch_home">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">home</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Highlight nodes'"
        @click="protein_active = !protein_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">hub</span>
      </Button>


      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Graph settings'"
        @click="tools_active = !tools_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">settings_motion_mode</span>
      </Button>


      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Export graph'"
        @click="export_active = !export_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">file_export</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Graph parameter'"
        @click="selection_active = !selection_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">tune</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Recenter graph'" @click="center">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">fullscreen</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Open AxoBot'" @click="chatbot">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">forum</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Open Axoword'" @click="word">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">docs</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain
        v-tooltip="label_check ? 'Show label' : 'Hide label'" @click="hide_labels(label_check)">
        <span v-if="!label_check"
          class="material-symbols-rounded group-hover:font-variation-ico-filled">subtitles</span>
        <span v-if="label_check"
          class="material-symbols-rounded group-hover:font-variation-ico-filled">subtitles_off</span>
      </Button>

      <Button v-if="mode != 'protein'" class="group" icon="material-symbols-rounded" text plain
        v-tooltip="'Switch graph'" @click="switch_graph">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">logout</span>
      </Button>
    </nav>
  </aside>
  <DraggableView v-show="selection_active" :initialPosition="initial_drag_position"
    wrapperClass="animate__animated animate__fadeInLeft animate__faster !w-[25rem] border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light"
    contentClass="!px-4 !py-1.5" handlerClass="!py-2.5 !px-4 !flex !items-center">
    <template #handler>
      <h3 class="text-base font-bold">
        Graph parameter
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-8 h-8" size="small" text rounded plain @click="selection_active = !selection_active">
          <span class="dark:text-white !text-2xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <SelectionList :data="gephi_data" :selection_active="selection_active" :active_subset="active_subset"
        :active_term="active_term" :mode="mode">
      </SelectionList>
    </template>
  </DraggableView>
  <DraggableView v-show="protein_active" :initialPosition="initial_drag_position"
    wrapperClass="animate__animated animate__fadeInLeft animate__faster !w-[24rem] border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light"
    contentClass="!px-4 !py-1.5" handlerClass="!py-2.5 !px-4 !flex !items-center">
    <template #handler>
      <h3 class="text-base font-bold">
        Highlight nodes
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-8 h-8" size="small" text rounded plain @click="protein_active = !protein_active">
          <span class="dark:text-white !text-2xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <ProteinList v-show="protein_active" :gephi_data="gephi_data" :mode="mode">
      </ProteinList>
    </template>
  </DraggableView>
  <DraggableView v-show="tools_active" :initialPosition="initial_drag_position"
    wrapperClass="animate__animated animate__fadeInLeft animate__faster !w-[25rem] border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light"
    contentClass="!px-4 !py-1.5" handlerClass="!py-2.5 !px-4 !flex !items-center">
    <template #handler>
      <h3 class="text-base font-bold">
        Graph settings
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-8 h-8" size="small" text rounded plain @click="tools_active = !tools_active">
          <span class="dark:text-white !text-2xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <SettingList v-show="tools_active" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index"
        :tools_active="tools_active" :mode="mode"></SettingList>
    </template>
  </DraggableView>
  <DraggableView v-show="export_active" :initialPosition="initial_drag_position"
    wrapperClass="animate__animated animate__fadeInLeft animate__faster !w-[18rem] border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light"
    contentClass="!px-4 !py-1.5" handlerClass="!py-2.5 !px-4 !flex !items-center">
    <template #handler>
      <h3 class="text-base font-bold">
        Export graph
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-8 h-8" size="small" text rounded plain @click="export_active = !export_active">
          <span class="dark:text-white !text-2xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <ExportList v-show="export_active" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index" :mode="mode">
      </ExportList>
    </template>
  </DraggableView>
</template>

<script>
import SettingList from "@/components/toolbar/modules/SettingList.vue";
import ExportList from "@/components/toolbar/modules/ExportList.vue";
import ProteinList from "@/components/toolbar/modules/ProteinList.vue";
import SelectionList from "@/components/toolbar/modules/SelectionList.vue";
import DraggableView from "@/components/DraggableView.vue";

export default {
  name: "ToolBar",
  props: ["mode", "gephi_data", "term_data", "active_subset", "active_term", "ensembl_name_index", "widget"],
  components: {
    SettingList,
    ExportList,
    ProteinList,
    SelectionList,
    DraggableView
  },
  data() {
    return {
      tools_active: false,
      export_active: false,
      protein_active: false,
      selection_active: false,
      label_check: true,
      initial_drag_position: { top: 60, left: 60 },
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