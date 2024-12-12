<!-- <template>
  <div
    id="menu-tools"
    :class="{
      'pathwaybar-small': pane_hidden === true,
      pathways: pane_hidden === false,
    }"
  >
    <div class="pathwaybar">
      <PathwayGraphList
        v-show="active_function === 'list'"
        :term_data="term_data"
      ></PathwayGraphList>
      <PathwayGraphGraphs
        v-if="active_function === 'graph'"
        :gephi_data="gephi_data"
        :filtered_terms="filtered_terms"
        :favourite_pathways="favourite_pathways"
      ></PathwayGraphGraphs>
    </div>
  </div>
</template>

<script>
import PathwayGraphList from "@/components/pathwaytools/PathwayGraphList.vue";
import PathwayGraphGraphs from "@/components/pathwaytools/PathwayGraphGraphs.vue";

export default {
  name: "PathwayGraphMenu",
  props: ["term_data", "active_term", "active_function", "sorted"],
  components: {
    PathwayGraphList,
    PathwayGraphGraphs,
  },
  data() {
    return {
      pane_hidden: false,
    };
  },
  methods: {
    dragElement(elmnt, val) {
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
        if (!val) return;
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = elmnt.offsetTop - pos2 + "px";
        elmnt.style.left = elmnt.offsetLeft - pos1 + "px";
      }

      function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
      }
    },
    resetElement(elmnt) {
      // set the element's new position:
      elmnt.style.top = null;
      elmnt.style.left = null;
      document.getElementById(elmnt.id + "_header").onmousedown = null;
    },
  },
};
</script>

<style></style> -->
