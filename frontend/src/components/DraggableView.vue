<template>
  <section :class="`absolute peer select-none z-[9] ${wrapperClass}`"
    :style="{ top: `${position.top}px`, left: `${position.left}px` }" ref="dragWrapper">
    <div ref="draggable">
      <header :class="`cursor-move ${handlerClass}`" @mousedown="onMouseDown" id="drag-handle">
        <slot name="handler" />
      </header>
    </div>
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
      default: () => ({ top: 60, left: 60 }),
    },
    minX: {
      type: Number,
      default: 60, // Minimum left coordinate
    },
    minY: {
      type: Number,
      default: 60, // Minimum top coordinate
    },
    dragHandle: {
      type: String,
      default: '#drag-handle', // CSS selector for the drag handle
    },
  },
  emits: ["active_resize_changed"],
  data() {
    return {
      position: { ...this.initialPosition },
      isDragging: false,
      dragOffset: { x: 0, y: 0 },
      resizeObserver: null
    };
  },
  mounted() {
    // Create a ResizeObserver instance
    const observer = new ResizeObserver((entries) => {
      for (let entry of entries) {
        // Handle the resize event
        this.$emit("active_resize_changed", entry.contentRect);
      }
    });

    // Start observing the element
    observer.observe(this.$refs.dragWrapper);

    // Store the observer in the component instance for cleanup
    this.resizeObserver = observer;
  },
  beforeUnmount() {
    // Stop observing when the component is destroyed
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
  },
  methods: {
    onMouseDown(event) {
      // Prevent default behavior (like clicking) when dragging starts
      event.preventDefault();

      if (event.button === 2) {
        // Prevent drag from right click
        return;
      }

      // Ensure the drag starts only from the handle and avoid errors
      if (this.dragHandle && this.$refs.draggable) {
        const handle = this.$refs.draggable.querySelector(this.dragHandle);
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
