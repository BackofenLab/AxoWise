<template>
  <div>
    <!-- Modal for export selection -->
    <div v-if="show_export" class="export-modal-overlay">
      <div class="export-modal">
        <h2>Select Export Type</h2>

        <!-- Export options -->
        <div class="export-options">
          <button class="export-option" @click="take_screen('white', 'png')">
            White / .png
          </button>
          <button class="export-option" @click="take_screen('black', 'png')">
            Black / .png
          </button>
          <button class="export-option" @click="take_screen('white', 'svg')">
            White / .svg
          </button>
          <button class="export-option" @click="take_screen('black', 'svg')">
            Black / .svg
          </button>
        </div>

        <!-- Close button -->
        <button class="close-btn" @click="show_export = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExportScreen",
  props: ["mode", "filter_views"],
  data() {
    return {
      show_export: false,
      currentView: null,
    };
  },
  mounted() {
    this.emitter.on("openExportScreen", (state) => {
      let checkView = new Set(this.filter_views);
      if (!checkView.has(state)) {
        this.show_export = true;
        this.currentView = state;
      }
    });
  },
  methods: {
    take_screen(mode, format) {
      let checkView = new Set(this.filter_views);
      if (!checkView.has(this.currentView)) {
        this.emitter.emit("exportGraph", {
          params: { mode, format },
          mode: this.currentView,
        });
        this.show_export = false; // Close modal after exporting
      }
    },
  },
};
</script>

<style scoped>
/* Button to trigger the modal */

.export-btn:hover {
  background-color: #45a049;
}

/* Modal overlay */
.export-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999998;
}

/* Modal content */
.export-modal {
  -webkit-backdrop-filter: blur(7.5px);
  border: 1px solid #e0e0e0;
  background-color: rgba(107, 107, 107, 0.5);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 999998;
}

.export-modal h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: white;
}

/* Export options */
.export-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.export-option {
  padding: 10px;
  border: none;
  background-color: #f0f0f0;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.export-option:hover {
  background-color: #ddd;
}

/* Close button */
.close-btn {
  margin-top: 20px;
  padding: 8px 16px;
  background-color: #ff4c4c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #e04343;
}
</style>
