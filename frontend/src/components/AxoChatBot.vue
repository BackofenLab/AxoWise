<template>
  <Dialog v-model:visible="windowCheck" header="AxoBot" position="bottomright" :minY="minVal" :minX="minVal"
    :maximizable="true" :pt="{
      root: {
        id: 'scrollBox',
        class:
          `!h-full w-[26rem] !bg-white/75 dark:!bg-slate-900/75 !backdrop-blur overflow-y-auto !mt-[${minVal}px] !ml-[${minVal}px]`,
      },
      header: { class: 'sticky top-0 !p-2 !px-3 !justify-start gap-3 !font-medium cursor-move backdrop-blur z-[1]' },
      headerActions: { class: '!ml-auto' },
      title: { class: '!text-base' },
      content: { class: '!px-3 !pb-2 !overflow-y-visible' },
      footer: { class: 'sticky bottom-0 !px-2 !pt-1 !pb-2 cursor-move backdrop-blur-xl !mt-auto' },
    }" @maximize="minVal = 0" @unmaximize="minVal = 60" @hide="windowCheck = false">
    <main class="flex flex-col">
      <ul class="flex flex-col gap-1.5">
        <li v-for="(msg, index) in messages" :key="index" :class="`flex flex-col p-3 rounded-lg
          ${index !== 0 ? 'backdrop-blur shadow-md' : ''}
          ${msg.sender === 'User' ? 'w-11/12 self-end' : ''}
          ${msg.sender === 'Bot' && index !== 0 ? 'my-2 bg-gradient-prime-opacity dark:bg-slate-800' : ''}
          ${msg.data && msg.data.length > 0 ? '!pt-0' : ''}
          `">
          <!-- First welcome message -->
          <div class="mb-8" v-show="index === 0">
            <figure
              class="w-16 h-16 rounded-full mx-auto mb-4 p-3 bg-gradient-prime-reverse shadow-[0_0_50px_0_rgba(68,184,166,0.26)]">
              <img src="@/assets/logo.png" alt="Bot Icon" />
            </figure>
            <h6 class="text-center whitespace-pre-wrap">{{ msg.text }}</h6>
          </div>

          <template v-if="index !== 0">
            <div :class="`flex gap-3 ${msg.sender === 'Bot' ? 'mb-5 flex-wrap' : 'gap-1.5 items-center'}`">
              <template v-if="msg.data && msg.data.length">
                <Splide :options="{ autoWidth: true, pagination: false, gap: '8px' }"
                  :class="`mb-1.5 ${msg.sender === 'Bot' ? 'w-[calc(100%+(12px*2))] -mx-3' : 'w-[80%] -ml-3'}`">
                  <SplideSlide v-for="(element, index) in msg.data" :key="index">
                    <Chip class="cursor-pointer" :pt="{
                      root: { class: 'h-6 dark:!bg-slate-700 !px-2' },
                      label: { class: '!text-sm' },
                    }" :label="element.id" @click="searchInput(element)" />
                  </SplideSlide>
                </Splide>
              </template>

              <figure v-if="msg.sender === 'Bot'" class="w-6 h-6 p-1 rounded-full bg-gradient-prime-reverse">
                <img src="@/assets/logo.png" alt="Bot Icon" />
              </figure>

              <Chip v-if="msg.ref && msg.sender === 'Bot'" class="cursor-pointer"
                :pt="{ root: { class: 'h-6 !bg-primary-500 !px-2 !py-0.5' }, label: { class: '!text-sm' } }"
                label="Reference" @click="searchRef(msg.ref)" />

              <Button class="w-6 h-6 !p-1.5 ml-auto" type="button" size="small" text plain rounded
                v-tooltip.left="{ value: 'Copy to clipboard', pt: { text: '!text-sm' } }"
                @click="copyToClipboard(msg.text)">
                <span class="material-symbols-rounded !text-lg"> content_copy </span>
              </Button>
              <Button class="w-6 h-6 !p-1.5" type="button" size="small" text plain rounded
                v-tooltip.left="{ value: 'Add to AxoWord', pt: { text: '!text-sm' } }" @click="addToWord(msg.text)">
                <span class="material-symbols-rounded !text-xl"> chat_add_on </span>
              </Button>
            </div>
            <p class="whitespace-pre-wrap">{{ msg.text }}</p>
          </template>
        </li>
      </ul>
    </main>

    <template #footer>
      <div class="flex flex-col w-full gap-2">
        <fieldset class="relative">
          <Textarea autoResize rows="1" class="!pr-[40.98px] !leading-tight" v-model="user_input" fluid autofocus
            placeholder="Type your message..." @keydown.enter.prevent="sendMessage" />
          <Button class="!absolute !bottom-1.5 !right-0 !border-0 !p-2 !h-9 hover:!bg-transparent" type="button" text
            plain @click="sendMessage">
            <span class="material-symbols-rounded font-variation-ico-filled !text-xl"> send </span>
          </Button>
        </fieldset>

        <template v-if="tags && tags.length">
          <Splide :options="{ autoWidth: true, pagination: false, gap: '8px' }">
            <SplideSlide v-for="(tag, index) in tags" :key="index">
              <div class="flex items-center gap-2 rounded-2xl cursor-pointer !h-6 dark:!bg-slate-700 !px-2">
                <span @click="searchInput(tag)" class="!text-sm">{{ tag.id }}</span>
                <span class="material-symbols-rounded !text-lg" @click="removeTag(index)"> cancel </span>
              </div>
            </SplideSlide>
          </Splide>
        </template>
      </div>
    </template>
  </Dialog>

  <Button v-show="showPersistentComponent" type="button" severity="primary" rounded
    :class="`!absolute z-[9] bottom-9 right-9 group/chat !w-16 !h-16 !border-2 !border-primary-200 !text-[#d3e4ff] hover:!text-white transition-all duration-500`"
    @click="windowCheck = !windowCheck">
    <img src="@/assets/logo.svg" />
    <span
      class="w-full h-full absolute top-0 left-0 bg-gradient-prime rounded-full transition-all duration-500 group-hover/chat:rotate-180 z-[-1]"></span>
  </Button>
</template>

<script>
import { useToast } from "primevue/usetoast";
import { Splide, SplideSlide } from "@splidejs/vue-splide";
export default {
  name: "AxoChatBot",
  components: {
    Splide,
    SplideSlide,
  },
  data() {
    return {
      user_input: "",
      messages: [{ sender: "Bot", text: "Hello! How can I assist you today?" }],
      windowCheck: false,
      tags: [],
      api: {
        chatbot: "api/subgraph/chatbot",
      },
      sourceToken: null,
      minVal: 60
    };
  },
  computed: {
    showPersistentComponent() {
      let route = this.$route.name;
      return route !== "home";
    },
  },
  mounted() {
    this.toast = useToast();
    let com = this;

    com.emitter.on("openChatbot", () => {
      com.windowCheck = !com.windowCheck;
    });

    com.emitter.on("addToChatbot", (data) => {
      this.addLink(data);
    });
  },
  methods: {
    scrollToEnd() {
      setTimeout(() => {
        const box = document.getElementById("scrollBox");
        box.scrollTo({
          top: box.scrollHeight,
          behavior: "smooth", // Add smooth scrolling
        });
      }, 1); // 1ms delay to render new item and allow the scroll to complete
    },
    copyToClipboard(text) {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          this.toast.add({ severity: 'success', detail: 'Message copied to clipboard.', life: 4000 });
        })
        .catch((err) => {
          console.error("Could not copy text: ", err);
        });
    },
    addToWord(text) {
      this.emitter.emit("addToWord", text);
      this.toast.add({ severity: 'success', detail: 'Message added to AxoWord.', life: 4000 });
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
        this.toast.add({ severity: 'error', detail: 'No citation graph.', life: 4000 });
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
      const userInput = this.user_input.trim();
      if (userInput !== "") {
        const messageTags = [...this.tags];
        let message = { text: userInput, data: messageTags };

        this.messages.push({
          sender: "User",
          text: userInput,
          data: messageTags,
        });
        this.getAnswer(message);
        this.user_input = '';
        this.scrollToEnd();
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