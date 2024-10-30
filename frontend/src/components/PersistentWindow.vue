<template>
  <div
    id="genchatbot"
    class="persistent-window"
    v-show="showPersistentComponent"
  >
    <div id="genchatbot_header" class="header">
      <h3>AxoBot</h3>
      <span class="close-btn" @click="closeWindow">×</span>
    </div>

    <div class="chat-history">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="[
          'message',
          msg.sender === 'User' ? 'user-message' : 'bot-message',
        ]"
      >
        <div v-if="msg.data">
          <span
            v-for="(element, index) in msg.data"
            :key="index"
            class="small-tag"
            @click="searchInput(element)"
          >
            {{ element.id }}
          </span>
        </div>
        <div v-if="msg.ref">
          <span class="small-tag blue" @click="searchRef(msg.ref)">
            reference
          </span>
        </div>
        <p>{{ msg.text }}</p>
        <img
          src="@/assets/pane/copy.png"
          v-on:click="copyToClipboard(msg.text)"
        />
        <img src="@/assets/toolbar/word.png" v-on:click="addToWord(msg.text)" />
      </div>
    </div>

    <div class="chat-input-container">
      <!-- Editable div with contenteditable attribute -->
      <div
        ref="editableDiv"
        id="input_chatbot"
        contenteditable="true"
        @keydown.enter.prevent="sendMessage"
        class="input-box"
      ></div>

      <div class="tag-container" v-if="tags.length">
        <span
          v-for="(tag, index) in tags"
          :key="index"
          class="tag"
          @click="searchInput(tag)"
        >
          {{ tag.id }}
          <span class="remove-tag" @click.stop="removeTag(index)">x</span>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PersistentWindow",
  data() {
    return {
      userInput: "",
      messages: [{ sender: "Bot", text: "Hello! How can I assist you today?" }],
      windowCheck: false,
      tags: [],
      api: {
        chatbot: "api/subgraph/chatbot",
      },
      sourceToken: null,
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
      ); // Example: Hide component on 'View3'
    },
  },
  mounted() {
    let com = this;
    com.dragElement(document.getElementById("genchatbot"));

    com.emitter.on("openChatbot", () => {
      com.windowCheck = !com.windowCheck;
    });

    com.emitter.on("addToChatbot", (data) => {
      this.addLink(data);
    });
  },
  methods: {
    copyToClipboard(text) {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          alert("Message copied to clipboard");
        })
        .catch((err) => {
          console.error("Could not copy text: ", err);
        });
    },
    addToWord(text) {
      this.emitter.emit("addToWord", text);
    },
    addLink(tag) {
      if (!this.windowCheck) this.windowCheck = true;
      if (tag && !this.tags.includes(tag)) {
        this.tags.push(tag);
      }
    },
    removeTag(index) {
      // Remove the tag at the given index
      this.tags.splice(index, 1);
    },
    searchInput(tag) {
      if (tag.type == "protein") {
        this.$router.push(tag.mode).then(() => {
          this.emitter.emit("searchNode", { node: tag.data, mode: tag.mode });
        });
      } else if (tag.type == "term") {
        this.emitter.emit("searchEnrichment", tag.data);
      } else if (tag.type == "subset") {
        this.$router.push(tag.mode).then(() => {
          this.emitter.emit("searchSubset", {
            subset: tag.data,
            mode: tag.mode,
          });
        });
      }
    },
    searchRef(ref) {
      if (this.$store.state.citation_graph_data) {
        this.$router.push("citation").then(() => {
          this.emitter.emit("searchSubset", {
            subset: this.pmid_nodes(ref),
            mode: "citation",
          });
        });
      } else {
        alert("no citation graph");
      }
    },
    pmid_nodes(list) {
      let data = this.$store.state.citation_graph_data.graph;
      var pmid_nodes = new Set(list);
      var pmidlist = data.nodes.filter((element) =>
        pmid_nodes.has(element.attributes["Name"])
      );
      return pmidlist;
    },
    dragElement(elmnt) {
      var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
      if (document.getElementById(elmnt.id + "_header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "_header").onmousedown =
          dragMouseDown;
      } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
      }

      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }
      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();

        // calculate the conditions:
        var parentWidth = window.innerWidth;
        var parentHeight = window.innerHeight;
        var elementWidth = elmnt.offsetWidth;
        var elementHeight = elmnt.offsetHeight;

        // calculate the new coordinates:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        // Calculate the new coordinates for top and left
        var newTop = elmnt.offsetTop - pos2;
        var newLeft = elmnt.offsetLeft - pos1;

        // ensure the element stays within bounds:
        if (newTop < 0) newTop = 0;
        if (newLeft < 0) newLeft = 0;
        if (newTop + elementHeight > parentHeight)
          newTop = parentHeight - elementHeight;
        if (newLeft + elementWidth > parentWidth)
          newLeft = parentWidth - elementWidth;

        // set the element's new position:
        elmnt.style.top = newTop + "px";
        elmnt.style.left = newLeft + "px";
      }

      function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
      }
    },
    sendMessage() {
      const inputDiv = this.$refs.editableDiv;
      const userInput = inputDiv.innerText.trim();
      if (userInput !== "") {
        const messageTags = [...this.tags];
        let message = { text: userInput, data: messageTags };

        this.messages.push({
          sender: "User",
          text: userInput,
          data: messageTags,
        });
        this.getAnswer(message);
        inputDiv.innerText = "";
      }
    },

    getAnswer(message) {
      let com = this;
      let formData = new FormData();
      formData.append("message", message.text);
      formData.append("background", JSON.stringify(message.data));

      if (this.sourceToken) {
        this.abort_chatbot();
      }

      this.emitter.emit("updateHistory", {
        type: "tags",
        data: [...this.tags],
      });

      this.messages.push({
        sender: "Bot",
        text: "Waiting for response...",
        data: [...this.tags],
        ref: null,
      });
      //POST request for generating pathways
      com.sourceToken = this.axios.CancelToken.source();
      com.axios
        .post(com.api.chatbot, formData, {
          cancelToken: com.sourceToken.token,
        })
        .then((response) => {
          const botMessageIndex = this.messages.length - 1;
          this.messages[botMessageIndex].ref = response.data.pmids;
          this.messages[botMessageIndex].text = response.data.message;
          this.sourceToken = null;
        });
    },
    abort_chatbot() {
      this.sourceToken.cancel("Request canceled");
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
  left: 1%;
  top: 1.5%;
  height: 97%;
  width: 24vw;
  -webkit-backdrop-filter: blur(7.5px);
  border: 1px solid #e0e0e0;
  background-color: rgb(107, 107, 107);
  box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.1);
  overflow: auto;
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  z-index: 99999;
  resize: both;
}

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

.chat-history {
  flex: 1;
  padding: 10px 15px;
  overflow-y: auto;
  background-color: rgb(107, 107, 107);
  display: flex;
  flex-direction: column;
}

.message {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word; /* Ensure long words or links wrap */
  word-break: break-word; /* Break long words */
  white-space: pre-wrap; /* Preserve formatting like newlines */
  line-height: 1.4;
  cursor: default;
}

.user-message {
  background-color: rgb(57, 57, 57);
  align-self: flex-end;
  color: white;
}

.bot-message {
  background-color: #ffffff;
  align-self: flex-start;
  border: 1px solid #e0e0e0;
}

.chat-input-container {
  padding: 10px 15px;
  background-color: rgb(107, 107, 107);
  border-top: 1px solid #e0e0e0;
}

.input-box {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  background-color: rgb(57, 57, 57);
  border-radius: 30px;
  box-sizing: border-box;
  font-size: 14px;
  outline: none;
  color: white;
}

.input-box::placeholder {
  color: rgb(237, 235, 235);
}

.tag-container {
  padding: 10px 15px;
  background-color: rgb(107, 107, 107);
}

.tag {
  display: inline-block;
  background-color: #555; /* Darker background color */
  color: #fff; /* White text for better contrast */
  padding: 5px 8px; /* Smaller padding */
  font-size: 14px; /* Smaller font size */
  border-radius: 8px; /* Slightly smaller rounded corners */
  margin: 0 5px 5px 0;
  cursor: pointer;
}

.small-tag {
  display: inline-block;
  background-color: #555; /* Darker background color */
  color: #fff; /* White text for better contrast */
  padding: 3px 6px; /* Smaller padding */
  font-size: 10px; /* Smaller font size */
  border-radius: 8px; /* Slightly smaller rounded corners */
  margin: 0 5px 5px 0;
  cursor: pointer;
}

.blue {
  background-color: rgb(24, 37, 213);
}

.remove-tag {
  cursor: pointer;
  color: rgb(175, 175, 175); /* Slightly darker red for remove button */
  font-size: 12px; /* Smaller "x" size */
}

.chat-history img {
  filter: invert(50%);
  position: relative;
  width: 0.7vw;
  margin-top: 0.5vw;
  bottom: 0;
}
</style>
