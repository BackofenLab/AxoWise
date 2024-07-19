<template>
  <div id="citation-tools" class="pathways">
    <div class="pathwaybar">
      <div id="citation-list">
        <div class="tool-section-term">
          <div class="citation-search">
            <img
              class="pathway-search-icon"
              src="@/assets/toolbar/search.png"
            />
            <input
              type="text"
              v-model="search_raw"
              class="empty"
              placeholder="search abstracts"
            />
          </div>
        </div>
        <div class="list-section">
          <div class="sorting">
            <a
              class="pubid_filter"
              v-on:click="
                sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
                sort_pr = '';
                sort_cb = '';
                sort_y = '';
              "
              >Pubmed ID</a
            >
            <a
              class="cited_filter"
              v-on:click="
                sort_cb = sort_cb === 'asc' ? 'dsc' : 'asc';
                sort_pr = '';
                sort_alph = '';
                sort_y = '';
              "
              >citation</a
            >
            <a
              class="year_filter"
              v-on:click="
                sort_y = sort_y === 'asc' ? 'dsc' : 'asc';
                sort_pr = '';
                sort_cb = '';
                sort_alph = '';
              "
              >year</a
            >
            <a
              class="fdr_filter"
              v-on:click="
                sort_pr = sort_pr === 'asc' ? 'dsc' : 'asc';
                sort_alph = '';
                sort_cb = '';
                sort_y = '';
              "
              >page rank</a
            >
          </div>

          <div
            class="results"
            tabindex="0"
            @keydown="handleKeyDown"
            ref="resultsContainer"
          >
            <table>
              <tbody>
                <tr
                  v-for="(entry, index) in filt_abstracts"
                  :key="index"
                  class="option"
                  :class="{ selected: selectedIndex === index }"
                  v-on:click="select_abstract(entry, index)"
                >
                  <td>
                    <div class="pathway-text">
                      <a href="#" ref="selectedNodes">{{ entry.id }}</a>
                    </div>
                  </td>
                  <td>
                    <div class="pathway-text">
                      <a href="#">{{ entry.attributes["Citation"] }}</a>
                    </div>
                  </td>
                  <td>
                    <div class="pathway-text">
                      <a href="#">{{ entry.attributes["Year"] }}</a>
                    </div>
                  </td>
                  <td>
                    <a class="fdr-class">{{
                      Math.log10(
                        parseFloat(entry.attributes["PageRank"])
                      ).toFixed(2)
                    }}</a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CitationList",
  props: ["citation_data", "active_node"],
  data() {
    return {
      search_raw: "",
      await_load: false,
      sort_alph: "",
      sort_pr: "",
      sort_cb: "",
      sort_y: "",
      selectedIndex: -1,
    };
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_abstracts() {
      var com = this;
      var filtered = com.citation_data.nodes;

      if (com.search_raw !== "") {
        // If search term is not empty, filter by search term
        var regex = new RegExp(com.regex, "i");
        filtered = filtered.filter(function (abstract) {
          return regex.test(abstract.attributes["Title"]);
        });
      }

      if (com.sort_alph == "asc") {
        filtered.sort((t1, t2) => t2.id - t1.id);
      } else if (com.sort_alph == "dsc") {
        filtered.sort((t1, t2) => t1.id - t2.id);
      }

      if (com.sort_cb == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["Citation"] - t1.attributes["Citation"]
        );
      } else if (com.sort_cb == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["Citation"] - t2.attributes["Citation"]
        );
      }

      if (com.sort_y == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["Year"] - t1.attributes["Year"]
        );
      } else if (com.sort_y == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["Year"] - t2.attributes["Year"]
        );
      }

      if (com.sort_pr == "asc") {
        filtered.sort(
          (t1, t2) => t2.attributes["PageRank"] - t1.attributes["PageRank"]
        );
      } else if (com.sort_pr == "dsc") {
        filtered.sort(
          (t1, t2) => t1.attributes["PageRank"] - t2.attributes["PageRank"]
        );
      }
      return new Set(filtered);
    },
  },
  methods: {
    select_abstract(abstract, index) {
      var com = this;
      com.selectedIndex = index;
      com.emitter.emit("searchNode", { node: abstract, mode: "citation" });
    },
    scrollToSelected(selectedDiv) {
      const parent = this.$refs.resultsContainer; // Updated line to use this.$refs

      if (!selectedDiv) {
        return;
      }

      const selectedDivPosition = selectedDiv.getBoundingClientRect();
      const parentBorders = parent.getBoundingClientRect();

      if (selectedDivPosition.bottom >= parentBorders.bottom) {
        selectedDiv.scrollIntoView(false);
      }

      if (selectedDivPosition.top <= parentBorders.top) {
        selectedDiv.scrollIntoView(true);
      }
    },
    handleKeyDown(event) {
      const keyCode = event.keyCode;

      if (keyCode === 38) {
        event.preventDefault();
        if (this.selectedIndex > 0) {
          this.selectedIndex--;
          this.scrollToSelected(this.$refs.selectedNodes[this.selectedIndex]);
          this.clickNode();
        }
      } else if (keyCode === 40) {
        event.preventDefault();
        if (this.selectedIndex < this.filt_abstracts.size - 1) {
          this.selectedIndex++;
          this.scrollToSelected(this.$refs.selectedNodes[this.selectedIndex]);
          this.clickNode();
        }
      }
    },
    clickNode() {
      const selectedNode = this.$refs.selectedNodes[this.selectedIndex];
      if (selectedNode) {
        selectedNode.click();
      }
    },
  },
};
</script>

<style>
.pathways #citation-list {
  width: 100%;
  height: 100%;
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: "ABeeZee", sans-serif;
}

.pathwaybar-small #citation-list {
  width: 99%;
  height: 96.92%;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  margin-left: 0.5%;
  border-radius: 5px;
  z-index: 997;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
}

.fdr_filter {
  position: absolute;
  left: 78.6%;
}
.cited_filter {
  position: absolute;
  left: 40.6%;
}
.year_filter {
  position: absolute;
  left: 60.6%;
}

.pathway-text {
  width: 92%;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
  margin-left: 2%;
}

.pathway-text a {
  cursor: default;
}

/* bookmark styles */

table {
  display: flex;
  width: 100%;
}

:focus {
  outline: 0 !important;
}

table tbody {
  width: 100%;
}
#citation-list td:first-child {
  width: 40%;
  align-self: center;
}
#citation-list td:nth-child(2) {
  color: #fff;
  font-size: 0.9vw;
  width: 20%;
  overflow: hidden;
  align-self: center;
}
#citation-list td:nth-child(3) {
  color: #fff;
  font-size: 0.9vw;
  width: 20%;
  overflow: hidden;
  align-self: center;
}
#citation-list td:last-child {
  font-size: 0.9vw;
  color: white;
  width: 20%;
  align-self: center;
}

.visualize-logo {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
/* .visualize-logo .bookmark-image {
    } */
.visualize-text {
  font-size: 0.95vw;
  color: white;
}

.context-confirm {
  font-family: "ABeeZee", sans-serif;
  margin-left: 1vw;
  font-size: 0.7vw;
  display: flex;
}

.context-confirm [type="checkbox"] + label {
  display: block;
  cursor: pointer;
  font-family: sans-serif;
  font-size: 24px;
  line-height: 1.3;
  position: absolute;
  left: 30%;
  margin-top: 0.7%;
}

.context-confirm [type="checkbox"] + label:before {
  width: 1.2vw;
  height: 0.6vw;
  border-radius: 30px;
  background-color: #ddd;
  content: "";
  transition: background-color 0.5s linear;
  z-index: 5;
  position: absolute;
}
.context-confirm [type="checkbox"] + label:after {
  width: 0.4vw;
  height: 0.4vw;
  border-radius: 30px;
  background-color: #fff;
  content: "";
  transition: margin 0.1s linear;
  box-shadow: 0px 0px 5px #aaa;
  position: absolute;
  top: 10%;
  margin: 0.09vw 0 0 0.09vw;
  z-index: 10;
}

.context-confirm [type="checkbox"]:checked + label:after {
  margin: 0.09vw 0 0 0.69vw;
}

.context-check {
  color: white;
  margin: 0 0 1vw 10%;
}
</style>
