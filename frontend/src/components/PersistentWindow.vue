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
      controller: null,
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
          this.emitter.emit("searchfavouriteSubset", {
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
    async streamChatbotResponse(formData) {
      let refData = null;
      if (this.controller) {
        this.controller.abort();
      }

      // Create a new AbortController instance
      this.controller = new AbortController();
      const signal = this.controller.signal; // Get the signal

      const botMessage = {
        sender: "Bot",
        text: "Waiting for response...", // Initially empty, will be updated progressively
        data: [...this.tags], // Add contextual data if needed
        ref: null, // This will hold the pmids when received
      };
      this.messages.push(botMessage);

      const response = await fetch(this.api.chatbot, {
        method: "POST",
        body: formData,
        signal: signal,
      });

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      let fullText = "";

      // Index of the newly added Bot message
      const botMessageIndex = this.messages.length - 1;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (done) break;

        // Decode the streamed data
        const chunk = decoder.decode(value || new Uint8Array(), {
          stream: !done,
        });
        // Parse the chunk as JSON to extract "messages" and "pmids"
        let parsedChunk = JSON.parse(chunk);
        // Check if it's a message part or pmids
        if (parsedChunk.message) {
          // Append message chunks to the fullText
          fullText += parsedChunk.message;

          // Update the bot message progressively
          this.updateBotMessage(fullText, botMessageIndex);
        }

        if (parsedChunk.pmids) {
          // If pmids are received, store them for later
          refData = parsedChunk.pmids;
          this.messages[botMessageIndex].ref = refData;
        }
      }
    },
    updateBotMessage(text, index) {
      // Ensure we're updating the correct (newest) bot message by index
      this.messages[index].text = text;
    },
    getAnswer(message) {
      let com = this;
      let formData = new FormData();
      formData.append("message", message.text);
      formData.append("background", JSON.stringify(message.data));

      com.streamChatbotResponse(formData);
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
</style>
