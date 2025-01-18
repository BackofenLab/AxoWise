<template>
  <div
    id="expdocument"
    class="persistent-window"
    v-show="showPersistentComponent"
  >
    <div id="expdocument_header" class="header">
      <h3>AxoWord</h3>
      <span class="close-btn" @click="closeWindow">×</span>
    </div>
    <div class="content-wrapper">
      <!-- Bullet Section -->
      <div class="bullet-section">
        <br />
        <h4>Protein history</h4>
        <ul>
          <li
            v-for="(bullet, index) in proteins"
            :key="index"
            @click="addBullet(bullet.label)"
          >
            {{ bullet.label }}
          </li>
        </ul>
        <br /><br />
        <h4>Abstract history</h4>
        <ul>
          <li
            v-for="(bullet, index) in abstracts"
            :key="index"
            @click="addBullet(bullet.label)"
          >
            {{ bullet.label }}
          </li>
        </ul>
        <br /><br />
        <h4>Favourite terms</h4>
        <ul>
          <li
            v-for="(bullet, index) in pathways"
            :key="index"
            @click="addBullet(bullet.name)"
          >
            {{ bullet.name }}
          </li>
        </ul>
        <br /><br />
        <h4>Current graphs</h4>
        <ul>
          <li @click="addScreen('black', 'png')">add current graph</li>
        </ul>
        <br /><br />
        <h4>Chatbot tag history</h4>
        <ul>
          <li
            v-for="(bullet, index) in tags"
            :key="index"
            @click="addBullet(bullet)"
          >
            {{ bullet.id }}
          </li>
        </ul>
      </div>
      <!-- Quill Editor Section -->
      <div class="editor-section">
        <div ref="editor"></div>
        <!-- Editor container -->
      </div>
    </div>
    <div class="export-bar">
      <button @click="textImprove">AI improve</button>
      <button @click="exportdocX">Export Document</button>
    </div>
  </div>
</template>

<script>
import Quill from "quill";
import "quill/dist/quill.snow.css";
import { saveAs } from "file-saver";
import * as quillToWord from "quill-to-word";
let quill = null;

export default {
  name: "DocumentWindow",
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
    };
  },
  computed: {
    showPersistentComponent() {
      let route = this.$route.name;
      return (
        this.windowCheck &&
        route !== "home" &&
        route !== "input" &&
        route !== "file" &&
        route !== "import"
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
    com.dragElement(document.getElementById("expdocument"));

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
    dragElement(elmnt) {
      var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
      if (document.getElementById(elmnt.id + "_header")) {
        document.getElementById(elmnt.id + "_header").onmousedown =
          dragMouseDown;
      } else {
        elmnt.onmousedown = dragMouseDown;
      }

      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
      }

      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        var parentWidth = window.innerWidth;
        var parentHeight = window.innerHeight;
        var elementWidth = elmnt.offsetWidth;
        var elementHeight = elmnt.offsetHeight;

        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        var newTop = elmnt.offsetTop - pos2;
        var newLeft = elmnt.offsetLeft - pos1;

        if (newTop < 0) newTop = 0;
        if (newLeft < 0) newLeft = 0;
        if (newTop + elementHeight > parentHeight)
          newTop = parentHeight - elementHeight;
        if (newLeft + elementWidth > parentWidth)
          newLeft = parentWidth - elementWidth;

        elmnt.style.top = newTop + "px";
        elmnt.style.left = newLeft + "px";
      }

      function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
      }
    },
    closeWindow() {
      this.windowCheck = false;
    },
  },
};
</script>

<style scoped>
.persistent-window {
  position: absolute;
  right: 1%;
  top: 1.5%;
  height: 97%;
  width: 50%;
  -webkit-backdrop-filter: blur(7.5px);
  border: 1px solid #e0e0e0;
  background-color: rgb(57, 57, 57);
  box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.1);
  overflow: auto;
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  z-index: 99999;
  resize: horizontal;
}

/* Header styles remain the same */
.header {
  background-color: rgb(57, 57, 57);
  color: white;
  padding: 15px;
  cursor: move;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  position: relative;
}

.close-btn {
  font-size: 20px;
  cursor: pointer;
  padding: 0 5px;
}

/* Flexbox layout for bullet section and editor */
.content-wrapper {
  display: flex;
  height: 100%;
}

/* Bullet section styles */
.bullet-section {
  width: 30%;
  height: 45vw;
  overflow-y: scroll;
  background-color: rgb(57, 57, 57);
  padding: 10px;
  color: white;
}

.bullet-section ul {
  list-style: none;
  padding: 0;
  overflow-y: scroll;
  height: 15%;
}

.bullet-section li {
  padding: 5px 0;
  font-size: 0.7vw;
  margin-left: 5px;
  cursor: pointer;
  color: white;
}

.bullet-section li:hover {
  color: #00aaff;
}

/* Editor styles */
#editor {
  width: 100%;
  padding: 10px;
  overflow-y: auto;
  z-index: 999999999;
}

.editor-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 45vw;
}

.export-bar {
  color: white;
  padding: 1%;
  width: 99%;
  display: flex;
  justify-content: end;
  cursor: move;
  display: flex;
  font-size: 16px;
  font-weight: bold;
  position: relative;
}

.export-bar button {
  padding: 8px 16px;
  margin-left: 2%;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.export-bar button:hover {
  background-color: #0056b3;
}
</style>

<style>
.ql-snow {
  background-color: rgba(255, 255, 255, 0.4);
}
</style>
