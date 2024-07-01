<template>
  <div id="route">
    <div class="search-field">
      <img class="search-field-icon" src="@/assets/toolbar/search.png" />
      <input
        type="text"
        v-model="search_raw"
        class="empty"
        placeholder="enter target protein"
        @keyup.enter="retrieve_path(search_raw)"
      />
    </div>
    <div class="request_answer">
      <span>connection: {{ path }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "RoutingNode",
  props: ["active_node", "gephi_data"],
  data() {
    return {
      search_raw: "",
      path: null,
      target_prot: null,
    };
  },
  mounted() {
    this.emitter.on("emptySet", (state) => {
      this.path = state;
    });
  },
  watch: {
    active_node() {
      if (!this.active_node) {
        this.search_raw = "";
        this.path = false;
      }
    },
  },
  methods: {
    retrieve_path(target) {
      if (!target) {
        this.emitter.emit("reset_protein", this.active_node);
        return;
      }

      this.target_prot = this.gephi_data.nodes.filter(function (node) {
        return node.attributes["Name"].toLowerCase() === target.toLowerCase();
      })[0];

      if (!this.target_prot) {
        this.path = false;
        return;
      }
      this.emitter.emit("searchPathway", {
        source: this.active_node.id,
        target: this.target_prot.id,
      });
    },
  },
};
</script>

<style>
#route {
  color: white;
  font-family: "ABeeZee", sans-serif;
  font-size: 0.7vw;
  width: 100%;
  height: 100%;
  padding: 2.3vw 1.3vw 0 1.3vw;
}

#route .search-field {
  width: 80%;
  left: 65%;
  display: flex;
  background: rgba(222, 222, 222, 0.3);
  transform: translateX(-70%);
  position: absolute;
  border-radius: 0;
  justify-content: center;
  z-index: 999;
}

#route .search-field input[type="text"] {
  margin-left: 10%;
  font-size: 0.7vw;
  width: 83%;
  background: none;
  color: white;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
  border: none;
}

.request_answer {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7vw;
}

.request_answer span {
  color: white;
  float: left;
  clear: left;
}
</style>
