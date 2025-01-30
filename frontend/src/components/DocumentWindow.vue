<template>
  <DraggableView v-show="showPersistentComponent" :initialPosition="initial_drag_position"
    contentClass="!pr-4 !pl-0 !pb-3 flex-1 grid grid-cols-1 md:grid-cols-12"
    handlerClass="flex items-center !justify-start !py-4 !px-4"
    wrapperClass="!h-[calc(100vh-77px)] !w-[44rem] !max-full border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light !overflow-hidden">
    <template #handler>
      <h3 class="text-base font-bold">
        AxoWord
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-8 h-8" size="small" text rounded plain @click="closeWindow()">
          <span class="dark:text-white !text-2xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <aside class="p-2 md:col-span-4">
        <Accordion :value="['0']" multiple class="!flex !flex-col !gap-4 !max-h-[77vh] !overflow-auto !pl-2">
          <AccordionPanel value="0" class="!border-0">
            <AccordionHeader class='!p-0 !gap-3' :pt="{ toggleicon: '!flex-shrink-0' }">
              <span class="material-symbols-rounded !text-xl !flex-shrink-0">history </span><span
                class="!flex-1 !leading-tight !line-clamp-2">Protein history</span>
            </AccordionHeader>
            <AccordionContent :pt="{ content: '!pl-6 !pt-3 !pb-0' }">
              <ul class="!flex !flex-col !gap-1">
                <li
                  class="!flex !items-center !gap-1.5 !cursor-pointer !py-1 rounded !px-2 hover:dark:bg-slate-100/10 hover:bg-slate-100 hover:!text-primary-400"
                  v-for="(bullet, index) in proteins" :key="index" @click="addBullet(bullet.label)">
                  <span class="material-symbols-rounded font-variation-ico-filled !text-[6px] !flex-shrink-0">circle
                  </span><span class="!text-sm !line-clamp-2">{{ bullet.label }}</span>
                </li>
              </ul>
            </AccordionContent>
          </AccordionPanel>
          <AccordionPanel value="1" class="!border-0">
            <AccordionHeader class='!p-0 !gap-3' :pt="{ toggleicon: '!flex-shrink-0' }">
              <span class="material-symbols-rounded !text-xl !flex-shrink-0">summarize </span><span
                class="!flex-1 !leading-tight !line-clamp-2">Abstract history</span>
            </AccordionHeader>
            <AccordionContent :pt="{ content: '!pl-6 !pt-3 !pb-0' }">
              <ul class="!flex !flex-col !gap-1">
                <li
                  class="!flex !items-center !gap-1.5 !cursor-pointer !py-1 rounded !px-2 hover:dark:bg-slate-100/10 hover:bg-slate-100 hover:!text-primary-400"
                  v-for="(bullet, index) in abstracts" :key="index" @click="addBullet(bullet.label)">
                  <span class="material-symbols-rounded font-variation-ico-filled !text-[6px] !flex-shrink-0">circle
                  </span><span class="!text-sm !line-clamp-2">{{ bullet.label }}</span>
                </li>
              </ul>
            </AccordionContent>
          </AccordionPanel>
          <AccordionPanel value="2" class="!border-0">
            <AccordionHeader class='!p-0 !gap-3' :pt="{ toggleicon: '!flex-shrink-0' }">
              <span class="material-symbols-rounded !text-xl !flex-shrink-0">star </span><span
                class="!flex-1 !leading-tight !line-clamp-2">Favourite terms</span>
            </AccordionHeader>
            <AccordionContent :pt="{ content: '!pl-6 !pt-3 !pb-0' }">
              <ul class="!flex !flex-col !gap-1">
                <li
                  class="!flex !items-center !gap-1.5 !cursor-pointer !py-1 rounded !px-2 hover:dark:bg-slate-100/10 hover:bg-slate-100 hover:!text-primary-400"
                  v-for="(bullet, index) in pathways" :key="index" @click="addBullet(bullet.name)">
                  <span class="material-symbols-rounded font-variation-ico-filled !text-[6px] !flex-shrink-0">circle
                  </span><span class="!text-sm !line-clamp-2">{{ bullet.name }}</span>
                </li>
              </ul>
            </AccordionContent>
          </AccordionPanel>
          <AccordionPanel value="3" class="!border-0">
            <AccordionHeader class='!p-0 !gap-3' :pt="{ toggleicon: '!flex-shrink-0' }">
              <span class="material-symbols-rounded !text-xl !flex-shrink-0">graph_3 </span><span
                class="!flex-1 !leading-tight !line-clamp-2">Current graphs</span>
            </AccordionHeader>
            <AccordionContent :pt="{ content: '!pl-6 !pt-3 !pb-0' }">
              <ul class="!flex !flex-col !gap-1">
                <li
                  class="!flex !items-center !gap-1.5 !cursor-pointer !py-1 rounded !px-2 hover:dark:bg-slate-100/10 hover:bg-slate-100 hover:!text-primary-400"
                  @click="addScreen('black', 'png')">
                  <span class="material-symbols-rounded font-variation-ico-filled !text-[6px] !flex-shrink-0">circle
                  </span><span class="!text-sm !line-clamp-2">Add current graph</span>
                </li>

              </ul>
            </AccordionContent>
          </AccordionPanel>
          <AccordionPanel value="4" class="!border-0">
            <AccordionHeader class='!p-0 !gap-3' :pt="{ toggleicon: '!flex-shrink-0' }">
              <span class="material-symbols-rounded !text-xl !flex-shrink-0">forum </span><span
                class="!flex-1 !leading-tight !line-clamp-2">Chatbot tag history</span>
            </AccordionHeader>
            <AccordionContent :pt="{ content: '!pl-6 !pt-3 !pb-0' }">
              <ul class="!flex !flex-col !gap-1">
                <li
                  class="!flex !items-center !gap-1.5 !cursor-pointer !py-1 rounded !px-2 hover:dark:bg-slate-100/10 hover:bg-slate-100 hover:!text-primary-400"
                  v-for="(bullet, index) in tags" :key="index" @click="addBullet(bullet)">
                  <span class="material-symbols-rounded font-variation-ico-filled !text-[6px] !flex-shrink-0">circle
                  </span><span class="!text-sm !line-clamp-2">{{ bullet.id }}</span>
                </li>
              </ul>
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </aside>
      <div class="flex flex-col p-2 md:col-span-8">
        <div
          class="max-h-[70vh] min-h-[40vh] border rounded-xl dark:!border-[#020617] dark:!bg-[#020617] bg-[#f3f3f3] border-[#f3f3f3]">
          <div ref="editor"></div>
        </div>
        <div class="flex items-center justify-end gap-4 mt-4">
          <Button severity="info" outlined label="AI improve" icon="pi pi-plus" size="small" @click="textImprove" />
          <Button severity="secondary" outlined label="Export Document" icon="pi pi-plus" size="small"
            @click="exportdocX" />
        </div>
      </div>
    </template>
  </DraggableView>
</template>

<script>
import DraggableView from "@/components/DraggableView.vue";
import Quill from "quill";
import "quill/dist/quill.snow.css";
import { saveAs } from "file-saver";
import * as quillToWord from "quill-to-word";
let quill = null;

export default {
  name: "DocumentWindow",
  components: {
    DraggableView
  },
  data() {
    return {
      windowCheck: false,
      abstracts: [],
      pathways: [],
      proteins: [],
      tags: [],
      api: {
        textenrich: "api/subgraph/textenrich",
      },
      initial_drag_position: { top: 65, left: 60 },
    };
  },
  computed: {
    showPersistentComponent() {
      let route = this.$route.name;
      return (
        this.windowCheck &&
        route !== "home"
      );
    },
    quillEditor() {
      return new Quill(this.$refs.editor, {
        theme: "snow",
        placeholder: "Start with your journey...",
        modules: {
          toolbar: [
            [{ header: [1, 2, false] }],
            ["bold", "italic", "underline"],
            ["link", "image"],
          ],
        },
      });
    },
  },
  mounted() {
    let com = this;

    com.emitter.on("openWord", () => {
      com.windowCheck = !com.windowCheck;
    });

    com.emitter.on("addToWord", (text) => {
      if (!com.windowCheck) {
        com.windowCheck = true;
      }
      com.addBullet(text);
    });

    com.emitter.on("addImageToWord", (img) => {
      if (!com.windowCheck) {
        com.windowCheck = true;
      }
      com.addImage(img);
    });

    this.emitter.on("updateFavouriteList", (value) => {
      this.pathways = value;
    });

    this.emitter.on("updateHistory", (value) => {
      if (value.type == "protein") com.proteins.unshift(value.data);
      if (value.type == "abstracts") com.abstracts.unshift(value.data);
      if (value.type == "tags")
        com.tags = [...new Set([...com.tags, ...value.data])].reverse();
    });

    com.pathways = com.$store.state.favourite_enrichments;

    quill = this.quillEditor;
  },
  methods: {
    addBullet(bullet) {
      // Get the current selection or place the bullet at the end
      if (typeof bullet === "object") this.addTag(bullet);
      else {
        var selection = quill.getSelection(true);
        if (selection) {
          quill.insertText(selection.index, `${bullet}\n`);
        } else {
          // If there is no selection, insert at the end of the document
          quill.insertText(0, `${bullet}`);
        }
      }
    },
    addTag(bullet) {
      if (bullet.type == "protein") this.addBullet(bullet.data.label);
      if (bullet.type == "subset")
        this.addBullet(
          `${bullet.id} (${bullet.data.map((node) => node.label).join(", ")})`
        );
      if (bullet.type == "term") this.addBullet(bullet.data.name);
    },
    addImage(imgURL) {
      var selection = quill.getSelection(true);
      if (selection) {
        quill.insertEmbed(selection.index, "image", imgURL);
      } else {
        // If there is no selection, insert at the end of the document
        quill.insertEmbed(0, "image", imgURL);
      }
    },
    addScreen(mode, format) {
      let path = this.$route.name;
      if (
        path == "protein-graph" ||
        path == "terms-graph" ||
        path == "citation-graph"
      ) {
        this.emitter.emit("exportGraphWord", {
          params: { mode, format },
          mode: path,
        });
      }
    },
    async exportdocX() {
      const delta = quill.getContents();
      const quillToWordConfig = {
        exportAs: "blob",
      };
      const docAsBlob = await quillToWord.generateWord(
        delta,
        quillToWordConfig
      );
      saveAs(docAsBlob, "word-export.docx");
    },
    async textImprove() {
      const delta = quill.getContents();
      var com = this;

      var formData = new FormData();
      formData.append("content", JSON.stringify(delta.ops));

      com.axios.post(com.api.textenrich, formData).then((response) => {
        console.log(response);
      });
    },
    closeWindow() {
      this.windowCheck = false;
    },
  },
};
</script>

<style>
.ql-container {
  height: calc(100% - 40px);
}

.ql-snow {
  background-color: rgba(255, 255, 255, 0.4);
}

.ql-toolbar.ql-snow,
.ql-container.ql-snow {
  background-color: transparent;
  border: none;
}

.ql-toolbar.ql-snow {
  border-bottom: 1px solid #b1b1b1;
}

.ql-formats .ql-picker-options {
  background-color: #f3f3f3;
  border: none;
  border-radius: 6px;
}

.p-dark .ql-toolbar.ql-snow,
.p-dark .ql-container.ql-snow {
  background-color: transparent;
}

.p-dark .ql-toolbar.ql-snow {
  border-bottom: 1px solid #10172b;
}

.p-dark .ql-formats .ql-header.ql-picker {
  color: white;
}

.p-dark .ql-formats button .ql-stroke,
.p-dark .ql-formats button .ql-fill {
  stroke: white;
}

.p-dark .ql-formats .ql-picker-options {
  background-color: #10172b;
}
</style>
