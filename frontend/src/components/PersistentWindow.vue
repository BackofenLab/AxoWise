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
        <p>{{ msg.text }}</p>
      </div>
    </div>

    <div class="chat-input">
      <input
        v-model="userInput"
        @keydown.enter="sendMessage"
        placeholder="Send a message"
        class="input-box"
      />
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
  },
  methods: {
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
      if (this.userInput.trim() !== "") {
        this.messages.push({ sender: "User", text: this.userInput });
        this.userInput = "";
        // Add bot response
        setTimeout(() => {
          this.messages.push({
            sender: "Bot",
            text: "Let me get back to you on that!",
          });
        }, 1000);
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
  line-height: 1.4;
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

.chat-input {
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
</style>
