<template>
  <div id="genchatbot" class="hidden persistent-window" v-show="showPersistentComponent && windowCheck">
    <div id="genchatbot_header" class="header">
      <h3>AxoBot</h3>
      <span class="close-btn" @click="closeWindow">×</span>
    </div>

    <div class="chat-history">
      <div v-for="(msg, index) in messages" :key="index" :class="[
        'message',
        msg.sender === 'User' ? 'user-message' : 'bot-message',
      ]">
        <div v-if="msg.data">
          <span v-for="(element, index) in msg.data" :key="index" class="small-tag" @click="searchInput(element)">
            {{ element.id }}
          </span>
        </div>
        <div v-if="msg.ref">
          <span class="small-tag blue" @click="searchRef(msg.ref)">
            reference
          </span>
        </div>
        <p>{{ msg.text }}</p>
        <img src="@/assets/pane/copy.png" v-on:click="copyToClipboard(msg.text)" />
        <img src="@/assets/toolbar/word.png" v-on:click="addToWord(msg.text)" />
      </div>
    </div>

    <div class="chat-input-container">
      <!-- Editable div with contenteditable attribute -->
      <div ref="editableDiv" id="input_chatbot" contenteditable="true" @keydown.enter.prevent="sendMessage"
        class="input-box"></div>

      <div class="tag-container" v-if="tags.length">
        <span v-for="(tag, index) in tags" :key="index" class="tag" @click="searchInput(tag)">
          {{ tag.id }}
          <span class="remove-tag" @click.stop="removeTag(index)">x</span>
        </span>
      </div>
    </div>
  </div>

  <Dialog v-if="windowCheck" v-model:visible="showPersistentComponent" header="AxoBot" position="bottomright"
    :closable="false" :minY="60" :minX="60" :pt="{
      root: {
        class:
          '!max-h-[70vh] w-[25rem] !mt-[60px] !ml-[60px] !bg-white/75 dark:!bg-slate-900/75 !backdrop-blur overflow-y-auto',
      },
      header: { class: 'sticky top-0 !p-2 !px-3 !justify-start gap-3 !font-medium cursor-move backdrop-blur z-[1]' },
      headerActions: { class: '!hidden' },
      title: { class: '!text-base ' },
      content: { class: '!px-3 !pb-2 !overflow-y-visible' },
      footer: { class: 'sticky bottom-0 !px-2 !pt-1 !pb-2 cursor-move backdrop-blur-xl' },
    }">
    <template #header>
      <span class="material-symbols-rounded font-variation-ico-filled text-primary-500 !text-lg"> headset_mic </span>
      AxoBot

      <Button class="ml-auto" size="small" text plain rounded @click="windowCheck = false">
        <span class="material-symbols-rounded"> close </span>
      </Button>
    </template>

    <main class="flex flex-col">
      <ul class="flex flex-col gap-1.5">
        <li
          v-for="(msg, index) in messages"
          :key="index"
          :class="`flex flex-col p-3 rounded-lg
          ${index !== 0 ? 'backdrop-blur shadow-md' : ''}
          ${msg.sender === 'User' ? 'w-11/12 flex-col-reverse self-end' : ''}
          ${msg.sender === 'Bot' && index !== 0 ? 'my-2 bg-gradient-prime-opacity dark:bg-slate-800' : ''}
          `"
        >
          <!-- First welcome message -->
          <div class="mb-8" v-show="index === 0">
            <figure
              class="w-16 h-16 rounded-full mx-auto mb-4 p-3 bg-gradient-prime-reverse shadow-[0_0_50px_0_rgba(68,184,166,0.26)]"
            >
              <img src="@/assets/logo.png" alt="Bot Icon" />
            </figure>
            <h6 class="text-center">{{ msg.text }}</h6>
          </div>

          <template v-if="index !== 0">
            <div v-if="msg.data">
              <span v-for="(element, index) in msg.data" :key="index" class="small-tag" @click="searchInput(element)">
                {{ element.id }}
              </span>
            </div>
            <div class="flex gap-3 mb-5">
              <figure class="w-6 h-6 p-1 rounded-full bg-gradient-prime-reverse">
                <img src="@/assets/logo.png" alt="Bot Icon" />
              </figure>
              <h6 class="m-0 text-center">AxoBot</h6>

              <Chip
                v-if="msg.ref"
                :pt="{ root: { class: 'h-6 !bg-primary-500 !px-2 !py-0.5' }, label: { class: '!text-sm' } }"
                label="Reference"
                @click="searchRef(msg.ref)"
              />

              <Button
                class="w-6 h-6 !p-1.5 ml-auto"
                type="button"
                size="small"
                text
                plain
                rounded
                v-tooltip.bottom="'Copy to clipboard'"
                @click="copyToClipboard(msg.text)"
              >
                <span class="material-symbols-rounded !text-xl"> content_copy </span>
              </Button>
              <Button
                class="w-6 h-6 !p-1.5"
                type="button"
                size="small"
                text
                plain
                rounded
                v-tooltip.bottom="'Add to AxoWord'"
                @click="addToWord(msg.text)"
              >
                <span class="material-symbols-rounded !text-xl"> chat_add_on </span>
              </Button>
            </div>
            <p>{{ msg.text }}</p>
          </template>
        </li>
      </ul>
    </main>
  </Dialog>

  <div v-show="showPersistentComponent" class="absolute peer select-none z-[9] cursor-grab"
    :style="{ top: `650px`, right: `60px` }">
    <Button type="button" severity="primary" rounded
      :class="`group/chat !w-16 !h-16 relative !border-2 !border-primary-200 !text-[#d3e4ff] hover:!text-white transition-all duration-500 z-[1]`"
      @click="windowCheck = !windowCheck">
      <img src="@/assets/logo.png" />
      <!-- <img
        class="transition-all duration-300 ease-out translate-x-0 opacity-100 group-hover/chat:-translate-x-10 group-hover/chat:opacity-0"
        src="@/assets/logo.png" />
      <img
        class="absolute transition-all duration-300 ease-in translate-x-10 opacity-0 group-hover/chat:translate-x-0 group-hover/chat:opacity-100"
        src="@/assets/logo.png" /> -->
      <span
        class="w-full h-full absolute top-0 left-0 bg-gradient-prime rounded-full transition-all duration-500 group-hover/chat:rotate-180 z-[-1]"></span>
    </Button>
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
        route !== "home" &&
        route !== "input" &&
        route !== "file" &&
        route !== "import"
      );
    },
  },
  mounted() {
    let com = this;
    
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
  },
};
</script>