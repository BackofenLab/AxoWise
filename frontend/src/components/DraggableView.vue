<template>
  <section :class="`absolute peer select-none z-[9] ${wrapperClass}`"
    :style="{ top: `${position.top}px`, left: `${position.left}px` }" ref="dragWrapper">
    <header :class="`cursor-grab ${handlerClass}`" @mousedown="onMouseDown" ref="draggable">
      <slot name="handler" />
    </header>
    <div v-if="$slots.content" :class="contentClass">
      <slot name="content" />
    </div>
  </section>
</template>

<script>
export default {
  props: {
    wrapperClass: {
      type: String,
      default: "",
    },
    handlerClass: {
      type: String,
      default: "",
    },
    contentClass: {
      type: String,
      default: "",
    },
    initialPosition: {
      type: Object,
      default: () => ({ top: 100, left: 100 }),
    },
    minX: {
      type: Number,
      default: 0, // Minimum left coordinate
    },
    minY: {
      type: Number,
      default: 0, // Minimum top coordinate
    },
    dragHandle: {
      type: String,
      default: null, // CSS selector for the drag handle
    },
  },
  data() {
    return {
      position: { ...this.initialPosition },
      isDragging: false,
      dragOffset: { x: 0, y: 0 },
    };
  },
  mounted() {
    // Safely access the handler element after DOM updates
    this.$nextTick(() => {
      if (this.dragHandle && this.$refs.handler) {
        const handle = this.$refs.handler.querySelector(this.dragHandle);
        if (handle) {
          // Add mousedown listener only to the handle
          handle.addEventListener("mousedown", this.onMouseDown);
        }
      }
    });
  },
  beforeUnmount() {
    // Remove event listener safely if handler exists
    if (this.dragHandle && this.$refs.handler) {
      const handle = this.$refs.handler.querySelector(this.dragHandle);
      if (handle) {
        handle.removeEventListener("mousedown", this.onMouseDown);
      }
    }
  },
  methods: {
    onMouseDown(event) {
      // Prevent default behavior (like clicking) when dragging starts
      event.preventDefault();

      // Ensure the drag starts only from the handle and avoid errors
      if (this.dragHandle && this.$refs.handler) {
        const handle = this.$refs.handler.querySelector(this.dragHandle);
        if (!handle || !handle.contains(event.target)) {
          return; // Stop if the event is not from the handle
        }
      }

      this.isDragging = true;
      this.dragOffset.x = event.clientX - this.position.left;
      this.dragOffset.y = event.clientY - this.position.top;

      // Add listeners for drag movement and release
      window.addEventListener("mousemove", this.onMouseMove);
      window.addEventListener("mouseup", this.onMouseUp);
    },
    onMouseMove(event) {
      if (!this.isDragging) return;

      const handler = this.$refs.draggable.querySelector(this.dragHandle);

      let newTop = event.clientY - this.dragOffset.y;
      let newLeft = event.clientX - this.dragOffset.x;

      const rect = this.$refs.dragWrapper.getBoundingClientRect();
      const containerWidth = window.innerWidth;
      const containerHeight = window.innerHeight;

      handler.classList.add("!pointer-events-none");

      newTop = Math.max(this.minY, Math.min(newTop, containerHeight - rect.height));
      newLeft = Math.max(this.minX, Math.min(newLeft, containerWidth - rect.width));

      this.position.top = newTop;
      this.position.left = newLeft;
    },
    onMouseUp() {
      this.isDragging = false;
      this.$refs.draggable.querySelector(this.dragHandle).classList.remove("!pointer-events-none");
      window.removeEventListener("mousemove", this.onMouseMove);
      window.removeEventListener("mouseup", this.onMouseUp);
    },
  },
};
</script>
