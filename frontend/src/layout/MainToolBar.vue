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


      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Export graph'"
        @click="export_active = !export_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">file_export</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Graph parameter'"
        @click="selection_active = !selection_active">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">filter_b_and_w</span>
      </Button>

      <Button class="group" icon="material-symbols-rounded" text plain v-tooltip="'Recenter graph'" @click="center">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">center_focus_strong</span>
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

      <Button v-if="mode != 'protein'" class="group" icon="material-symbols-rounded" text plain v-tooltip="'Switch graph'" @click="switch_graph">
        <span class="material-symbols-rounded group-hover:font-variation-ico-filled">logout</span>
      </Button>
    </nav>

    <Dialog v-model:visible="selection_active" header="Graph parameter" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[25rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <!-- @selection_active_changed="selection_active = $event" -->
      <SelectionList :data="gephi_data" :selection_active="selection_active" :active_subset="active_subset"
        :active_term="active_term" :mode="mode">
      </SelectionList>
    </Dialog>

    <Dialog v-model:visible="protein_active" header="Highlight nodes" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[24rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <!-- @protein_active_changed="protein_active = $event" -->
      <ProteinList v-show="protein_active" :gephi_data="gephi_data" :mode="mode">
      </ProteinList>
    </Dialog>

    <Dialog v-model:visible="keyword_active" header="Highlight nodes" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[24rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <KeywordList v-show="keyword_active" :gephi_data="gephi_data" :mode="mode">
      </KeywordList>
    </Dialog>

    <Dialog v-model:visible="tools_active" header="Graph settings" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[25rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <!-- @tools_active_changed="tools_active = $event" -->
      <SettingList v-show="tools_active" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index"
        :tools_active="tools_active" :mode="mode"></SettingList>
    </Dialog>

    <Dialog v-model:visible="export_active" header="Export graph" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[18rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
      content: { class: '!px-4' }
    }">
      <ExportList v-show="export_active" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index" :mode="mode">
      </ExportList>
    </Dialog>
  </aside>
</template>

<script>
import SettingList from "@/components/toolbar/modules/SettingList.vue";
import ExportList from "@/components/toolbar/modules/ExportList.vue";
import ProteinList from "@/components/toolbar/modules/ProteinList.vue";
import KeywordList from "@/components/toolbar/modules/KeywordList.vue";
import SelectionList from "@/components/toolbar/modules/SelectionList.vue";

export default {
  name: "ToolBar",
  props: ["mode", "gephi_data", "term_data", "active_subset", "active_term", "ensembl_name_index", "widget"],
  components: {
    SettingList,
    ExportList,
    ProteinList,
    KeywordList,
    SelectionList,
  },
  data() {
    return {
      tools_active: false,
      export_active: false,
      protein_active: false,
      keyword_active: false,
      selection_active: false,
      label_check: true,
    };
  },
  mounted() {
    var com = this;

    this.emitter.on("selection_active_changed", (state) => {
      com.selection_active = state;
    });

    this.emitter.on("protein_active_changed", (state) => {
      com.protein_active = state;
    });

    this.emitter.on("keyword_active_changed", (state) => {
      com.keyword_active = state;
    });
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