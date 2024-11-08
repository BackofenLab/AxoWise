<template>
  <aside :class="`py-4 animate__animated animate__faster ${widget ? 'animate__fadeInDown' : 'w-0 animate__fadeOutUp'}`">
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


      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Export graph'" @click="export_active = !export_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">file_export</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Graph parameter'"
        @click="selection_active = !selection_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">filter_b_and_w</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Re-center'" @click="center">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">center_focus_strong</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Chat bot'" @click="chatbot">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">forum</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Show label'"
        @click="hide_labels(label_check)">
        <span v-if="!label_check"
          class="material-symbols-rounded group-hover:font-variation-ico-filled">subtitles</span>
        <span v-if="label_check"
          class="material-symbols-rounded group-hover:font-variation-ico-filled">subtitles_off</span>
      </Button>
    </nav>

    <Dialog v-model:visible="selection_active" header="Graph parameter" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[25rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <SelectionList :data="gephi_data" :selection_active="selection_active" :active_subset="active_subset"
        :active_term="active_term" :mode="mode" @selection_active_changed="selection_active = $event">
      </SelectionList>
    </Dialog>

    <Dialog v-model:visible="protein_active" header="Highlight nodes" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[24rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <ProteinList v-show="protein_active" :gephi_data="gephi_data" :mode="mode"
        @protein_active_changed="protein_active = $event">
      </ProteinList>
    </Dialog>

    <Dialog v-model:visible="tools_active" header="Graph settings" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[25rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <MenuWindow v-show="tools_active" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index"
        :tools_active="tools_active" :mode="mode" @tools_active_changed="tools_active = $event"></MenuWindow>
    </Dialog>

    <Dialog v-model:visible="export_active" header="Export graph" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[18rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
      content: { class: '!px-4' }
    }">
      <ExportWindow v-show="export_active" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index"
        :mode="mode"></ExportWindow>
    </Dialog>
  </aside>
</template>

<script>
import MenuWindow from "@/components/toolbar/windows/MenuWindow.vue";
import ExportWindow from "@/components/toolbar/windows/ExportWindow.vue";
import ProteinList from "@/components/toolbar/modules/ProteinList.vue";
import SelectionList from "@/components/toolbar/modules/SelectionList.vue";

export default {
  name: "MainToolBar",
  props: ["gephi_data", "term_data", "active_subset", "active_term", "ensembl_name_index", "widget"],
  components: {
    MenuWindow,
    ExportWindow,
    ProteinList,
    SelectionList,
  },
  data() {
    return {
      tools_active: false,
      export_active: false,
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